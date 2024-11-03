from game.page import Page
from game.player import Target
from numpy import random
from game.maze.energy_drink import Energy_Drink
from game.maze.key import Key

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
        self.items = [
            Key(0, 0, engine.config.obj_radius),
            Energy_Drink(0, 0, engine.config.obj_radius)
        ]

        self.picked_up_items = []
        self.available_trails = 2 * max(len(map), len(map[0]))
        self.max_trails = 2 * max(len(map), len(map[0]))

        self.start_game()
        self.generate_items()

    def render(self):
        self.engine.screen.fill((self.engine.config.black))
        self.move_player()
        self.draw_maze()
        self.draw_trails()

        self.draw_items()
        self.draw_target()
        self.draw_player()
        
        self.draw_keyboard_legend()
        self.draw_items_overlay()

    def draw_keyboard_legend(self):
            gray = (150, 150, 150, 168)  
            dark_gray = (60, 60, 60, 68)  
            black = (20, 20, 20, 128)
            white = (255, 255, 255, 128)

            font = self.pygame.font.Font(None, 24)

            base_x = 20
            base_y = self.engine.screen.get_height() - 180

            overlay = self.pygame.Surface((270, 170), self.pygame.SRCALPHA)
            overlay.fill(black)  
            self.engine.screen.blit(overlay, (base_x - 5, base_y))

            movement_text = font.render("Movement", True, white)
            self.screen.blit(movement_text, (base_x + 19, base_y + 10))

            keys = [('W', base_x + 45, base_y + 10 + 20), 
                    ('A', base_x + 15, base_y + 10 + 20 + 30), 
                    ('S', base_x + 45, base_y + 10 + 20 + 30), 
                    ('D', base_x + 75, base_y + 10 + 20 + 30)]
            
            for label, x, y in keys:
                box_rect = self.pygame.Rect(x, y, 30, 30)
                self.pygame.draw.rect(self.screen, dark_gray, box_rect)
                self.pygame.draw.rect(self.screen, white, box_rect, 2)

                key_text = font.render(label, True, white)
                text_rect = key_text.get_rect(center=box_rect.center)
                self.screen.blit(key_text, text_rect)


            
            spacebar_rect = self.pygame.Rect(base_x + 10, base_y + 130, 100, 30)
            spacebar_fill = self.pygame.Rect(base_x + 10, base_y + 130, 100 * (self.available_trails / self.max_trails), 30)

            # print(100 * (self.available_trails / self.max_trails))
            
            self.pygame.draw.rect(self.screen, dark_gray, spacebar_rect)
            self.pygame.draw.rect(self.screen, (93, 183, 100, 128), spacebar_fill)
            self.pygame.draw.rect(self.screen, white, spacebar_rect, 2)

            space_text = font.render("Space", True, white)
            space_text_rect = space_text.get_rect(center=spacebar_rect.center)
            self.screen.blit(space_text, space_text_rect)  

            leave_trail_text = font.render("Leave Trail", True, white)
            self.screen.blit(leave_trail_text, (base_x + 20, base_y + 110))

            select_text = font.render("Select Items", True, white)
            self.screen.blit(select_text, (base_x + 19 + 120, base_y + 10))

            q_text = font.render("Q", True, white)
            box_rect = self.pygame.Rect(base_x + 154, base_y + 10 + 35, 30, 30)
            self.pygame.draw.rect(self.screen, dark_gray, box_rect)
            self.pygame.draw.rect(self.screen, white, box_rect, 2)
            text_rect = q_text.get_rect(center=box_rect.center)
            self.screen.blit(q_text, text_rect)

            e_text = font.render("E", True, white)
            box_rect = self.pygame.Rect(base_x + 189, base_y + 10 + 35, 30, 30)
            self.pygame.draw.rect(self.screen, dark_gray, box_rect)
            self.pygame.draw.rect(self.screen, white, box_rect, 2)
            text_rect = e_text.get_rect(center=box_rect.center)
            self.screen.blit(e_text, text_rect)

            use_text = font.render("Use Item", True, white)
            self.screen.blit(use_text, (base_x + 19 + 132, base_y + 110))
            f_text = font.render("F", True, white)
            box_rect = self.pygame.Rect(base_x + 170, base_y + 130, 30, 30)
            self.pygame.draw.rect(self.screen, dark_gray, box_rect)
            self.pygame.draw.rect(self.screen, white, box_rect, 2)
            text_rect = f_text.get_rect(center=box_rect.center)
            self.screen.blit(f_text, text_rect)


    def generate_items(self):
        for item in self.items:
            ok = False
            while(not ok or self.map[y][x] == 0 or (x == self.start[0] and y == self.start[1]) or (x == self.end[0] and y == self.end[1])):       
                x = random.randint(0, self.engine.mapX)
                y = random.randint(0, self.engine.mapY)
                x = x * 2 + 1
                y = y * 2 + 1
                ok = True
                for other in self.items:
                    if(other.X == x and other.Y == y and other != item):
                        ok = False
                        break
            item.X = x
            item.Y = y

        for item in self.items:
            item.X = item.X * self.cellsize + self.cellsize / 2
            item.Y = item.Y * self.cellsize + self.cellsize / 2
        
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

        self.engine.target = Target(targetX, targetY, self.engine.config.obj_radius) 
        self.target = self.engine.target
        self.target.open = False

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
    def draw_items_overlay(self):
        dark_gray = (60, 60, 60, 68)  
        black = (20, 20, 20, 128)
        white = (255, 255, 255, 128)

        base_x = 20
        base_y = 20

        offset_x = base_x + 10

        overlay = self.pygame.Surface((210, 100), self.pygame.SRCALPHA)
        overlay.fill(black)  
        self.engine.screen.blit(overlay, (base_x - 5, base_y))  

        for item in self.picked_up_items:
            if(item.used):
                continue
            renderx = offset_x
            rendery = base_y + 10
            offset_x += 80 + 10
            item_sprite = item.texture.convert_alpha()
            scaled = self.pygame.transform.scale(item_sprite, (80, 80))
            self.screen.blit(scaled, (renderx, rendery))
            if(item.selected):
                sel_sprite = self.engine.selected_sprite.convert_alpha()
                scaled = self.pygame.transform.scale(sel_sprite, (80, 80))
                self.screen.blit(scaled, (renderx, rendery))

    def draw_items(self):
        for item in self.items:
            if(item.picked_up):
                continue
            renderx = (item.X - self.player.X + self.engine.screen.get_width() // 2)
            rendery = (item.Y - self.player.Y + self.engine.screen.get_height() // 2)
            if(renderx + self.cellsize < 0 or rendery + self.cellsize < 0 or renderx > self.engine.screen.get_width() or rendery > self.engine.screen.get_height()):
                continue
            sprite = item.texture.convert_alpha()
            scaled = self.pygame.transform.scale(sprite, (item.R * 2, item.R * 2))
            self.screen.blit(scaled, (renderx - item.R, rendery - item.R))

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
        
        if(self.is_within_target_range([newX, newY]) and self.target.open):
            self.engine.page = self.engine.swap_to_score(self.pygame.time.get_ticks(), self.map, self.end, self.start)

        for item in self.items:
            if(item.picked_up):
                continue
            if((newX - item.X) * (newX - item.X) + (newY - item.Y) * (newY - item.Y) < (self.player.R + item.R) * (self.player.R + item.R)):
                item.picked_up = True
                self.picked_up_items.append(item)
                if(not self.any_items_selected()):
                    item.selected = True
                print("Picked up item")

        return True
    
    def any_items_selected(self):
        for item in self.items:
            if(item.selected):
                return True
        return False

    def select_next_item(self):
        for i in range(len(self.picked_up_items)):
            if(self.picked_up_items[i].selected):
                self.picked_up_items[i].selected = False
                self.picked_up_items[(i + 1) % len(self.picked_up_items)].selected = True
                break
    def select_prev_item(self):
        for i in range(len(self.picked_up_items)):
            if(self.picked_up_items[i].selected):
                self.picked_up_items[i].selected = False
                self.picked_up_items[(i - 1) % len(self.picked_up_items)].selected = True
                break

    def use_selected_item(self):
        for item in self.picked_up_items:
            if(item.selected):
                if(self.use_item(item)):
                    self.select_next_item()
                    self.picked_up_items.remove(item)          
                break

    def use_item(self, item):
        if(isinstance(item, Energy_Drink)):
            self.player.speed += 2
            return True
        if(isinstance(item, Key)):
            if(self.is_within_target_range([self.player.X, self.player.Y])):
                self.target.open = True
                return True
        return False
    
    def is_within_target_range(self, player_coords):
        return (player_coords[0] - self.target.X) * (player_coords[0] - self.target.X) + (player_coords[1] - self.target.Y) * (player_coords[1] - self.target.Y) + 64 < (self.player.R + self.target.R) * (self.player.R + self.target.R)


    
    def handle_event(self, event):
        if(event.type == self.pygame.KEYDOWN):
            if(
                event.key == self.pygame.K_w or
                event.key == self.pygame.K_s or
                event.key == self.pygame.K_a or
                event.key == self.pygame.K_d
                ):
                    self.player.moving = True
            if(event.key == self.pygame.K_q):
                self.select_prev_item()
            if(event.key == self.pygame.K_e):
                self.select_next_item()
            if(event.key == self.pygame.K_f):
                self.use_selected_item()

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


