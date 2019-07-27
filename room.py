import pygame


class Room:
    def __init__(self, width, height, left, right, top, bottom, center_pillar, x_cord, y_cord, player_size=64):
        self.width = width
        self.height = height
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.player_size = player_size
        self.center_pillar = center_pillar

    def draw_room(self, screen, line_color, thickness):
        # pygame.draw.lines(screen, color, closed, pointlist, thickness)
        if (self.top):
            pygame.draw.lines(screen, line_color, False, [(self.x_cord, self.y_cord), (self.x_cord + (self.width - self.player_size) / 2, self.y_cord)], thickness)
            pygame.draw.lines(screen, line_color, False, [(self.x_cord + (self.width + self.player_size) / 2, self.y_cord), (self.x_cord + self.width, self.y_cord)], thickness)
        else:
            pygame.draw.lines(screen, line_color, False, [(self.x_cord, self.y_cord), (self.x_cord + self.width, self.y_cord)], thickness)

        if (self.bottom):
            pygame.draw.lines(screen, line_color, False, [(self.x_cord, self.y_cord + self.height), (self.x_cord + (self.width - self.player_size) / 2), self.y_cord + self.height], thickness)
            pygame.draw.lines(screen, line_color, False, [(self.x_cord + (self.width + self.player_size) / 2, self.y_cord + self.height), (self.x_cord + self.width, self.y_cord + self.height)], thickness)
        else:
            pygame.draw.lines(screen, line_color, False, [(self.x_cord, self.y_cord + self.height), (self.x_cord + self.width, self.y_cord + self.height)], thickness)

        if (self.right):
            pygame.draw.lines(screen, line_color, False, [(self.x_cord + self.width, self.y_cord), (self.x_cord + self.width, self.y_cord + (self.height - self.player_size) / 2)], thickness)
            pygame.draw.lines(screen, line_color, False, [(self.x_cord + self.width, self.y_cord + (self.height + self.player_size) / 2), (self.x_cord + self.width, self.y_cord + self.height)], thickness)
        else:
            pygame.draw.lines(screen, line_color, False, [(self.x_cord + self.width, self.y_cord), (self.x_cord + self.width, self.y_cord + self.height)], thickness)

        if (self.left):
            pygame.draw.lines(screen, line_color, False, [(self.x_cord, self.y_cord), (self.x_cord, self.y_cord + (self.height - self.player_size) / 2)], thickness)
            pygame.draw.lines(screen, line_color, False, [(self.x_cord, self.y_cord + (self.height + self.player_size) / 2), (self.x_cord, self.y_cord + self.height)], thickness)
        else:
            pygame.draw.lines(screen, line_color, False, [(self.x_cord, self.y_cord), (self.x_cord, self.y_cord + self.height)], thickness)

        if (self.center_pillar):
            pygame.draw.lines(screen, line_color, True, [(self.x_cord + self.player_size, self.y_cord + self.player_size), (self.x_cord + self.width - self.player_size, self.y_cord + self.player_size), (self.x_cord + self.width - self.player_size, self.y_cord + self.height - self.player_size), (self.x_cord + self.player_size, self.y_cord + self.height - self.player_size)], thickness)
