# Use the official Python image as a base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy only the dependency files into the container
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application
COPY . /app

# Expose the port the app runs on
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "frontend/main.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
