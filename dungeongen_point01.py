#Dungeon Generator v0.02
# Chris Pack
#=====================================================
from Tkinter import *
import random
import tkMessageBox
import Pmw

dungeon = []
rooms_in_dungeon = 0#so now I can add x rooms to a dungeon and then know to stop
#rooms_to_add = 25
pixels_per_square = 48
#current_room = 0

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
            print "You cannot face Dennis!"
        
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
                #print "room ", room, " needs connected doors"
                room.doors_finished = True
                return True, room
            else:
                pass
                #print "room ", room, " is done."
    #print "No unfinished rooms in dungeon"
    return False, room
            
def fill_a_room(empty_room):
    #global dungeon
    random_number = 3#guaranteed by fair die roll to be random    #   number of doors to add
    roomx,roomy = empty_room.get_coordinates()
    roomwide,roomtall = empty_room.get_size()
    #print "number of doors in empty room:", len(empty_room.doors)
    #print "empty room is", empty_room
    #print "number of doors it thinks it has:", empty_room.num_of_doors
    
    #two parts:
    #====================================================
    #Fill-a-Room part 1: insert number of doors into room
    #====================================================

    #for (counter = 0 counter < random_number counter++)
    for doors_to_add in range (0, random_number):
        #print "door creation iteration ", doors_to_add
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
                #print "Pretend I did something east"
                #templocx = empty_room.x_coordinate + empty_room.x_size
                templocx = roomx + roomwide -1
                templocy = roomy + roomtall/2
                tempfacing2 = "west"
                templocx2 = templocx + 1
                templocy2 = templocy
            
            if tempfacing == "south":
                #print "Pretend I did something south"
                templocx = roomx + roomwide/2
                templocy = roomy + roomtall - 1
                tempfacing2 = "north"
                templocx2 = templocx
                templocy2 = templocy + 1
            
            if tempfacing == "west":
                #print "Pretend I did something west"
                templocx = roomx
                templocy = roomy + roomtall/2
                tempfacing2 = "east"
                templocx2 = templocx - 1
                templocy2 = templocy
            
            if tempfacing == "north":
                #print "Pretend I did something north"
                templocx = roomx + roomwide/2
                templocy = roomy
                tempfacing2 = "south"
                templocx2 = templocx
                templocy2 = templocy - 1
            
            #am I creating doors that will overlap other rooms in the future?
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
                #dungeon.append(tempdoorin)
                empty_room.add_door(tempdoorin)#create door
                tempdoorout.set_coordinates(templocx2,templocy2)
                tempdoorout.set_direction(tempfacing2)
                #tempdoorout.add_door()#create partner door don't want this associated with teh room
                tempdoorout.feat_type = temptype
                #tempdoorout.printme = 0
                dungeon.append(tempdoorout)
                tempdoorin.partnerdoor = tempdoorout
                tempdoorout.partnerdoor = tempdoorin
                stilltrying = False
            else:
                #print "this door overlaps another"
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
            #
        if sidestried >3:#  sidestried==4
            pass
            #print "tried all the times and couldn't place another door"
            #return
    #
    #print "doors added to current room", empty_room.num_of_doors
    #====================================================
    #Fill-a-Room part 2: insert rooms onto doors
    #====================================================
    if empty_room.num_of_doors == 0:
        pass
        #print "no doors in this room"
        #ERROR this should never happen
        
    #for this_door in range (0, empty_room.num_of_doors):
    for this_door in empty_room.doors:
        #print "room creation iteration", len(empty_room.doors)
        temp_room = Room()
        temp_loc_x = 0
        temp_loc_y = 0
        #create random size
        #actually make these random later
        temp_size_x = 3
        temp_size_y = 3
        temp_type = "room"
        temp_door_facing = this_door.get_direction()
        #temp_size_x, temp_size_y = create_a_room()
        randkey = 0
        
        randkey = random.randint(1,10)
        #print randkey
        while randkey > 0:
            temp_size_x, temp_size_y = create_a_room(randkey)
            #print temp_size_x, temp_size_y
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
                #pass
                this_door.printme = 0
                this_door.partnerdoor.printme = 0
                #print "this room overlaps another"
                #flag this door DO NOT PRINT
                #sidestried +=1
            temp_room.room_is_legal = 1
            #print "added or did not add room"
            #===========================================================
            randkey -= 1
        
