FROM python:3.11

# Set environment variables
ENV API_KEY 38d089808acd67f9a32d59629a4578a8
ENV SECRET_KEY 217e937592f0ea3c1975629980430a541c3c690b6c55fd8beff9a49bec86d16f

# Create the workdir
WORKDIR /app

# Copy the code to the workdir
COPY . /app

# Install the app requirements
RUN pip install -r requirements.txt

# Expose the app port
EXPOSE 8000

# Start the FastApi app with a sleep command so we give time to postgres to be fully up
CMD sleep 20 && python api_setup.py && uvicorn main:app --host=0.0.0.0 --port=8000