#!/bin/bash


# Create .env file with APP key
echo "APP=DEV" > .env

# Run firebase emulators:start
firebase emulators:start --import seed_data