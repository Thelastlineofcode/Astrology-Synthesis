# API Documentation

## Overview

The Roots Revealed API provides comprehensive endpoints for astrological chart creation, calculation, and interpretation. This RESTful API supports birth chart management, BMAD (Birth Matrix Analysis Dashboard) personality analysis, and Symbolon card interpretations.

**Version**: 1.0.0  
**Base URL**: `http://localhost:5000`  
**API Base URL**: `http://localhost:5000/api`

## Documentation Tools

### Swagger UI (Recommended)

Interactive API documentation with request/response examples:

**URL**: [http://localhost:5000/api-docs](http://localhost:5000/api-docs)

Features:
- Try out endpoints directly in the browser
- See request/response schemas
- View example requests and responses
- Test authentication flows

### OpenAPI Specification

Download the OpenAPI 3.0 specification:

**URL**: [http://localhost:5000/api-docs.json](http://localhost:5000/api-docs.json)

### Postman Collection

Import the Postman collection for API testing:

**File**: `backend/Roots-Revealed-API.postman_collection.json`

The collection includes:
- All API endpoints organized by category
- Pre-configured request examples
- Environment variables for token management
- Test scripts for automatic token extraction

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Registration Flow

1. Register a new user at `/api/auth/register`
2. Receive JWT token in response
3. Use token in Authorization header for protected endpoints

### Token Usage

Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Token Lifecycle

- **Issued**: On registration or login
- **Expires**: After 24 hours (configurable)
- **Refresh**: Use `/api/auth/refresh` to get a new token
- **Revoke**: Use `/api/auth/logout` (client-side token removal)

## API Endpoints

### Health & Info

#### GET /
Get basic API information and available endpoints.

**Response**: `200 OK`
```json
{
  "message": "Roots Revealed API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/api/health",
    "auth": "/api/auth",
    "charts": "/api/charts",
    "docs": "/api-docs"
  }
}
```

#### GET /api/health
Health check endpoint to verify API status.

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "API is healthy",
  "timestamp": "2025-10-29T06:00:00.000Z",
  "uptime": 1234.56,
  "environment": "development"
}
```

---

### Authentication Endpoints

#### POST /api/auth/register
Register a new user account.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

**Validation Rules**:
- `email`: Valid email format (required)
- `password`: Minimum 6 characters (required)
- `name`: Non-empty string (required)

**Response**: `201 Created`
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "1234567890",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses**:
- `400 Bad Request`: Validation errors or user already exists

---

#### POST /api/auth/login
Authenticate user and receive JWT token.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "1234567890",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses**:
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Invalid credentials

---

#### POST /api/auth/logout
Logout the current user (invalidate session).

**Headers**: `Authorization: Bearer <token>`

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Logout successful"
}
```

**Note**: Currently handled client-side by removing the token. Future versions will implement server-side token invalidation.

---

#### POST /api/auth/refresh
Refresh the JWT token.

**Headers**: `Authorization: Bearer <token>`

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or expired token

---

### Chart Management Endpoints

All chart endpoints require authentication.

#### GET /api/charts
Get all birth charts for the authenticated user with pagination.

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `page` (optional): Page number (default: 1, min: 1)
- `limit` (optional): Items per page (default: 10, min: 1, max: 100)

**Example**: `/api/charts?page=1&limit=10`

**Response**: `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": "1234567890",
      "userId": "9876543210",
      "name": "My Birth Chart",
      "birthDate": "1990-01-15",
      "birthTime": "14:30",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "createdAt": "2025-10-28T12:00:00.000Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 25,
    "totalPages": 3
  }
}
```

---

#### POST /api/charts
Create a new birth chart.

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "name": "My Birth Chart",
  "birthDate": "1990-01-15",
  "birthTime": "14:30",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

**Validation Rules**:
- `name`: Non-empty string (required)
- `birthDate`: ISO 8601 date format (required)
- `birthTime`: HH:MM format, 24-hour (required)
- `latitude`: Float between -90 and 90 (required)
- `longitude`: Float between -180 and 180 (required)

**Response**: `201 Created`
```json
{
  "success": true,
  "message": "Chart created successfully",
  "data": {
    "id": "1234567890",
    "userId": "9876543210",
    "name": "My Birth Chart",
    "birthDate": "1990-01-15",
    "birthTime": "14:30",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "createdAt": "2025-10-28T12:00:00.000Z"
  }
}
```

---

#### GET /api/charts/:id
Get a specific birth chart by ID.

**Headers**: `Authorization: Bearer <token>`

**URL Parameters**:
- `id`: Chart ID

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "1234567890",
    "userId": "9876543210",
    "name": "My Birth Chart",
    "birthDate": "1990-01-15",
    "birthTime": "14:30",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "createdAt": "2025-10-28T12:00:00.000Z"
  }
}
```

**Error Responses**:
- `404 Not Found`: Chart not found or doesn't belong to user

---

#### PUT /api/charts/:id
Update an existing birth chart.

**Headers**: `Authorization: Bearer <token>`

**URL Parameters**:
- `id`: Chart ID

**Request Body** (all fields optional):
```json
{
  "name": "Updated Chart Name",
  "birthDate": "1990-01-15",
  "birthTime": "15:00",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Chart updated successfully",
  "data": {
    "id": "1234567890",
    "userId": "9876543210",
    "name": "Updated Chart Name",
    "birthDate": "1990-01-15",
    "birthTime": "15:00",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "createdAt": "2025-10-28T12:00:00.000Z"
  }
}
```

**Error Responses**:
- `400 Bad Request`: Validation errors
- `404 Not Found`: Chart not found or doesn't belong to user

---

#### DELETE /api/charts/:id
Delete a birth chart.

**Headers**: `Authorization: Bearer <token>`

**URL Parameters**:
- `id`: Chart ID

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Chart deleted successfully"
}
```

