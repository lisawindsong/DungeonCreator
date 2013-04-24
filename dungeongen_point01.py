#Dungeon Generator v0.01
# Chris Pack
#=====================================================

dungeon = []
rooms_in_dungeon = 0#so now I can add x rooms to a dungeon and then know to stop
rooms_to_add = 10
#current_room = 0

def find_a_room(dungeon_list):
    for room in dungeon_list:
        if room.room_type == "room":
            if room.doors_finished == False:
                print "room ", room, " needs connected doors"
                room.doors_finished = True
                return True, room
            else:
                print "room ", room, " is done."
    print "No unfinished rooms in dungeon"
    return False, room
            
def fill_a_room(empty_room):
    #global dungeon
    random_number = 3#guaranteed by fair die roll to be random    #   number of doors to add
    roomx,roomy = empty_room.get_coordinates()
    roomwide,roomtall = empty_room.get_size()
    print "number of doors in empty room:", len(empty_room.doors)
    print "empty room is", empty_room
    print "number of doors it thinks it has:", empty_room.num_of_doors
    
    #two parts:
    #part 1: insert number of doors into room
    #
    #for (counter = 0 counter < random_number counter++)
    for doors_to_add in range (0, random_number):
        print "door creation iteration ", doors_to_add
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
                templocx = roomx + roomwide
                templocy = roomy + roomtall/2
                tempfacing2 = "west"
                templocx2 = templocx + 1
                templocy2 = templocy
            
            if tempfacing == "south":
                #print "Pretend I did something south"
                templocx = roomx + roomwide/2
                templocy = roomy + roomtall
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
                dungeon.append(tempdoorout)
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
            print "tried all the times and couldn't place another door"
            #return
    #
    print "doors added to current room", empty_room.num_of_doors
    #part 2: insert room on the end of each door
    #
    if empty_room.num_of_doors == 0:
        print "no doors in this room"
        
    #for this_door in range (0, empty_room.num_of_doors):
    for this_door in empty_room.doors:
        print "room creation iteration", len(empty_room.doors)
        temp_room = Room()
        temp_loc_x = 0
        temp_loc_y = 0
        #create random size
        #actually make these random later
        temp_size_x = 10
        temp_size_y = 10
        temp_type = "room"
        temp_door_facing = this_door.get_direction()
        
        if temp_door_facing == "north":
            temp_loc_x = this_door.x_coordinate - (temp_size_x/2)
            temp_loc_y = this_door.y_coordinate - temp_size_y
            temp_loc_y = temp_loc_y - 1
        
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
            temp_loc_x = temp_loc_x - 1
            temp_loc_y = this_door.y_coordinate - (temp_size_y/2)
        
        #new room location x and Y now determined, now look for conflicts.
        temp_room.set_coordinates(temp_loc_x, temp_loc_y)
        temp_room.set_size(temp_size_x,temp_size_y)
        temp_room.set_type(temp_type)
        temp_room.get_my_coordinates_list()
        #====================================================================
        for each_room in dungeon:
            if each_room.room_type == "room":
                for room_coordinates in range (0, len(each_room.my_coordinates)):
                    if temp_room.are_you_in_this_square(each_room.my_coordinates[room_coordinates]):
                        temp_room.room_is_legal = 0
        #====================================================================
        if temp_room.room_is_legal == 1:
            temp_room.add_room()#win            
            print "this room is legal"
            #stilltrying = False
        else:
            print "this room overlaps another"
            #sidestried +=1
        temp_room.room_is_legal = 1
        print "added or did not add room"
        #===========================================================

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
        
    def set_type(self, type):
        self.room_type = type

    def get_coordinates(self):
        return self.x_coordinate, self.y_coordinate

    def get_size(self):
        return self.x_size, self.y_size
    
    def are_you_in_this_square(self, (x, y)):
        tempxsize = self.x_size
        tempxstart = self.x_coordinate
        tempxfinish = tempxstart + tempxsize
        
        tempysize = self.y_size
        tempystart = self.y_coordinate
        tempyfinish = tempystart + tempysize
        
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
        print len(dungeon)
        global rooms_in_dungeon
        rooms_in_dungeon += 1
        self.get_my_coordinates_list()
        #print "added a room to the dungeon."
        print "current number of rooms in dungeon: " , rooms_in_dungeon
        
class Feature:
    #feat_type: door, trap, treasure
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
    
    def set_room(Room):
        #pass
        my_room = Room #this should be correct
    
    def are_you_in_this_square(self, (x, y)):
        tempx = self.x_coordinate        
        tempy = self.y_coordinate
        
        if (x == tempx and y == tempy):
            #print "in the door's range"
            return True#the coordinate passed in is in the door's range
        else:
            #print "not in the room's range"
            return False
            
    def is_door(x, y):#arguments: theoretical door x/y
        pass
        #for sizeof(my_room.doors)#my_room.doors[]?
            #if(my_room.doors[x]
            # for each item in the list "my_room.doors"
            #   look at the x/y coordinate.  if the x/y coordinate = the x/y coordinate passed in
            #       return true
            #   else
            #       return false

