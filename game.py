# Summer Game Jam 2019
# Team Moral Support (Code: Matt Madden and Zubair Khan; Art: Trent Madden; Music and Sound: Kenon Brinkley)
# game.py -- Main Class

import pygame
import os
import sys
import ihandler
import fish
import room
import eel
import math


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
        self.image_fish = []
        for i in range(0, 6):
            self.image_fish.append(pygame.image.load("res/gfx/fish_" + str(i) + ".png"))
        self.image_minnow = []
        for i in range(0, 18):
            self.image_minnow.append(pygame.image.load("res/gfx/minnow_" + str(i) + ".png"))
        self.image_wall = pygame.image.load("res/gfx/wall.png")
        self.image_floor = pygame.image.load("res/gfx/floor.png")

        # make sound objects
        pygame.mixer.music.load("res/sfx/music.wav")
        self.sound_dash = pygame.mixer.Sound("res/sfx/eel-attack.wav")
        # self.sound_light = pygame.mixer.Sound("res/sfx/light.wav")

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

        pygame.mixer.music.play(-1)  # the -1 makes it play forever
        if self.debug:
            self.game_init()

        self.running = True
        self.show_fps = self.debug

        self.gamestate = 0
        if self.debug:
            self.gamestate = 1

        self.run()
        self.quit()

    def game_init(self):
        self.player = fish.Fish()
        self.level_one = room.MapMaker(0, 0, 15)
        self.enemies = []
        num_eels = 0
        for i in range(0, len(self.level_one.rooms)):
            for j in range(0, len(self.level_one.rooms[i].eels)):
                new_eel = eel.Eel()
                self.enemies.append(new_eel)
                self.enemies[num_eels].spawn(self.level_one.rooms[i].eels[j][0], self.level_one.rooms[i].eels[j][1], self.level_one.rooms[i].eels[j][2])
                self.enemies[num_eels].room = i
                num_eels += 1

        self.player_room = [0, 0]
        self.player_safe = [self.player.x, self.player.y]

        self.floor_tiles = []
        far_left = 0
        far_right = 0
        far_top = 0
        far_bot = 0
        for curr_room in self.level_one.rooms:
            if curr_room.x_cord < far_left:
                far_left = curr_room.x_cord
            elif curr_room.x_cord + self.SCREEN_WIDTH > far_right:
                far_right = curr_room.x_cord + self.SCREEN_WIDTH
            if curr_room.y_cord < far_top:
                far_top = curr_room.y_cord
            elif curr_room.y_cord + self.SCREEN_HEIGHT > far_bot:
                far_bot = curr_room.y_cord + self.SCREEN_HEIGHT
        no_x_tiles = int(abs(far_left - far_right) / 640) + 2
        no_y_tiles = int(math.ceil(abs(far_top - far_bot) / 640)) + 2
        far_left -= 640
        far_top -= 640
        for x in range(0, no_x_tiles):
            for y in range(0, no_y_tiles):
                self.floor_tiles.append([far_left + (640 * x), far_top + (640 * y)])

        self.minnow_tick = 0
        self.minnow_MAX = 10
        self.minnow_frame = 0
        self.minnow_MFRAME = 17

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

        if self.gamestate == 0:
            event = ""
            while event != "EMPTY":
                event = self.ihandler.key_queue()
                if event == "FISH DASH":
                    self.game_init()
                    self.gamestate = 1
                    break
            return

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
            # self.sound_light.play()
        else:
            self.player.using_light = False

        if self.ihandler.get_state("FISH DASH"):
            if not self.player.speeding:
                self.sound_dash.play()
                self.player.dash(player_inputs)
        else:
            self.player.speeding = False

        self.player.update(delta)

        # check for collisions
        wall_collision = False
        tile_rect = None
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.w, self.player.h)
        for i in range(0, len(self.level_one.rooms)):
            if abs(self.level_one.rooms[i].x_cord - self.player_room[0]) > self.SCREEN_WIDTH:
                continue
            if abs(self.level_one.rooms[i].y_cord - self.player_room[1]) > self.SCREEN_HEIGHT:
                continue
            for x in range(0, len(self.level_one.rooms[i].tiles)):
                for y in range(0, len(self.level_one.rooms[i].tiles[0])):
                    x_val = self.level_one.rooms[i].x_cord + (x * 20) - self.player.cx
                    y_val = self.level_one.rooms[i].y_cord + (y * 20) - self.player.cy
                    if x_val + 20 < 0 or x_val >= self.SCREEN_WIDTH or y_val + 20 < 0 or y_val >= self.SCREEN_HEIGHT:
                        continue
                    if self.level_one.rooms[i].tiles[x][y] == 1:
                        tile_rect = pygame.Rect(x_val, y_val, 20, 20)
                        if player_rect.colliderect(tile_rect):
                            wall_collision = True
                            break
                if wall_collision:
                    break
            if wall_collision:
                break

        if wall_collision:
            while player_rect.colliderect(tile_rect):
                self.player.x -= self.player.dx
                self.player.y -= self.player.dy
                player_rect = pygame.Rect(self.player.x, self.player.y, self.player.w, self.player.h)
            self.player.dx = 0
            self.player.dy = 0
            self.player.ax = 0
            self.player.ay = 0
        else:
            self.player_safe[0] = self.player.x
            self.player_safe[1] = self.player.y

        room_x = (self.player.x + self.player.cx) / self.SCREEN_WIDTH
        if room_x > 0:
            room_x = math.floor(room_x)
        elif room_x < 0:
            room_x = -math.ceil(-room_x)
        room_x *= self.SCREEN_WIDTH
        room_y = (self.player.y + self.player.cy) / self.SCREEN_HEIGHT
        if room_y > 0:
            room_y = math.floor(room_y)
        elif room_y < 0:
            room_y = -math.ceil(-room_y)
        room_y *= self.SCREEN_HEIGHT
        self.player_room = [room_x, room_y]

        # for i in range(0, len(self.level_one.rooms[i].minnows)):
        #     minnowRect = pygame.Rect(self.level_one.rooms[i].x_cord + (self.level_one.rooms[i].minnows[i][0] * 20) - self.player.cx, self.level_one.rooms[i].y_cord + (self.level_one.rooms[i].minnows[i][1] * 20) - self.player.cy, 20, 20)
        #     if playerRect.colliderect(minnowRect):
        #         self.player.energy = self.player.MAX_ENERGY
        #         del self.level_one.rooms[i].minnows[i]
        #         break
        for i in range(0, len(self.level_one.rooms)):
            if self.level_one.rooms[i].x_cord != self.player_room[0]:
                continue
            if self.level_one.rooms[i].y_cord != self.player_room[1]:
                continue
            for j in range(0, len(self.level_one.rooms[i].minnows)):
                minnow_rect = pygame.Rect(self.level_one.rooms[i].x_cord + (self.level_one.rooms[i].minnows[j][0] * 20) - self.player.cx, self.level_one.rooms[i].y_cord + (self.level_one.rooms[i].minnows[j][1] * 20) - self.player.cy, 20, 20)
                if player_rect.colliderect(minnow_rect):
                    self.player.energy = self.player.MAX_ENERGY
                    del self.level_one.rooms[i].minnows[j]
                    break

        player_sound = False
        chase = False
        player_center = [self.player.x + (self.player.w / 2), self.player.y + (self.player.h / 2)]
        room_indices = []
        for i in range(0, len(self.level_one.rooms)):
            if abs(self.level_one.rooms[i].x_cord - self.player_room[0]) > self.SCREEN_WIDTH:
                continue
            if abs(self.level_one.rooms[i].y_cord - self.player_room[1]) > self.SCREEN_HEIGHT:
                continue
            room_indices.append(i)

        for i in range(0, len(self.enemies) - 1):
            if not self.enemies[i].room in room_indices:
                continue
            player_sound = False
            chase = False
            self.enemies[i].center = [self.enemies[i].x + (self.enemies[i].w / 2) - self.player.cx, self.enemies[i].y + (self.enemies[i].h / 2) - self.player.cy]
            if self.player.speeding:
                if (abs(player_center[0] - self.enemies[i].center[0]) <= self.enemies[i].LISTEN_DIST
                        and abs(player_center[1] - self.enemies[i].center[1]) <= self.enemies[i].LISTEN_DIST):
                    player_sound = [self.player.x + self.player.cx, self.player.y + self.player.cy]
            see_dist = self.enemies[i].SEE_DIST
            if self.player.using_light:
                see_dist = 300
            if (abs(player_center[0] - self.enemies[i].center[0]) <= see_dist
                    and abs(player_center[1] - self.enemies[i].center[1]) <= see_dist):
                player_sound = [self.player.x + self.player.cx, self.player.y + self.player.cy]
                chase = True
            self.enemies[i].update(delta, player_sound, chase)
            enemy_rect = pygame.Rect(self.enemies[i].x, self.enemies[i].y, self.enemies[i].w, self.enemies[i].h)
            for i in range(0, len(self.level_one.rooms)):
                if abs(self.level_one.rooms[i].x_cord - self.player_room[0]) > self.SCREEN_WIDTH:
                    continue
                if abs(self.level_one.rooms[i].y_cord - self.player_room[1]) > self.SCREEN_HEIGHT:
                    continue
                for x in range(0, len(self.level_one.rooms[i].tiles)):
                    for y in range(0, len(self.level_one.rooms[i].tiles[0])):
                        x_val = self.level_one.rooms[i].x_cord + (x * 20) - self.player.cx
                        y_val = self.level_one.rooms[i].y_cord + (y * 20) - self.player.cy
                        if self.level_one.rooms[i].tiles[x][y] == 1:
                            tile_rect = pygame.Rect(x_val, y_val, 20, 20)
                            if enemy_rect.colliderect(tile_rect):
                                wall_collision = True
                                break
                    if wall_collision:
                        break
                if wall_collision:
                    break
            # if wall_collision:
            #    while enemy_rect.colliderect(tile_rect):
            #         self.enemies[i].x -= self.enemies[i].dx
            #         self.enemies[i].y -= self.enemies[i].dy
            #         enemy_rect = pygame.Rect(self.enemies[i].x, self.enemies[i].y, self.enemies[i].w, self.enemies[i].h)
            if player_rect.colliderect(enemy_rect):
                self.gamestate = 0

        self.minnow_tick += delta
        if self.minnow_tick >= self.minnow_MAX:
            self.minnow_tick -= self.minnow_MAX
            self.minnow_frame += 1
            if self.minnow_frame > self.minnow_MFRAME:
                self.minnow_frame = 0

    def rotate_center(self, image, angle):

        loc = image.get_rect().center
        rot_sprite = pygame.transform.rotate(image, angle)
        rot_sprite.get_rect().center = loc
        return rot_sprite

    def render(self):

        if self.gamestate == 0:

            self.screen.fill(self.BLACK)
            header = self.bigfont.render("Sea Nothing", False, self.WHITE)
            instructions = self.bigfont.render("Press A to start", False, self.WHITE)
            self.screen.blit(header, (self.SCREEN_WIDTH / 8, self.SCREEN_HEIGHT / 2 - 50))
            self.screen.blit(instructions, (self.SCREEN_WIDTH / 8, self.SCREEN_HEIGHT / 2 - 20))

            pygame.display.flip()

            return

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

        # self.screen.fill(self.GREEN)
        # render floor
        for floor_tile in self.floor_tiles:
            x_cord = floor_tile[0] - self.player.cx
            y_cord = floor_tile[1] - self.player.cy
            if x_cord + self.SCREEN_WIDTH < 0 or x_cord >= self.SCREEN_WIDTH:
                continue
            if y_cord + self.SCREEN_HEIGHT < 0 or y_cord >= self.SCREEN_HEIGHT:
                continue
            self.screen.blit(self.image_floor, (x_cord, y_cord))

        # render room
        for i in range(0, len(self.level_one.rooms)):
            if abs(self.level_one.rooms[i].x_cord - self.player_room[0]) > self.SCREEN_WIDTH:
                continue
            if abs(self.level_one.rooms[i].y_cord - self.player_room[1]) > self.SCREEN_HEIGHT:
                continue
            for minnow in self.level_one.rooms[i].minnows:
                x_val = self.level_one.rooms[i].x_cord + (minnow[0] * 20) - self.player.cx
                y_val = self.level_one.rooms[i].y_cord + (minnow[1] * 20) - self.player.cy
                self.screen.blit(self.image_minnow[self.minnow_frame], (x_val, y_val))
            for x in range(0, len(self.level_one.rooms[i].tiles)):
                for y in range(0, len(self.level_one.rooms[i].tiles[0])):
                    x_val = self.level_one.rooms[i].x_cord + (x * 20) - self.player.cx
                    y_val = self.level_one.rooms[i].y_cord + (y * 20) - self.player.cy
                    if x_val + 20 < 0 or x_val >= self.SCREEN_WIDTH or y_val + 20 < 0 or y_val >= self.SCREEN_HEIGHT:
                        continue
                    if self.level_one.rooms[i].tiles[x][y] == 1 or self.level_one.rooms[i].tiles[x][y] == 1:
                        self.screen.blit(self.image_wall, (x_val, y_val))

        # render player
        self.screen.blit(self.rotate_center(self.image_fish[self.player.animation_counter], self.player.angle), (self.player.x, self.player.y))
        # pygame.draw.rect(self.screen, self.RED, (self.player.x, self.player.y, self.player.w, self.player.h), False)

        # render enemies
        for i in range(0, len(self.enemies) - 1):
            pygame.draw.rect(self.screen, self.BLUE, (self.enemies[i].x - self.player.cx, self.enemies[i].y - self.player.cy, self.enemies[i].w, self.enemies[i].h), False)

        if not self.nolight:
            self.screen.blit(mask, (0, 0))

        # render player HUD
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
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_F1 or event.key == pygame.K_F2 or event.key == pygame.K_F3:
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
