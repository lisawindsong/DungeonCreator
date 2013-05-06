#Dungeon Generator v0.03
# Chris Pack
#=====================================================
from Tkinter import *
import random
import tkMessageBox
import Pmw

dungeon = []
rooms_in_dungeon = 0#so now I can add x rooms to a dungeon and then know to stop
pixels_per_square = 48

def draw_door(acanvas,adoor):
    point1x,point1y = adoor.get_coordinates()
    point1x *= pixels_per_square
    point1y *= pixels_per_square
    point2x = point1x
    point2y = point1y
    facing = adoor.direction
    if adoor.printme == 1:
        if facing == "east":
            point1x += .75 * pixels_per_square
            point1y += .25 * pixels_per_square
            point2x += 1 * pixels_per_square
            point2y += .75 * pixels_per_square
        elif facing == "south":
            point1x += .25 * pixels_per_square
            point1y += .75 * pixels_per_square
            point2x += .75 * pixels_per_square
            point2y += 1 * pixels_per_square
        elif facing == "west":
            point1x += 0 * pixels_per_square
            point1y += .25 * pixels_per_square
            point2x += .25 * pixels_per_square
            point2y += .75 * pixels_per_square
        elif facing == "north":
            point1x += .25 * pixels_per_square
            point1y += 0 * pixels_per_square
            point2x += .75 * pixels_per_square
            point2y += .25 * pixels_per_square
        else:
            pass
            #print "You cannot face Dennis!"
        
        acanvas.create_rectangle(point1x, point1y, point2x, point2y, fill="brown")

def create_a_room(number):
    temprand = random.randint(1,number)
    
    if temprand == 10:
        return 8, 12
    elif temprand == 9:
        return 8, 8
    elif temprand == 8:
        return 6,8
    elif temprand == 7:
        return 8,6
    elif temprand == 6:
        return 6,6
    elif temprand == 5:
        return 4,4
    elif temprand == 4:
        return 2,4
    elif temprand == 3:
        return 4,2
    elif temprand == 2:
        return 2,2
    elif temprand == 1:
        return 1,3

def find_a_room(dungeon_list):
    for room in dungeon_list:
        if room.room_type == "room" or room.room_type == "hall":
            if room.doors_finished == False:
                room.doors_finished = True
                return True, room
            else:
                pass
                #print "room ", room, " is done."
    #print "No unfinished rooms in dungeon"
    return False, room
            
