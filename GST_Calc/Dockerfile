# Use the official Python image
FROM python

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn

# Copy the FastAPI application into the container
COPY . .

# Command to run the application
CMD [ "uvicorn", "main:app",  "--host", "0.0.0.0", "--port", "8080"]