
import requests
import os
import openai
from PIL import Image
from io import BytesIO
import secrets
from openai import OpenAI
import json
import time




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



    
campaign = DM
response1 = campaign.messageAPI(campaign,"I want to start I new campaign, can you help?")
print(response1)