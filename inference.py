import requests

BASE_URL = "http://localhost:7860"

def run():
    print("[START]")

    reset = requests.post(f"{BASE_URL}/reset").json()
    print("[RESET]", reset)

    action = {"action": "Allow"}

    step = requests.post(f"{BASE_URL}/step", json=action).json()
    print("[STEP]", step)

    state = requests.get(f"{BASE_URL}/state").json()
    print("[STATE]", state)

    print("[END]")

if __name__ == "__main__":
    run()
