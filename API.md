# API Documentation

## Base URL

```
https://f1-report-system-[hash]-uc.a.run.app
```

## Endpoints

### Health Check

```http
GET /
```

Returns service status.

**Response:**

```json
{
  "status": "healthy",
  "service": "F1 Report System"
}
```

### Generate Race Report

```http
POST /analyze
```

Generate a social media post for a specific F1 race.

**Request Body:**

```json
{
  "race_input": "Monaco"
}
```

Accepts either:
- GP name (e.g., "Monaco", "Bahrain")
- Round number (e.g., "1", "8")

**Response:**

```json
{
  "race_id": "2025_R8",
  "gp_name": "Monaco Grand Prix",
  "social_media_post": "Race report content...",
  "timestamp": "2025-11-25T10:30:00.123456"
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid race input or data unavailable
- `500` - Report generation failed

### List All Reports

```http
GET /history
```

Retrieve all stored race reports.

**Response:**

```json
[
  {
    "race_id": "2025_R1",
    "gp_name": "Bahrain Grand Prix",
    "timestamp": "2025-11-25T10:00:00.123456"
  },
  {
    "race_id": "2025_R8",
    "gp_name": "Monaco Grand Prix",
    "timestamp": "2025-11-25T10:30:00.123456"
  }
]
```

### Search Reports

```http
POST /search
```

Search stored reports by race ID or GP name.

**Request Body:**

```json
{
  "query": "Monaco"
}
```

**Response:**

```json
[
  {
    "race_id": "2025_R8",
    "gp_name": "Monaco Grand Prix",
    "timestamp": "2025-11-25T10:30:00.123456"
  }
]
```

### Get Specific Report

```http
GET /report/{race_id}
```

Retrieve a specific race report by ID.

**Parameters:**
- `race_id` - Race identifier (e.g., "2025_R8")

**Response:**

```json
{
  "data": {
    "race_id": "2025_R8",
    "race_data": {
      "year": 2025,
      "round": 8,
      "gp_info": {
        "name": "Monaco Grand Prix",
        "country": "Monaco",
        "circuit": "Circuit de Monaco"
      },
      "podium": [
        {
          "position": 1,
          "full_name": "Driver Name",
          "team": "Team Name",
          "grid_position": 1,
          "time": "1:29:30.123",
          "points": 25.0
        }
      ],
      "final_results": []
    },
    "social_media_post": "Race report content...",
    "timestamp": "2025-11-25T10:30:00.123456"
  },
  "timestamp": "2025-11-25T10:30:00.123456"
}
```

**Status Codes:**
- `200` - Success
- `404` - Report not found

## Error Responses

All endpoints return errors in this format:

```json
{
  "detail": "Error message"
}
```

## Rate Limits

Cloud Run default limits apply. Adjust service configuration for higher throughput.

## Authentication

Current deployment allows unauthenticated access. For production, configure Cloud Run authentication.

