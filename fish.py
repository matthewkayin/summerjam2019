# Summer Game Jam 2019
# Team Moral Support (Code: Matt Madden and Zubair Khan; Art: Trent Madden; Music and Sound: Kenon Brinkley)
# fish.py - The player class

import math


class Fish():
    def __init__(self):
        self.x = 1280 / 2
        self.y = 720 / 2
        self.w = 20
        self.h = 36
        self.dx = 0
        self.dy = 0
        self.ax = 0
        self.ay = 0
        self.cx = 0
        self.cy = 0

        self.CAMERA_THRESHOLD = 0.75
        self.CAMERA_RIGHT = 1280 * self.CAMERA_THRESHOLD
        self.CAMERA_LEFT = 1280 * (1 - self.CAMERA_THRESHOLD)
        self.CAMERA_UP = 720 * (1 - self.CAMERA_THRESHOLD)
        self.CAMERA_DOWN = 720 * self.CAMERA_THRESHOLD

        self.ACC_SPEED = 0.02
        self.DEC_SPEED = 0.01
        self.MAX_VEL = 2
        self.EXTRA_VEL = 2
        self.EXTRA_ACC = 0.02

        self.using_light = False
        self.speeding = False

        self.energy = 100
        self.MAX_ENERGY = 100
        self.ENERGY_TICK = 1 / 30
        self.DASH_COST = 30
        self.RUN_COST = 1 / 2
        self.LIGHT_COST = 1 / 4

        self.angle = 90

    def update(self, delta):
        max_dx = self.dx
        max_dy = self.dy

        # update player speed based on acceleration
        self.dx += self.ax * delta
        self.dy += self.ay * delta

        # apply decceleration from the water
        if self.dx > 0:
            self.dx -= self.DEC_SPEED * delta
        elif self.dx < 0:
            self.dx += self.DEC_SPEED * delta
        if self.dy > 0:
            self.dy -= self.DEC_SPEED * delta
        elif self.dy < 0:
            self.dy += self.DEC_SPEED * delta

        # decide which max velocity to use
        max_dx = max(max_dx, self.MAX_VEL + (self.speeding * self.EXTRA_VEL))
        max_dy = max(max_dy, self.MAX_VEL + (self.speeding * self.EXTRA_VEL))

        # if the player is above the max speed cap their speed
        if self.dx > max_dx:
            self.dx = max_dx
        elif self.dx < -max_dx:
            self.dx = -max_dx
        if self.dy > max_dy:
            self.dy = max_dy
        elif self.dy < -max_dy:
            self.dy = -max_dy

        # update the player position based on their speed
        self.x += self.dx * delta
        self.y += self.dy * delta

        # update the camera based on player movement
        if self.x > self.CAMERA_RIGHT:
            dist = self.x - self.CAMERA_RIGHT
            self.cx += dist
            self.x -= dist
        elif self.x < self.CAMERA_LEFT:
            dist = self.CAMERA_LEFT - self.x
            self.cx -= dist
            self.x += dist
        if self.y > self.CAMERA_DOWN:
            dist = self.y - self.CAMERA_DOWN
            self.cy += dist
            self.y -= dist
        elif self.y < self.CAMERA_UP:
            dist = self.CAMERA_UP - self.y
            self.cy -= dist
            self.y += dist

        # update the players energy resources
        self.energy += self.ENERGY_TICK
        if self.energy > self.MAX_ENERGY:
            self.energy = self.MAX_ENERGY
        if self.speeding:
            if self.energy < self.RUN_COST:
                self.speeding = False
            else:
                self.energy -= self.RUN_COST
        if self.using_light:
            if self.energy < self.LIGHT_COST:
                self.using_light = False
            else:
                self.energy -= self.LIGHT_COST

    def set_direction(self, inputs):
        self.ax = inputs[0] * (self.ACC_SPEED + (self.speeding * self.EXTRA_ACC))
        self.ay = inputs[1] * (self.ACC_SPEED + (self.speeding * self.EXTRA_ACC))
        if inputs[0] == 0 and inputs[1] == 0:
            return
        # if inputs[0] == 0:
        #    if inputs[1] > 0:
        #        self.angle = 270
        #    elif inputs[1] < 0:
        #        self.angle = 90
        # else:
        self.angle = math.degrees(math.atan2(inputs[1], inputs[0]))
        if self.angle < 0:
            self.angle *= -1
        elif self.angle > 0:
            self.angle = 360 - self.angle
        self.angle -= 90

    def dash(self, inputs):
        DASH_COST = 30
        if (inputs[0] == 0 and inputs[1] == 0) or self.speeding or self.energy < DASH_COST:
            return
        self.energy -= DASH_COST
        self.dx = self.MAX_VEL * inputs[0]
        self.dy = self.MAX_VEL * inputs[1]
        self.speeding = True

    def can_dash(self):
        return self.energy >= self.DASH_COST
