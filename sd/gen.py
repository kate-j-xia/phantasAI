from diffusers import StableDiffusionPipeline
from torch import autocast

import time

start = time.time()
# Load the model
print(f'{start}: loading stable difussion model ...')
pipe = StableDiffusionPipeline.from_pretrained("benjamin-paine/stable-diffusion-v1-5")
pipe = pipe.to("cuda")  # Ensure it runs on GPU

pipe.enable_attention_slicing()
# pipe = pipe.to(torch.device("cuda")).half()
print(f'got the model...')

# Generate an image
ts = time.time()
print(f'after {ts - start} sec, generating image...')
# prompt = "A fantasy landscape with mountains"
prompt = "an asian girl with big eyes and long hair doing ballet"
with autocast("cuda"):
    image = pipe(prompt).images[0]

ts = time.time()
# Save the image
print(f'{ts}: image DONE after {ts - start} sec, saving...')
image.save("output_image.png")

