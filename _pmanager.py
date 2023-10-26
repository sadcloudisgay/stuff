import subprocess
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

def send_error_to_callback(uuid, error):
    try:
        response = requests.get(callbackurl + "/error", params={"uuid": uuid, "error": error})
        if response.json()["success"]:
            return 0
        else:
            print(f"Error: {response.json()['error']}")
            return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

def attack_status_thread():
    while True:
        try:
            # every 5 seconds, check if attack status is ended, if so, kill the process and exit
            response = requests.get(callbackurl + "/status", params={"uuid": uuid})
            if response.json()["success"]:
                status = response.json()["status"]
                if status == "ended":
                    print(f"Attack ended. Exiting...")
                    os.killpg(os.getpgid(pid), signal.SIGKILL)  # Kill the process group
                    sys.exit(0)
            else:
                print(f"Error: {response.json()['error']}")
        except Exception as e:
            print(f"Error: {str(e)}")

        time.sleep(5)

def run_command_with_timeout(command, timeout_seconds, uuid, callbackurl):
    try:
        # Start the process
        process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)

        # Get the PID of the process
        pid = process.pid
        print(f"Started process with PID {pid}")

        # Wait for the process to complete or timeout
        start_time = time.time()
        while True:
            return_code = process.poll()
            if return_code is not None:
                break

            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time >= timeout_seconds:
                print(f"Process timed out after {timeout_seconds} seconds. Killing process with PID {pid}...")
                os.killpg(os.getpgid(pid), signal.SIGKILL)  # Kill the process group
                response = requests.get(callbackurl + "/ended", params={"uuid": uuid})
                if response.json()["success"]:
                    return 0
                else:
                    print(f"Error: {response.json()['error']}")
                    return 1

            time.sleep(0.5)  # Adjust the sleep interval as needed

        return process.returncode

    except Exception as e:
        send_error_to_callback(uuid, str(e))
        return 1

if __name__ == "__main__":
    required_packages = ["subprocess", "time", "sys", "os", "signal", "requests", "threading"]

    if not is_pip_installed():
        print("pip is not installed. Attempting to install it...")
        install_pip()

    # try import
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Package {package} is not installed. Attempting to install it...")
            install_missing_packages([package])
    
    import subprocess
    import time
    import sys
    import os
    import signal
    import requests
    import threading

    if len(sys.argv) < 4:
        print("Usage: python _pmanager.py <command> <timeout_seconds> <uuid> <callbackurl>")
        sys.exit(1)

    command = sys.argv[1]
    timeout_seconds = float(sys.argv[2])
    uuid = sys.argv[3]
    callbackurl = sys.argv[4]

    t = threading.Thread(target=attack_status_thread)
    t.start()

    return_code = run_command_with_timeout(command, timeout_seconds, uuid, callbackurl)

    if return_code != 0:
        send_error_to_callback(uuid, "Errorcode " + str(return_code))

    sys.exit(return_code)
