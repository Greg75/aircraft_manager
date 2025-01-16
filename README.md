# Aircraft Manager API

This repository contains a FastAPI application for managing aircraft data. The application includes endpoints for health checks, database management, and aircraft-related operations.

## Features

- **Health Check**: Ensures the application and database are operational.
- **Aircraft Management**: Provides routes for managing aircraft data.
- **Database Integration**: Automatically creates database tables on startup.

## Prerequisites

- Python 3.8+
- PostgreSQL database.
- [Poetry](https://python-poetry.org/) for dependency management.
- Environment variables set up via a `.env` file.

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/Greg75/aircraft_manager.git
    cd aircraft_manager
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies using Poetry:

    ```bash
    poetry install
    ```

4. Create a `.env` file with the following variables:

    ```env
    HOST=127.0.0.1
    PORT=8000
    RELOAD=True
    DATABASE_URL=<your-database-url>
    ```

## Running the Application

Start the FastAPI server by running:

```bash
python main.py
```

The application will be available at `http://127.0.0.1:8000` by default.

## Endpoints

### Health Check

**GET** `/health`

- Returns the health status of the application and database.
- Example response when healthy:

  ```json
  {
      "status": "HEALTHY",
      "database": "OK"
  }
  ```

- Example response when unhealthy:

  ```json
  {
      "status": "UNHEALTHY",
      "database": "DOWN"
  }
  ```

### Aircraft Management

**Base Path**: `/aircrafts`

#### Show All Aircraft

**GET** `/`

- Returns a list of all aircraft in the database.
- Response model: `list[AircraftDisplaySchema]`

#### Add an Aircraft

**POST** `/add_aircraft/`

- Adds a new aircraft to the database.
- Request body: `AircraftBaseSchema`
- Response model: `AircraftDisplaySchema`

#### Update an Aircraft

**PATCH** `/update_aircraft/{aircraft_id}`

- Updates an existing aircraft in the database.
- Path parameter: `aircraft_id` (int)
- Request body: `AircraftUpdateSchema`
- Response model: `AircraftUpdateSchema`

#### Delete an Aircraft

**DELETE** `/delete_aircraft/{aircraft_id}`

- Deletes an aircraft from the database.
- Path parameter: `aircraft_id` (int)
- Response: Confirmation message.

### Aircraft Performance

#### Calculate Range

**GET** `/performance/range/{parameters}`

- Calculates the range of an aircraft based on input parameters.
- Request parameters: `InputAircraftPerformanceRangeSchema`
- Response model: `OutputAircraftPerformanceRangeSchema`

#### Calculate Endurance

**GET** `/performance/endurance/{parameters}`

- Calculates the endurance of an aircraft based on input parameters.
- Request parameters: `InputAircraftPerformanceEnduranceSchema`
- Response model: `OutputAircraftPerformanceEnduranceSchema`

## Code Overview

### Key Files

- **`main.py`**: Entry point for the application. Initializes the FastAPI instance and includes routing.
- **`aircraft_manager/src/utils/init_db.py`**: Handles database table creation.
- **`aircraft_manager/src/router/api.py`**: Defines API routes for aircraft management.
- **`aircraft_manager/src/config/database.py`**: Manages database connections.

### Lifespan Events

- **Startup**: Creates database tables.
- **Shutdown**: Closes database connections gracefully.

## Development

1. Enable FastAPI's auto-reload feature for development by setting `RELOAD=True` in the `.env` file.
2. Run the server using:

    ```bash
    uvicorn main:app --host 127.0.0.1 --port 8000 --reload
    ```

## Logging

The application uses Python's built-in `logging` module for logging important events and errors.

## Testing

To add unit or integration tests, consider using [pytest](https://pytest.org/):

1. Install pytest:

    ```bash
    poetry add pytest --dev
    ```

2. Run tests:

    ```bash
    pytest
    ```

## Deployment

Use a production-ready server like Gunicorn or Docker for deploying the application. Example Gunicorn command:

```bash
gunicorn -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:8000
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
