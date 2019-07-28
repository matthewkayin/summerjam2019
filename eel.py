import random


class Eel():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 30
        self.h = 90
        self.pace_points = [[0, 0], [100, 100]]
        self.center = 0

        self.SPEED = 0.5
        self.EXTRA_SPEED = 3.8
        self.PACE_LENGTH = 700
        self.PROX_THRESHOLD = 1

        self.follow_location = [0, 0]
        self.following = 1
        self.chasing = False
        self.follow_countdown = 0

        self.LISTEN_DIST = 450
        self.SEE_DIST = 150

    def spawn(self, x_vals, y_vals, pace_offset):
        self.x = random.randint(x_vals[0], x_vals[1])
        self.y = random.randint(y_vals[0], y_vals[1])
        self.pace_points[0][0] = self.x
        self.pace_points[0][1] = self.y
        self.pace_points[1][0] = self.x + (pace_offset[0] * self.PACE_LENGTH)
        self.pace_points[1][1] = self.y + (pace_offset[1] * self.PACE_LENGTH)
        self.follow_location = self.pace_points[self.following]

    def update(self, delta, player, chase):
        if player:
            if chase:
                self.chasing = True
            self.follow_location = player
            self.follow_countdown = 240
        if self.follow_countdown > 0:
            self.follow_countdown -= 1
            if self.follow_countdown == 0:
                self.follow_location = self.pace_points[self.following]
                self.chasing = False
        if self.follow_location == self.pace_points[self.following]:
            if abs(self.x - self.follow_location[0]) <= self.PROX_THRESHOLD and abs(self.y - self.follow_location[1]) <= self.PROX_THRESHOLD:
                if self.following == 0:
                    self.following = 1
                else:
                    self.following = 0
                self.follow_location = self.pace_points[self.following]
        if abs(self.x - self.follow_location[0]) > self.PROX_THRESHOLD:
            dirX = 1
            if self.x > self.follow_location[0]:
                dirX = -1
            self.x += (self.SPEED + (self.EXTRA_SPEED * self.chasing)) * delta * dirX
        if abs(self.y - self.follow_location[1]) > self.PROX_THRESHOLD:
            dirY = 1
            if self.y > self.follow_location[1]:
                dirY = -1
            self.y += (self.SPEED + (self.EXTRA_SPEED * self.chasing)) * delta * dirY
