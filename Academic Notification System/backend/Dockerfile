# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependency files to the container
COPY pyproject.toml poetry.lock ./

# Install poetry
RUN pip install poetry

# Install the dependencies
RUN poetry install

# Copy the rest of the application code to the container
COPY . /app

# Install protobuf compiler
RUN apt-get update && \
    apt-get install -y protobuf-compiler && \
    rm -rf /var/lib/apt/lists/*

# Compile the protobuf file
RUN protoc -I=. --python_out=. notification.proto

# Expose the desired port
EXPOSE 8080

# Command to run the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

