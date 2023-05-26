# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.9

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Copy requirements and install them before the rest of the files so they can be cached
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set the working directory to /app
# NOTE: all the directives that follow in the Dockerfile will be executed in
# that directory.
WORKDIR /app

# copy source code
COPY . .

EXPOSE 8000
