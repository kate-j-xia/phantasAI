from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
from torch import autocast, float16

from PIL import Image

import time

model_id = "benjamin-paine/stable-diffusion-v1-5"

def get_pipeline(use_image=False):
    start = time.time()
    # Load the model
    print(f'loading stable difussion model...use_image = {use_image}\n')
    if use_image:
        print(f'using image2image pipeline...\n')
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=float16)
    else:
        print(f'using text2Image pipeline...\n')
        pipe = StableDiffusionPipeline.from_pretrained("benjamin-paine/stable-diffusion-v1-5")
    pipe = pipe.to("cuda")  # Ensure it runs on GPU
    # pipe = pipe.to(torch.device("cuda")).half()
    pipe.enable_attention_slicing()
    
    ts = time.time()

    print(f'got the model in {int(ts - start)} sec...')
    return pipe
    
def from_text(pipe, prompt):
    if pipe is None or prompt is None:
        print(f'Please enter a prompt...')
        return
    start = time.time()
    # Generate an image
    # prompt = "A fantasy landscape with mountains"
    # prompt = "an asian girl with big eyes and long hair doing ballet"
    with autocast("cuda"):
        image = pipe(prompt).images[0]

    ts = time.time()
    filename = f'text-img-{(str(ts))[-6:]}.png'
    print(f'image GENERATED after {int(ts - start)} sec, saving in {filename}...')
    image.save(filename)
    return filename

def from_image(pipe, prompt, init_image_path, 
               strength=0.75, num_inference_steps=120, guidance_scale=7.5):
    if pipe is None or prompt is None:
        print(f'Please enter a prompt...')
        return
    # Load the initial image
    start = time.time()
    init_image = Image.open(init_image_path).convert("RGB")
    init_image = init_image.resize((768, 768))  # Resize to 512x512 if necessary

    # Generate image based on the uploaded picture
    generated_image = pipe(prompt=prompt, image=init_image, strength=strength, 
                           num_inference_steps=num_inference_steps, guidance_scale=guidance_scale).images[0]

    ts = time.time()
    filename = f'{init_image_path}-gen-{(str(ts))[-6:]}.png'
    print(f'image GENERATED after {int(ts - start)} sec, saving in {filename}...')

    generated_image.save(filename)
    return filename

def gen_image(use_image, prompt, input_image=None):
    pipe = get_pipeline(use_image)
    output_file = "output_file.png"
    if use_image:
        print(f'generating image based on the image of {input_image}\n')
        output_file = from_image(pipe, prompt, init_image_path=input_image)
    else: 
        print(f'generating image for prompt:  {prompt}\n')
        output_file = from_text(pipe, prompt)
    return output_file

if __name__=="__main__":
    use_image = False
    # prompt = "generate a cartoon cute version"
    # prompt = "an asian girl with big eyes and long hair in a dark, drapery, flowery dress"
    # prompt = "portrait photo of a old warrior chief"
    prompt = "tintype photography of a melancholic gothic fairy-like female and flower, dark background"

    input_image = "vv-frontyard conv.jpeg"
    
    print(f'===To generate an image ===\n')

    output_file = gen_image(use_image, prompt, input_image)