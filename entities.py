from maths import *


class Entity:
    ANIMALS = ["Bear", "Chicken", "Deer", "Wolf", "Horse", "Boar"]

    def __init__(self, vector3, szName, health=0, playername="", szName2=""):
        self.vector3 = vector3
        self.szName = szName
        self.szName2 = szName2
        self.health = health
        self.playername = playername
        self.entity = self.setup()

    def setup(self):
        if self.szName == "Player":
            return Player(self.vector3, self.health, self.playername)
        elif self.szName == "LootContai":
            return Lootable(self.vector3, self.szName2)
        elif self.szName == "Stash":
            return Stash(self.vector3)
        elif self.szName == "OreResource":
            return Node(self.vector3, self.szName2)
        elif self.szName == "SupplyDrop":
            return Supplydrop(self.vector3)
        elif self.szName in self.ANIMALS:
            return Animal(self.vector3, self.szName)

    def __str__(self):
        return "BaseEntity"


class Player:
    def __init__(self, vector3, health, name):
        self.render = True
        self.vector3 = Vector3(vector3[0], vector3[1], vector3[2])
        self.health = health
        self.name = name
        self.height = 1.8
        self.x_scratch = 0.3
        self.box_color = "red"
        self.snap_color = "yellow"

    def __str__(self):
        return "Player"


class Lootable:
    def __init__(self, vector3, name):
        self.render = True
        self.vector3 = Vector3(vector3[0], vector3[1], vector3[2])
        self.name = name
        self.height = 1
        self.x_scratch = 0.5
        self.box_color = "purple"

        self.name = self.setup()

    def setup(self):
        if "crate_normal" in self.name and "crate_normal_2" not in self.name:
            return "Military crate"
        elif "crate_mine" in self.name:
            return "Mine crate"
        elif "crate_basic" in self.name:
            return "Wooden crate"
        elif "foodbox" in self.name:
            return "Foodbox"
        elif "crate_normal_2" in self.name:
            return "Normal box"
        elif "crate_tools" in self.name:
            return "Tool box"
        elif "vehicle_parts" in self.name:
            return "Vehicle parts"
        elif "crate_elite" in self.name:
            return "Elite crate"
        elif "barrel" in self.name:
            self.render = False
            return "Barrel"

    def __str__(self):
        return "Loot"


class Stash:
    def __init__(self, vector3, name="Stash"):
        self.render = True
        self.vector3 = Vector3(vector3[0], vector3[1], vector3[2])
        self.height = 0.5
        self.name = "Stash"
        self.x_scratch = 0.2
        self.box_color = "yellow"

    def __str__(self):
        return "Stash"

class Node:
    def __init__(self, vector3, name):
        self.render = True
        self.vector3 = Vector3(vector3[0], vector3[1], vector3[2])
        self.name = name
        self.height = 1.0
        self.x_scratch = 0.8
        self.box_color = self.setup()

    def setup(self):
        if "sul" in self.name:
            self.name = "Sulfur ore"
            return "yellow"
        elif "sto" in self.name:
            self.name = "Stone ore"
            return "blue"
        elif "met" in self.name:
            self.name = "Metal ore"
            return "brown"
        else:
            self.render = False

    def __str__(self):
        return "Node"


class Supplydrop:
    def __init__(self, vector3, name="SupplyDrop"):
        self.render = True
        self.vector3 = Vector3(vector3[0], vector3[1], vector3[2])
        self.name = name
        self.height = 4.0
        self.box_color = "orange"
        self.x_scratch = 0.3

    def __str__(self):
        return "Supplydrop"


class Animal:
    def __init__(self, vector3, name):
        self.render = True
        self.vector3 = Vector3(vector3[0], vector3[1], vector3[2])
        self.name = name
        self.height = self.setup()
        self.box_color = "cyan"
        self.x_scratch = 0.3

    def setup(self):
        if self.name == "Boar":
            return 1.0
        elif self.name == "Bear":
            return 1.5
        elif self.name == "Chicken":
            return 0.5
        elif self.name == "Deer":
            return 1.5
        elif self.name == "Wolf":
            return 1.0
        elif "Horse" in self.name:
            self.name = "Horse"
            return 1.5

    def __str__(self):
        return "Animal"
