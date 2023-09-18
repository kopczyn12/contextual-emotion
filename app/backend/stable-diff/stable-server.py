from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from io import BytesIO
import base64 
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_credentials=True, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

access_token = "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"

device = "cuda"
model_id = "stable_final.safetensors"
pipe = StableDiffusionPipeline.from_ckpt(model_id, revision="fp16", torch_dtype=torch.float16, use_auth_token=access_token)
pipe.to(device)

@app.get("/")
def generate(prompt: str): 
    with autocast(device): 
        image = pipe(prompt, num_inference_steps=35, width=512, height=512).images[0]

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    imgstr = base64.b64encode(buffer.getvalue())

    return Response(content=imgstr, media_type="image/png")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)