**Error Responses**:
- `404 Not Found`: Chart not found or doesn't belong to user

---

### Calculation & Interpretation Endpoints

#### POST /api/charts/calculate
Calculate astrological chart data for given birth information.

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "birthDate": "1990-01-15",
  "birthTime": "14:30",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "houseSystem": "Placidus"
}
```

**Validation Rules**:
- `birthDate`: ISO 8601 date format (required)
- `birthTime`: HH:MM format, 24-hour (required)
- `latitude`: Float between -90 and 90 (required)
- `longitude`: Float between -180 and 180 (required)
- `houseSystem` (optional): One of: Placidus, Koch, Whole Sign, Equal (default: Placidus)

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "planets": [
      {
        "name": "Sun",
        "longitude": 295.5,
        "latitude": 0.0,
        "sign": "Capricorn",
        "house": 10,
        "isRetrograde": false
      },
      {
        "name": "Moon",
        "longitude": 123.2,
        "latitude": 5.1,
        "sign": "Cancer",
        "house": 4,
        "isRetrograde": false
      }
    ],
    "houses": [
      {
        "number": 1,
        "longitude": 120.5,
        "sign": "Cancer"
      }
    ],
    "aspects": [
      {
        "planet1": "Sun",
        "planet2": "Moon",
        "aspect": "Trine",
        "orb": 2.5
      }
    ],
    "metadata": {
      "birthDate": "1990-01-15",
      "birthTime": "14:30",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "houseSystem": "Placidus",
      "calculatedAt": "2025-10-29T06:00:00.000Z"
    }
  }
}
```

**Note**: Current implementation returns mock data. Production version will use Swiss Ephemeris for accurate calculations.

---

#### GET /api/charts/:id/interpretation
Get BMAD analysis and Symbolon card interpretations for a chart.

**Headers**: `Authorization: Bearer <token>`

