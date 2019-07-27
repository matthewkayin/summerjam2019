# Summer Game Jam 2019
# Team Moral Support (Code: Matt Madden and Zubair Khan; Art: Trent Madden; Music and Sound: Kenon Brinkley)
# fish.py - The player class


class Fish():
    def __init__(self):
        self.x = 1280 / 2
        self.y = 600
        self.w = 40
        self.h = 40
        self.dx = 0
        self.dy = 0
        self.ax = 0
        self.ay = 0

        self.ACC_SPEED = 0.02
        self.DEC_SPEED = 0.01
        self.MAX_VEL = 2
        self.EXTRA_VEL = 2
        self.EXTRA_ACC = 0.02

        self.using_light = False
        self.speeding = False

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

    def set_direction(self, inputs):
        self.ax = inputs[0] * (self.ACC_SPEED + (self.speeding * self.EXTRA_ACC))
        self.ay = inputs[1] * (self.ACC_SPEED + (self.speeding * self.EXTRA_ACC))
