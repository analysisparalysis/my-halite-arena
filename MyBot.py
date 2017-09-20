from hlt import *
from networking import *

import logging
logging.basicConfig(filename='log.log',level=logging.DEBUG)
def log(string):
    logging.debug(string)
    return;

myID, gameMap = getInit()
sendInit("MyPythonBot")

def locations_to_sites(locationlist):
    #takes a list of locations and returns a list of sites
    sitelist = []
    for location in locationlist:
        sitelist.append(gameMap.getSite(location))
    return sitelist

def get_adjacent_locations(location):
    al = []
    al.append(gameMap.getLocation(location, NORTH))
    al.append(gameMap.getLocation(location, EAST))
    al.append(gameMap.getLocation(location, SOUTH))
    al.append(gameMap.getLocation(location, WEST))
    return al

def get_adjacent_sites(location):
    #returns a list of site objects adjacent to the argument location
    neighboringSites = []
    for neighboringLocation in get_adjacent_locations(location):
        neighboringSites.append(gameMap.getSite(neighboringLocation))
    return neighboringSites

def get_highest_production(locationlist):
    productionValues = []
    for location in locationlist:
        site = gameMap.getSite(location)
        productionValues.append(site.production)
    for location in locationlist:
        site = gameMap.getSite(location)
        if site.production == max(productionValues):
            return location


def get_lowest_strength(sitelist):
    #inputs list of sites, outputs lowest
    lowest = []
    sitestrengths = []
    for site in sitelist:
        sitestrengths.append(gameMap.getSite(location).strength)
    for site in sitelist:
        if site.strength == min(sitestrengths):
            lowest.append(site)
    return lowest

def get_angle(l1, l2):
    angle = gameMap.getAngle(l1, l2)
    angle = math.floor(round(angle * 57.295779513, 0) + 90)
    while angle > 360:
        angle -= 360
    while angle < 0:
        angle += 360
    return angle

def get_cardinal_direction(l1, l2):
    angle = get_angle(l1, l2)
    if angle > 315 or angle <= 45:
        return NORTH
    if angle > 45 and angle <= 135:
        return EAST
    if angle > 135 and angle <= 225:
        return SOUTH
    if angle > 225 and angle <= 315:
        return WEST

def acquire_targets(unitLocation):
    targets = []
    for adjacent_location in get_adjacent_locations(unitLocation):
        adjacent_site = gameMap.getSite(adjacent_location)
        if gameMap.getSite(unitLocation).strength > gameMap.getSite(adjacent_location).strength and adjacent_site.owner != myID: # an adjacent space can be killed, mark it as a target
            targets.append(adjacent_location)
    return targets
    #returns list of locations

def surrounded_by_allies(unitLocation):
    for adjacentLocation in get_adjacent_locations(unitLocation):
        adjacentSite = gameMap.getSite(adjacentLocation)
        if adjacentSite.owner != myID:
            return False
        else:
            continue
    return True

def get_nearest_territory(unitLocation):
    distances = []
    for location in enemyLocations:
        distances.append(gameMap.getDistance(unitLocation, location))
    for location in enemyLocations:
        if gameMap.getDistance(unitLocation, location) == min(distances):
            return location


def getMove(unitLocation):
    if enemyStrength > alliedStrength * 1.25 and enemyProduction < alliedProduction:
        return directive_defend(unitLocation)
    else:
        return directive_attack(unitLocation)

def directive_defend(unitLocation):
    return STILL

def directive_attack(unitLocation):
    move = STILL
    if gameMap.getSite(unitLocation).strength == 0:
        return STILL
    if surrounded_by_allies(unitLocation):
        return get_cardinal_direction(unitLocation, get_nearest_territory(unitLocation))
    if acquire_targets(unitLocation) != []:
        move = get_cardinal_direction(unitLocation, get_highest_production(acquire_targets(unitLocation)))
    return move

while True:
    moves = []
    enemyLocations = []
    enemyStrength = 0
    enemyProduction = 0

    alliedLocations = []
    alliedProduction = 0
    alliedStrength = 0
    neutralLocations = []
    gameMap = getFrame()
    for y in range(gameMap.height): # build our board data
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                alliedLocations.append(location)
            elif gameMap.getSite(location).owner == 0:
                neutralLocations.append(location)
            else:
                enemyLocations.append(location)

    for alliedLocation in alliedLocations:
        alliedSite = gameMap.getSite(alliedLocation)
        alliedStrength += alliedSite.strength
        alliedProduction += alliedSite.production

    for enemyLocation in enemyLocations:
        enemySite = gameMap.getSite(enemyLocation)
        enemyStrength += enemySite.strength
        enemyProduction += enemySite.production

    for alliedLocation in alliedLocations: #loop through troops and give orders
        moves.append(Move(alliedLocation, getMove(alliedLocation)))
    sendFrame(moves)