def fill_a_room(empty_room):
    random_number = 3#guaranteed by fair die roll to be random    #number of doors to add
    roomx,roomy = empty_room.get_coordinates()
    roomwide,roomtall = empty_room.get_size()

    #two parts:
    #====================================================
    #Fill-a-Room part 1: insert number of doors into room
    #====================================================

    for doors_to_add in range (0, random_number):
        tempdoorin = Feature()
        tempdoorout = Feature()
        templocx = 1
        templocy = 1
        templocx2 = 1
        templocy2 = 1
        tempfacing = "east"#if facing = east, new second door facing "west"
        tempfacing2 = "east"
        temptype = "door"
        stilltrying = True
        sidestried = 0
        #if there is no door in locxy place door
        #if there is a door in xy, move to next wall
        while stilltrying and (sidestried < 4):
            if tempfacing == "east":
                templocx = roomx + roomwide -1
                templocy = roomy + roomtall/2
                tempfacing2 = "west"
                templocx2 = templocx + 1
                templocy2 = templocy
            
            if tempfacing == "south":
                templocx = roomx + roomwide/2
                templocy = roomy + roomtall - 1
                tempfacing2 = "north"
                templocx2 = templocx
                templocy2 = templocy + 1
            
            if tempfacing == "west":
                templocx = roomx
                templocy = roomy + roomtall/2
                tempfacing2 = "east"
                templocx2 = templocx - 1
                templocy2 = templocy
            
            if tempfacing == "north":
                templocx = roomx + roomwide/2
                templocy = roomy
                tempfacing2 = "south"
                templocx2 = templocx
                templocy2 = templocy - 1
            
            #make sure there isn't enother door in this spot already
            for each_door in dungeon:
                if each_door.feat_type == "door":
                    if each_door.are_you_in_this_square((templocx,templocy)):
                        tempdoorin.door_is_legal = 0
            #here I switch the door wall and try another
            
            if tempdoorin.door_is_legal == 1:
                #print "this door is legal"
                tempdoorin.set_coordinates(templocx,templocy)
                tempdoorin.set_direction(tempfacing)
                tempdoorin.feat_type = temptype
                empty_room.add_door(tempdoorin)#create door
                tempdoorout.set_coordinates(templocx2,templocy2)
                tempdoorout.set_direction(tempfacing2)
                tempdoorout.feat_type = temptype
                #tempdoorout.printme = 0
                dungeon.append(tempdoorout)#create shadow door
                tempdoorin.partnerdoor = tempdoorout
                tempdoorout.partnerdoor = tempdoorin
                stilltrying = False
            else:
                if tempfacing == "east":
                    tempfacing = "south"
                elif tempfacing == "south":
                    tempfacing = "west"
                elif tempfacing == "west":
                    tempfacing = "north"
                elif tempfacing == "north":
                    tempfacing = "east"
                sidestried +=1
            tempdoorin.door_is_legal = 1
            #print "end of doors loop, restarting"
        if sidestried >3:
            pass
            #print "tried all the times and couldn't place another door"
            
    #====================================================
    #Fill-a-Room part 2: insert rooms onto doors
    #====================================================
    if empty_room.num_of_doors == 0:
        pass
        #print "no doors in this room"
        #ERROR this should never happen
        
    for this_door in empty_room.doors:
        temp_room = Room()
        temp_loc_x = 0
        temp_loc_y = 0
        temp_size_x = 3
        temp_size_y = 3
        temp_type = "room"
        temp_door_facing = this_door.get_direction()
        randkey = 0
        
        randkey = random.randint(1,10)
        while randkey > 0:
            temp_size_x, temp_size_y = create_a_room(randkey)
            if temp_size_x == 1:
                temp_type = "hall"
                if temp_door_facing == "east" or temp_door_facing == "west":
                    temp_size_x = 3
                    temp_size_y = 1
            
            if temp_door_facing == "north":
                temp_loc_x = this_door.x_coordinate - (temp_size_x/2)
                temp_loc_y = this_door.y_coordinate - temp_size_y
            
            if temp_door_facing == "south":
                temp_loc_x = this_door.x_coordinate - (temp_size_x/2)
                temp_loc_y = this_door.y_coordinate
                temp_loc_y = temp_loc_y + 1
            
            if temp_door_facing == "east":
                temp_loc_x = this_door.x_coordinate
                temp_loc_x = temp_loc_x + 1
                temp_loc_y = this_door.y_coordinate - (temp_size_y/2)
            
            if temp_door_facing == "west":
                temp_loc_x = this_door.x_coordinate - temp_size_x
                temp_loc_y = this_door.y_coordinate - (temp_size_y/2)
            
            #new room location x and Y now determined, now look for conflicts.
            temp_room.set_coordinates(temp_loc_x, temp_loc_y)
            temp_room.set_size(temp_size_x,temp_size_y)
            temp_room.set_type(temp_type)
            temp_room.get_my_coordinates_list()
            #====================================================================
            for each_room in dungeon:
                if each_room.room_type == "room" or each_room.room_type == "hall":
                    for room_coordinates in range (0, len(each_room.my_coordinates)):
                        if temp_room.are_you_in_this_square(each_room.my_coordinates[room_coordinates]):
                            temp_room.room_is_legal = 0
            #====================================================================
            if temp_room.room_is_legal == 1:
                temp_room.add_room()#win            
                #print "this room is legal"
                randkey = 1
                this_door.printme = 1
                this_door.partnerdoor.printme = 1
                #stilltrying = False
            else:
                this_door.printme = 0
                this_door.partnerdoor.printme = 0
                #flag this door and it's shadow door DO NOT PRINT
            temp_room.room_is_legal = 1
            #===========================================================
            randkey -= 1
        