#------------------------------
#-----          main program start
#------------------------------
entry = Room()
entry.set_coordinates(20, 20)
entry.set_size(10,20)
entry.set_type("room")
entry.add_room() # is this silly?
entry.doors_finished = True
#doors out of room
door1_1 = Feature()
door1_1.feat_type = "door"
door1_1.set_direction("east")
door1_1.set_coordinates(29,30)

door1_2 = Feature()
door1_2.feat_type = "door"
door1_2.set_direction("south")
door1_2.set_coordinates(25,39)

door1_3 = Feature()
door1_3.feat_type = "door"
door1_3.set_direction("west")
door1_3.set_coordinates(20,30)

door1_4 = Feature()
door1_4.feat_type = "door"
door1_4.set_direction("north")
door1_4.set_coordinates(25,20)

entry.add_door(door1_1)
entry.add_door(door1_2)
entry.add_door(door1_3)
entry.add_door(door1_4)

#doors into next room
door2_1 = Feature()
door2_1.feat_type = "door"
door2_1.set_direction("west")
door2_1.set_coordinates(30,30)

door2_2 = Feature()
door2_2.feat_type = "door"
door2_2.set_direction("north")
door2_2.set_coordinates(25,40)

door2_3 = Feature()
door2_3.feat_type = "door"
door2_3.set_direction("east")
door2_3.set_coordinates(19,30)

door2_4 = Feature()
door2_4.feat_type = "door"
door2_4.set_direction("south")
door2_4.set_coordinates(25,19)
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
    temp_size_x = 10
    temp_size_y = 10
    temp_type = "room"
    temp_door_facing = this_door.get_direction()
    
    if temp_door_facing == "north":
        temp_loc_x = this_door.x_coordinate - (temp_size_x/2)
        temp_loc_y = this_door.y_coordinate - temp_size_y
        temp_loc_y = temp_loc_y - 1
        
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
        temp_loc_x = temp_loc_x - 1
        temp_loc_y = this_door.y_coordinate - (temp_size_y/2)

    temp_room.set_coordinates(temp_loc_x,temp_loc_y)
    temp_room.set_size(temp_size_x,temp_size_y)

    print temp_room.get_coordinates()
    temp_room.room_type = temp_type
    temp_room.add_room()
    print "there are", len(temp_room.doors), "doors in this room"
    

#for each_room in dungeon:
#    if each_room.room_type == "room":
#        print "these are my coordinates:"
#        print each_room.my_coordinates
#        print "those were my coordinates"            

#======================================================================
#------------------------       Main loop       -----------------------
#======================================================================
while rooms_in_dungeon < rooms_to_add:
    #global current_room #FIXME make sure this doesn't mask anything
    #temp_room = Room()
    #make new random room size
    #room coordinates will be based off of corresponding door
    #temp_room.set_coordinates(10,10)
    #temp_room.set_size(10,10)
    #temp_room.set_type("room")
    ohdeargod = True

#I need the "look through teh whole dungeon array and see if any object is in this location" function
    
    ohdeargod, current_room = find_a_room(dungeon)
    if ohdeargod == False:
        print "everything is ruined forever"
        break#this shouldn't happen, and right now if it happens I'm screwed

    #current_room should now be set to the first room without any doors
    #==========================
    #----  THIS IS WHERE I AM: working on filling a given room with doors and more rooms?
    #==========================
    fill_a_room(current_room)
    
    #check that this room does not overlap any other rooms
    #for each_room in dungeon:
    #    if each_room.room_type == "room":
    #        for room_coordinates in range (0, len(each_room.my_coordinates)):
    #            if temp_room.are_you_in_this_square(each_room.my_coordinates[room_coordinates]):
    #                temp_room.room_is_legal = 0
    #                #here I downgrade the room type and try another
    #if temp_room.room_is_legal == 1:
    #    print "this room is legal"
    #else:
    #    print "this room overlaps another"
    #temp_room.add_room()
    #end if
    #current_room = temp_room#the room is legal and added to teh list

    
print "end of dungeon building loop, max rooms reached" #done with the whole thing.
    #unhandled case: dungeon didn't build enough   rooms to hit cap?  what then?
#if (find_a_room(first_room) == True):
    #print "#fill this room with doors and rooms"
#else:
    #"#(next)"

#import tkinter
#main window
#canvas
#loop through dungeon loop, and draw all things
#canvas has methods to draw things.
#tk image class to import pictures?
#draw line, draw thing
#main loop: hands control of program to TK ui
#part of teh tk library
#   here "callback" performs functions like things...just make the thing drawing.
