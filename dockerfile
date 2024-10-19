# Use the Windows base image
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Set the working directory
WORKDIR /app

# Copy all files from the current directory to the Docker container
COPY . /app



# Install pip and the required Python packages
RUN python -m pip install --upgrade pip
RUN pip install flask wmi pywin32

# Expose the port that Flask will run on
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]