def get_monster(cr):
    crmin = cr - 1
    crmax = cr + 1
    temprand = random.randint(crmin, crmax)
    
    if temprand == 0:
        monsterrand = random.randint(1, 14)
        #return "Level 0 monster"
        if monsterrand == 1:
            return "CR 1/8 Bat, p. 131"
        elif monsterrand == 2:
            return "CR 1/4 Kobold, p.183"
        elif monsterrand == 3:
            return "CR 1/4 Rat, p. 132"
        elif monsterrand == 4:
            return "CR 1/4 Mite, p. 207"
        elif monsterrand == 5:
            return "CR 1/3 Dire Rat, p. 232"
        elif monsterrand == 6:
            return "Cr 1/3 Duergar, p. 117"
        elif monsterrand == 7:
            return "CR 1/3 Fire Beetle, p. 33"
        elif monsterrand == 8:
            return "CR 1/3 Goblin, p. 156"
        elif monsterrand == 9:
            return "CR 1/3 Orc, p. 222"
        elif monsterrand == 10:
            return "Cr 1/3 Skeleton, Human, p. 250"
        elif monsterrand == 11:
            return "CR 1/2 Giant Centipede, p. 43"
        elif monsterrand == 12:
            return "CR 1/2 Hobgoblin, p. 175"
        elif monsterrand == 13:
            return "CR 1/2 Stirge, p. 260"
        elif monsterrand == 14:
            return "CR 1/2 Vegepygmy, p. 273"
        elif monsterrand == 15:
            return "CR 1/2 Zombie, Human, p. 288"
        else:
            return "CR 1/4 Kobold, p.183"
            
    elif temprand == 1:
        #return "Level 1 monster"
        monsterrand = random.randint(1, 11)
        if monsterrand == 1:
            return "CR 1 Darkmantle, p. 55"
        elif monsterrand == 2:
            return "CR 1 Earth Elemental, small, p. 122"
        elif monsterrand == 3:
            return "CR 1 Ghoul, p. 146"
        elif monsterrand == 4:
            return "CR 1 Giant Spider, p. 258"
        elif monsterrand == 5:
            return "CR 1 Gnoll, p. 155"
        elif monsterrand == 6:
            return "Cr 1 Goblin Dog, p. 157"
        elif monsterrand == 7:
            return "CR 1 Spider Swarm, p. 258"
        elif monsterrand == 8:
            return "CR 1 Troglodyte, p. 267"
        elif monsterrand == 9:
            return "CR 1 Kobolds (2), p. 183"
        elif monsterrand == 10:
            return "Cr 1 Dire Rats (2), p. 232"
        elif monsterrand == 11:
            return "CR 1 Drow (2), p. 114"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 2:
        #return "Level 2 monster"
        monsterrand = random.randint(1, 17)
        if monsterrand == 1:
            return "CR 2 Giant Ant, p. 16"
        elif monsterrand == 2:
            return "CR 2 Dire Bat, p. 30"
        elif monsterrand == 3:
            return "CR 2 Bat Swarm, p. 30"
        elif monsterrand == 4:
            return "CR 2 Bugbear, p. 38"
        elif monsterrand == 5:
            return "CR 2 Cave Fisher, p. 41"
        elif monsterrand == 6:
            return "CR 2 Choker, p. 45"
        elif monsterrand == 7:
            return "CR 2 Dark Creeper, p. 53"
        elif monsterrand == 8:
            return "CR 2 Demon, Dretch, p. 60"
        elif monsterrand == 9:
            return "CR 2 Demon, Quast, p. 66"
        elif monsterrand == 10:
            return "CR 2 Iron Cobra, p. 182"
        elif monsterrand == 11:
            return "CR 2 Wererat, p. 197"
        elif monsterrand == 12:
            return "CR 2 Werewolf, p. 198"
        elif monsterrand == 13:
            return "CR 2 Morlock, p. 209"
        elif monsterrand == 14:
            return "CR 2 Rat Swarm, p. 232"
        elif monsterrand == 15:
            return "CR 2 Skeletal Champion, p. 252"
        elif monsterrand == 16:
            return "CR 2 Vargoville, p. 272"
        elif monsterrand == 17:
            return "CR 2 Kobolds (3), p. 183"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 3:
        #return "Level 3 monster"
        monsterrand = random.randint(1, 14)
        if monsterrand == 1:
            return "CR 3 Medium Animated Object, p. 14"
        elif monsterrand == 2:
            return "CR 3 Derro, p. 70"
        elif monsterrand == 3:
            return "CR 3 Drow Noble, p. 115"
        elif monsterrand == 4:
            return "CR 3 Medium Earth Elemental, p. 122"
        elif monsterrand == 5:
            return "CR 3 Gelatinous Cube, p. 138"
        elif monsterrand == 6:
            return "Cr 3 Hell Hound, p. 173"
        elif monsterrand == 7:
            return "CR 3 Ogre, p. 220"
        elif monsterrand == 8:
            return "CR 3 Rust Monster, p. 238"
        elif monsterrand == 9:
            return "CR 3 Shadow, p. 245"
        elif monsterrand == 10:
            return "Cr 3 Violet Fungus, p. 274"
        elif monsterrand == 11:
            return "CR 3 Wight, p. 276"
        elif monsterrand == 12:
            return "CR 3 Yeth Hound, p. 286"
        elif monsterrand == 13:
            return "CR 3 Kobolds (4), p. 183"
        elif monsterrand == 14:
            return "CR 3 Dire Rat + 2 Rat Swarms, p. 232"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 4:
        #return "Level 4 monster"
        monsterrand = random.randint(1, 12)
        if monsterrand == 1:
            return "CR 4 Hound, Archon, p.19"
        elif monsterrand == 2:
            return "CR 4 Barghest, p. 27"
        elif monsterrand == 3:
            return "CR 4 Beetle, Giant Stag, p. 33"
        elif monsterrand == 4:
            return "CR 4 Centipede Swarm, p. 43"
        elif monsterrand == 5:
            return "CR 4 Dark Stalker, p. 54"
        elif monsterrand == 6:
            return "Cr 4 Gargoyle, p. 137"
        elif monsterrand == 7:
            return "CR 4 Hydra, p. 178"
        elif monsterrand == 8:
            return "CR 4 Mimic, p. 205"
        elif monsterrand == 9:
            return "CR 4 Minotaur, p. 206"
        elif monsterrand == 10:
            return "Cr 4 Otyugh, p. 223"
        elif monsterrand == 11:
            return "CR 4 Kobolds (5), p. 183"
        elif monsterrand == 12:
            return "CR 4 Dire Rats (2) + Rat Swarm, p. 232"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 5:
        #return "Level 5 monster"
        monsterrand = random.randint(1, 16)
        if monsterrand == 1:
            return "CR 5 Army Ant Swarm, p. 16"
        elif monsterrand == 2:
            return "CR 5 Basidirond, p. 28"
        elif monsterrand == 3:
            return "CR 5 Basilisk, p. 29"
        elif monsterrand == 4:
            return "CR 5 Cloaker, p. 47"
        elif monsterrand == 5:
            return "CR 5 Cyclops, p. 52"
        elif monsterrand == 6:
            return "CR 5 Large Earth Elemental, p. 122"
        elif monsterrand == 7:
            return "CR 5 Gibbering Mouther, p. 153"
        elif monsterrand == 8:
            return "CR 5 Manticore, p. 199"
        elif monsterrand == 9:
            return "CR 5 Mummy, p. 210"
        elif monsterrand == 10:
            return "CR 5 Ochre Jelly, p. 218"
        elif monsterrand == 11:
            return "CR 5 Phase Spider, p. 226"
        elif monsterrand == 12:
            return "CR 5 Troll, p. 268"
        elif monsterrand == 13:
            return "CR 5 Wraith, p. 281"
        elif monsterrand == 14:
            return "CR 5 Dire Rat (4) + 2 Rat Swarms, p. 232"
        elif monsterrand == 15:
            return "CR 5 Rust Monster (2), p. 238"
        elif monsterrand == 16:
            return "CR 5 Kobolds (6), p. 183"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 6:
        #return "Level 6 monster"
        monsterrand = random.randint(1, 10)
        if monsterrand == 1:
            return "CR 6 Demon, Babau, p. 57"
        elif monsterrand == 2:
            return "CR 6 Wood Golem, p. 164"
        elif monsterrand == 3:
            return "CR 6 Half-Fiend Minotaur, p. 171"
        elif monsterrand == 4:
            return "CR 6 Lamia, p. 186"
        elif monsterrand == 5:
            return "CR 6 Salamander, p. 240"
        elif monsterrand == 6:
            return "CR 6 Xill, p. 283"
        elif monsterrand == 7:
            return "CR 6 Xorn, p. 284"
        elif monsterrand == 8:
            return "CR 6 Drow Noble + 4 Drow, p. 114"
        elif monsterrand == 9:
            return "CR 6 Ogre (3), p. 220"
        elif monsterrand == 10:
            return "CR 6 Kobolds (8), p. 183"
        else:
            return "CR 1/4 Kobold, p.183"        
        
    elif temprand == 7:
        #return "Level 7 monster"
        monsterrand = random.randint(1, 10)
        if monsterrand == 1:
            return "CR 7 Black Pudding, p. 35"
        elif monsterrand == 2:
            return "CR 7 Demon, Shadow, p. 67"
        elif monsterrand == 3:
            return "CR 7 Black Dragon, young, p. 92"
        elif monsterrand == 4:
            return "CR 7 Drider, p. 113"
        elif monsterrand == 5:
            return "CR 7 Huge Earth Elemental, p. 122"
        elif monsterrand == 6:
            return "CR 7 Ghost, p. 144"
        elif monsterrand == 7:
            return "CR 7 Flesh Golem, p. 160"
        elif monsterrand == 8:
            return "CR 7 Spectre, p. 256"
        elif monsterrand == 9:
            return "CR 7 Ochre Jelly (3), p. 218"
        elif monsterrand == 10:
            return "CR 7 Kobolds (12), p. 183"
        else:
            return "CR 1/4 Kobold, p.183"            
        
    elif temprand == 8:
        #return "Level 8 monster"
        monsterrand = random.randint(1, 9)
        if monsterrand == 1:
            return "CR 8 Demon, Mabasu, p. 64"
        elif monsterrand == 2:
            return "CR 8 Intellect Devourer, p. 180"
        elif monsterrand == 3:
            return "CR 8 Green Dragon, young, p. 96"
        elif monsterrand == 4:
            return "CR 8 Mohrg, p. 180"
        elif monsterrand == 5:
            return "CR 8 Dark Naga, p. 211"
        elif monsterrand == 6:
            return "CR 8 Oni, Ogre Mage, p. 221"
        elif monsterrand == 7:
            return "CR 8 Greater Shadow, p. 245"
        elif monsterrand == 8:
            return "CR 8 Drow Noble + 8 Drow, p. 114"
        elif monsterrand == 9:
            return "CR 8 Kobolds (16), p. 183"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 9:
        #return "Level 9 monster"
        monsterrand = random.randint(1, 8)
        if monsterrand == 1:
            return "CR 9 Demon, Urock, p. 67"
        elif monsterrand == 2:
            return "CR 9 Greater Earth Elemental, p. 123"
        elif monsterrand == 3:
            return "CR 9 Nessian Hell Hound, p. 173"
        elif monsterrand == 4:
            return "CR 9 Spirit Naga, p. 213"
        elif monsterrand == 5:
            return "CR 9 Vampire, p. 270"
        elif monsterrand == 6:
            return "CR 9 Black Pudding (2), p. 35"
        elif monsterrand == 7:
            return "CR 9 Drider (2), p. 113"
        elif monsterrand == 8:
            return "CR 9 Flesh Golem (2), p. 160"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 10:
        #return "Level 10 monster"
        monsterrand = random.randint(1, 6)
        if monsterrand == 1:
            return "CR 10 Bebilith, p. 32"
        elif monsterrand == 2:
            return "CR 10 Devourer, p. 82"
        elif monsterrand == 3:
            return "CR 10 Red Dragon, young, p. 98"
        elif monsterrand == 4:
            return "CR 10 Clay Golem, p. 159"
        elif monsterrand == 5:
            return "CR 10 Greater Shadow (2), p. 245"
        elif monsterrand == 6:
            return "CR 10 Black Pudding (3), p. 35"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 11:
        #return "Level 11 monster"
        monsterrand = random.randint(1, 5)
        if monsterrand == 1:
            return "CR 11 Black Dragon, adult, p. 82"
        elif monsterrand == 2:
            return "CR 11 Elder Earth Elemental, p. 123"
        elif monsterrand == 3:
            return "CR 11 Stone Golem, p. 163"
        elif monsterrand == 4:
            return "CR 11 Retriever, p. 234"
        elif monsterrand == 5:
            return "CR 11 Vampire (2), p. 270"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 12:
        #return "Level 12 monster"
        monsterrand = random.randint(1, 6)
        if monsterrand == 1:
            return "CR 12 Green Dragon, adult, p. 96"
        elif monsterrand == 2:
            return "CR 12 Lich, p. 188"
        elif monsterrand == 3:
            return "CR 12 Purple Worm, p. 230"
        elif monsterrand == 4:
            return "CR 12 Clay Golem (2), p. 159"
        elif monsterrand == 5:
            return "CR 12 Bebilith (2), p. 32"
        elif monsterrand == 6:
            return "CR 12 Roper, p. 237"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 13:
        #return "Level 13 monster"
        monsterrand = random.randint(1, 5)
        if monsterrand == 1:
            return "CR 13 Demon, Glabrezu, p. 61"
        elif monsterrand == 2:
            return "CR 13 Elder Earth Elemental (2), p. 123"
        elif monsterrand == 3:
            return "CR 13 Stone Golem (2), p. 163"
        elif monsterrand == 4:
            return "CR 13 Iron Golem, p. 162"
        elif monsterrand == 5:
            return "CR 13 Regriever (2), p. 234"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 14:
        #return "Level 14 monster"
        monsterrand = random.randint(1, 5)
        if monsterrand == 1:
            return "CR 14 Demon, Nalfeshnee, p. 65"
        elif monsterrand == 2:
            return "CR 14 Red Dragon, adult, p. 98"
        elif monsterrand == 3:
            return "CR 14 Crag Linnorm, p. 190"
        elif monsterrand == 4:
            return "CR 14 Lich (2) + 2 Zombies, Human, p. 188, 288"
        elif monsterrand == 5:
            return "CR 14 Stone Golem (3), p. 163"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 15:
        #return "Level 15 monster"
        monsterrand = random.randint(1, 3)
        if monsterrand == 1:
            return "CR 15 Red Dragon, adult + Red Dragon, young, p. 82"
        elif monsterrand == 2:
            return "CR 15 Neothelid, p. 214"
        elif monsterrand == 3:
            return "CR 15 Iron Golem (2), p. 162"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 16:
        #return "Level 16 monster"
        monsterrand = random.randint(1, 6)
        if monsterrand == 1:
            return "CR 16 Black Dragon, Ancient, p. 93"
        elif monsterrand == 2:
            return "CR 16 Iron Golem (3), p. 162"
        elif monsterrand == 3:
            return "CR 16 Demon, Nalfeshnee (2), p. 65"
        elif monsterrand == 4:
            return "CR 16 Red Dragon, adult (2), p. 98"
        elif monsterrand == 5:
            return "CR 16 Crag Linnorm (2), p. 190"
        elif monsterrand == 6:
            return "CR 16 Lich (4) + 6 Zombies, Human, p. 188, 288"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 17:
        #return "Level 17 monster"
        monsterrand = random.randint(1, 3)
        if monsterrand == 1:
            return "CR 17 Demon, Marilith, p. 63"
        elif monsterrand == 2:
            return "CR 17 Green Dragon, Ancient, p. 97"
        elif monsterrand == 3:
            return "CR 17 Iron Golem (4), p. 162"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 18:
        #return "Level 18 monster"
        monsterrand = random.randint(1, 3)
        if monsterrand == 1:
            return "CR 18 Neothelid (2), p. 214"
        elif monsterrand == 2:
            return "CR 18 Black Dragon, Ancient (2), p. 97"
        elif monsterrand == 3:
            return "CR 18 Iron Golem (5), p. 162"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 19:
        #return "Level 19 monster"
        monsterrand = random.randint(1, 3)
        if monsterrand == 1:
            return "CR 19 Green Dragon, Ancient (2), p. 97"
        elif monsterrand == 2:
            return "CR 19 Red Dragon, Ancient, p. 99"
        elif monsterrand == 3:
            return "CR 19 Demon, Marilith (2), p. 63"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 20:
        #return "Level 20 monster"
        monsterrand = random.randint(1, 2)
        if monsterrand == 1:
            return "CR 20 Demon, Balor, p. 58"
        elif monsterrand == 2:
            return "CR 20 Demon, Marilith (3), p. 63"
        else:
            return "CR 1/4 Kobold, p.183"
        
    elif temprand == 21:
        #return "Level 21 monster"
        monsterrand = random.randint(1, 3)
        if monsterrand == 1:
            return "CR 20 Demon, Balor (2), p. 58"
        elif monsterrand == 2:
            return "CR 19 Red Dragon, Ancient (2), p. 99"
        elif monsterrand == 3:
            return "CR 25 Tarrasque"
        else:
            return "CR 1/4 Kobold, p.183"
        
    else:
        return "Dread Gazebo"#it is too late.  You have angered the gazebo.
    
