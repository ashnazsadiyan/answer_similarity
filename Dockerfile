FROM public.ecr.aws/lambda/python:3.11


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