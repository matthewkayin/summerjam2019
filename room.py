import random


class Room:
    def __init__(self, file_name, x_cord, y_cord, top, bottom, right, left, include_eel):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.minnows = []
        self.eels = []
        self.finish = []
        self.tiles = []
        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left
        self.include_eel = include_eel

        data = []
        map_file = open("Rooms/" + file_name + ".txt", "r")
        for line in map_file.read().splitlines():
            data.append(list(map(int, line.split(" "))))

        for x in range(0, len(data[0])):
            self.tiles.append([])
            for y in range(0, len(data)):
                self.tiles[x].append(data[y][x])

        num_minnos = 1
        for i in range(0, num_minnos):
            placed = False
            while not placed:
                minno_x = random.randint(0, len(self.tiles) - 1)
                minno_y = random.randint(0, len(self.tiles[0]) - 1)
                if self.tiles[minno_x][minno_y] == 0:
                    self.minnows.append([minno_x, minno_y])
                    placed = True

        if self.include_eel:
            x = int(len(self.tiles) / 2)
            center = self.x_cord + (x * 20)
            self.eels.append([[center, center], [self.y_cord + 320, self.y_cord + 400], [0, 1]])

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

    def generate_end(self):
        placed = False
        while not placed:
            x = random.randint(0, len(self.tiles) - 1)
            y = random.randint(0, len(self.tiles[0]) - 1)
            if self.tiles[x][y] == 0:
                self.finish.append([x, y])
                placed = True


class MapMaker:
    def __init__(self, x_cord, y_cord, max_rooms):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.max_rooms = max_rooms
        self.possible_rooms = ["tbrl_A", "tbrl_B", "tbrl_pillars", "tbrl_C"]
        self.rooms = []
        curr_x = x_cord
        curr_y = y_cord
        room_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        starting_room = Room("tbrl_empty", curr_x, curr_y, False, False, False, False, False)
        self.rooms.append(starting_room)
        x_grid = random.randint(0, len(room_grid) - 1)
        y_grid = random.randint(0, len(room_grid) - 1)
        room_grid[x_grid][y_grid] = 1
        for x in range(0, self.max_rooms):
            dir_set = False
            # top right bot left
            possible_direction = [True, True, True, True]
            if y_grid == 0 or room_grid[x_grid][y_grid - 1] == 1:
                possible_direction[0] = False
            if x_grid == 9 or room_grid[x_grid + 1][y_grid] == 1:
                possible_direction[1] = False
            if y_grid == 9 or room_grid[x_grid][y_grid + 1] == 1:
                possible_direction[2] = False
            if x_grid == 0 or room_grid[x_grid - 1][y_grid] == 1:
                possible_direction[3] = False
            if not (possible_direction[0] or possible_direction[1] or possible_direction[2] or possible_direction[3]):
                dir_set = True
            while not dir_set:
                direction = random.randint(0, 3)
                if direction == 0 and possible_direction[0]:
                    if not self.rooms[x].top:
                        curr_y -= 720
                        self.rooms[x].top_used()
                        map = random.randint(0, len(self.possible_rooms) - 1)
                        new_room = Room(self.possible_rooms[map], curr_x, curr_y, False, True, False, False, True)
                        self.rooms.append(new_room)
                        dir_set = True
                elif direction == 1 and possible_direction[1]:
                    if not self.rooms[x].right:
                        curr_x += 1280
                        self.rooms[x].right_used()
                        map = random.randint(0, len(self.possible_rooms) - 1)
                        new_room = Room(self.possible_rooms[map], curr_x, curr_y, False, False, False, True, True)
                        self.rooms.append(new_room)
                        dir_set = True
                elif direction == 2 and possible_direction[2]:
                    if not self.rooms[x].bottom:
                        curr_y += 720
                        self.rooms[x].bottom_used()
                        map = random.randint(0, len(self.possible_rooms) - 1)
                        new_room = Room(self.possible_rooms[map], curr_x, curr_y, True, False, False, False, True)
                        self.rooms.append(new_room)
                        dir_set = True
                elif x_grid > 0 and possible_direction[3]:
                    if not self.rooms[x].left:
                        curr_x -= 1280
                        self.rooms[x].left_used()
                        map = random.randint(0, len(self.possible_rooms) - 1)
                        new_room = Room(self.possible_rooms[map], curr_x, curr_y, False, False, True, False, True)
                        self.rooms.append(new_room)
                        dir_set = True
        for x in range(0, len(self.rooms) - 1):
            self.rooms[x].close_entrances()
        end_room = random.randint(0, len(self.rooms) - 1)
        self.rooms[end_room].generate_end()
