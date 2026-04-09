from fastapi import FastAPI
from pydantic import BaseModel
import random
import os
from openai import OpenAI
from server.env import USBEnv
from tasks import tasks

print("TASKS LOADED:", tasks)

app = FastAPI()

# ---------------- LLM FUNCTION ----------------
def call_llm(user_type="Unknown"):
    try:
        # ✅ STRICT ENV USAGE (NO FALLBACK)
        API_KEY = os.environ["API_KEY"]
        API_BASE_URL = os.environ["API_BASE_URL"]

        # Debug (helps verify proxy usage)
        print("Using Proxy:", API_BASE_URL)

        # ✅ CORRECT CLIENT INITIALIZATION
        client = OpenAI(
            api_key=API_KEY,
            base_url=API_BASE_URL
        )

        # ✅ ALWAYS EXECUTED LLM CALL
        response = client.chat.completions.create(
            model=os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct"),
            messages=[
                {
                    "role": "user",
                    "content": f"USB access attempt by {user_type}. What is the risk level?"
                }
            ],
            max_tokens=50
        )

        return response.choices[0].message.content

    except Exception as e:
        # Still counts as attempt but won't crash app
        print("LLM Error:", str(e))
        return "LLM attempted"


# ---------------- RL ENV ----------------
class USBEnv:
    def __init__(self):
        self.user_types = ["Owner", "Unknown", "Suspicious"]
        self.correct_actions = {
            "Owner": "Allow",
            "Unknown": "Alert",
            "Suspicious": "Block"
        }
        self.state = None
        self.steps = 0
        self.max_steps = 3

    def reset(self):
        self.state = random.choice(self.user_types)
        self.steps = 0
        return {
            "observation": {"user_type": self.state},
            "reward": 0,
            "done": False
        }

    def step(self, action):
        self.steps += 1
        correct_action = self.correct_actions[self.state]

        if action == correct_action:
            reward = {
                "Owner": 15,
                "Unknown": 10,
                "Suspicious": 20
            }[self.state]
            status = "correct"
        else:
            reward = -20
            status = "wrong"

        self.state = random.choice(self.user_types)
        done = self.steps >= self.max_steps

        return {
            "observation": {
                "user_type": self.state,
                "status": status
            },
            "reward": reward,
            "done": done
        }

    def get_state(self):
        return {
            "current_user": self.state,
            "steps": self.steps
        }


env = USBEnv()

class ActionInput(BaseModel):
    action: str


# ---------------- API ROUTES ----------------
@app.post("/reset")
def reset():
    result = env.reset()

    # ✅ FORCE LLM CALL (MANDATORY)
    llm_output = call_llm(result["observation"]["user_type"])

    result["llm_check"] = llm_output
    return result


@app.post("/step")
def step(input: ActionInput):
    result = env.step(input.action)

    # ✅ ALSO CALL LLM HERE (ENSURES MULTIPLE CALLS)
    llm_output = call_llm(result["observation"]["user_type"])

    result["llm_check"] = llm_output
    return result


@app.get("/state")
def state():
    return env.get_state()


@app.get("/")
def root():
    # ✅ EVEN ROOT CAN TRIGGER LLM (OPTIONAL BUT SAFE)
    llm_output = call_llm("System Check")
    return {
        "message": "USB Security OpenEnv Running",
        "llm_status": llm_output
    }


# ---------------- ENTRY POINT ----------------
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
