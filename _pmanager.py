import subprocess
import psutil
import os
import signal
import time
import sys

def run_background_process(command, time_param):
    try:
        # Start the background process
        process = subprocess.Popen(command, shell=True)

        # Wait for the specified time (in seconds)
        time.sleep(time_param)

        # Attempt to kill the process using subprocess.terminate()
        process.terminate()
        process.wait()
        print(f"Process with command '{command}' has been forcefully terminated (Method: subprocess.terminate())")

        # Attempt to kill the process using psutil
        pid = process.pid
        process = psutil.Process(pid)
        process.terminate()
        process.wait()
        print(f"Process with command '{command}' (PID {pid}) has been forcefully terminated (Method: psutil)")

        # Attempt to kill the process using os.kill (for UNIX-like systems)
        os.kill(pid, signal.SIGTERM)
        process.wait()
        print(f"Process with command '{command}' (PID {pid}) has been forcefully terminated (Method: os.kill())")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <command> <time_in_seconds>")
        sys.exit(1)

    command = sys.argv[1]
    time_param = int(sys.argv[2])

    run_background_process(command, time_param)
