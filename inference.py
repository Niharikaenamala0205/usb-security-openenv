import os
from openai import OpenAI
import requests

BASE_URL = "http://localhost:7860"

def call_llm():
    client = OpenAI(
        base_url=os.environ["API_BASE_URL"],
        api_key=os.environ["API_KEY"],
    )

    response = client.chat.completions.create(
        model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
        messages=[{"role": "user", "content": "Evaluate USB security"}],
        max_tokens=5
    )

    return response.choices[0].message.content


def run():
    print("[START]")

    # RESET
    res = requests.post(f"{BASE_URL}/reset").json()
    print("[STEP] reset:", res)

    # STEP LOOP
    for i in range(3):
        action = "Allow"
        step_res = requests.post(
            f"{BASE_URL}/step",
            json={"action": action}
        ).json()

        print("[STEP] step:", step_res)

    # 🔥 IMPORTANT: CALL LLM HERE
    llm_output = call_llm()
    print("[STEP] llm:", llm_output)

    print("[END]")


if __name__ == "__main__":
    run()
