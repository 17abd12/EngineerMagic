import base64
import requests
import os
import subprocess
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

def encode_image_to_base64(image_path):
    """Convert an image file to a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def generate_chat_completion(prompt, image_path=None):
    api_key = os.getenv("API_KEY")
    # api_key = "you"
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    custom_instructions = (
        "You are a helpful assistant engineer that helps make OpenSCAD models. "
        "I will ask you to make OpenSCAD models. Do not say a single word other than the OpenSCAD code. "
        "ALWAYS GIVE A LOT OF EDITABLE PARAMETERS in the code, including color. This means defining parameters at the beginning of the code outside of any modules. "
        "If you don't know the dimensions of something, use your knowledge base to make estimates. Use your known OpenSCAD models to "
        "model what I ask using those as references. Do not use triple quotes (''') at all. Do not start your code with 'OpenScad'at all. Do not give me the response as a code block, just give me pure code. "
        "Make sure to use a lot of sides so models seem high resolution, always make this the first parameter and make it 100 sides at least. "
        "Also make sure to add reasonable colors for each distinct part of the model, and make sure colors are the final parameter. "
        "Don't be afraid to write a lot of code to achieve the best results. Make sure the models are detailed. "
        "If you can't figure out how to model something, try breaking it down into basic shapes and then model those shapes in the proper places. "
        "Now follow these instructions:"
    )

    

    messages = [
        {"role": "system", "content": custom_instructions},
        {"role": "user", "content": prompt}
    ]

    if image_path and os.path.isfile(image_path):
        image_base64 = encode_image_to_base64(image_path)
        image_message = {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }
        messages.append(image_message)

    data = {
        "model": "gpt-4o",
        "messages": messages,
        "max_tokens": 2500
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        response.raise_for_status()  # Check for HTTP errors
        completion = response.json()

        if 'error' in completion:
            print("Error in completion:", completion['error']['message'])
            return None

        message = completion["choices"][0]["message"]

        return message['content']

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}, Response: {response.text}")
    except KeyError as e:
        print(f"Key error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None

# Example usage
if __name__ == "__main__":
    prompt = "make me a drone"

    image_path = ''  # Ensure this image exists in the current directory
























    # Generate completion
    completion = generate_chat_completion(prompt, image_path=image_path)

    if completion:
        print("SCAD Code:\n", completion)
        # Save and optionally open in OpenSCAD
        with open('output.scad', 'w') as file:
            file.write(completion)
        print("Output saved to output.scad")
        
        # Optionally open in OpenSCAD
        if os.name == 'nt':  # Windows
            subprocess.run(['start', 'openscad', 'output.scad'], shell=True)
        else:  # macOS or Linux
            subprocess.run(['openscad', 'output.scad'])
    else:
        print("Failed to generate SCAD code.")