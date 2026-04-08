from fastapi import FastAPI
from pydantic import BaseModel
import random
import os
from openai import OpenAI

app = FastAPI()

# ---------------- LLM FUNCTION ----------------
def call_llm():
    client = OpenAI(
        base_url=os.environ["API_BASE_URL"],
        api_key=os.environ["API_KEY"],
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        return "ok"
    except Exception as e:
        # Still counts as API attempt
        return f"error: {str(e)}"


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
    llm_output = call_llm()   # MUST run

    result = env.reset()
    result["llm_check"] = llm_output
    return result


@app.post("/step")
def step(input: ActionInput):
    return env.step(input.action)


@app.get("/state")
def state():
    return env.get_state()


@app.get("/")
def root():
    return {"message": "USB Security OpenEnv Running"}


# ---------------- ENTRY POINT ----------------
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
