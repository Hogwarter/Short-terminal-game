import random

print("Welcome to the text adventure!\n")
name = input("What is your name, adventurer?\n")

print("Greetings, " + name + ". Let us go on a quest!")


dead = False

currentLocation = {
    "type": "forest",
    "enemies": [],
    "loot": [],
    "buildings": [],
}
location = [0,0] # X, Y


def mainLoop():

    generateCurrentLocation()

    while not dead:
        command = input("Enter a command: ").lower()

        command = command.split()

        if(len(command) < 1):
            continue

        if(command[0] == "exit"):
            exit()

        if(command[0] == "go"):
            if(len(command) < 2):
                print("Go where?")
                continue
            
            if(command[1] == "north"):
                go("north")
            elif(command[1] == "east"):
                go("east")
            elif(command[1] == "south"):
                go("south")
            elif(command[1] == "west"):
                go("west")
            else:
                print("Go where")





    

    print("Game over")



def go(direction):
    directions = {"north": 1, "south":-1,"west":-1,"east":1}

    if(direction == "north" or direction == "south"):
        location[1] += directions[direction]

    if(direction == "east" or direction == "west"):
        location[0] += directions[direction]

    
    print("Went "+direction)
    print("Location:",location)

    generateCurrentLocation()


def generateCurrentLocation():

    locationType = "forest"

    enemies = []

    if(random.randint(0,10) <= 3):
        enemies.append("bear")


    loot = []

    if(random.randint(0,10) <= 5):
        loot.append("chest")

    buildings = []

    if(random.randint(0,100) <= 5):
        buildings.append("old house")
    
    global currentLocation

    currentLocation = {
        "type": locationType,
        "enemies": enemies,
        "loot": loot,
        "buildings": buildings,
    }

    describeLocation()



def describeLocation():

    global currentLocation

    print("You are in a "+currentLocation["type"])

    if(len(currentLocation["enemies"]) > 0):
        print("Enemies nearby: "+",".join(currentLocation["enemies"]))

    if(len(currentLocation["loot"]) > 0):
        print("Loot nearby: "+",".join(currentLocation["loot"]))

    if(len(currentLocation["buildings"]) > 0):
        print("Buildings nearby: "+",".join(currentLocation["buildings"]))


    




mainLoop()