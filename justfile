# Clash Royale Stats Tracker - Just Commands

# List all available commands
default:
    @just --list

# Run the development server
run:
    source .venv/bin/activate && python app.py

# Stop the server (kill process on port 3000)
stop:
    lsof -ti:3000 | xargs kill -9 2>/dev/null || echo "No server running on port 3000"

# Install dependencies
install:
    uv venv
    uv pip install flask requests pandas pyarrow python-dotenv

# Clean data files
clean-data:
    rm -f data/*.parquet

# Clean Python cache
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

# Firebase deployment commands
firebase-deploy:
    firebase deploy

firebase-deploy-hosting:
    firebase deploy --only hosting

firebase-deploy-functions:
    firebase deploy --only functions

firebase-deploy-firestore:
    firebase deploy --only firestore

firebase-serve:
    firebase serve
