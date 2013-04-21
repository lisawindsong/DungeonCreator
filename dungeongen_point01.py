#Dungeon Generator v0.01
# Chris Pack
#=====================================================

dungeon = []
rooms_in_dungeon = 0#so now I can add x rooms to a dungeon and then know to stop
rooms_to_add = 10
current_room = 0

def find_a_room(dungeon_list):#probably not declared correctly
    for room in dungeon_list:
        if room.room_type == "room":
            if room.doors_finished == False:
                print "room ", room, " needs connected doors"
                room.doors_finished == True
                return True, room#if can't return a null room, set 'room' to the global 'current_room'
            else:
                print "room ", room, " is done."
    print "No unfinished rooms in dungeon"
    return False,current_room
            
def fill_a_room(empty_room):
    random_number = 4#guaranteed by fair die roll to be random
    #   number of doors to add
    #two parts: part 1: insert number of doors into room
    #
    #for (counter = 0 counter < random_number counter++
    for empty_room in range (0, random_number):
        print "door creation iteration ", range
        tempdoor = Feature()
        temploc = 1,1
        tempfacing = East
        #if there is no door in locxy place door
        #if there is a door in xy, move to next wall
        print "Pretend I did something cool"
        #new room at that door
        #empty_room.num_of_doors+=1
    #
    #part 2: insert room on the end of each door
    #
    for this_door in range (0, door.num_of_doors):
        temp_room = Room()
        temp_loc_x = 0
        temp_loc_y = 0
        #create random size
        #actually make these random later
        temp_size_x = 10
        temp_size_y = 10
        temp_type = "room"
        temp_door_facing = this_door.getfacing()
        
        if temp_door_facing == "east":
            temp_loc_x = this_door.x_coordinate - (temp_size_x/2)
            temp_loc_y = this_door.y_coordinate - temp_size_y
        
        if temp_door_facing == "south":
            temp_loc_x = this_door.x_coordinate - (temp_size_x/2)
            temp_loc_y = this_door.y_coordinate
        
        if temp_door_facing == "east":
            temp_loc_x = this_door.x_coordinate
            temp_loc_y = this_door.y_coordinate - (temp_size_y/2)
        
        if temp_door_facing == "west":
            temp_loc_x = this_door.x_coordinate - temp_size_x
            temp_loc_y = this_door.y_coordinate - (temp_size_y/2)
        
        #new room location x and Y now determined, now look for conflicts.
        for first_room in dungeon:#incomplete
            if(first_room.are_you_in_this_square(x,y) == True):
                print "there is already a room in this square, go to hell"
                #I need a new square
                break
            #if(nobody was true):
                print "I totally added teh room"
                temp_room.add_room()#win

#need a function in Room() to return a list with all of it's squares x/y

class Room:
    #room_type: room, hall, stairs? grand hall? chamber?
    room_type = 0
    x_coordinate = 0
    y_coordinate = 0
    x_size = 0
    y_size = 0
    door1 = 0#this will be changed
    num_of_doors = 0
    doors = []
    doors_finished = False
    my_coordinates = []
    room_is_legal = 1

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
        
    def these_are_my_squares(self):
        pass
        #I think I need a function here that can return a list that has in it the x/y coordinate pair
        #of every square in that room.  maybe a start/finish that I can extrapolate out?  would be smaller.
        #
    
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
        self.doors.append(door)
        self.num_of_doors = len(self.doors)

    def get_doors(self):
        return self.num_of_doors
        
    def add_room(self):
        dungeon.append(self)
        global rooms_in_dungeon
        rooms_in_dungeon += 1
        self.get_my_coordinates_list()
        #print "added a room to the dungeon."
        print "current number of rooms in dungeon: " , rooms_in_dungeon
        
class Feature:
    #feat_type: door, trap, treasure
    my_room = 0
    feat_type = 0
    x_coordinate = 0
    y_coordinate = 0
    x_size = 1
    y_size = 1
    direction = "north" #exits are north,south,and dennis

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
entry.set_coordinates(23, 17)
entry.set_size(10,20)
entry.set_type("room")
entry.add_room() # is this silly?
#entry.get_my_coordinates_list()  added to add_room
#print entry.my_coordinates

#I need the "look through teh whole dungeon array and see if any object is in this location" function
#for each_room in dungeon:
#    if each_room.room_type == "room":
#    #if room_type == "room":
#        print "I found a room in ", each_room
#======================================================================
#------------------------       Main loop       -----------------------
#======================================================================
while rooms_in_dungeon < rooms_to_add:
    global current_room #FIXME make sure this doesn't mask anything
    temp_room = Room()
    #temp_door = Feature()
    #make new random room size
    #room coordinates will be based off of corresponding door
    temp_room.set_coordinates(10,10)
    temp_room.set_size(10,10)
    temp_room.set_type("room")
    #check that this room does not overlap any other rooms
    for each_room in dungeon:
        if each_room.room_type == "room":
            for room_coordinates in range (0, len(each_room.my_coordinates)):
                if temp_room.are_you_in_this_square(each_room.my_coordinates[room_coordinates]):
                    temp_room.room_is_legal = 0
                    #here I downgrade the room type and try another
    if temp_room.room_is_legal == 1:
        print "this room is legal"
    else:
        print "this room overlaps another"
    temp_room.add_room()
    #end if
    current_room = temp_room#the room is legal and added to teh list
    
#I need the "look through teh whole dungeon array and see if any object is in this location" function
    for first_room in dungeon:
        if first_room.room_type == "room":
            if first_room.doors_finished == False:
                print "room ", first_room, " needs connected doors"
                first_room.doors_finished = True
                #here: fill this room with doors
            else:
                pass
                #print "this room is finished" this statement works
        else:
            print "this is not a 'room'"

    print "done with this room" #I don't think this is done with the dungeon at this point
print "end of dungeon building loop, max rooms reached" #done with the whole thing.
    #unhandled case: dungeon didn't build enough   rooms to hit cap?  what then?
#if (find_a_room(first_room) == True):
    #print "#fill this room with doors and rooms"
#else:
    #"#(next)"
