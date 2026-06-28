#!/bin/bash
set -e

cd /opt/render/project/src/backend || cd backend

echo "Starting uvicorn server..."
python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
