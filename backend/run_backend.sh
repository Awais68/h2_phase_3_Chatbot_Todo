#!/bin/bash

# Navigate to backend hf_deployment directory
cd "$(dirname "$0")/hf_deployment"

# Activate existing venv and run
source venv/bin/activate
python -m uvicorn app:app --reload --port 8000
