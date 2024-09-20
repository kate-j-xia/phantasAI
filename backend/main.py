from fastapi import FastAPI
import uvicorn

from sd.gen import gen_image

app = FastAPI()

@app.get("/generate/")
async def generate_image(prompt: str):
    use_image = True
    prompt = "generate a cartoon cute version"
    input_image = "vv-frontyard conv.jpeg"
    output_file = "vv-frontyard-new"
    print(f'generate_image(): {prompt}\n')

    output = gen_image(use_image, prompt, input_image, output_file)
    return {"message": "Image generated", "path": output}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=6188)