class Room:
    #room_type: room, hall, stairs? grand hall? chamber?
    def __init__(self):
        self.room_type = 0
        self.feat_type = 0
        self.x_coordinate = 0
        self.y_coordinate = 0
        self.x_size = 0
        self.y_size = 0
        self.num_of_doors = 0
        self.doors = []
        self.doors_finished = False
        self.my_coordinates = []
        self.room_is_legal = 1
    
    def __str__(self):
        return "room("+ ", ".join([str(self.x_coordinate), str(self.y_coordinate), str(self.x_size), str(self.y_size)])+ ")"
        
    def get_my_coordinates_list(self):
        for width in range(0, self.x_size):
            for height in range(0, self.y_size):
                tempx = width + self.x_coordinate
                tempy = height + self.y_coordinate
                self.my_coordinates.append((tempx,tempy))
            
    def set_coordinates(self, x, y):
        self.x_coordinate = x
        self.y_coordinate = y

    def set_size(self, x, y):
        self.x_size = x
        self.y_size = y
        
    def set_type(self, roomtype):
        self.room_type = roomtype

    def get_coordinates(self):
        return self.x_coordinate, self.y_coordinate

    def get_size(self):
        return self.x_size, self.y_size
    
    def are_you_in_this_square(self, (x, y)):
        tempxsize = self.x_size
        tempxstart = self.x_coordinate
        tempxfinish = tempxstart + tempxsize -1
        
        tempysize = self.y_size
        tempystart = self.y_coordinate
        tempyfinish = tempystart + tempysize -1
        
        if (((x >= tempxstart) and (x <= tempxfinish)) and ((y>= tempystart) and (y<= tempyfinish))):
            return True#the coordinate passed in is in the room's range
        else:
            return False

    def add_door(self,door):
        dungeon.append(door)
        self.doors.append(door)
        self.num_of_doors = len(self.doors)

    def get_doors(self):
        return self.num_of_doors
        
    def add_room(self):
        dungeon.append(self)
        global rooms_in_dungeon
        if self.room_type == "room":#only count "rooms" for the purpose of dungeon size. halls are boring.
            rooms_in_dungeon += 1
        self.get_my_coordinates_list()
        
