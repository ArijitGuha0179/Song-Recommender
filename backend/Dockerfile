# Use the official Python image as the base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Flask app
COPY . .

# Expose the port you want the Flask app to run on
EXPOSE 8223

# Set environment variables for Flask
# ENV FLASK_APP=app.py
# ENV FLASK_ENV=production

# Start the Flask app on the specified port
CMD ["python3","app.py"]