**URL Parameters**:
- `id`: Chart ID

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "chartId": "1234567890",
    "bmadAnalysis": {
      "personalityProfile": {
        "coreTraits": ["Leadership", "Ambition", "Practical"],
        "strengths": ["Strategic thinking", "Goal-oriented", "Disciplined"],
        "challenges": ["Workaholic tendencies", "Emotional restraint"]
      },
      "behaviorPredictions": {
        "careerPath": "Executive or entrepreneurial roles with high responsibility",
        "relationships": "Seeks stability and commitment, values loyalty",
        "lifeThemes": "Achievement, recognition, and building lasting legacy"
      }
    },
    "symbolonCards": [
      {
        "name": "The Father (Sun in Capricorn)",
        "meaning": "Authority, responsibility, and achievement",
        "position": "Sun in Capricorn in 10th House",
        "interpretation": "Strong father archetype energy. Natural leader with high ambitions."
      }
    ],
    "insights": "This chart shows a powerful blend of ambition and emotional depth...",
    "generatedAt": "2025-10-29T06:00:00.000Z"
  }
}
```

**Error Responses**:
- `404 Not Found`: Chart not found or doesn't belong to user

**Note**: Current implementation returns mock interpretations. Production version will use BMAD analysis engine and Symbolon interpretation service.

---

## Error Handling

### Standard Error Response

All errors follow this format:

```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "statusCode": 400
  }
}
```

### Validation Error Response

Validation errors include field-specific details:

```json
{
  "success": false,
  "errors": [
    {
      "field": "email",
      "message": "Valid email is required"
    },
    {
      "field": "password",
      "message": "Password must be at least 6 characters"
    }
  ]
}
```

### HTTP Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data or validation error
- `401 Unauthorized` - Missing, invalid, or expired authentication token
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error (contact support)

---

## Rate Limiting

**Status**: Not yet implemented (planned for future release)

Planned limits:
- 100 requests per minute per IP
- 1000 requests per hour per user
- 50 chart calculations per day per user

---

## Best Practices

### 1. Token Management

- Store tokens securely (httpOnly cookies or secure storage)
- Refresh tokens before expiration
- Clear tokens on logout
- Never expose tokens in URLs or logs

### 2. Error Handling

- Always check the `success` field in responses
- Handle all documented error codes
- Provide user-friendly error messages
- Log errors for debugging

### 3. API Calls

- Use pagination for list endpoints
- Cache responses when appropriate
- Handle network failures gracefully
- Implement retry logic for transient failures

### 4. Performance

- Minimize unnecessary API calls
- Use GET /api/charts with pagination instead of multiple individual requests
- Calculate charts only when needed (calculations are resource-intensive)
- Cache interpretation results

---

## Testing

### Manual Testing with cURL

```bash
# 1. Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}'

# 2. Login (save the token)
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  | jq -r '.data.token')

# 3. Create Chart
curl -X POST http://localhost:5000/api/charts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Test Chart",
    "birthDate":"1990-01-15",
    "birthTime":"14:30",
    "latitude":40.7128,
    "longitude":-74.0060
  }'

# 4. Get All Charts
curl -X GET http://localhost:5000/api/charts \
  -H "Authorization: Bearer $TOKEN"

# 5. Calculate Chart
curl -X POST http://localhost:5000/api/charts/calculate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "birthDate":"1990-01-15",
    "birthTime":"14:30",
    "latitude":40.7128,
    "longitude":-74.0060
  }'
```

### Automated Testing

Run the test suite:

```bash
cd backend
npm test
```

Test coverage includes:
- Authentication flows
- Chart CRUD operations
- Calculation endpoints
- Interpretation endpoints
- Input validation
- Error handling
- Pagination

---

## Support & Feedback

- **GitHub Issues**: [Report bugs or request features](https://github.com/Thelastlineofcode/Astrology-Synthesis/issues)
- **Documentation**: This file and Swagger UI
- **API Status**: Check `/api/health` endpoint

---

## Version History

### v1.0.0 (2025-10-29)

**Initial Release**

- Complete authentication system (register, login, logout, refresh)
- Chart management (CRUD operations)
- Chart calculation endpoint (mock implementation)
- Chart interpretation with BMAD and Symbolon (mock implementation)
- Pagination support for list endpoints
- Comprehensive Swagger/OpenAPI documentation
- Postman collection for testing
- Full test coverage

**Planned for v1.1.0**:
- Real Swiss Ephemeris integration for calculations
- Real BMAD analysis engine integration
- Real Symbolon interpretation service
- Rate limiting
- Database persistence (currently in-memory)
- Advanced filtering and search
- Chart sharing capabilities

---

**Last Updated**: October 29, 2025  
**API Version**: 1.0.0  
**Documentation Version**: 1.0.0
