# Dockerfile

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files to container
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Set default command
CMD ["python", "app.py"]
