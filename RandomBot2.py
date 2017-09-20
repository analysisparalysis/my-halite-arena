from hlt import *
from networking import *

myID, gameMap = getInit()
sendInit("RandomPythonBot")

def getMove(site):
    if gameMap.getSite(site).strength < 200:
        return STILL
    else:
        return random.choice(DIRECTIONS)
while True:
    moves = []
    enemySites = []
    alliedSites = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                alliedSites.append(location)
    for alliedSite in alliedSites:
        moves.append(Move(alliedSite, getMove(alliedSite)))
    sendFrame(moves)
