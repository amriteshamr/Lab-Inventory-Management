# Use the official Python image as the base
FROM python:3.11.4-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current project files to the container
COPY . /app

# Install system dependencies for SQLite and other tools
RUN apt-get update && apt-get install -y \
    gcc \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir Flask Flask-Login SQLAlchemy

# Expose the port Flask runs on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Command to run the Flask app
CMD ["python", "app.py"]
