# Use an official Python runtime as a parent image
FROM python:3-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install netflix-conductor client from the included source
WORKDIR /app/lib/netflix-conductor-client
RUN python setup.py install
WORKDIR /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV WF_SERVER localhost:8080
ENV HOST_HOST_PORT http://localhost:5000
ENV REDIS_HOST localhost
ENV REDIS_PORT 6379
ENV REDIS_DB 0
ENV MONGO_HOST localhost
ENV MONGO_PORT 27017
ENV STORAGE_TASK_NAME store_metadata
ENV SEARCHER_TASK_NAME search_metadata

# Run main.py when the container launches
CMD gunicorn -w 4 -b 0.0.0.0:5000 main:app

