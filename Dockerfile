FROM ubuntu:20.04

# Install Python and pip
RUN apt-get -y update && \
    apt-get install -y python3 python3-pip ffmpeg

# Create a directory for data
RUN mkdir /tmp/data

# Set the TRANSFORMERS_CACHE environment variable
ENV TRANSFORMERS_CACHE "/tmp/data"

# Copy requirements.txt and install the required packages
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy app.py
COPY main.py .

# Set the CMD for the Lambda function
CMD [ "main.handler" ]