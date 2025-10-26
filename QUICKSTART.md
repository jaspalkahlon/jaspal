# Fashion Guru Bot - Quick Start & Testing Guide

## Quick Deploy to Google Cloud (5 Minutes)

### Prerequisites Check

Before starting, make sure you have:
- [ ] Google Cloud account (free tier is fine)
- [ ] Credit card for verification (won't be charged unless you exceed free tier)
- [ ] Terminal/command line access

### Step 1: Install Google Cloud SDK (2 minutes)

**On macOS:**
```bash
# Install via Homebrew (recommended)
brew install --cask google-cloud-sdk

# Or use the installer
curl https://sdk.cloud.google.com | bash
```

**On Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**On Windows:**
Download installer from: https://cloud.google.com/sdk/docs/install

**Verify installation:**
```bash
gcloud --version
```

### Step 2: Authenticate (1 minute)

```bash
# Login to Google Cloud
gcloud auth login

# This will open a browser - sign in with your Google account
```

### Step 3: Create or Select Project (1 minute)

**Option A: Create a new project**
```bash
# Create project
gcloud projects create fashion-guru-bot-001 --name="Fashion Guru Bot"

# Set as active project
gcloud config set project fashion-guru-bot-001

# Enable billing (required for Cloud Run)
# Go to: https://console.cloud.google.com/billing
# Link your project to a billing account
```

**Option B: Use existing project**
```bash
# List your projects
gcloud projects list

# Set your project
gcloud config set project YOUR-PROJECT-ID
```

### Step 4: Enable Required APIs (30 seconds)

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

### Step 5: Deploy! (3-5 minutes)

Navigate to your project directory:
```bash
cd /home/user/jaspal

# Deploy to Cloud Run
gcloud run deploy fashion-guru-bot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 5000 \
  --memory 512Mi \
  --timeout 300
```

**What happens:**
1. Cloud Build creates a container from your code
2. Uploads to Container Registry
3. Deploys to Cloud Run
4. Gives you a public URL

**Output will look like:**
```
Building using Dockerfile and deploying container to Cloud Run service [fashion-guru-bot]...
✓ Creating Container Repository...
✓ Uploading sources...
✓ Building Container... This may take a few minutes.
✓ Deploying to Cloud Run...

Service URL: https://fashion-guru-bot-xxxxx-uc.a.run.app
```

**Copy this URL - you'll need it for testing!**

---

## Testing Your Deployment

### Test 1: Health Check

```bash
# Replace with your actual service URL
export BOT_URL="https://fashion-guru-bot-xxxxx-uc.a.run.app"

# Test health endpoint
curl $BOT_URL/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "Fashion Guru Bot",
  "modules": [
    "pattern_intelligence",
    "fabric_oracle",
    "troubleshooting",
    "trend_synthesis",
    "color_psychology",
    "design_critique"
  ]
}
```

### Test 2: Chat with the Bot

**Test: Fabric Recommendation**
```bash
curl -X POST $BOT_URL/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_001",
    "message": "What fabric should I use for a summer dress?"
  }'
```

**Test: Pattern Guidance**
```bash
curl -X POST $BOT_URL/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_002",
    "message": "How do I draft a basic skirt pattern?"
  }'
```

**Test: Troubleshooting**
```bash
curl -X POST $BOT_URL/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_003",
    "message": "My seams are puckering, what should I do?"
  }'
```

**Test: Trend Analysis**
```bash
curl -X POST $BOT_URL/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_004",
    "message": "What are the current fashion trends?"
  }'
```

**Test: Color Psychology**
```bash
curl -X POST $BOT_URL/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_005",
    "message": "What does the color red mean in fashion?"
  }'
```

**Test: Design Critique**
```bash
curl -X POST $BOT_URL/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_006",
    "message": "I would like feedback on my dress design"
  }'
```

### Test 3: List Modules

```bash
curl $BOT_URL/modules
```

### Test 4: Get Statistics

```bash
curl $BOT_URL/stats
```

---

## Interactive Testing (Web Browser)

You can also test using a simple HTML page. Create this file locally:

**test-bot.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Fashion Guru Bot Tester</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        #chatbox { border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background: #e3f2fd; text-align: right; }
        .bot { background: #f5f5f5; }
        input { width: 80%; padding: 10px; }
        button { padding: 10px 20px; }
    </style>
</head>
<body>
    <h1>Fashion Guru Bot Tester</h1>

    <div>
        <input type="text" id="bot-url" placeholder="Enter your bot URL" value="https://fashion-guru-bot-xxxxx-uc.a.run.app">
    </div>

    <div id="chatbox"></div>

    <div>
        <input type="text" id="message" placeholder="Ask me about fashion...">
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        const userId = 'web_user_' + Math.random().toString(36).substr(2, 9);

        function sendMessage() {
            const botUrl = document.getElementById('bot-url').value;
            const message = document.getElementById('message').value;

            if (!message) return;

            // Display user message
            addMessage('user', message);
            document.getElementById('message').value = '';

            // Send to bot
            fetch(`${botUrl}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, message: message })
            })
            .then(r => r.json())
            .then(data => {
                addMessage('bot', data.response.message);
            })
            .catch(err => {
                addMessage('bot', 'Error: ' + err.message);
            });
        }

        function addMessage(type, text) {
            const chatbox = document.getElementById('chatbox');
            const div = document.createElement('div');
            div.className = `message ${type}`;
            div.textContent = text;
            chatbox.appendChild(div);
            chatbox.scrollTop = chatbox.scrollHeight;
        }

        // Enter key to send
        document.getElementById('message').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
```

**How to use:**
1. Save as `test-bot.html`
2. Open in your web browser
3. Enter your bot URL
4. Start chatting!

---

## Python Test Script

Create a simple Python test script:

**test_bot.py:**
```python
#!/usr/bin/env python3
import requests
import sys

# Replace with your actual URL
BOT_URL = "https://fashion-guru-bot-xxxxx-uc.a.run.app"

def test_health():
    """Test health endpoint"""
    print("\n1. Testing Health Endpoint...")
    response = requests.get(f"{BOT_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_chat(message):
    """Test chat endpoint"""
    print(f"2. Testing Chat: '{message}'")
    response = requests.post(
        f"{BOT_URL}/chat",
        json={"user_id": "test_user", "message": message}
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    if data['success']:
        print(f"\nBot Response:\n{data['response']['message']}\n")
    else:
        print(f"Error: {data.get('error')}\n")

def test_modules():
    """Test modules endpoint"""
    print("3. Testing Modules Endpoint...")
    response = requests.get(f"{BOT_URL}/modules")
    print(f"Status: {response.status_code}")
    print(f"Modules: {response.json()['modules']}\n")

def main():
    if len(sys.argv) > 1:
        global BOT_URL
        BOT_URL = sys.argv[1]

    print(f"Testing Fashion Guru Bot at: {BOT_URL}")
    print("="*60)

    try:
        test_health()
        test_modules()
        test_chat("What fabric should I use for a summer dress?")
        print("\n✅ All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    main()
```

**Run it:**
```bash
python test_bot.py https://your-actual-url.run.app
```

---

## Monitoring Your Deployment

### View Logs
```bash
# Stream live logs
gcloud run services logs tail fashion-guru-bot --region us-central1

# Or view in browser
# Go to: https://console.cloud.google.com/run
# Click your service > Logs tab
```

### Check Usage
```bash
# View in Cloud Console
# Go to: https://console.cloud.google.com/run
# Click your service > Metrics tab
```

---

## Common Issues & Solutions

### Issue: "Permission denied" when deploying

**Solution:**
```bash
# Make sure you're authenticated
gcloud auth login

# Verify your project
gcloud config get-value project
```

### Issue: "Billing not enabled"

**Solution:**
Go to https://console.cloud.google.com/billing and link a billing account

### Issue: "Container failed to start"

**Solution:**
```bash
# Check logs
gcloud run services logs read fashion-guru-bot --region us-central1 --limit 50
```

### Issue: Can't access deployment URL

**Solution:**
```bash
# Check if service is running
gcloud run services describe fashion-guru-bot --region us-central1

# Make sure it's public
gcloud run services add-iam-policy-binding fashion-guru-bot \
  --region us-central1 \
  --member="allUsers" \
  --role="roles/run.invoker"
```

---

## Cleanup (When Done Testing)

**Stop spending money:**
```bash
# Delete the service
gcloud run services delete fashion-guru-bot --region us-central1

# Delete the container images (optional)
gcloud container images delete gcr.io/YOUR-PROJECT-ID/fashion-guru-bot
```

---

## Next Steps

After successful testing:
1. ✅ Share the URL with team members
2. ✅ Integrate into your apps/websites
3. ✅ Set up monitoring alerts
4. ✅ Configure custom domain (optional)
5. ✅ Add authentication (if needed)

---

**Need help?** Check the full deployment guide in `GOOGLE_CLOUD_DEPLOYMENT.md`
