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
ENV WF_SERVER 172.17.0.2:8080
ENV HOST_ADDR_PORT 127.0.0.1:5000

# Run main.py when the container launches
CMD ["python", "main.py"]
