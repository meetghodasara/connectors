#!/bin/sh

# Start the connector (WORKDIR is /opt/connector as set in the Dockerfile)
cd /opt/connector
python3 main.py
