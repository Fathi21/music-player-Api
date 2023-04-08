FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .
COPY manage.py .

# Install the required dependencies
RUN python pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose port 8000 for the Django server
EXPOSE 8000

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
