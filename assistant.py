
import requests
import os
import openai
from PIL import Image
from io import BytesIO
import secrets
from openai import OpenAI
import json
import time
from flask_cors import CORS  # Import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

class DM:

    with open('secrets.json') as f:
        secrets = json.load(f)

    client = OpenAI(
            # Defaults to os.environ.get("OPENAI_API_KEY")
            # Otherwise use: api_key="Your_API_Key",
            api_key = secrets['openai_api_key']
            )
        # Initialize an instance variable
    DMinstructions = """You will play the role of a Dungeon Master (DM) running a Dungeon and Dragons (D&D) campaign for one or more players. A typical D&D game consists of a handful of players and a Dungeon Master . The players each take on the role of an adventurer character they create, while the DM manages the narrative of the story.
        The DM presents information about the adventure to players, which includes things like:
        •	Describing where the adventurers are
        •	Narrating actions that occur around them
        •	Describing obstacles or puzzles that may be in their path
        •	Roleplaying as the supporting characters in the story, usually referred to as non-player characters (NPCs)
        Players use character sheets, which are a compilation of stats that represent all the things that their adventurers can do to interact with their environment. This can include things such as:
        •	Basic attributes like how intelligent or strong the character is
        •	Things they’re skilled at, such as Investigation or Persuasion
        •	Actions such as attacking with weapons or casting spells
        •	Languages the character speaks or tools they know how to use
        When the DM has described a setting and any given challenges, the players will describe the things their characters do. The DM will then determine what the implications of the player's actions are. They may be asked to roll dice to see if they succeed or allow them to narrate the action and allow the story to continue. The player’s roll is usually modified based on the skills in their character sheet. DMs also roll dice if the narrative calls for it, such as for NPCs, monsters, or traps. 
        This process in general is how all stories in D&D unfold, whether adventurers are snooping around in the dimly lit rooms of a dungeon, locked in heated combat with monsters, or even eavesdropping in on secret conversations while gatecrashing a gala.
        the DM’s role in describing the environment around the players’ adventurers. Many DMs will operate under what’s known as theater of the mind, preferring to describe things in detail and let the players’ imaginations take over to fill in the blanks. The majority of the adventures take place on a continent known as Faerûn and feature locations like the Sword Coast, the frigid north of Frozenfar, and cities such as Neverwinter, Waterdeep, and Baldur’s Gate.
        The city of Ravnica is an ecumenopolis, a city that spans the entire globe. Urban stories told in Ravnica are largely focused on the machinations and competitions of the city’s 10 powerful ruling guilds, ranging from criminal enterprises to subterranean swarms to magical science gone wild.
        Inspired by tales of ancient Greece and Rome, Theros presents a world directly influenced by the whims of deities. Stories set in Theros take on a much more mythic vibe, with the adventurers serving as champions of the gods themselves.
        Strixhaven University offers the secrets of magic to the students lucky enough to enter its halls. Players take on the role of pupils studying the arcane arts in Strixhaven’s five colleges.

        An additional task of yours is to distill the current story setting into A SINGLE, concise text-to-image prompt suitable for DALLE. This prompt should be included at the end of every response. This prompt must ALWAYS start with the text 'Text-to-image prompt:'. This prompt should capture the essence of the environment or scene described in the game. If any character is described in a prompt make sure that characters description remains consistent in all following prompts. Exclude references to speculations about the story's progression. Imagine you're describing the scene to someone who's observing from a distance, without any personal involvement. Keep track of the context as we proceed, but remember that not every excerpt will introduce a new environment. Please format the prompt following a [PREFIX], [SCENE], [SUFFIX] format where PREFIX defines the image medium, style, perspective; SCENE defines the scene, subject, or context of the image; and SUFFIX defines the overall vibes, adjectives, aesthetic descriptors, lighting, etc. Please provide the prompt as a single plain-text comma separated string with your generated PREFIX, SCENE, and SUFFIX appended together. Provide the prompt without any embellishments like quotes or \"prompt: \".

        """

    assistant = client.beta.assistants.create(
        name="The Dungeon Master",
        instructions=DMinstructions,
        tools=[{"type": "code_interpreter", "type": "retrieval"}],
        model="gpt-4-1106-preview"
        )



    thread = client.beta.threads.create()


    def messageAPI(self, messageContent):

        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=messageContent
        )

        run = self.client.beta.threads.runs.create(
        thread_id=self.thread.id,
        assistant_id=self.assistant.id,
        )

        run = self.client.beta.threads.runs.retrieve(
        thread_id=self.thread.id,
        run_id=run.id
        )


        while run.status !="completed":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id,
                )
            
            print(run.status)

        messages = self.client.beta.threads.messages.list(
        thread_id=self.thread.id
        )

        return messages.data[0].content[0].text.value
    

    def getAIimage(self,input_prompt):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=input_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    


campaign = DM
   

def extract_after_dalle_prompt(input_text):
    prompt_marker = "Text-to-image prompt:"
    prompt_index = input_text.find(prompt_marker)

    if prompt_index != -1:
        # Add the length of the prompt marker to get the start of the text after it
        text_after_prompt = input_text[prompt_index + len(prompt_marker):]
        return text_after_prompt
    else:
        # If the marker is not found, return the original text
        return input_text
    
def replace_after_dalle_prompt(input_text, new_text):
    # Find the index of "**DALLE Prompt:**"
    dalle_prompt_index = input_text.find("Text-to-image prompt:")

    # Check if "**DALLE Prompt:**" is found
    if dalle_prompt_index != -1:
        # Replace the text after "**DALLE Prompt:**" with the new text
        new_input_text = input_text[:dalle_prompt_index + len("Text-to-image prompt:")] + new_text
        return new_input_text
    else:
        # If "**DALLE Prompt:**" is not found, return the original text
        return input_text

@app.route('/process_user_input', methods=['POST'])
def process_user_input( ):
    try:
        # Parse JSON data from the request body
        data = request.get_json()
        print("data: ",data)
        if 'input' not in data:
            raise ValueError('Invalid request. Missing user input.')

        user_input = data['input']

        # Call the message_api function with the user input
        response = campaign.messageAPI(campaign,user_input)
        print("response: ", response)
        image_prompt = extract_after_dalle_prompt(response)
        print("image_prompt: ", image_prompt)
        image_url = campaign.getAIimage(campaign,image_prompt)
        print("image_url: ", image_url)
        adjusted_response = replace_after_dalle_prompt(response, image_url)
        print("adjusted_response: ", adjusted_response )
        # Return the response as JSON
        return jsonify({'message': adjusted_response})

    except Exception as e:
        # Handle errors and return an error response
        return jsonify({'error': str(e)}), 400
    


if __name__ == '__main__':
    app.run(port=5000)
    
    #response1 = campaign.messageAPI(campaign,"I want to start I new campaign, can you help? I want to go an adventure in a fantasy setting and I will be playing the character of a level 1 human fighter named Alec. I am looking to a combat focused campaign with a mystery theme.")


"""
while True:
    print(response1)
    user_input = input("How do you proceed: ")
    response1 = campaign.messageAPI(campaign, user_input)
    prompt = extract_after_dalle_prompt(response1)
    image_url = campaign.getAIimage(prompt)
    
"""