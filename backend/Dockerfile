# Use the official Python base image
FROM python:3.12
ENV PYTHONDONTWRITEBYTECODE 1
# Set the working directory in the container
WORKDIR /app
# Copy the requirements file to the working directory
COPY Pipfile .
COPY Pipfile.lock .
# Install the required dependencies
RUN pip install pipenv
RUN pipenv install --deploy --system
# Copy the application code to the working directory
COPY . .
# Run the migrations
RUN aerich init -t app.config.TORTOISE_ORM
# Expose the port on which the application will run
EXPOSE 8000
# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]