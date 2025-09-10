import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import load_dotenv
import os
from time import sleep
from io import BytesIO

# Load environment variables (.env file should have HuggingFaceAPIKey)
load_dotenv()
API_TOKEN = os.getenv("HuggingFaceAPIKey")

if not API_TOKEN:
    raise RuntimeError("HuggingFaceAPIKey not found in environment variables. Please set it in the .env file.")

# Hugging Face inference API URL
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

DATA_FOLDER = "Data"
REQUEST_FILE = r"Frontend\Files\ImageGeneration.data"


async def query(payload, max_retries=3):
    """Make an API call with retries and exponential backoff."""
    for attempt in range(max_retries):
        try:
            response = await asyncio.to_thread(
                requests.post,
                API_URL,
                headers=HEADERS,
                json=payload,
                timeout=60  # 60 seconds timeout for slow API
            )
            if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
                return response.content
            else:
                print(f"Attempt {attempt + 1} failed with status {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} raised an exception: {e}")
        
        if attempt < max_retries - 1:
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
    print("Max retries reached. Skipping this request.")
    return None


async def generate_images_async(prompt: str, num_images=2):
    """Generate multiple images concurrently with the Hugging Face API."""
    tasks = []
    for _ in range(num_images):
        # Simplified prompt for better API compatibility
        payload = {"inputs": prompt}
        tasks.append(asyncio.create_task(query(payload)))
    image_bytes_list = await asyncio.gather(*tasks)
    # Filter out any failed requests (None)
    return [img_bytes for img_bytes in image_bytes_list if img_bytes is not None]


def save_images(prompt: str, image_bytes_list):
    prompt_fixed = prompt.replace(" ", "_")
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    for i, image_bytes in enumerate(image_bytes_list, 1):
        file_path = os.path.join(DATA_FOLDER, f"{prompt_fixed}{i}.jpg")
        with open(file_path, "wb") as f:
            f.write(image_bytes)
        print(f"Saved image: {file_path}")


def open_images(prompt: str, num_images=2):
    prompt_fixed = prompt.replace(" ", "_")
    for i in range(1, num_images + 1):
        image_path = os.path.join(DATA_FOLDER, f"{prompt_fixed}{i}.jpg")
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")


def GenerateImages(prompt: str):
    print(f"Starting generation for prompt: {prompt}")
    try:
        image_bytes_list = asyncio.run(generate_images_async(prompt))
    except Exception as e:
        print(f"Error during async generation: {e}")
        return

    if image_bytes_list:
        save_images(prompt, image_bytes_list)
        open_images(prompt, len(image_bytes_list))
    else:
        print("No images generated due to request errors.")


def monitor_file_and_generate():
    print("Starting file monitoring for image generation requests.")
    while True:
        try:
            if not os.path.exists(REQUEST_FILE):
                print(f"Waiting for request file: {REQUEST_FILE}")
                sleep(2)
                continue

            with open(REQUEST_FILE, "r") as f:
                data = f.read().strip()

            if not data:
                sleep(2)
                continue

            try:
                prompt, status = map(str.strip, data.split(",", 1))
            except ValueError:
                print(f"Malformed data in {REQUEST_FILE}: {data}")
                sleep(2)
                continue

            if status.lower() == "true":
                print("Detected generation request.")
                GenerateImages(prompt)
                with open(REQUEST_FILE, "w") as f:
                    f.write("False,False")
                print("Generation complete, monitoring resumed.")
            else:
                sleep(2)
        except Exception as e:
            print(f"Error during monitoring: {e}")
            sleep(5)


if __name__ == "__main__":
    monitor_file_and_generate()
