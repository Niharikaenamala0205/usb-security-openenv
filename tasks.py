from server.env import USBEnv

env = USBEnv()

# -------- Graders --------
def grader1(output):
    return isinstance(output, dict)

def grader2(output):
    return output is not None

def grader3(output):
    return True

# -------- Tasks --------
tasks = [
    {
        "name": "reset_task",
        "grader": grader1
    },
    {
        "name": "step_task",
        "grader": grader2
    },
    {
        "name": "custom_task",
        "grader": grader3
    }
]
