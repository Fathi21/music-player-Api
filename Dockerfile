FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Start the Django server
CMD ["python", "manage.py", "runserver"]
