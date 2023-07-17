#!/usr/bin/env python3
import os
import subprocess

from dotenv import load_dotenv

load_dotenv()

# Get the environment variable
env_var = os.getenv("MODE")

# Based on the environment variable, decide which script to run
if env_var == "CONFLUENCE":
    subprocess.run(["python", "summarize_blogposts.py"])
elif env_var == "AZURE":
    subprocess.run(["python", "azure_blog_reader.py"])
else:
    print("Environment variable is not set to a recognized value.")
