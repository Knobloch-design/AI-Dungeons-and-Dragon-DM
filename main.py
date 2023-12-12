import json
import time
from openai import OpenAI

with open('secrets.json') as f:
    secrets = json.load(f)

client = OpenAI(
    # Defaults to os.environ.get("OPENAI_API_KEY")
    # Otherwise use: api_key="Your_API_Key",
    api_key = secrets['openai_api_key']
)


response = client.images.generate(
  model="dall-e-3",
  prompt="digital painting, a human fighter descending an ancient spiral staircase into a shadowy undercroft with a legendary spring at its heart, surrounded by signs of chaos and abandoned weapons, eerie and somber with a single torch casting flickering light on the surroundings",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print(image_url)