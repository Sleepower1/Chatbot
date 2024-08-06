import json

class Character:
    def __init__(self, name=None, description=None, health=None, attack_power=None, magic_power=None, inventory=None):
        self.name = name
        self.description = description
        self.health = health
        self.attack_power = attack_power
        self.magic_power = magic_power
        self.inventory = inventory

    def update_health(self, health):
        self.health = health

    def update_inventory(self, inventory):
        self.inventory = inventory

    def __str__(self):
        return f'Character: {self.name}\n {self.description} \n Health:{self.health} \n Attack:{self.attack_power}\n Magic Power:{self.magic_power}\n Inventory:{self.inventory}'

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "health": self.health,
            "attack_power": self.attack_power,
            "magic_power": self.magic_power,
            "inventory": self.inventory
        }

    def save_to_json(self):
        with open(f"character_data/{self.name.replace(' ', '_')}.json", 'w') as file:
            json.dump(self.to_dict(), file, indent=4)
            print("save completed")