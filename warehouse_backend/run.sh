#!/bin/bash
# Quick start script for Warehouse Backend API

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "Please edit .env with your Odoo connection details!"
    exit 1
fi

# Run the application
echo "Starting Warehouse Scanner Backend API..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
