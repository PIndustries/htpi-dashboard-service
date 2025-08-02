# HTPI Dashboard Service

Real-time dashboard analytics and metrics service for the HTPI healthcare system.

## Features

- Real-time statistics (patients, claims, encounters, insurance)
- Recent activity tracking
- System alerts and notifications
- Automatic dashboard updates via broadcasts
- Multi-tenant support

## Architecture

This service provides:
- Aggregated statistics for dashboards
- Real-time activity feeds
- System-wide alerts
- Simulated real-time updates every 30 seconds

## NATS Subscriptions

- `htpi.dashboard.get.stats` - Get dashboard statistics
- `htpi.dashboard.get.activity` - Get recent activity
- `htpi.dashboard.get.alerts` - Get system alerts

## Broadcast Channels

- `admin.broadcast.dashboard.*` - Admin dashboard updates
- `customer.broadcast.dashboard.*` - Customer dashboard updates

## Environment Variables

```bash
NATS_URL=nats://localhost:4222
```

## Running Locally

```bash
pip install -r requirements.txt
python app.py
```

## Docker Deployment

```bash
docker build -t htpi-dashboard-service .
docker run -e NATS_URL=nats://host.docker.internal:4222 htpi-dashboard-service
```