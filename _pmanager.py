import subprocess
import time
import os
import signal
import sys

def is_pip_installed():
    try:
        subprocess.check_call(["python3", "-m", "pip", "--version"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error checking if pip is installed: {e}")
        return False
        

def install_pip():
    try:
        subprocess.check_call(["sudo", "apt-get", "update"])
        subprocess.check_call(["sudo", "apt-get", "install", "-y", "python3-pip"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing pip: {e}")
        sys.exit(1)

def install_missing_packages(packages):
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")
            sys.exit(1)

def run_command_with_timeout(command, timeout_seconds):
    try:
        # Start the process
        process = subprocess.Popen(command, shell=True)

        # Get the PID of the process
        pid = process.pid

        # Wait for the process to complete or timeout
        start_time = time.time()
        while True:
            return_code = process.poll()
            if return_code is not None:
                break

            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time >= timeout_seconds:
                # forcefully kill it using 'terminate' command
                process.terminate()
                # forcefully kill it using 'kill' command
                os.kill(pid, signal.SIGKILL)
                # forcefully kill it using 'kill' command
                os.system("kill -9 {}".format(pid))
                return 1
                

            # Add a short sleep to reduce CPU usage
            time.sleep(0.1)  # Adjust the sleep interval as needed

        return process.returncode

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    required_packages = ["subprocess"]

    if not is_pip_installed():
        print("pip is not installed. Attempting to install it...")
        install_pip()

    try:
        import subprocess
    except ImportError:
        print("The 'subprocess' module is missing. Installing it...")
        install_missing_packages(["subprocess"])

    if len(sys.argv) != 3:
        print("Usage: python pmanager.py <command> <timeout_seconds>")
        sys.exit(1)

    command = sys.argv[1]
    timeout_seconds = float(sys.argv[2])

    return_code = run_command_with_timeout(command, timeout_seconds)
    sys.exit(return_code)
