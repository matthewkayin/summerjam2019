class Room:
    def __init__(self, file_name, x_cord, y_cord):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.minnows = []
        self.tiles = []

        map_file = open("Rooms/" + file_name + ".txt", "r")
        for line in map_file.read().splitlines():
            self.tiles.append(list(map(int, line.split(" "))))

        for x in range(0, len(self.tiles)):
            for y in range(0, len(self.tiles[0])):
                if self.tiles[x][y] == 2:
                    self.minnows.append([x, y])
