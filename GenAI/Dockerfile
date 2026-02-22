# Use the official Python image from the Docker Hub
FROM python:3.12-slim

WORKDIR /app

# Copy all files into the container (inc_summarizer.py, step0.py  etc.)
COPY . .
COPY .env .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port Streamlit runs on
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "inc_summarizer.py", "--server.port=8501", "--server.address=0.0.0.0"]