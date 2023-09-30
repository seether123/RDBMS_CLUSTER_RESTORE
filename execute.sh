#!/bin/bash

# Run the Python script and capture its output
python_output=$(python3 restore.py)

# Check the Python script's output and execute another script based on it
case "$python_output" in
          *"Snapshots created yesterday for cluster"*)
            echo "snaphshot has been created, please wait we are working on restoring and creating a new rds cluster....."
            python3 rds_instance.py && python3 get_cluster_endpoint.py && python3 route53_addition.py && \
            python3 jira_stop.py && python3 jira_start.py && python3 url_check.py
    # Add the command to execute your other script here
           ;;
         *)
          echo "No action required."
           ;;
esac
