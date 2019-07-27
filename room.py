class Room:
    def __init__(self, data, x_cord, y_cord):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.tiles = []
        for x in range(0, len(data)):
            self.tiles.append([])
            for y in range(0, len(data[0])):
                self.tiles[x].append(data[x][y])
