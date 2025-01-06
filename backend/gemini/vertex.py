import os
import time
import asyncio

import vertexai
from google.cloud import aiplatform

from vertexai.language_models import TextGenerationModel

from vertexai.preview.generative_models import GenerativeModel, Image

from vertexai.preview.vision_models import ImageGenerationModel

import google.generativeai as genai


# imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

GCLOUD_PROJECT_ID = "katex8-420522"
GCLOUD_REGION = 'us-west1'
SUMMARIZATION_MODE_ID = 'gemini-1.5-flash-002'  # 'text-bison@002' 
IMAGE_GEN_MODEL_ID = 'imagen-3.0-generate-001' 
SUMMARY_PROMPT = "Provide a summary with all the key points for the following text: "
GENAI_API_KEY = "" # get from env var

# List all endpoints in the project
def list_endpoints():
    endpoints = aiplatform.Endpoint.list()
    for endpoint in endpoints:
        print(f"Endpoint name: {endpoint.name}, Display name: {endpoint.display_name}")

def summarize(text: str) -> str:
    """Generate a summary of the input text using Vertex AI's language model."""

    parameters = {
        "temperature": 0,
        "max_output_tokens": 256,
        "top_p": 0.95,
        "top_k": 40,
    }
    # model = TextGenerationModel.from_pretrained(SUMMARIZATION_MODE_ID)
    model = GenerativeModel(SUMMARIZATION_MODE_ID)
    # response = model.predict(text, **parameters)
    summary = model.generate_content(SUMMARY_PROMPT + text)
    print(f'summarize(): {summary}')
    
    # print(f"summarize_text(): {response.text}")
    return 'DONE'

async def generate_image_from_text(user_id: str, text: str) -> str:
    """Generate an image from the text using Google Gemini API."""
    # model = aiplatform.ImageGenerationModel.from_pretrained(IMAGE_GEN_MODEL_ID)
    # response = model.predict(instances=[{"prompt": text}])
    # image_url = response.predictions[0]["content"]
    # model = genai.ImageGenerationModel(IMAGE_GEN_MODEL_ID) # "gemini-1.5-flash-002"
    # response = model.generate_content([text, image])
    start = time.time()

    # vertex_sc_file = "gemini/katex8-vertex-sc.json"
    
    # if not os.path.exists(vertex_sc_file):
    #     print(f"File not found at {vertex_sc_file}")
    #     return 
  
    # print(f"File found at {vertex_sc_file}")
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = vertex_sc_file

    # vertexai.init(project=GCLOUD_PROJECT_ID, location=GCLOUD_REGION)
    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

    images = model.generate_images(
        # prompt="An beautiful asian girl with long black hair, big eyes in a flowery dress in Alaska landscape background",
        # prompt="A black panther laying on a big tree in Savanna",
        # prompt="a drawing of a pride of lions under a big tree while roaring",
        # prompt="a very realistic drawing of a black panther and tiger fighting ",
      
        # prompt=" a super realistic drawing of an Australian sheperd with a bunch of puppies in front of a beautiful mansion",
        prompt = text,
        # Optional parameters
        number_of_images=1,
        language="en",
        # You can't use a seed value and watermark at the same time.
        # add_watermark=False,
        # seed=100,
        aspect_ratio="1:1",
        safety_filter_level="block_some",
        person_generation="allow_adult",
    )

    ts = time.time()
    image_url = f'imagen_{(str(ts))[-6:]}.jpg'
    images[0].save(location=image_url, include_generation_parameters=False)

    # Optional. View the generated image in a notebook.
    # images[0].show()

    print(f"Created image using {len(images[0]._image_bytes)} bytes, in {(ts - start)} seconds.")
    # Example response:
    # Created output image using 1234567 bytes

    # Display the generated images
    # for index, image in enumerate(response.images):
    #     image._pil_image.show()
    #     # Save the image using the PIL library's save function
    #     image._pil_image.save(f'image_{index}.jpg')

    return image_url # response

async def visualize(user_id: str, prompt: str):

    vertex_sc_file = "config/katex8-vertex-sc.json"
    
    if not os.path.exists(vertex_sc_file):
        print(f"File not found at {vertex_sc_file}")
        return 
  
    print(f"File found at {vertex_sc_file}")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = vertex_sc_file
    # GENAI_API_KEY = os.environ["GENAI_API_KEY"]

    vertexai.init(project=GCLOUD_PROJECT_ID, location=GCLOUD_REGION)
    # genai.configure(api_key=GENAI_API_KEY) # the gemini imagen api is still not available

    # Initialize the model
    # model = GenerativeModel("text-bison")
    print(f'visualize(): vertex initialized...')

    input_text = """
            imagine a suburb residential area -  
            draw a color painting of a beautiful modern, ah, 
            french house with lavish landscaping in the front, ah, 
            with mostly drought tolerant plants, and trees.
            """

    image_prompt = """
            a beautiful modern french house with lavish landscaping in the front, 
            which has mostly drought tolerant plants, trees and colorful flowers
        """
    # Summarize the text
    # summary = model.generate_text(prompt=f"Summarize: {input_text}")
    # summary = summarize(input_text)
    # print(f'got summary: {summary}')

    # Generate an image based on the text
    # image = model.generate_image(prompt=summary, image_resolution="256x256")

    # Display or save the image
    # You can use a library like PIL or OpenCV to display the image
    # Or, save the image to a file
    # image.save("generated_image.png")

    print(f'visualize(): calling Vertex API with prompt: \n{prompt}\n')
    # Generate an image based on the summary
    image_url = await generate_image_from_text(user_id, prompt)
    print(f"Generated Image URL: {image_url}")
    return image_url

if __name__ == '__main__':
    user_id = 'test_user_688'
    prompt = """
        pencil sketch for a 2-story modern french house with a bay window on one side and 
        a front porch, a solid wood front door, and a small garage on the other side
        """
    
    asyncio.run(visualize(user_id, prompt))