"""
import subprocess
import time

def run_server():
    print("Starting server...")
    subprocess.Popen(["python", "server.py"])

def run_client():
    print("Starting client...")
    subprocess.Popen(["python", "client.py"])

def main():
    run_server()
    time.sleep(1)  # Give the server some time to start
    run_client()

if __name__ == "__main__":
    main()
"""