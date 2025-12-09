# foxhole-db
JSON API for Foxhole recipes.

Currently supported recipes:
- Refinery
- Factory

## Requirements
- Python3
- uv

## Installation
```
uv sync
```

## Running the server
```
fastapi dev app/main.py
```
Runs the server on localhost on port 8000.

## Documentation
Once the server is running, please visit `localhost:8000/docs` or `localhost:8000/redoc` to view the API documentation.

### Additional Documentation
The API endpoints process the datamined data into more human readable JSON.

There is caching of these results into JSON files in the `/public` directory. Once cached, the API endpoints will just show these files instead of doing processing.

Delete the files in `/public` if you want to run processing again (for example, if you have new datamined data).
