# Event Logging API

## Overview
This project is a simple Flask-based web application designed to log and retrieve events through a RESTful API. It allows users to post events with specific details and retrieve them using unique event IDs. This project aims to provide a basic, yet functional, event logging system with thread-safe operations.

## Features
- **Create Event**: Log new events with details like event type, service name, and additional data.
- **Retrieve All Events**: Fetch a list of all logged events.
- **Retrieve Specific Event**: Fetch a specific event by its unique event ID.

## Endpoints
### POST /events
Logs a new event.

**Request Body:**
```json
{
    "event_type": "string",
    "service_name": "string",
    "additional_data": "string"
}
```

**Response:**
- `201 Created`: Returns the created event with its unique ID.

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"event_type": "ERROR", "service_name": "AuthService", "additional_data": "Timeout error"}' http://localhost:5000/events
```

### GET /events
Retrieves all logged events.

**Response:**
- `200 OK`: Returns a list of all events.

**Example:**
```bash
curl -X GET http://localhost:5000/events
```

### GET /events/<int:event_id>
Retrieves a specific event by its ID.

**Response:**
- `200 OK`: Returns the event with the specified ID.
- `404 Not Found`: If no event is found with the given ID.

**Example:**
```bash
curl -X GET http://localhost:5000/events/1
```

## Implementation Details
- **Thread Safety**: Utilizes `threading.Lock` to ensure thread-safe operations on the event log.
- **Unique IDs**: Generates unique IDs for each event using `itertools.count`.
- **Error Handling**: Proper error handling for invalid requests and not found resources.
- **Timestamps**: Adds a creation date timestamp to each logged event.

## Getting Started
### Prerequisites
- Python 3.x
- Flask

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/event-logging-api.git
    ```
2. Change to the project directory:
    ```bash
    cd event-logging-api
    ```
3. Install the required packages:
    ```bash
    pip install flask
    ```

### Running the Application
1. Run the Flask app:
    ```bash
    python app.py
    ```
2. The application will start on `http://localhost:5000`.

## Author
Cedric Harfouche

## Acknowledgments
This project was a learning experience in web development with Flask and thread-safe programming in Python. 
