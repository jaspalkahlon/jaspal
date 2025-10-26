#!/bin/bash

# Fashion Guru Bot - Quick Deploy Script for Google Cloud Run
# This script automates the deployment process

set -e  # Exit on error

echo "=========================================="
echo "Fashion Guru Bot - Google Cloud Deployment"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo -e "${GREEN}✓ gcloud CLI found${NC}"

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo -e "${YELLOW}You need to authenticate first...${NC}"
    gcloud auth login
fi

echo -e "${GREEN}✓ Authenticated${NC}"

# Get or create project
echo ""
echo "Project Setup"
echo "-------------"
gcloud projects list --format="table(projectId,name)" 2>/dev/null || true

echo ""
read -p "Enter your project ID (or press Enter to create new): " PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    # Generate random project ID
    RANDOM_ID=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 8 | head -n 1)
    PROJECT_ID="fashion-guru-bot-${RANDOM_ID}"

    echo -e "${YELLOW}Creating new project: ${PROJECT_ID}${NC}"
    gcloud projects create "$PROJECT_ID" --name="Fashion Guru Bot"

    echo -e "${YELLOW}Please enable billing for this project:${NC}"
    echo "https://console.cloud.google.com/billing/linkedaccount?project=${PROJECT_ID}"
    read -p "Press Enter after enabling billing..."
fi

# Set project
gcloud config set project "$PROJECT_ID"
echo -e "${GREEN}✓ Project set: ${PROJECT_ID}${NC}"

# Enable required APIs
echo ""
echo "Enabling required APIs..."
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

echo -e "${GREEN}✓ APIs enabled${NC}"

# Choose region
echo ""
echo "Available regions:"
echo "1. us-central1 (Iowa)"
echo "2. us-east1 (South Carolina)"
echo "3. europe-west1 (Belgium)"
echo "4. asia-northeast1 (Tokyo)"
read -p "Choose region (1-4, default: 1): " REGION_CHOICE

case $REGION_CHOICE in
    2) REGION="us-east1" ;;
    3) REGION="europe-west1" ;;
    4) REGION="asia-northeast1" ;;
    *) REGION="us-central1" ;;
esac

echo -e "${GREEN}✓ Region: ${REGION}${NC}"

# Service name
SERVICE_NAME="fashion-guru-bot"

# Deploy
echo ""
echo "=========================================="
echo "Deploying to Cloud Run..."
echo "This will take 3-5 minutes..."
echo "=========================================="
echo ""

gcloud run deploy "$SERVICE_NAME" \
    --source . \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --port 5000 \
    --memory 512Mi \
    --timeout 300 \
    --quiet

# Get service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format="value(status.url)")

echo ""
echo "=========================================="
echo -e "${GREEN}✓ Deployment Successful!${NC}"
echo "=========================================="
echo ""
echo "Service URL: ${SERVICE_URL}"
echo ""

# Test deployment
echo "Testing deployment..."
echo ""

echo "1. Health Check:"
HEALTH_RESPONSE=$(curl -s "${SERVICE_URL}/health")
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
fi

echo ""
echo "2. Chat Test:"
CHAT_RESPONSE=$(curl -s -X POST "${SERVICE_URL}/chat" \
    -H "Content-Type: application/json" \
    -d '{"user_id":"test","message":"Hello"}')

if echo "$CHAT_RESPONSE" | grep -q "success"; then
    echo -e "${GREEN}✓ Chat endpoint working${NC}"
else
    echo -e "${RED}✗ Chat endpoint failed${NC}"
fi

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Your Fashion Guru Bot is live at:"
echo "${SERVICE_URL}"
echo ""
echo "Test it with:"
echo "  curl ${SERVICE_URL}/health"
echo ""
echo "Or chat:"
echo "  curl -X POST ${SERVICE_URL}/chat \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"user_id\":\"test\",\"message\":\"What fabric for summer dress?\"}'"
echo ""
echo "View logs:"
echo "  gcloud run services logs tail ${SERVICE_NAME} --region ${REGION}"
echo ""
echo "View in Cloud Console:"
echo "  https://console.cloud.google.com/run/detail/${REGION}/${SERVICE_NAME}"
echo ""
echo -e "${GREEN}Happy designing! 🎨${NC}"
echo ""
