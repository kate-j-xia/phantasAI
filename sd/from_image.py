

def generate_img2img(prompt, init_image_path, strength=0.75, num_inference_steps=50, guidance_scale=7.5):
    # Load the initial image
    init_image = Image.open(init_image_path).convert("RGB")
    init_image = init_image.resize((512, 512))  # Resize to 512x512 if necessary

    # Generate image based on the uploaded picture
    generated_image = pipe(prompt=prompt, image=init_image, strength=strength, 
                           num_inference_steps=num_inference_steps, guidance_scale=guidance_scale).images[0]

    # Save or display the generated image
    generated_image.save("output_image.png")
    return generated_image

