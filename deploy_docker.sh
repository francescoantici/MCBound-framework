#!/bin/sh

# Create image
docker build -t MCBound .

# Start the framework
docker run -p $1:8080 -d -i MCBound 
