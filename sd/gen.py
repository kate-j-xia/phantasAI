from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
from torch import autocast
from PIL import Image

import time

def get_pipeline(from_image=False):
    start = time.time()
    # Load the model
    print(f'{start}: loading stable difussion model ...')
    if from_image:
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained("benjamin-paine/stable-diffusion-v1-5")
    else:
        pipe = StableDiffusionPipeline.from_pretrained("benjamin-paine/stable-diffusion-v1-5")
    pipe = pipe.to("cuda")  # Ensure it runs on GPU

    pipe.enable_attention_slicing()
    # pipe = pipe.to(torch.device("cuda")).half()
    ts = time.time()

    print(f'got the model in {int(ts - start)} sec...')

    return pipe
    
def from_text(pipe, prompt, filename="output_image.png"):
    if pipe is None or prompt is None:
        print(f'Please enter a prompt...')
        return
    start = time.time()
    # Generate an image
    # prompt = "A fantasy landscape with mountains"
    prompt = "an asian girl with big eyes and long hair doing ballet"
    with autocast("cuda"):
        image = pipe(prompt).images[0]

    ts = time.time()
    print(f'image GENERATED after {int(ts - start)} sec, saving in {filename}...')
    image.save(f'{filename}.png')

def from_image(pipe, prompt, init_image_path, 
               strength=0.75, num_inference_steps=50, guidance_scale=7.5,
               filename="output_image.png"):
    if pipe is None or prompt is None:
        print(f'Please enter a prompt...')
        return
    # Load the initial image
    start = time.time()
    init_image = Image.open(init_image_path).convert("RGB")
    init_image = init_image.resize((512, 512))  # Resize to 512x512 if necessary

    # Generate image based on the uploaded picture
    generated_image = pipe(prompt=prompt, image=init_image, strength=strength, 
                           num_inference_steps=num_inference_steps, guidance_scale=guidance_scale).images[0]

    ts = time.time()
    print(f'image GENERATED after {int(ts - start)} sec, saving in {filename}...')

    generated_image.save(f'{filename}.png')
    return generated_image

def gen_image():
    from_image = True
    prompt = "generate a cartoon version that's similar to Despicable Me style"
    file = "vv-in-frontyard"
    pipe = get_pipeline(from_image)
    if from_image:
        from_image(pipe, prompt, filename=file)
    else: 
        from_text(pipe, prompt, file)