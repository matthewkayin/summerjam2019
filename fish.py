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

        # if the player is above the max speed cap their speed
        if self.dx > self.MAX_VEL:
            self.dx = self.MAX_VEL
        elif self.dx < -self.MAX_VEL:
            self.dx = -self.MAX_VEL
        if self.dy > self.MAX_VEL:
            self.dx = self.MAX_VEL
        elif self.dy < -self.MAX_VEL:
            self.dy = self.MAX_VEL

        # update the player position based on their speed
        self.x += self.dx * delta
        self.y += self.dy * delta

    def set_direction(self, inputs):
        self.ax = inputs[0] * self.ACC_SPEED
        self.ay = inputs[1] * self.ACC_SPEED
