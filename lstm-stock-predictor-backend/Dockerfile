# Use an official Python runtime as a parent image
# FROM python:3.11

# Set the working directory to the application directory
# WORKDIR /app/

# # Copy the application code to the container
# COPY . .

# # Install any needed packages specified in requirements.txt
# RUN pip install -r requirements.txt

# EXPOSE 5000
# # Define the command to run your Python application
# CMD ["python", "-m", "flask", "--app", "./lstm_stock_predictor.py", "run"]

FROM python:3.9-slim-buster
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=lstm_stock_predictor.py
CMD ["flask", "run", "--host", "0.0.0.0"]