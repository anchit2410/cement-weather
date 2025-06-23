# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /adani-power-coal
# Copy the current directory contents into the container 
COPY . /adani-power-coal

# Copy the requirements file to the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN python3 -m pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80


# Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