class Feature:
    #feat_type: door, monster, stairs, trap, treasure
    def __init__(self):
        self.my_room = 0
        self.room_type = 0
        self.feat_type = 0
        self.x_coordinate = 0
        self.y_coordinate = 0
        self.x_size = 1
        self.y_size = 1
        self.direction = "north" #exits are north,south,and dennis
        self.door_is_legal = 1
        self.printme = 1
        self.partnerdoor = 0
        self.monsterdata = ""

    def __str__(self):
        return "door("+ ", ".join([str(self.x_coordinate), str(self.y_coordinate), str(self.x_size), str(self.y_size)])+ ")"
    def set_size(self, x, y):
        self.x_size = x
        self.y_size = y
    
    def set_coordinates(self, x, y):
        self.x_coordinate = x
        self.y_coordinate = y

    def get_coordinates(self):
        return self.x_coordinate, self.y_coordinate

    def get_type(self):
        return self.feat_type

    def get_direction(self):
        return self.direction

    def set_direction(self, newdirection):
        self.direction = newdirection

    #def place_door(self, wallsize):
        #pass
    
    def are_you_in_this_square(self, (x, y)):
        tempx = self.x_coordinate        
        tempy = self.y_coordinate
        
        if (x == tempx and y == tempy):
            return True#the coordinate passed in is in the door's range
        else:
            return False
            
    #def is_door(self,x, y):#arguments: theoretical door x/y
        #pass
            
