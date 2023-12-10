import requests
import os
import openai
from PIL import Image
from io import BytesIO
import secrets
from openai import OpenAI
import json
import time


with open('secrets.json') as f:
    secrets = json.load(f)

client = OpenAI(
    # Defaults to os.environ.get("OPENAI_API_KEY")
    # Otherwise use: api_key="Your_API_Key",
    api_key = secrets['openai_api_key']
)

"""chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
      messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "how can I display the response of an openai assistant in python?"},
  ]
)
print(chat_completion.choices[0].message.content)"""

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter", "type": "retrieval"}],
    model="gpt-4-1106-preview"
)

thread = client.beta.threads.create()






message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
)

run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)




while run.status !="completed":
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id,
        )
    
    print(run.status)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print(messages.data[0].content[0].text.value)


message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `2x + 10 = 14`. Can you help me?"
)
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
)
run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

while run.status !="completed":
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id,
        )
    
    print(run.status)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print(messages.data[0].content[0].text.value)

print(messages)

"""print("run: ", run)

print("messages: ", messages)

print("message: ", message)"""