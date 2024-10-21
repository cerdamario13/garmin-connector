FROM python:3.11-slim

# set the working directory
WORKDIR /app/src

# Copy the cirrect directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV FLASK_APP=app.py

# Run Flask with the appropriate host and port
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]