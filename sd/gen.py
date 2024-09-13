from diffusers import StableDiffusionPipeline
from torch import autocast

# Load the model
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("cuda")  # Ensure it runs on GPU

# pipe.enable_attention_slicing()
# pipe = pipe.to(torch.device("cuda")).half()

# Generate an image
prompt = "A fantasy landscape with mountains"
with autocast("cuda"):
    image = pipe(prompt).images[0]

# Save the image
image.save("output_image.png")

