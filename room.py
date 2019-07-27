class Room:
    def __init__(self, file_name, x_cord, y_cord):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.tiles = []
        map_file = open("Rooms/" + file_name + ".txt", "r")
        for line in map_file.read().splitlines():
            self.tiles.append(list(map(int, line.split(" "))))
