from fastapi import FastAPI, Request
from pydantic import BaseModel
from subprocess import run, PIPE
import uuid
import os

app = FastAPI()

MODEL_PATH = "./llama.cpp/models/llama-2-7b-chat.Q4_K_M.gguf"
LLAMA_BIN = "./llama.cpp/main"  # or server if using server mode

class PromptRequest(BaseModel):
    prompt: str
    n_predict: int = 512

@app.post("/complete")
async def complete(req: PromptRequest):
    temp_id = str(uuid.uuid4())
    prompt_file = f"/tmp/{temp_id}.txt"

    with open(prompt_file, "w") as f:
        f.write(req.prompt)

    cmd = [
        LLAMA_BIN,
        "-m", MODEL_PATH,
        "-f", prompt_file,
        "-n", str(req.n_predict)
    ]

    result = run(cmd, stdout=PIPE, stderr=PIPE, text=True)
    os.remove(prompt_file)

    if result.returncode != 0:
        return {"error": "LLM_FAILURE", "stderr": result.stderr}

    return {"response": result.stdout}