#=================================================
#-----          main program start
#=================================================

def make_a_dungeon(rooms, rating, dungeon):

#create static starting room
    entry = Room()
    entry.set_coordinates(5, 5)
    entry.set_size(3,5)
    entry.set_type("room")
    entry.add_room()
    entry.doors_finished = True
    #doors out of room
    door1_1 = Feature()
    door1_1.feat_type = "door"
    door1_1.set_direction("east")
    door1_1.set_coordinates(7,7)
    
    door1_2 = Feature()
    door1_2.feat_type = "door"
    door1_2.set_direction("south")
    door1_2.set_coordinates(6,9)
    
    door1_3 = Feature()
    door1_3.feat_type = "door"
    door1_3.set_direction("west")
    door1_3.set_coordinates(5,7)
    
    door1_4 = Feature()
    door1_4.feat_type = "door"
    door1_4.set_direction("north")
    door1_4.set_coordinates(6,5)
    
    entry.add_door(door1_1)
    entry.add_door(door1_2)
    entry.add_door(door1_3)
    entry.add_door(door1_4)
    
    #doors into next room
    door2_1 = Feature()
    door2_1.feat_type = "door"
    door2_1.set_direction("west")
    door2_1.set_coordinates(8,7)
    
    door2_2 = Feature()
    door2_2.feat_type = "door"
    door2_2.set_direction("north")
    door2_2.set_coordinates(6,10)
    
    door2_3 = Feature()
    door2_3.feat_type = "door"
    door2_3.set_direction("east")
    door2_3.set_coordinates(4,7)
    
    door2_4 = Feature()
    door2_4.feat_type = "door"
    door2_4.set_direction("south")
    door2_4.set_coordinates(6,4)
    
    dungeon.append(door2_1)#we don't add shadow doors
    dungeon.append(door2_2)
    dungeon.append(door2_3)
    dungeon.append(door2_4)
    
    for this_door in entry.doors:
        temp_room = Room()
        temp_loc_x = 0
        temp_loc_y = 0
        temp_size_x = 3
        temp_size_y = 3
        temp_type = "room"
        temp_door_facing = this_door.get_direction()
        
        if temp_door_facing == "north":
            temp_loc_x = this_door.x_coordinate - (temp_size_x/2)
            temp_loc_y = this_door.y_coordinate - temp_size_y
            
        if temp_door_facing == "south":
            temp_loc_x = this_door.x_coordinate - (temp_size_x/2)
            temp_loc_y = this_door.y_coordinate
            temp_loc_y = temp_loc_y + 1
            
        if temp_door_facing == "east":
            temp_loc_x = this_door.x_coordinate
            temp_loc_x = temp_loc_x + 1
            temp_loc_y = this_door.y_coordinate - (temp_size_y/2)
            
        if temp_door_facing == "west":
            temp_loc_x = this_door.x_coordinate - temp_size_x
            temp_loc_y = this_door.y_coordinate - (temp_size_y/2)
    
        temp_room.set_coordinates(temp_loc_x,temp_loc_y)
        temp_room.set_size(temp_size_x,temp_size_y)
    
        temp_room.room_type = temp_type
        temp_room.add_room()
         
