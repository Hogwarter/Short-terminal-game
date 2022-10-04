import random

print("Welcome to the text adventure!\n")
name = input("What is your name, adventurer?\n")

print("Greetings, " + name + ". Let us go on a quest!")

initSeed = random.randint(0,1000000)

dead = False

currentLocation = {
    "type": "forest",
    "enemies": [],
    "loot": [],
    "buildings": [],
}
location = [0,0] # X, Y

inventory = []
hp = 10


def mainLoop():

    generateCurrentLocation()

    while not dead:
        command = input("Enter a command: ").lower()

        command = command.split()

        if(len(command) < 1):
            continue

        if(command[0] == "exit"):
            exit()

        if(command[0] == "status"):
            print("HP:",hp)
            print("Inventory:",inventory)

        if(command[0] == "look"):
            if(len(command) < 2):
                print("Look where?")
                continue
            if(command[1] == "around"):
                describeLocation()

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

            continue

        if(command[0] == "fight" and len(currentLocation["enemies"]) > 0):
            if(len(command) < 2):
                print("Fight what?")
                continue

            if(command[1] in currentLocation["enemies"]):
                fight(command[1])
            else:
                print("Fight what?")

            continue

        if(command[0] == "loot" and len(currentLocation["loot"]) > 0):
            if(len(command) < 2):
                print("Loot what?")
                continue


            if(command[1] in currentLocation["loot"]):
                loot(command[1])
            else:
                print("Loot what?")

            continue





    

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

    locationSeed = int(str(location[0]) + "44" + str(location[1]))
    random.seed(initSeed+locationSeed)

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



def loot(lootType):
    global currentLocation
    global inventory

    enemyLoot = {
        "bear": ["meat","fur"]
    }

    chestLoot = [
        "dagger",
        "food",
        "nothing"
    ]


    if(lootType.split("_")[0] == "dead"):
        enemy = lootType.replace("dead_","")
        victoryLoot = enemyLoot[enemy][random.randint(0,len(enemyLoot[enemy])-1)]
        
        print("There is:",victoryLoot)
        if(input("keep it? (y/n)": ).lower() == "y"):
            inventory.append(victoryLoot)
        
        currentLocation["loot"].remove(lootType)

    elif(lootType == "chest"):
        chestContent = chestLoot[random.randint(0,len(chestLoot)-1)]

        print("There is: ",chestContent)

        if(chestContent == "nothing"):
            return
        
        if(input("keep it? (y/n): ").lower() == "y"):
            inventory.append(chestContent)
        
        currentLocation["loot"].remove(lootType)

        




def fight(enemy):
    
    global currentLocation
    global inventory
    global hp

    enemyHPlist = {
        "bear": 25
    }

    enemyDMGlist = {
        "bear": 1
    }

    fighting = True
    enemyHP = enemyHPlist[enemy]
    
    print("You are fighting against",enemy)
    print("The enemy has %s HP" % enemyHP)


    while(fighting):
        fightAction = input("Enter a command [fight]: ")

        fightAction = fightAction.split()
        
        if(len(fightAction) <= 0):
            continue

        if(fightAction[0] == "exit"):
            exit()

        if(fightAction[0] == "help"):
            print("Available commands:")
            print("escape (doesn't work always)")
            print("fight (hits the enemy, you can specify to hit the enemy with a weapon in your inventory)")
            print("status (shows your hp, inventory and enemy hp)")
            continue

        if(fightAction[0] == "status"):
            print("HP:",hp)
            print("enemy HP:",enemyHP)
            print("Inventory:",inventory)
        
        # Try to escape
        if(fightAction[0] == "escape"):
            if(random.randint(0,10) >= 3):
                print("You managed to escape")
                fighting = False
                continue
            
        # Player attacks
        elif(fightAction[0] == "fight" or fightAction[0] == "hit" or fightAction[0] == "attack"):
            damage = 1


            if(len(fightAction) == 3):
                if(fightAction[1] == "with" or fightAction[1] == "using"):
                    if(fightAction[2] in inventory):
                        damage = getDmgValue(fightAction[2])

            if(len(fightAction) == 4):
                if(fightAction[1] == enemy):
                    if(fightAction[2] == "with" or fightAction[2] == "using"):
                        if(fightAction[3] in inventory):
                            damage = getDmgValue(fightAction[3])

            enemyHP -= damage

            print(enemy,"hit -"+str(damage)+"hp")

            if(enemyHP <= 0):
                

                print("The enemy has been slain!")
                print("The dead body of",enemy,"can be looted (loot dead_"+enemy+")")
                currentLocation["loot"].append("dead_" +enemy)
                currentLocation["enemies"].remove(enemy)
                fighting = False
                continue

        
        # Enemy attacks
        if(random.randint(0,5) >= 3):
            dmg = enemyDMGlist[enemy]
            print(enemy,"attacks you -"+str(dmg)+"hp")
            hp -= dmg
            





def getDmgValue(item):

    dmg = 0

    weapons = {
        "dagger": 3,
        "sword": 5
    }

    if(item in weapons):
        dmg = weapons[item]


    return dmg



mainLoop()
