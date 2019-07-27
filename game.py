# Summer Game Jam 2019
# Team Moral Support (Code: Matt Madden and Zubair Khan; Art: Trent Madden; Music and Sound: Kenon Brinkley)
# game.py -- Main Class

import pygame
import os
import sys
import ihandler
import fish
import room


class Game():
    def __init__(self):
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.TARGET_FPS = 60

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)

        self.debug = False
        self.nolight = False

        for argument in sys.argv:
            if argument == "--debug":
                self.debug = True
            elif argument == "--nolight":
                self.nolight = True

        pygame.init()
        if self.debug:
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        else:
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        # make image objects
        # self.image_ball = pygame.image.load("res/ball.png")

        # make sound objects
        # pygame.mixer.music.load("res/storms.wav")
        # self.beep = pygame.mixer.Sound("res/beep.wav")

        pygame.font.init()
        self.smallfont = pygame.font.SysFont("Serif", 14)
        self.bigfont = pygame.font.SysFont("Serif", 22)
        self.fps_text = self.smallfont.render("FPS", False, self.GREEN)

        pygame.joystick.init()
        self.AXIS_THRESHOLD = 0.001
        self.joystick_labels = []
        self.joystick_label_pool = "ABCDEFGHIJ"  # we shouldn't ever need more than this
        self.joystick_count = pygame.joystick.get_count()
        self.joystick_text = self.smallfont.render("Joysticks: " + str(self.joystick_count), False, self.GREEN)
        for i in range(0, self.joystick_count):
            pygame.joystick.Joystick(i).init()
            self.joystick_labels.append(self.joystick_label_pool[i])
        self.ihandler = ihandler.IHandler(["AXIS FISH HORIZ", "AXIS FISH VERT", "FISH DASH", "FISH LIGHT"])

        self.game_init()

        self.running = True
        self.show_fps = self.debug

        self.run()
        self.quit()

    def game_init(self):
        # pygame.mixer.music.play(-1)  # the -1 makes it play forever
        self.player = fish.Fish()
        self.room = room.Room([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]], 0, 0)

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.ihandler.load_mapping(False)
                elif event.key == pygame.K_F2:
                    self.ihandler.start_mapping()
                elif event.key == pygame.K_F3:
                    self.show_fps = not self.show_fps
                else:
                    self.ihandler.key_down("K" + str(event.key))
            elif event.type == pygame.KEYUP:
                if event.key != pygame.K_ESCAPE and event.key != pygame.K_F1 and event.key != pygame.K_F2 and event.key != pygame.K_F3:
                    self.ihandler.key_up("K" + str(event.key))
            elif event.type == pygame.JOYBUTTONDOWN:
                self.ihandler.key_down(self.joystick_labels[event.joy] + str(event.button))
            elif event.type == pygame.JOYBUTTONUP:
                self.ihandler.key_up(self.joystick_labels[event.joy] + str(event.button))
            elif event.type == pygame.JOYAXISMOTION:
                axis = self.joystick_labels[event.joy] + "x" + str(event.axis)
                pos = pygame.joystick.Joystick(event.joy).get_axis(event.axis)
                if self.ihandler.is_mapped_axis(axis):
                    self.ihandler.axis_moved(axis, pos)
                axis_pos = axis + "+"
                axis_neg = axis + "-"
                if abs(pos) <= self.AXIS_THRESHOLD:
                    self.ihandler.key_up(axis_pos)
                    self.ihandler.key_up(axis_neg)
                elif pos > 0:
                    self.ihandler.key_down(axis_pos)
                    self.ihandler.key_up(axis_neg)
                elif pos < 0:
                    self.ihandler.key_down(axis_neg)
                    self.ihandler.key_up(axis_pos)
            elif event.type == pygame.JOYHATMOTION:
                axis = self.joystick_labels[event.joy] + "t" + str(event.hat)
                axis_h_pos = axis + "h+"
                axis_h_neg = axis + "h-"
                axis_v_pos = axis + "v+"
                axis_v_neg = axis + "v-"
                pos = pygame.joystick.Joystick(event.joy).get_hat(event.hat)
                if pos[0] == 0:
                    self.ihandler.key_up(axis_h_pos)
                    self.ihandler.key_up(axis_h_neg)
                elif pos[0] == 1:
                    self.ihandler.key_down(axis_h_pos)
                    self.ihandler.key_up(axis_h_neg)
                elif pos[0] == -1:
                    self.ihandler.key_up(axis_h_pos)
                    self.ihandler.key_down(axis_h_neg)
                if pos[1] == 0:
                    self.ihandler.key_up(axis_v_pos)
                    self.ihandler.key_up(axis_v_neg)
                elif pos[1] == 1:
                    self.ihandler.key_down(axis_v_pos)
                    self.ihandler.key_up(axis_v_neg)
                elif pos[1] == -1:
                    self.ihandler.key_up(axis_v_pos)
                    self.ihandler.key_down(axis_v_neg)

    def update(self, delta):
        # handle inputs from ihandler
        event = ""
        while event != "EMPTY":
            event = self.ihandler.key_queue()

        player_inputs = [0, 0]
        player_inputs[0] = self.ihandler.get_state("AXIS FISH HORIZ")
        player_inputs[1] = self.ihandler.get_state("AXIS FISH VERT")
        self.player.set_direction(player_inputs)

        if self.ihandler.get_state("FISH LIGHT"):
            self.player.using_light = True
        else:
            self.player.using_light = False

        if self.ihandler.get_state("FISH DASH"):
            self.player.dash(player_inputs)
        else:
            self.player.speeding = False

        self.player.update(delta)

    def render(self):
        if not self.nolight:
            mask = pygame.surface.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT)).convert_alpha()
            mask.fill((0, 0, 0, 255))

            lower_radius = int((self.player.w / 2) + 10)
            radius = lower_radius + 30
            t = 255
            delta = 10
            rdelta = int(10 / 4)
            if self.player.using_light:
                radius += 220
                delta -= 5
                rdelta = delta
            light_location = (int(self.player.x + (self.player.w / 2)), int(self.player.y + (self.player.h / 2)))
            while radius > lower_radius:
                t -= delta
                radius -= rdelta
                pygame.draw.circle(mask, (0, 0, 0, t), light_location, radius)
            if not self.player.using_light:
                t = 110
            pygame.draw.circle(mask, (0, 0, 0, t), light_location, radius)

        self.screen.fill(self.GREEN)

        for x in range(0, len(self.room.tiles)):
            for y in range(0, len(self.room.tiles[0])):
                if self.room.tiles[x][y] == 1:
                    pygame.draw.rect(self.screen, self.WHITE, (self.room.x_cord + (x * 20) - self.player.cx, self.room.y_cord + (y * 20) - self.player.cy, 20, 20), False)

        pygame.draw.rect(self.screen, self.RED, (self.player.x, self.player.y, self.player.w, self.player.h), False)

        # pygame.draw.rect(self.screen, self.RED, (pos[0], pos[1], 20, 20), False)
        # self.screen.blit(self.image_ball, (pos[0], pos[1]))

        if not self.nolight:
            self.screen.blit(mask, (0, 0))

        pygame.draw.rect(self.screen, self.YELLOW, (5, 5, self.player.energy, 20), False)
        pygame.draw.rect(self.screen, self.YELLOW, (5 + self.player.energy, 5, 100 - self.player.energy, 20), True)
        pygame.draw.rect(self.screen, self.BLUE, (115, 5, 20, 20), not self.player.can_dash())

        if self.show_fps:
            self.screen.blit(self.fps_text, (0, 0))
            self.screen.blit(self.joystick_text, (0, 15))

        pygame.display.flip()

    def map_input(self):
        self.screen.fill(self.BLACK)

        header = self.bigfont.render("Mapping Key Inputs!", False, self.WHITE)
        instructions = self.bigfont.render("Press the key you want for... " + self.ihandler.to_map(), False, self.WHITE)
        self.screen.blit(header, (self.SCREEN_WIDTH / 8, self.SCREEN_HEIGHT / 2 - 50))
        self.screen.blit(instructions, (self.SCREEN_WIDTH / 8, self.SCREEN_HEIGHT / 2 - 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_F1 or event.key == pygame.K_F2 or event.key == pygame.K_F3:
                    print("You can't map those keys!")
                    continue
                self.ihandler.key_down("K" + str(event.key))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_F1 or event.key == pygame.K_F2 or event.key == pygame.K_F3:
                    continue
                self.ihandler.key_up("K" + str(event.key))
            elif event.type == pygame.JOYBUTTONDOWN:
                self.ihandler.key_down(self.joystick_labels[event.joy] + str(event.button))
            elif event.type == pygame.JOYBUTTONUP:
                self.ihandler.key_up(self.joystick_labels[event.joy] + str(event.button))
            elif event.type == pygame.JOYAXISMOTION:
                axis = self.joystick_labels[event.joy] + "x" + str(event.axis)
                pos = pygame.joystick.Joystick(event.joy).get_axis(event.axis)
                if self.ihandler.to_map().startswith("AXIS ") and pos != 0:
                    self.ihandler.key_down(axis)
                    self.ihandler.key_up("AXIS KEYUP")
                    continue
                axis_pos = axis + "+"
                axis_neg = axis + "-"
                if abs(pos) <= self.AXIS_THRESHOLD:
                    self.ihandler.key_up(axis_neg)
                elif pos > 0:
                    self.ihandler.key_down(axis_pos)
                elif pos < 0:
                    self.ihandler.key_down(axis_neg)
            elif event.type == pygame.JOYHATMOTION:
                axis = self.joystick_labels[event.joy] + "t" + str(event.hat)
                axis_h_pos = axis + "h+"
                axis_h_neg = axis + "h-"
                axis_v_pos = axis + "v+"
                axis_v_neg = axis + "v-"
                pos = pygame.joystick.Joystick(event.joy).get_hat(event.hat)
                if pos[0] == 0:
                    self.ihandler.key_up(axis_h_pos)
                elif pos[0] == 1:
                    self.ihandler.key_down(axis_h_pos)
                elif pos[0] == -1:
                    self.ihandler.key_down(axis_h_neg)
                if pos[1] == 0:
                    self.ihandler.key_up(axis_v_pos)
                elif pos[1] == 1:
                    self.ihandler.key_down(axis_v_pos)
                elif pos[1] == -1:
                    self.ihandler.key_down(axis_v_neg)

    def run(self):
        SECOND = 1000
        UPDATE_TIME = SECOND / 60
        before_time = pygame.time.get_ticks()
        before_sec = before_time
        frames = 0
        delta = 0
        while self.running:
            self.clock.tick(self.TARGET_FPS)
            if self.ihandler.is_mapping():
                self.map_input()
            else:
                self.input()
                self.update(delta)
                self.render()
                frames += 1

            after_time = pygame.time.get_ticks()
            delta = (after_time - before_time) / UPDATE_TIME
            if after_time - before_sec >= SECOND:
                self.fps_text = self.smallfont.render('FPS: ' + str(frames), False, self.GREEN)
                frames = 0
                before_sec += SECOND
            before_time = pygame.time.get_ticks()

    def quit(self):
        pygame.joystick.quit()
        pygame.font.quit()
        pygame.quit()


os.environ['SDL_VIDEO_CENTERED'] = '1'  # centers the pygame window
game = Game()
