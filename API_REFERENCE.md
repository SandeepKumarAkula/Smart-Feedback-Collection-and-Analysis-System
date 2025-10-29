# 🔌 API Reference - Smart Feedback Collection and Analysis System

## Overview

This document provides comprehensive API documentation for the Smart Feedback Collection and Analysis System. The API follows RESTful principles and returns JSON responses.

**Base URL:** `http://your-domain.com` or `https://your-replit-app.repl.co`

---

## Table of Contents

1. [Authentication](#authentication)
2. [Public API Endpoints](#public-api-endpoints)
3. [Protected API Endpoints](#protected-api-endpoints)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [Examples](#examples)

---

## Authentication

### Session-Based Authentication

The API uses Flask session-based authentication. After successful login, a session cookie is set that must be included in subsequent requests.

**Session Cookie Name:** `session`

**Session Data:**
```json
{
  "user_id": 1,
  "user_name": "John Doe",
  "user_role": "user"
}
```

### Login Flow

```http
POST /login
Content-Type: application/x-www-form-urlencoded

email=user@example.com&password=SecurePassword123
```

**Response:**
- **Success:** Redirect to appropriate dashboard with session cookie
- **Failure:** Redirect to login page with error message

---

## Public API Endpoints

### 1. Get Sentiment Statistics

Returns aggregated sentiment statistics for all feedback.

**Endpoint:** `GET /api/sentiment-stats`

**Authentication:** None required

**Request:**
```http
GET /api/sentiment-stats HTTP/1.1
Host: your-domain.com
Accept: application/json
```

**Response:**
```json
{
  "positive": 45,
  "negative": 12,
  "neutral": 23
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `positive` | integer | Count of positive feedback |
| `negative` | integer | Count of negative feedback |
| `neutral` | integer | Count of neutral feedback |

**Status Codes:**
- `200 OK` - Success

**Example cURL:**
```bash
curl -X GET https://your-domain.com/api/sentiment-stats
```

**Example JavaScript:**
```javascript
fetch('/api/sentiment-stats')
  .then(response => response.json())
  .then(data => {
    console.log('Positive:', data.positive);
    console.log('Negative:', data.negative);
    console.log('Neutral:', data.neutral);
  });
```

---

### 2. Get Chart Data

Returns comprehensive analytics data for visualizations.

**Endpoint:** `GET /api/chart-data`

**Authentication:** None required

**Request:**
```http
GET /api/chart-data HTTP/1.1
Host: your-domain.com
Accept: application/json
```

**Response:**
```json
{
  "sentiment": {
    "Positive": 45,
    "Negative": 12,
    "Neutral": 23
  },
  "categories": {
    "Product": 30,
    "Service": 25,
    "Support": 15,
    "Website": 8,
    "Other": 2
  },
  "category_sentiment": {
    "Product": {
      "Positive": 20,
      "Neutral": 8,
      "Negative": 2
    },
    "Service": {
      "Positive": 15,
      "Neutral": 7,
      "Negative": 3
    },
    "Support": {
      "Positive": 8,
      "Neutral": 5,
      "Negative": 2
    },
    "Website": {
      "Positive": 5,
      "Neutral": 2,
      "Negative": 1
    },
    "Other": {
      "Positive": 1,
      "Neutral": 1,
      "Negative": 0
    }
  },
  "ratings": {
    "1": 3,
    "2": 5,
    "3": 12,
    "4": 28,
    "5": 32
  },
  "timeline": {
    "2025-10-15": 8,
    "2025-10-16": 12,
    "2025-10-17": 15,
    "2025-10-18": 20,
    "2025-10-19": 25
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `sentiment` | object | Sentiment distribution counts |
| `sentiment.Positive` | integer | Count of positive feedback |
| `sentiment.Negative` | integer | Count of negative feedback |
| `sentiment.Neutral` | integer | Count of neutral feedback |
| `categories` | object | Feedback count by category |
| `category_sentiment` | object | Nested sentiment breakdown per category |
| `ratings` | object | Distribution of 1-5 star ratings |
| `timeline` | object | Daily feedback counts (date: count) |

**Status Codes:**
- `200 OK` - Success

**Example cURL:**
```bash
curl -X GET https://your-domain.com/api/chart-data
```

**Example JavaScript:**
```javascript
fetch('/api/chart-data')
  .then(response => response.json())
  .then(data => {
    // Use data for Chart.js visualizations
    console.log('Sentiment:', data.sentiment);
    console.log('Categories:', data.categories);
    console.log('Timeline:', data.timeline);
  });
```

**Example Python:**
```python
import requests

response = requests.get('https://your-domain.com/api/chart-data')
data = response.json()

print(f"Total Positive: {data['sentiment']['Positive']}")
print(f"Total Negative: {data['sentiment']['Negative']}")
print(f"Total Neutral: {data['sentiment']['Neutral']}")
```

---

## Protected API Endpoints

### 3. Submit Guest Feedback

Submit feedback as a guest user (no authentication required).

**Endpoint:** `POST /guest-feedback`

**Authentication:** None required (but must not be logged in)

**Request:**
```http
POST /guest-feedback HTTP/1.1
Host: your-domain.com
Content-Type: application/x-www-form-urlencoded

name=John+Doe&email=john@example.com&category=Product&message=Great+product!&rating=5
```

**Form Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Guest's full name |
| `email` | string | Yes | Guest's email address |
| `category` | string | Yes | Feedback category (Product/Service/Support/Website/Other) |
| `message` | string | Yes | Feedback message text |
| `rating` | integer | No | Star rating (1-5) |

**Response:**
- **Success:** Redirect to home page with success message
- **Failure:** Redirect to feedback form with error message

**Sentiment Analysis:**
The system automatically analyzes the `message` field and assigns a sentiment:
- **Positive:** Polarity > 0.1
- **Negative:** Polarity < -0.1
- **Neutral:** -0.1 ≤ Polarity ≤ 0.1

**Example cURL:**
```bash
curl -X POST https://your-domain.com/guest-feedback \
  -d "name=John Doe" \
  -d "email=john@example.com" \
  -d "category=Product" \
  -d "message=This product exceeded my expectations!" \
  -d "rating=5"
```

**Example JavaScript:**
```javascript
const formData = new FormData();
formData.append('name', 'John Doe');
formData.append('email', 'john@example.com');
formData.append('category', 'Product');
formData.append('message', 'Great product!');
formData.append('rating', '5');

fetch('/guest-feedback', {
  method: 'POST',
  body: formData
})
.then(response => {
  if (response.redirected) {
    window.location.href = response.url;
  }
});
```

---

### 4. Submit User Feedback

Submit feedback as a registered user (authentication required).

**Endpoint:** `POST /user-feedback`

**Authentication:** Required (must be logged in as 'user' role)

**Request:**
```http
POST /user-feedback HTTP/1.1
Host: your-domain.com
Content-Type: application/x-www-form-urlencoded
Cookie: session=<session-cookie>

category=Service&message=Excellent+customer+service!&rating=5
```

**Form Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `category` | string | Yes | Feedback category |
| `message` | string | Yes | Feedback message text |
| `rating` | integer | No | Star rating (1-5) |

**Note:** User's name and ID are automatically retrieved from session.

**Response:**
- **Success:** Redirect to user dashboard with success message
- **Failure:** Redirect to feedback form with error message

**Example cURL:**
```bash
curl -X POST https://your-domain.com/user-feedback \
  -b "session=<session-cookie>" \
  -d "category=Service" \
  -d "message=Excellent customer service!" \
  -d "rating=5"
```

---

### 5. Delete Feedback (Admin Only)

Delete a specific feedback entry.

**Endpoint:** `POST /admin/delete-feedback/<id>`

**Authentication:** Required (must be logged in as 'admin' role)

**Request:**
```http
POST /admin/delete-feedback/42 HTTP/1.1
Host: your-domain.com
Cookie: session=<admin-session-cookie>
```

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Feedback ID to delete |

**Response:**
- **Success:** Redirect to admin dashboard with success message
- **Failure:** 404 Not Found if feedback doesn't exist

**Status Codes:**
- `302 Found` - Redirect after successful deletion
- `404 Not Found` - Feedback ID doesn't exist
- `403 Forbidden` - Not authorized (not admin)

**Example cURL:**
```bash
curl -X POST https://your-domain.com/admin/delete-feedback/42 \
  -b "session=<admin-session-cookie>"
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| `200` | OK | Request successful |
| `302` | Found | Redirect (common for form submissions) |
| `400` | Bad Request | Invalid request parameters |
| `401` | Unauthorized | Authentication required |
| `403` | Forbidden | Insufficient permissions |
| `404` | Not Found | Resource not found |
| `500` | Internal Server Error | Server error |

### Error Response Format

For API endpoints, errors are typically handled via Flask flash messages and redirects. For JSON endpoints:

```json
{
  "error": "Error message description",
  "status": 400
}
```

### Common Error Scenarios

#### 1. Unauthorized Access
```http
GET /user-dashboard HTTP/1.1
Host: your-domain.com
```

**Response:** Redirect to `/login` with flash message: "Please login to access this page."

#### 2. Insufficient Permissions
```http
GET /admin-dashboard HTTP/1.1
Host: your-domain.com
Cookie: session=<user-session-cookie>
```

**Response:** Redirect to `/` with flash message: "Admin access required."

#### 3. Invalid Feedback ID
```http
POST /admin/delete-feedback/99999 HTTP/1.1
Host: your-domain.com
Cookie: session=<admin-session-cookie>
```

**Response:** `404 Not Found`

---

## Rate Limiting

Currently, the API does not implement rate limiting. For production deployments, consider implementing:

- **Per-IP rate limiting:** 100 requests per minute
- **Per-user rate limiting:** 1000 requests per hour
- **Feedback submission limiting:** 10 submissions per hour per IP

**Recommended Implementation:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)

@app.route('/api/chart-data')
@limiter.limit("60 per minute")
def chart_data():
    # ... implementation
```

---

## Examples

### Complete Workflow Example

#### 1. Register a New User

```javascript
// Register
fetch('/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    name: 'Jane Smith',
    email: 'jane@example.com',
    password: 'SecurePass123!'
  })
});
```

#### 2. Login

```javascript
// Login
fetch('/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    email: 'jane@example.com',
    password: 'SecurePass123!'
  }),
  credentials: 'include' // Important: Include cookies
});
```

#### 3. Submit Feedback

```javascript
// Submit feedback (as logged-in user)
fetch('/user-feedback', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    category: 'Product',
    message: 'Amazing product! Highly recommend.',
    rating: '5'
  }),
  credentials: 'include'
});
```

#### 4. View Analytics

```javascript
// Get chart data
fetch('/api/chart-data', {
  credentials: 'include'
})
.then(response => response.json())
.then(data => {
  // Create Chart.js visualizations
  createSentimentChart(data.sentiment);
  createCategoryChart(data.categories);
  createTimelineChart(data.timeline);
});
```

### Python Integration Example

```python
import requests
from requests.sessions import Session

# Create session to persist cookies
session = Session()

# Base URL
BASE_URL = 'https://your-domain.com'

# 1. Login
login_data = {
    'email': 'admin@example.com',
    'password': 'AdminPass123!'
}
response = session.post(f'{BASE_URL}/login', data=login_data)

# 2. Get chart data
chart_data = session.get(f'{BASE_URL}/api/chart-data').json()

# 3. Analyze data
total_feedback = sum(chart_data['sentiment'].values())
positive_percentage = (chart_data['sentiment']['Positive'] / total_feedback) * 100

print(f"Total Feedback: {total_feedback}")
print(f"Positive Percentage: {positive_percentage:.2f}%")

# 4. Get sentiment stats
sentiment_stats = session.get(f'{BASE_URL}/api/sentiment-stats').json()
print(f"Sentiment Stats: {sentiment_stats}")
```

### Chart.js Integration Example

```javascript
// Fetch data and create charts
async function initializeCharts() {
  try {
    const response = await fetch('/api/chart-data');
    const data = await response.json();
    
    // Sentiment Pie Chart
    const sentimentCtx = document.getElementById('sentimentChart').getContext('2d');
    new Chart(sentimentCtx, {
      type: 'pie',
      data: {
        labels: ['Positive', 'Negative', 'Neutral'],
        datasets: [{
          data: [
            data.sentiment.Positive,
            data.sentiment.Negative,
            data.sentiment.Neutral
          ],
          backgroundColor: ['#28a745', '#dc3545', '#6c757d']
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Sentiment Distribution'
          }
        }
      }
    });
    
    // Timeline Line Chart
    const timelineCtx = document.getElementById('timelineChart').getContext('2d');
    new Chart(timelineCtx, {
      type: 'line',
      data: {
        labels: Object.keys(data.timeline),
        datasets: [{
          label: 'Feedback Count',
          data: Object.values(data.timeline),
          borderColor: '#007bff',
          backgroundColor: 'rgba(0, 123, 255, 0.1)',
          fill: true
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Feedback Timeline'
          }
        }
      }
    });
    
  } catch (error) {
    console.error('Error fetching chart data:', error);
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initializeCharts);
```

---

## Data Models

### User Object

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user",
  "created_at": "2025-10-15T10:30:00Z"
}
```

### Feedback Object

```json
{
  "id": 42,
  "user_id": 1,
  "guest_name": null,
  "guest_email": null,
  "category": "Product",
  "message": "Great product! Highly recommend.",
  "rating": 5,
  "sentiment": "Positive",
  "timestamp": "2025-10-29T14:30:00Z"
}
```

### Guest Feedback Object

```json
{
  "id": 43,
  "user_id": null,
  "guest_name": "Jane Smith",
  "guest_email": "jane@example.com",
  "category": "Service",
  "message": "Excellent customer service!",
  "rating": 5,
  "sentiment": "Positive",
  "timestamp": "2025-10-29T15:00:00Z"
}
```

---

## Best Practices

### 1. Always Include Credentials
```javascript
fetch('/api/endpoint', {
  credentials: 'include' // Important for session cookies
});
```

### 2. Handle Redirects Properly
```javascript
fetch('/login', {
  method: 'POST',
  body: formData,
  redirect: 'follow'
})
.then(response => {
  if (response.redirected) {
    window.location.href = response.url;
  }
});
```

### 3. Error Handling
```javascript
fetch('/api/chart-data')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    // Process data
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

### 4. Validate Input
```javascript
function validateFeedback(message, rating) {
  if (!message || message.trim().length === 0) {
    throw new Error('Message is required');
  }
  if (rating && (rating < 1 || rating > 5)) {
    throw new Error('Rating must be between 1 and 5');
  }
}
```

---

## Changelog

### Version 1.0 (October 29, 2025)
- Initial API documentation
- Added `/api/sentiment-stats` endpoint
- Added `/api/chart-data` endpoint
- Documented authentication flow
- Added comprehensive examples

---

## Support

For API support or questions:
- **GitHub Issues:** [Create an issue](https://github.com/SandeepKumarAkula/Smart-Feedback-Collection-and-Analysis-System/issues)
- **Email:** kumarakula44@gmail.com

---

**Document Version:** 1.0  
**Last Updated:** October 29, 2025  
**Author:** Sandeep Kumar Akula
