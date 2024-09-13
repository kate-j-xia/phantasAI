from fastapi import FastAPI
from diffusers import StableDiffusionPipeline
from torch import autocast

app = FastAPI()

# Load the model at startup
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to("cuda").half()
pipe.enable_attention_slicing()

@app.get("/generate/")
async def generate_image(prompt: str):
    with autocast("cuda"):
        image = pipe(prompt).images[0]
    image.save("generated_image.png")
    return {"message": "Image generated", "path": "generated_image.png"}