#======================================================================
#------------------------       Main loop       -----------------------
#======================================================================
    while rooms_in_dungeon < rooms:
        ohdeargod = True

        ohdeargod, current_room = find_a_room(dungeon)
        if ohdeargod == False:
            #no rooms left to add doors to, and not enough rooms in dungeon
            break#this shouldn't happen
    
        #current_room is now set to the first room in the dungeon list without doors
        fill_a_room(current_room)
        
    #print "end of dungeon building loop, max rooms reached" #done with the whole thing.

#manually add stairs to the first room
    tempfeature = Feature()
    tempfeature.feat_type = "stairs"
    tempfeature.set_coordinates(6,7)
    dungeon.append(tempfeature)

#populate the dungeon with level appropriate encounters
    for each_room in dungeon:
        evil = 0
        monster = 0
        if each_room.room_type == "room":
            evil = random.randint(0,1)#50/50 chance of a monster in a room
            if evil == 1:
                tempfeature = Feature()
                tempfeature.feat_type = "monster"
                tempfeature.monsterdata = get_monster(rating)
                tempx, tempy = each_room.get_coordinates()
                tempfeature.set_coordinates(tempx + 1, tempy + 1)
                dungeon.append(tempfeature)
    
    return dungeon
#=======================================================================
#------------------------       Display loop    ------------------------
#=======================================================================
def generatedungeon(rooms, cr):
    global rooms_in_dungeon
    global dungeon
    rooms_in_dungeon = 0
    dungeon = []
    make_a_dungeon(int(rooms), int(cr), dungeon)

    draw_everything(tehcanvas, dungeon)
    
