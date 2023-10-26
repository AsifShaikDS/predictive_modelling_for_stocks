# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory to the application directory
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Define the command to run your Python application
CMD ["python", "model.py"]
