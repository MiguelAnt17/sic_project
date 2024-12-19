# Use the official Python image
FROM python:3.11

# Setting the working directory
WORKDIR /usr/src/myapp

# Copy the required files to the container
COPY producer6.py .

# Install kafka-python in the container
RUN pip install kafka-python

# Run producer.py when the container launches
CMD ["python", "-u", "producer6.py"]