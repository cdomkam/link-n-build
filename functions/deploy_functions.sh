#!/bin/bash


# Create .env file with APP key
echo "APP=PROD" > .env

# Run deploy functions
firebase deploy --only functions