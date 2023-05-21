# Base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the working directory
COPY . /app

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD [ "python", "main.py" ]