def get_monster(cr):
    print "hand monster"
    crmin = cr - 1
    crmax = cr + 1
    temprand = random.randint(crmin, crmax)
    
    if temprand == 0:
        return "Level 0 monster"
    elif temprand == 1:
        return "Level 1 monster"
    elif temprand == 2:
        return "Level 2 monster"
    elif temprand == 3:
        return "Level 3 monster"
    elif temprand == 4:
        return "Level 4 monster"
    elif temprand == 5:
        return "Level 5 monster"
    elif temprand == 6:
        return "Level 6 monster"
    elif temprand == 7:
        return "Level 7 monster"
    elif temprand == 8:
        return "Level 8 monster"
    elif temprand == 9:
        return "Level 9 monster"
    elif temprand == 10:
        return "Level 10 monster"
    elif temprand == 11:
        return "Level 11 monster"
    elif temprand == 12:
        return "Level 12 monster"
    elif temprand == 13:
        return "Level 13 monster"
    elif temprand == 14:
        return "Level 14 monster"
    elif temprand == 15:
        return "Level 15 monster"
    elif temprand == 16:
        return "Level 16 monster"
    elif temprand == 17:
        return "Level 17 monster"
    elif temprand == 18:
        return "Level 18 monster"
    elif temprand == 19:
        return "Level 19 monster"
    elif temprand == 20:
        return "Level 20 monster"
    elif temprand == 21:
        return "Boss monster"
    else:
        return "grue"
    
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
                #print "height = ", height
                tempx = width + self.x_coordinate
                tempy = height + self.y_coordinate
                #print "coordinates are ", tempx, tempy
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
            #print "in the room's range"
            return True#the coordinate passed in is in the room's range
        else:
            #print "not in the room's range"
            return False

    def add_door(self,door):
        dungeon.append(door)
        self.doors.append(door)
        self.num_of_doors = len(self.doors)

    def get_doors(self):
        return self.num_of_doors
        
    def add_room(self):
        dungeon.append(self)
        #print len(dungeon)
        global rooms_in_dungeon
        if self.room_type == "room":#only count "rooms" for the purpose of dungeon size. halls are boring.
            rooms_in_dungeon += 1
        self.get_my_coordinates_list()
        #print "added a room to the dungeon."
        #print "current number of rooms in dungeon: " , rooms_in_dungeon
        
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

    def place_door(self, wallsize):
        pass
        #
        #check to see if this place has a door in it
        #
        #dungeon.append(self)
        # can I call add_door here, to the room it is in?  I'd like to
        #my_room.add_door(self)#something like this?
    
    #def set_room(self,Room):
        #pass
        #my_room = Room #this should be correct
    
    def are_you_in_this_square(self, (x, y)):
        tempx = self.x_coordinate        
        tempy = self.y_coordinate
        
        if (x == tempx and y == tempy):
            #print "in the door's range"
            return True#the coordinate passed in is in the door's range
        else:
            #print "not in the room's range"
            return False
            
    def is_door(self,x, y):#arguments: theoretical door x/y
        pass
        #for sizeof(my_room.doors)#my_room.doors[]?
            #if(my_room.doors[x]
            # for each item in the list "my_room.doors"
            #   look at the x/y coordinate.  if the x/y coordinate = the x/y coordinate passed in
            #       return true
            #   else
            #       return false
            
#=================================================
#-----          main program start
#=================================================

def make_a_dungeon(rooms, rating, dungeon):

    entry = Room()
    entry.set_coordinates(5, 5)
    entry.set_size(3,5)
    entry.set_type("room")
    entry.add_room() # is this silly?
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
    #entry.get_my_coordinates_list()  added to add_room
    #print entry.my_coordinates
    dungeon.append(door2_1)
    dungeon.append(door2_2)
    dungeon.append(door2_3)
    dungeon.append(door2_4)
    
    for this_door in entry.doors:
        temp_room = Room()
        temp_loc_x = 0
        temp_loc_y = 0
        #create random size
        #actually make these random later
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
    
        #print temp_room.get_coordinates()
        temp_room.room_type = temp_type
        temp_room.add_room()
        #print "there are", len(temp_room.doors), "doors in this room"
    #for each_room in dungeon:
    #    if each_room.room_type == "room":
    #        print "these are my coordinates:"
    #        print each_room.my_coordinates
    #        print "those were my coordinates"            
