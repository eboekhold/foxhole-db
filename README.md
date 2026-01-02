# foxhole-db
JSON API for Foxhole recipes.

Currently supported recipes:
- Refinery
- Factory
- Vehicles

## Requirements
- Python3
- uv

## Installation
```
uv sync
```

## Running the server
```
uv run fastapi dev app/main.py
```
Runs the server on localhost on port 8000.

## Documentation
Once the server is running, please visit `localhost:8000/docs` or `localhost:8000/redoc` to view the API documentation.

Currently supported endpoints:
- `/refinery`
- `/factory`
- `/vehicles`

These endpoints are cached after first request and reused for all Nth requests after. Delete the corresponding files in the `/public` directory if you want to clean the cache. You can skip saving to cache with the `CACHE_RESULTS` flag in `recipes/shared.py`. (causing this flag to skip loading is a TODO)
