from fastapi import FastAPI

import sd


app = FastAPI()

@app.get("/generate/")
async def generate_image(prompt: str):
    sd.from_image()
    return {"message": "Image generated", "path": "generated_image.png"}


