# Use an official Python runtime as a parent image
FROM python:3.9-slim-bookworm

# Install ffmpeg dan dependencies yang diperlukan
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port your Flask app runs on (default is 5000)
EXPOSE 5000

# Run the Flask application when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]