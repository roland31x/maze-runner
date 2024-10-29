from game.page import Page
from game.player import Target
from numpy import random

class Maze(Page):
    def __init__(self, engine, map, tilemap):
        super().__init__(engine)
        self.map = map
        self.tilemap = tilemap
        self.cellsize = engine.cellsize
        self.player = engine.player
        self.target = None
        self.start = [0,0]
        self.end = [0,0]
        self.dirs = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        self.finished = False
        self.trails = []
        self.available_trails = 2 * max(len(map), len(map[0]))
        self.max_trails = 2 * max(len(map), len(map[0]))
        self.start_game()

    def render(self):
        self.engine.screen.fill((self.engine.config.black))
        self.move_player()
        self.draw_maze()
        self.draw_trails()

        self.draw_target()
        self.draw_player()
        
        self.draw_keyboard_legend()

    def draw_keyboard_legend(self):
            gray = (150, 150, 150, 168)  
            dark_gray = (60, 60, 60, 68)  
            black = (20, 20, 20, 128)
            white = (255, 255, 255, 128)

            font = self.pygame.font.Font(None, 24)

            base_x = 20
            base_y = self.engine.screen.get_height() - 120

            overlay = self.pygame.Surface((320, 155), self.pygame.SRCALPHA)
            overlay.fill(black)  
            self.engine.screen.blit(overlay, (base_x - 5, base_y - 40))

            movement_text = font.render("Movement", True, white)
            self.screen.blit(movement_text, (base_x + 42, base_y - 25))

            keys = [('W', base_x + 60, base_y), 
                    ('A', base_x + 10, base_y + 50), 
                    ('S', base_x + 60, base_y + 50), 
                    ('D', base_x + 110, base_y + 50)]
            
            for label, x, y in keys:
                box_rect = self.pygame.Rect(x, y, 50, 50)
                self.pygame.draw.rect(self.screen, dark_gray, box_rect)
                self.pygame.draw.rect(self.screen, white, box_rect, 2)

                key_text = font.render(label, True, white)
                text_rect = key_text.get_rect(center=box_rect.center)
                self.screen.blit(key_text, text_rect)


            
            spacebar_rect = self.pygame.Rect(base_x + 200, base_y + 20, 100, 50)
            spacebar_fill = self.pygame.Rect(base_x + 200, base_y + 20, 100 * (self.available_trails / self.max_trails), 50)

            # print(100 * (self.available_trails / self.max_trails))
            
            self.pygame.draw.rect(self.screen, dark_gray, spacebar_rect)
            self.pygame.draw.rect(self.screen, (93, 183, 100, 128), spacebar_fill)
            self.pygame.draw.rect(self.screen, white, spacebar_rect, 2)

            space_text = font.render("Space", True, white)
            space_text_rect = space_text.get_rect(center=spacebar_rect.center)
            self.screen.blit(space_text, space_text_rect)  

            leave_trail_text = font.render("Leave Trail", True, white)
            self.screen.blit(leave_trail_text, (base_x + 210, base_y))

            
        
    def start_game(self):
        startX = random.randint(0, self.engine.mapX)
        startY = random.randint(0, self.engine.mapY)
        
        targetX = random.randint(0, self.engine.mapX)
        targetY = random.randint(0, self.engine.mapY)

        while(targetX == startX and targetY == startY):
            targetX = random.randint(0, self.engine.mapX)
            targetY = random.randint(0, self.engine.mapY)

        self.start = [startX * 2 + 1, startY * 2 + 1]
        self.end = [targetX * 2 + 1, targetY * 2 + 1]    

        targetX = (targetX * 2 + 1) * self.cellsize + self.cellsize / 2
        targetY = (targetY * 2 + 1) * self.cellsize + self.cellsize / 2

        self.engine.target = Target(targetX, targetY)
        self.target = self.engine.target

        

        self.player.X = (startX * 2 + 1) * self.cellsize + self.cellsize / 2
        self.player.Y = (startY * 2 + 1) * self.cellsize + self.cellsize / 2
        
    def draw_maze(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):              
                    renderx = (x * self.cellsize - self.player.X + self.engine.screen.get_width() // 2)
                    rendery = (y * self.cellsize - self.player.Y + self.engine.screen.get_height() // 2)
                    if(renderx + self.cellsize < 0 or rendery + self.cellsize < 0 or renderx > self.engine.screen.get_width() or rendery > self.engine.screen.get_height()):
                        continue
                    self.screen.blit(self.tilemap[y][x] if self.map[y][x] == 0 else self.engine.floor, (renderx, rendery))
                    # self.pygame.draw.rect(self.engine.screen, self.engine.config.light_gray, (renderx, rendery, self.cellsize, self.cellsize))
    
    def draw_target(self):
        renderx = (self.target.X - self.player.X + self.engine.screen.get_width() // 2)
        rendery = (self.target.Y - self.player.Y + self.engine.screen.get_height() // 2)
        if(renderx + self.target.R < 0 or rendery + self.target.R < 0 or renderx > self.engine.screen.get_width() or rendery > self.engine.screen.get_height()):
            return
        sprite = self.target.sprites[self.target.open].convert_alpha()
        scaled = self.pygame.transform.scale(sprite, (self.target.R * 2, self.target.R * 2))
        self.screen.blit(scaled, (renderx - self.target.R, rendery - self.target.R))

    def draw_player(self):
        sprite = self.player.sprites[self.player.last_dir][0 if not self.player.moving else int((self.pygame.time.get_ticks() // 100)) % 4].convert_alpha()
        scaled = self.pygame.transform.scale(sprite, (self.player.R * 2, self.player.R * 2))
        self.screen.blit(scaled, (self.engine.screen.get_width() // 2 - self.player.R, self.engine.screen.get_height() // 2 - self.player.R))

    def draw_trails(self):
        for trail in self.trails:
            x = trail[0]
            y = trail[1]
            renderx = (x - self.player.X + self.engine.screen.get_width() // 2)
            rendery = (y - self.player.Y + self.engine.screen.get_height() // 2)
            if(renderx + self.cellsize < 0 or rendery + self.cellsize < 0 or renderx > self.engine.screen.get_width() or rendery > self.engine.screen.get_height()):
                continue
            self.screen.blit(self.engine.paint, (renderx - self.player.R, rendery - self.player.R))

    def move_player(self):
        keys = self.pygame.key.get_pressed()
        if keys[self.pygame.K_w]:
            if(self.legal(self.dirs[0])):
                self.player.move(self.dirs[0], 0)
        if keys[self.pygame.K_s]:
            if(self.legal(self.dirs[2])):
                self.player.move(self.dirs[2], 2)
        if keys[self.pygame.K_a]:
            if(self.legal(self.dirs[1])):
                self.player.move(self.dirs[1], 1)
        if keys[self.pygame.K_d]:
            if(self.legal(self.dirs[3])):
                self.player.move(self.dirs[3], 3)


    def legal(self, dir):
        newX = self.player.X + dir[0] * self.player.speed
        newY = self.player.Y + dir[1] * self.player.speed

        left = newX - self.player.R
        right = newX + self.player.R
        top = newY - self.player.R
        bottom = newY + self.player.R

        if(left // self.cellsize < 0 or top // self.cellsize < 0 or right // self.cellsize >= len(self.map[0]) or bottom // self.cellsize >= len(self.map)):
            return False
        if(self.map[int(bottom // self.cellsize)][int(right // self.cellsize)] == 0 or 
           self.map[int(top // self.cellsize)]   [int(left // self.cellsize)]  == 0 or 
           self.map[int(top // self.cellsize)]   [int(right // self.cellsize)] == 0 or 
           self.map[int(bottom // self.cellsize)][int(left // self.cellsize)]  == 0):
            return False
        
        if((newX - self.target.X) * (newX - self.target.X) + (newY - self.target.Y) * (newY - self.target.Y) < (self.player.R + self.target.R) * (self.player.R + self.target.R)):
            self.engine.page = self.engine.swap_to_score(self.pygame.time.get_ticks(), self.map, self.end, self.start)

        return True
    
    def handle_event(self, event):
        if(event.type == self.pygame.KEYDOWN):
            if(
                event.key == self.pygame.K_w or
                event.key == self.pygame.K_s or
                event.key == self.pygame.K_a or
                event.key == self.pygame.K_d
                ):
                    self.player.moving = True
            if(event.key == self.pygame.K_ESCAPE):
                self.engine.page = self.engine.swap_to_main_menu()

            if event.key == self.pygame.K_SPACE:
                if(self.available_trails > 0):
                    self.trails.append([self.player.X, self.player.Y])
                    self.available_trails -= 1

        if(event.type == self.pygame.KEYUP):
            if( (
                    event.key == self.pygame.K_w or
                    event.key == self.pygame.K_s or
                    event.key == self.pygame.K_a or
                    event.key == self.pygame.K_d
                ) 
                and
                (
                    self.pygame.key.get_pressed()[self.pygame.K_w] == 0 and
                    self.pygame.key.get_pressed()[self.pygame.K_s] == 0 and
                    self.pygame.key.get_pressed()[self.pygame.K_a] == 0 and
                    self.pygame.key.get_pressed()[self.pygame.K_d] == 0
                )):
                self.player.moving = False


