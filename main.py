import google.generativeai as genai
import json
import os
from character_data import Character
genai.configure(api_key="")
model = genai.GenerativeModel('gemini-1.5-flash')


def extract_json(text):
    start = text.find('```json')
    end = text.find('```', start + 7)

    if start == -1 or end == -1:
        return None, text

    json_part = text[start + 7:end].strip()
    remaining_text = text[:start] + text[end + 3:]

    return json_part, remaining_text.strip()


def main():
    history = ""
    setting = input("Enter the setting: ")
    print(setting)
    sure = input("Are you sure? (y/n): ")
    while sure != 'y':
        setting = input("Enter the setting: ")
        sure = input("Are you sure? (y/n): ")

    character_name = input("Enter the character name: ")
    print(character_name)
    sure = input("Are you sure? (y/n): ")
    while sure != 'y':
        character_name = input("Enter the character name: ")
        sure = input("Are you sure? (y/n): ")

    character_desc = input("Enter the character description: ")
    print(character_desc)
    sure = input("Are you sure? (y/n): ")
    while sure != 'y':
        character_desc = input("Enter the character description: ")
        sure = input("Are you sure? (y/n): ")

    scenario = input("Enter the scenario: ")
    print(scenario)
    sure = input("Are you sure? (y/n): ")
    while sure != 'y':
        scenario = input("Enter the scenario: ")
        sure = input("Are you sure? (y/n): ")

    prompt = (
        f"You are writing a story with the following setting: {setting}, character name: {character_name}, character description: {character_desc}, and scenario: {scenario}. "
        "Please create an in-depth story that has a lot of open-ended suggested options for the user in the format A, B, C. "
        "End the text section with 'but the choice is yours' as well as display the character data in JSON format, formatted like this:\n"
        "{\n"
        '  "name": "Wumbo",\n'
        '  "description": "A small man with 4 legs and an elephant trunk for an arm.",\n'
        '  "health": 30,\n'
        '  "attack_power": 20,\n'
        '  "magic_power": 10,\n'
        '  "inventory": {\n'
        '    "apples": "A basket of Red Delicious apples"\n'
        '  }\n'
        "}\n"
        "do not add any flavour text to the json file. "
        "Your final response should look like this:\n"
        "The wind whipped around Mr. Wooly, biting at his face like a hungry wolf. He squinted, the snow blurring his vision, and adjusted the fur-lined hood of his thick coat. He was a man built for this, a mountain man through and through, his body toughened by years of battling the unforgiving elements. But even he was starting to feel the strain.\n"
        "Suggested options:\n"
        "**A.** **Push on:** He could attempt to trek through the storm, hoping to find a new shelter or a path down the mountain. The danger is high, but the potential rewards are equally so.\n"
        "**B.** **Stay put:** He could try to build a new fire, conserve his remaining energy, and wait out the storm. This might take a while, but it's safer than venturing out into the blizzard.\n"
        "**C.** **Seek out a cave:** He could search for a natural cave or rock overhang, hoping to find some semblance of protection. It would be a risky gamble, but the potential for safety and shelter could be worth it.\n"
        "But the choice is yours.\n"
        "```json\n"
        "{\n"
        '  "name": "Mr. Wooly",\n'
        '  "description": "A big man that has adapted to the elements",\n'
        '  "health": 75,\n'
        '  "attack_power": 15,\n'
        '  "magic_power": 0,\n'
        '  "inventory": {\n'
        '    "dried_meat": "A small pouch of dried meat",\n'
        '    "axe": "A sturdy axe for chopping wood",\n'
        '    "fur_lined_coat": "A thick coat lined with animal fur",\n'
        '    "wool_hat": "A warm wool hat",\n'
        '    "water_skin": "A leather water skin, nearly empty"\n'
        '  }\n'
        "}\n"
        "```\n"
    )

    response = model.generate_content(prompt)
    json_part, remaining_text = extract_json(str(response.text))
    print(response.text)
    if json_part:
        try:
            json_data = json.loads(json_part)

            # Create the character_data folder if it doesn't exist
            os.makedirs("character_data", exist_ok=True)

            # Create the JSON file with the character's name
            file_name = f"character_data/{character_name.replace(' ', '_')}.json"
            with open(file_name, 'w') as json_file:
                json.dump(json_data, json_file, indent=2)

            print(f"JSON file '{file_name}' has been created.")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
    else:
        print("No JSON data found in the string.")
    character1 = Character(
    name=json_data["name"],
    description=json_data["description"],
    health = json_data["health"],
    attack_power=json_data["attack_power"],
    magic_power=json_data["magic_power"],
    inventory=json_data["inventory"]
)
    print("\nRemaining text:")
    print(remaining_text)
    print(character1)

    history += remaining_text
    prompt = input("What will you do next: ")
    while prompt != "end":
        if prompt == "save":
            character1.save_to_json()
            break
        response = model.generate_content(
            f"you are playing the role of a story teller, so far this is what has happened in the story: {history} the user wants to do this: {prompt},these are your characters current stats{character1} if there are any changes made to the character return a json file in the format"
            "{\n"
        '  "name": "Wumbo",\n'
        '  "description": "A small man with 4 legs and an elephant trunk for an arm.",\n'
        '  "health": 30,\n'
        '  "attack_power": 20,\n'
        '  "magic_power": 10,\n'
        '  "inventory": {\n'
        '    "apples": "A basket of Red Delicious apples"\n'
        '  },\n'
        "} do not add any flavour text to the json file"
        )
        if '```json' in str(response.text):
            json_part, remaining_text = extract_json(str(response.text))
            json_data = json.loads(json_part)
            character1.update_health(json_data["health"])
            character1.update_inventory(json_data["inventory"])
            print("\nRemaining text:")
            print(remaining_text)

        print(response.text)
        #print(response)
        print(character1)
        history += str(response.text)
        prompt = input("What will you do next: ")


if __name__ == "__main__":
    main()
