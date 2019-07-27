class Room:
    def __init__(self, data, x_cord, y_cord):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.minnows = []
        self.tiles = []
        for x in range(0, len(data)):
            self.tiles.append([])
            for y in range(0, len(data[0])):
                if data[x][y] == 2:
                    self.tiles[x].append(0)
                    self.minnows.append([x, y])
                else:
                    self.tiles[x].append(data[x][y])
