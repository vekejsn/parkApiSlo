# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies required for Python packages and git
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libffi-dev \
    python3-dev

# Clone your application repository
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache

RUN git clone https://github.com/vekejsn/parkApiSlo.git

WORKDIR /usr/src/app/parkApiSlo

# Install pipenv
RUN pip install pipenv

# Install dependencies using pipenv
RUN pipenv install --deploy --ignore-pipfile

# Expose the port the app runs on
EXPOSE 16000

# Run the application using pipenv
CMD ["pipenv", "run", "python3", "main.py"]



