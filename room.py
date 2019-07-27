import pygame


class Tile:
    def __init__(self, screen, size, is_wall, is_pillar, x, y):
        self.screen = screen
        self.size = size
        self.is_wall = is_wall
        self.is_pillar = is_pillar
        self.x = x
        self.y = y

    def draw_tile(self):
        if self.is_wall:
            pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.size, self.size), False)
        elif self.is_pillar:
            pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.size, self.size), False)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.size, self.size), False)


class Room:
    def __init__(self, screen, width, height, left, right, top, bottom, center_pillar, x_cord, y_cord, tile_size = 20):
        self.screen = screen
        self.width = width
        self.height = height
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.center_pillar = center_pillar
        self.tile_size = tile_size
        array = []
        for x in range(self.x_cord, self.x_cord + self.width * tile_size, tile_size):
            x_tile = int(x - self.x_cord / tile_size)
            array.append([x_tile])
            for y in range(self.y_cord, self.y_cord + self.height * tile_size, tile_size):
                y_tile = int(y - self.y_cord / tile_size)
                array[x_tile].append[y_cord]
                array[x_tile][y_tile] = Tile(screen, tile_size, False, False, x, y)
        # self.center_pillar = center_pillar

    def create_room(self, screen, line_color, thickness):
        # pygame.draw.lines(screen, color, closed, pointlist, thickness)
        for x in range(self.x_cord, self.x_cord + self.width * self.tile_size, self.tile_size):
            for y in range(self.y_cord, self.y_cord + self.height * self.tile_size, self.tile_size):
                x_tile = int(x - self.x_cord / self.tile_size)
                y_tile = int(y - self.y_cord / self.tile_size)
                self.array[x_tile][y_tile].draw_tile
        # if (self.top):
        #     # while self.x_cord < self.x_cord + self.width:
        #     pygame.draw.lines(screen, line_color, False, [(self.x_cord, self.y_cord), (self.x_cord + (self.width - self.player_size) / 2, self.y_cord)], thickness)
        #     pygame.draw.lines(screen, line_color, False, [(self.x_cord + (self.width + self.player_size) / 2, self.y_cord), (self.x_cord + self.width, self.y_cord)], thickness)
        # else:
        #     pygame.draw.lines(screen, line_color, False, [(self.x_cord, self.y_cord), (self.x_cord + self.width, self.y_cord)], thickness)
        #
        # if (self.bottom):
        #     pygame.draw.lines(screen, line_color, False, [(self.x_cord, self.y_cord + self.height), (self.x_cord + (self.width - self.player_size) / 2), self.y_cord + self.height], thickness)
        #     pygame.draw.lines(screen, line_color, False, [(self.x_cord + (self.width + self.player_size) / 2, self.y_cord + self.height), (self.x_cord + self.width, self.y_cord + self.height)], thickness)
        # else:
        #     pygame.draw.lines(screen, line_color, False, [(self.x_cord, self.y_cord + self.height), (self.x_cord + self.width, self.y_cord + self.height)], thickness)
        #
        # if (self.right):
        #     pygame.draw.lines(screen, line_color, False, [(self.x_cord + self.width, self.y_cord), (self.x_cord + self.width, self.y_cord + (self.height - self.player_size) / 2)], thickness)
        #     pygame.draw.lines(screen, line_color, False, [(self.x_cord + self.width, self.y_cord + (self.height + self.player_size) / 2), (self.x_cord + self.width, self.y_cord + self.height)], thickness)
        # else:
        #     pygame.draw.lines(screen, line_color, False, [(self.x_cord + self.width, self.y_cord), (self.x_cord + self.width, self.y_cord + self.height)], thickness)
        #
        # if (self.left):
        #     pygame.draw.lines(screen, line_color, False, [(self.x_cord, self.y_cord), (self.x_cord, self.y_cord + (self.height - self.player_size) / 2)], thickness)
        #     pygame.draw.lines(screen, line_color, False, [(self.x_cord, self.y_cord + (self.height + self.player_size) / 2), (self.x_cord, self.y_cord + self.height)], thickness)
        # else:
        #     pygame.draw.lines(screen, line_color, False, [(self.x_cord, self.y_cord), (self.x_cord, self.y_cord + self.height)], thickness)
        #
        # if (self.center_pillar):
        #     pygame.draw.lines(screen, line_color, True, [(self.x_cord + self.player_size, self.y_cord + self.player_size), (self.x_cord + self.width - self.player_size, self.y_cord + self.player_size), (self.x_cord + self.width - self.player_size, self.y_cord + self.height - self.player_size), (self.x_cord + self.player_size, self.y_cord + self.height - self.player_size)], thickness)


# class Map:
#     def __init__(self, screen, screen_width, screen_height):
#         self.screen = screen