def draw_everything(acanvas,adungeon):
    acanvas.delete('all')
    tempxmin = 0
    tempymin = 0
    tempxmax = 19
    tempymax = 17
    
    for each_room in adungeon:
        if each_room.room_type == "room" or each_room.room_type == "hall":
            #print each_room.my_coordinates
            for each_pair in each_room.my_coordinates:
                tempx,tempy = each_pair
                if tempx < tempxmin:
                    tempxmin = tempx
                if tempx > tempxmax:
                    tempxmax = tempx
                if tempy < tempymin:
                    tempymin = tempy
                if tempy > tempymax:
                    tempymax = tempy
    #adjust canvas size to dungeon size with at least one square of padding    
    tempxmin -=1
    tempymin -=1
    tempxmax +=2
    tempymax +=2

    acanvas.config(scrollregion = (tempxmin * pixels_per_square, tempymin * pixels_per_square, tempxmax * pixels_per_square, tempymax * pixels_per_square))
    #move scrollbars to the middle-ish
    acanvas.xview_moveto(.3)
    acanvas.yview_moveto(.3)
    
    for each_room in adungeon:
        if each_room.room_type == "room" or each_room.room_type == "hall":
            point1x,point1y = each_room.get_coordinates()
            sizex,sizey = each_room.get_size()
            point2x = point1x + sizex
            point2y = point1y + sizey
            #change the size of each room to scale
            point1x *= pixels_per_square
            point1y *= pixels_per_square
            point2x *= pixels_per_square
            point2y *= pixels_per_square
            
            acanvas.create_rectangle(point1x, point1y, point2x, point2y, fill="gray50", outline="black", width = 5, )
    #--------------------------------------------------------------------------------------------------------
    for each_door in adungeon:
        if each_door.feat_type == "door":
            draw_door(acanvas,each_door)
    #--------------------------------------------------------------------------------------------------------
    #draw the grid
    for counterx in range(tempxmin,tempxmax):
        acanvas.create_line(counterx * pixels_per_square, tempymin * pixels_per_square, counterx * pixels_per_square, tempymax * pixels_per_square)
    
    for countery in range(tempymin,tempymax):
        acanvas.create_line(tempxmin * pixels_per_square, countery * pixels_per_square, tempxmax * pixels_per_square, countery * pixels_per_square)
    #draw the entry stairs
    for each_stairs in adungeon:
        if each_stairs.feat_type == "stairs":
            tempx, tempy = each_stairs.get_coordinates()
            acanvas.create_image(tempx * pixels_per_square, tempy * pixels_per_square, image = stairs1, anchor = NW)
    #draw all monster tokens
    for each_monster in adungeon:
        if each_monster.feat_type == "monster":
            tempx,tempy = each_monster.get_coordinates()
            monsterid = acanvas.create_image(tempx * pixels_per_square, tempy * pixels_per_square, image = monster1, anchor = NW)
            balloon.tagbind(acanvas, monsterid, each_monster.monsterdata)
        
        
class levelselect:#Generate button options selection box
    def __init__(self, parent, command):
        self.command = command
        self.parent = parent
    
    def prompt(self):
        top = self.top = Toplevel(self.parent)
        top.transient(self.parent)
        top.grab_set()
        #----------------------------------------------
        frame1 = Frame(top)
        frame1.pack(side = TOP, fill = Y, expand = TRUE)
        
        crlabel = Label(frame1, text = "Party Level")
        crlabel.pack(side = LEFT)
        self.level = Scale(frame1, orient = HORIZONTAL, from_ = 1, to = 20)
        self.level.pack(side=LEFT)
        #-----------------------------------------------
        frame2 = Frame(top)
        frame2.pack(side = TOP, fill = Y, expand = TRUE)
        
        roomslabel = Label(frame2, text = "Number of Rooms")
        roomslabel.pack(side = LEFT)
        self.totalrooms = Scale(frame2, orient = HORIZONTAL, from_=5, to=100)
        self.totalrooms.pack(side = LEFT)
        #-----------------------------------------------
        frame3 = Frame(top)
        frame3.pack(side = TOP, fill = Y, expand = TRUE)
        buttonok = Button(frame3, text="OK", command=self.ok)
        buttonok.pack(pady = 5, side = LEFT)
        buttoncancel = Button(frame3, text = "Cancel", command = self.cancel)
        buttoncancel.pack(padx = 5, side = LEFT)

    def ok(self):
        crlevel = self.level.get()
        numrooms = self.totalrooms.get()
        self.top.destroy()
        self.command(numrooms, crlevel)
    def cancel(self):
        self.top.destroy()
#about button: thanks to tkMessageBox
def aboutbox():
    tkMessageBox.showinfo("About","DungeonGenerator for Pathfinder, by Chris Pack. \n \n Enter your party level and the number of rooms in Generate. \n Hover over monster tokens for monster info. \n Special thanks to Alisa Pack, James Switzer, and Pasha Wrangell.")

top = Tk()
tehframe = Frame(top)
Pmw.initialise(top)
tehframe.pack(side = LEFT, fill = Y, expand = TRUE)
#save picture files to variables
stairs1 = PhotoImage(file = 'stairs1.gif')
monster1 = PhotoImage(file = 'monster1.gif')

settingsbox = levelselect(top, generatedungeon)
#show hover text on monsters, tooltips thanks to PythonMegaWidgets
balloon = Pmw.Balloon(top)

generatebutton = Button(tehframe, text="Generate", command = settingsbox.prompt)
generatebutton.pack(side = TOP)

aboutbutton = Button(tehframe, text = "About", command = aboutbox)
aboutbutton.pack(side = TOP, fill = X, pady = 3)

quitbutton = Button(tehframe, text = "Quit", command = quit)
quitbutton.pack(side = TOP, fill = X)

mapscrollx = Scrollbar(top, orient = HORIZONTAL)
mapscrollx.pack(side = BOTTOM, fill = X)
mapscrolly = Scrollbar(top, orient = VERTICAL)
mapscrolly.pack(side = RIGHT, fill = Y)

tehcanvas = Canvas(top, bg="gray30", height = 800, width = 800, xscrollcommand = mapscrollx.set, yscrollcommand = mapscrolly.set, scrollregion = (-2000,-2000,3000,3000))
mapscrollx.config(command = tehcanvas.xview)
mapscrolly.config(command = tehcanvas.yview)
draw_everything(tehcanvas,dungeon)

tehcanvas.pack()
top.mainloop()
