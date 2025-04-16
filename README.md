# SIMS Worker Service

This service integrates with the SIMS dashboard API and performs automated tasks.

## Local Setup

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the main script:
   ```bash
   python twitter.py
   ```

The script will automatically:
- Connect to SIMS dashboard API
- Fetch required data
- Process according to configured settings

## Docker Deployment

To run the service using Docker:

```bash
sudo docker compose up -d sims_worker_x
```

This will:
- Build the container if not already built
- Start the service in detached mode
- Run the worker process in the background

## Note

Make sure you have the proper credentials and environment variables set up before running the service. 