# Base Image
FROM pytorch/pytorch:2.4.1-cuda12.1-cudnn9-runtime

# Don't Write Bytecode
ENV PYTHONDONTWRITEBYTECODE=1

# No Buffer
ENV PYTHONUNBUFFERED=1

# Define the working directory
WORKDIR /app

# First copy the requirements file
COPY requirements.txt /app

# Install requirements
RUN python -m pip install -r requirements.txt

# Copy all files after updating requirements
# Ensures that libraries are not reinstalled every time
COPY . /app/

# Run the script
ENTRYPOINT ["python", "src/create_newsletter.py"]