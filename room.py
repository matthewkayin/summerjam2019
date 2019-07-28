import random


class Room:
    def __init__(self, file_name, x_cord, y_cord, top, bottom, right, left):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.minnows = []
        self.tiles = []
        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left

        data = []

        map_file = open("Rooms/" + file_name + ".txt", "r")
        for line in map_file.read().splitlines():
            data.append(list(map(int, line.split(" "))))

        for x in range(0, len(data[0])):
            self.tiles.append([])
            for y in range(0, len(data)):
                self.tiles[x].append(data[y][x])

        # for x in range(0, len(self.tiles)):
        #     for y in range(0, len(self.tiles[0])):
        #         if self.tiles[x][y] == 2:
        #             self.minnows.append([x, y])

        num_minnos = 1
        for i in range(0, num_minnos):
            placed = False
            while not placed:
                minno_x = random.randint(0, len(self.tiles) - 1)
                minno_y = random.randint(0, len(self.tiles[0]) - 1)
                if self.tiles[minno_x][minno_y] == 0:
                    self.tiles[minno_x][minno_y] = 2
                    self.minnows.append([minno_x, minno_y])
                    placed = True

        if self.top:
            self.top_used()
        if self.bottom:
            self.bottom_used()
        if self.left:
            self.left_used()
        if self.right:
            self.right_used()

    def close_entrances(self):
        for x in range(0, len(self.tiles)):
            for y in range(0, len(self.tiles[0])):
                if self.tiles[x][y] > 5:
                    self.tiles[x][y] = 1

    def top_used(self):
        for x in range(0, len(self.tiles)):
            for y in range(0, len(self.tiles[0])):
                if self.tiles[x][y] == 9:
                    self.tiles[x][y] = 0

    def right_used(self):
        for x in range(0, len(self.tiles)):
            for y in range(0, len(self.tiles[0])):
                if self.tiles[x][y] == 8:
                    self.tiles[x][y] = 0

    def bottom_used(self):
        for x in range(0, len(self.tiles)):
            for y in range(0, len(self.tiles[0])):
                if self.tiles[x][y] == 7:
                    self.tiles[x][y] = 0

    def left_used(self):
        for x in range(0, len(self.tiles)):
            for y in range(0, len(self.tiles[0])):
                if self.tiles[x][y] == 6:
                    self.tiles[x][y] = 0


class MapMaker:
    def __init__(self, x_cord, y_cord, max_rooms):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.max_rooms = max_rooms
        self.possible_rooms = ["tbrl_A", "tbrl_B", "tbrl_pillars", "tbrl_C"]
        self.rooms = []
        curr_x = x_cord
        curr_y = y_cord
        starting_room = Room("tbrl_empty", curr_x, curr_y, False, False, False, False)
        self.rooms.append(starting_room)
        for x in range(0, self.max_rooms):
            dir_set = False
            while not dir_set:
                direction = random.randint(0, 3)
                if direction == 0:
                    if not self.rooms[x].top:
                        curr_y -= 720
                        self.rooms[x].top_used()
                        map = random.randint(0, len(self.possible_rooms) - 1)
                        new_room = Room(self.possible_rooms[map], curr_x, curr_y, False, True, False, False)
                        self.rooms.append(new_room)
                        dir_set = True
                elif direction == 1:
                    if not self.rooms[x].right:
                        curr_x += 1280
                        self.rooms[x].right_used()
                        map = random.randint(0, len(self.possible_rooms) - 1)
                        new_room = Room(self.possible_rooms[map], curr_x, curr_y, False, False, False, True)
                        self.rooms.append(new_room)
                        dir_set = True
                elif direction == 2:
                    if not self.rooms[x].bottom:
                        curr_y += 720
                        self.rooms[x].bottom_used()
                        map = random.randint(0, len(self.possible_rooms) - 1)
                        new_room = Room(self.possible_rooms[map], curr_x, curr_y, True, False, False, False)
                        self.rooms.append(new_room)
                        dir_set = True
                else:
                    if not self.rooms[x].left:
                        curr_x -= 1280
                        self.rooms[x].left_used()
                        map = random.randint(0, len(self.possible_rooms) - 1)
                        new_room = Room(self.possible_rooms[map], curr_x, curr_y, False, False, True, False)
                        self.rooms.append(new_room)
                        dir_set = True
        for x in range(0, len(self.rooms) - 1):
            self.rooms[x].close_entrances()
