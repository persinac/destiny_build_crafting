# Destiny Build Crafting - API

Best mod building this side of the Mississippi

# App Building

## Pre-req
Install requirements:
``pip install -r requirements.txt``

## Local
Straight up local dev? 
``uvicorn api:app --reload``

## Docker
Getting fancy? 

### Build the image
``docker build -t destinybuildcraft:latest .``

### Start the container

#### Background
``docker run --name destinybuildcraft -d -p 3001:5000 destinybuildcraft:latest``

#### Blocking
``docker run --name destinybuildcraft -p 3001:5000 destinybuildcraft:latest``

### Stop the container
``docker stop destinybuildcraft``

### Remove the container
``docker rm destinybuildcraft``

### Access the container
``docker exec -it destinybuildcraft /bin/bash``

### TODO
Link the volume so that we don't have to rebuild the container locally