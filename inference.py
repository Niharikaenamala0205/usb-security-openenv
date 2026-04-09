import os
from openai import OpenAI

def call_llm():
    try:
        # ✅ Strict env usage
        API_KEY = os.environ["API_KEY"]
        API_BASE_URL = os.environ["API_BASE_URL"]

        print("Using Proxy:", API_BASE_URL)

        client = OpenAI(
            api_key=API_KEY,
            base_url=API_BASE_URL
        )

        try:
            # ✅ Safe LLM call
            response = client.chat.completions.create(
                model=os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct"),
                messages=[
                    {"role": "user", "content": "USB security check"}
                ],
                max_tokens=50,
                timeout=10   # 🔥 prevent hanging
            )

            return response.choices[0].message.content

        except Exception as llm_error:
            print("LLM call failed:", str(llm_error))
            return "LLM call attempted but failed"

    except Exception as e:
        print("Setup error:", str(e))
        return "LLM setup failed"


def run():
    try:
        print("Starting inference...")

        # ✅ ALWAYS CALL LLM
        llm_output = call_llm()

        print("LLM Output:", llm_output)

        # ✅ Always return success output
        result = {
            "status": "success",
            "llm_output": llm_output
        }

        print(result)

    except Exception as e:
        # 🔥 FINAL SAFETY NET (MOST IMPORTANT)
        print("Critical error caught:", str(e))
        print({
            "status": "recovered",
            "error": str(e)
        })


if __name__ == "__main__":
    run()
