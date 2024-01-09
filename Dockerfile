FROM public.ecr.aws/lambda/python:3.11

RUN mkdir /tmp/cache

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY main.py ${LAMBDA_TASK_ROOT}
CMD [ "main.handler" ]