#======================================================================
#------------------------       Main loop       -----------------------
#======================================================================
    while rooms_in_dungeon < rooms:#rooms_to_add:#rooms:
        ohdeargod = True

        ohdeargod, current_room = find_a_room(dungeon)
        if ohdeargod == False:
            #print "everything is ruined forever"
            break#this shouldn't happen, and right now if it happens I'm screwed
    
        #current_room should now be set to the first room without any doors
    
        fill_a_room(current_room)
        
    print "end of dungeon building loop, max rooms reached" #done with the whole thing.
        #unhandled case: dungeon didn't build enough   rooms to hit cap?  what then?
    #if (find_a_room(first_room) == True):
        #print "#fill this room with doors and rooms"
    #else:
        #"#(next)"
    tempfeature = Feature()
    tempfeature.feat_type = "stairs"
    tempfeature.set_coordinates(6,7)
    dungeon.append(tempfeature)

    #insert code to put monsters in rooms here
    for each_room in dungeon:
        evil = 0
        monster = 0
        if each_room.room_type == "room":
            evil = random.randint(0,1)
            if evil == 1:
                #monster = get_monster(rating)
                tempfeature = Feature()
                tempfeature.feat_type = "monster"
                tempfeature.monsterdata = get_monster(rating)
                tempx, tempy = each_room.get_coordinates()
                #print tempx, tempy
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
    #for all in dungeon:
    #    print all
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
                    
    #print tempxmin, tempymin, tempxmax, tempymax
    tempxmin -=1
    tempymin -=1
    tempxmax +=2
    tempymax +=2
    #print tempxmin, tempymin, tempxmax, tempymax
    acanvas.config(scrollregion = (tempxmin * pixels_per_square, tempymin * pixels_per_square, tempxmax * pixels_per_square, tempymax * pixels_per_square))
                #print tempx, tempy
    
    acanvas.xview_moveto(.3)
    acanvas.yview_moveto(.3)
    
    for each_room in adungeon:
        if each_room.room_type == "room" or each_room.room_type == "hall":
            point1x,point1y = each_room.get_coordinates()
            sizex,sizey = each_room.get_size()
            point2x = point1x + sizex
            point2y = point1y + sizey
            #size of each room to scale
            point1x *= pixels_per_square
            point1y *= pixels_per_square
            point2x *= pixels_per_square
            point2y *= pixels_per_square
            
            acanvas.create_rectangle(point1x, point1y, point2x, point2y, fill="gray50", outline="black", width = 5, )
    #--------------------------------------------------------------------------------------------------------
    for each_door in adungeon:
        if each_door.feat_type == "door":
            draw_door(acanvas,each_door)
            #print "door", each_room
            #print each_room.get_coordinates()s
    #--------------------------------------------------------------------------------------------------------
    for counterx in range(tempxmin,tempxmax):
        acanvas.create_line(counterx * pixels_per_square, tempymin * pixels_per_square, counterx * pixels_per_square, tempymax * pixels_per_square)
    
    for countery in range(tempymin,tempymax):
        acanvas.create_line(tempxmin * pixels_per_square, countery * pixels_per_square, tempxmax * pixels_per_square, countery * pixels_per_square)
    
    for each_stairs in adungeon:
        if each_stairs.feat_type == "stairs":
            tempx, tempy = each_stairs.get_coordinates()
            acanvas.create_image(tempx * pixels_per_square, tempy * pixels_per_square, image = stairs1, anchor = NW)
            
    for each_monster in adungeon:
        if each_monster.feat_type == "monster":
            tempx,tempy = each_monster.get_coordinates()
            monsterid = acanvas.create_image(tempx * pixels_per_square, tempy * pixels_per_square, image = monster1, anchor = NW)
            balloon.tagbind(acanvas, monsterid, each_monster.monsterdata)
        
        
class levelselect:
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

def aboutbox():
    tkMessageBox.showinfo("About","DungeonGenerator for Pathfinder, by Chris Pack. \n \n Enter your party level and the number of rooms in Generate.")

top = Tk()
tehframe = Frame(top)
Pmw.initialise(top)
tehframe.pack(side = LEFT, fill = Y, expand = TRUE)

stairs1 = PhotoImage(file = 'stairs1.gif')
monster1 = PhotoImage(file = 'monster1.gif')

settingsbox = levelselect(top, generatedungeon)

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
