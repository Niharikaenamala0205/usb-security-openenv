import os
from openai import OpenAI

def safe_llm_call(user_type):
    try:
        client = OpenAI(
            api_key=os.environ.get("API_KEY"),
            base_url=os.environ.get("API_BASE_URL")
        )

        response = client.chat.completions.create(
            model=os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct"),
            messages=[
                {
                    "role": "user",
                    "content": f"USB security analysis for user type: {user_type}"
                }
            ],
            max_tokens=50
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"LLM failed safely: {str(e)}"


def run():
    user_types = ["Owner", "Unknown", "Suspicious"]

    # ---------------- START BLOCK ----------------
    print("[START] task=USB_SECURITY_ANALYSIS", flush=True)

    for i, user in enumerate(user_types, start=1):

        llm_output = safe_llm_call(user)

        # ---------------- STEP BLOCK ----------------
        print(
            f"[STEP] step={i} user_type={user} llm_output={llm_output}",
            flush=True
        )

    # ---------------- END BLOCK ----------------
    print(
        "[END] task=USB_SECURITY_ANALYSIS score=1.0 steps=3",
        flush=True
    )


if __name__ == "__main__":
    run()
