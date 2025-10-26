# Fashion Guru Bot - API Documentation

## Overview

The Fashion Guru Bot API provides RESTful endpoints for interacting with the bot's modules and managing conversations.

**Base URL:** `http://localhost:5000` (default)

**Content-Type:** `application/json`

## Authentication

Currently, no authentication is required. For production deployment, implement API keys or OAuth2.

## Endpoints

### 1. Health Check

Check if the API is running and get basic information.

**Endpoint:** `GET /health`

**Response:**
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

**Status Codes:**
- `200 OK`: Service is healthy

---

### 2. Chat

Send a message to the bot and receive a response.

**Endpoint:** `POST /chat`

**Request Body:**
```json
{
  "user_id": "user123",
  "message": "What fabric should I use for a summer dress?",
  "context": {}  // Optional
}
```

**Response:**
```json
{
  "success": true,
  "response": {
    "message": "**Fabric Recommendations for Your Dress:**\n\n**Cotton**...",
    "intent": {
      "primary_pillar": "pillar1",
      "module": "fabric_oracle",
      "confidence": 0.9,
      "type": "technical"
    },
    "module": "fabric_oracle",
    "timestamp": "2025-10-26T12:34:56.789Z",
    "context_length": 2
  }
}
```

**Status Codes:**
- `200 OK`: Message processed successfully
- `400 Bad Request`: Missing required fields
- `500 Internal Server Error`: Processing error

**Example with cURL:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "How do I draft a bodice pattern?"
  }'
```

**Example with Python:**
```python
import requests

response = requests.post('http://localhost:5000/chat', json={
    'user_id': 'user123',
    'message': 'What are the current fashion trends?'
})

data = response.json()
print(data['response']['message'])
```

---

### 3. List Modules

Get a list of all available bot modules.

**Endpoint:** `GET /modules`

**Response:**
```json
{
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

**Status Codes:**
- `200 OK`: Modules retrieved successfully

---

### 4. Module Information

Get information about a specific module.

**Endpoint:** `GET /modules/<module_name>`

**Parameters:**
- `module_name`: Name of the module

**Response:**
```json
{
  "name": "fabric_oracle",
  "type": "FabricOracle",
  "available": true
}
```

**Status Codes:**
- `200 OK`: Module found
- `404 Not Found`: Module doesn't exist

**Example:**
```bash
curl http://localhost:5000/modules/fabric_oracle
```

---

### 5. Get User Context

Retrieve conversation context for a specific user.

**Endpoint:** `GET /context/<user_id>`

**Parameters:**
- `user_id`: Unique user identifier

**Response:**
```json
{
  "user_id": "user123",
  "context": {
    "user_id": "user123",
    "messages": [
      {
        "role": "user",
        "content": "What fabric for summer dress?",
        "timestamp": "2025-10-26T12:30:00",
        "metadata": {}
      },
      {
        "role": "assistant",
        "content": "For a summer dress...",
        "timestamp": "2025-10-26T12:30:01",
        "metadata": {}
      }
    ],
    "user_profile": {
      "skill_level": "beginner",
      "interests": [],
      "learning_path": [],
      "projects": []
    },
    "session_data": {},
    "created_at": "2025-10-26T12:00:00",
    "last_updated": "2025-10-26T12:30:01"
  }
}
```

**Status Codes:**
- `200 OK`: Context retrieved successfully
- `500 Internal Server Error`: Error retrieving context

---

### 6. Delete User Context

Delete conversation context for a specific user.

**Endpoint:** `DELETE /context/<user_id>`

**Parameters:**
- `user_id`: Unique user identifier

**Response:**
```json
{
  "success": true,
  "message": "Context for user user123 deleted"
}
```

**Status Codes:**
- `200 OK`: Context deleted successfully
- `500 Internal Server Error`: Error deleting context

**Example:**
```bash
curl -X DELETE http://localhost:5000/context/user123
```

---

### 7. Bot Statistics

Get bot usage statistics.

**Endpoint:** `GET /stats`

**Response:**
```json
{
  "active_conversations": 15,
  "modules_loaded": 6
}
```

**Status Codes:**
- `200 OK`: Statistics retrieved successfully

---

## Webhooks

The bot supports webhooks for popular messaging platforms.

### Webhook Endpoint

**Endpoint:** `POST /webhook/<platform>`

**Supported Platforms:**
- `slack`
- `discord`
- `telegram`

**Example (Slack):**
```bash
curl -X POST http://localhost:5000/webhook/slack \
  -H "Content-Type: application/json" \
  -d '{
    "event": {
      "user": "U123456",
      "text": "What fabric should I use?",
      "channel": "C123456"
    }
  }'
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

**Common Error Codes:**
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider adding rate limiting to prevent abuse.

**Recommended Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1635264000
```

---

## CORS

CORS is enabled for all origins by default. For production, configure specific allowed origins in `config.yaml`.

---

## Best Practices

### 1. Use Unique User IDs
```python
# Good
user_id = f"user_{uuid.uuid4()}"

# Bad
user_id = "anonymous"
```

### 2. Handle Errors Gracefully
```python
try:
    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

### 3. Maintain Context
```python
# Keep the same user_id for a conversation
user_id = "user123"

# First message
response1 = chat(user_id, "What fabric for summer dress?")

# Follow-up (context maintained)
response2 = chat(user_id, "What about winter?")
```

### 4. Check Module Availability
```python
modules = requests.get(f"{BASE_URL}/modules").json()
if "fabric_oracle" in modules['modules']:
    # Proceed with fabric-related queries
    pass
```

---

## Integration Examples

### Python SDK (Simplified)

```python
class FashionGuruClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.user_id = None

    def chat(self, message, user_id=None):
        if user_id is None:
            user_id = self.user_id or "default_user"

        response = requests.post(
            f"{self.base_url}/chat",
            json={"user_id": user_id, "message": message}
        )
        return response.json()

    def get_modules(self):
        response = requests.get(f"{self.base_url}/modules")
        return response.json()

# Usage
client = FashionGuruClient()
result = client.chat("What are current fashion trends?")
print(result['response']['message'])
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

class FashionGuruClient {
  constructor(baseUrl = 'http://localhost:5000') {
    this.baseUrl = baseUrl;
  }

  async chat(userId, message) {
    const response = await axios.post(`${this.baseUrl}/chat`, {
      user_id: userId,
      message: message
    });
    return response.data;
  }

  async getModules() {
    const response = await axios.get(`${this.baseUrl}/modules`);
    return response.data;
  }
}

// Usage
const client = new FashionGuruClient();
client.chat('user123', 'How do I draft a skirt pattern?')
  .then(data => console.log(data.response.message));
```

---

## WebSocket Support (Future)

Currently, the API uses HTTP REST. WebSocket support for real-time conversations is planned for a future release.

---

## Versioning

Current API Version: **v1.0.0**

The API follows semantic versioning. Breaking changes will result in a new major version.

---

## Support

For API issues or questions:
- GitHub Issues: [github.com/yourusername/fashion-guru-bot/issues](https://github.com/yourusername/fashion-guru-bot/issues)
- Email: support@fashiongurubot.com
