from game.page import Page
from game.player import Target, ConfigObjectDrawable
from numpy import random
from game.maze.items.energy_drink import Energy_Drink
from game.maze.items.key import Key
from game.maze.items.magnifying_glass import Magnifying_Glass
from game.maze.items.maze_map import Maze_Map

class Maze(Page):
    def __init__(self, engine, map, tilemap):
        super().__init__(engine)
        self.map = map
        self.tilemap = tilemap
        self.player = engine.player
        self.target = None
        self.start = [0,0]
        self.end = [0,0]
        self.dirs = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        self.finished = False
        self.trails = []
        self.items = [
            Key(0, 0, engine.config),
            Energy_Drink(0, 0, engine.config),
            Magnifying_Glass(0, 0, engine.config),
            Maze_Map(0, 0, engine.config)
        ]
        self.engine.default()
        self.picked_up_items = []
        self.available_trails = 2 * max(len(map), len(map[0]))
        self.max_trails = 2 * max(len(map), len(map[0]))
        self.draw_mini_map = False

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
        if(self.draw_mini_map):
            self.draw_mini_map_overlay()

    def draw_mini_map_overlay(self):
        overlay_sprite = self.engine.map_overlay
        scaled = self.pygame.transform.scale(overlay_sprite, (700, 700))
        self.screen.blit(scaled, (self.engine.screen.get_width() // 2 - 350, self.engine.screen.get_height() // 2 - 350))

        max_height = 350
        max_width = 350
        cell_height = max_height // len(self.map)
        cell_width = max_width // len(self.map[0])

        if(cell_height < cell_width):
            offset_x = self.engine.screen.get_width() / 2 - (len(self.map[0]) * cell_height) / 2
            offset_y = self.engine.screen.get_height() / 2 - (len(self.map) * cell_height) / 2
        else:
            offset_x = self.engine.screen.get_width() / 2 - (len(self.map[0]) * cell_width) / 2
            offset_y = self.engine.screen.get_height() / 2 - (len(self.map) * cell_width) / 2

        offset_y -= 30

        cell_height = min(cell_height, cell_width)

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == 1:
                    continue
                color = self.engine.config.black  # Default to black for 0
                self.pygame.draw.rect(self.engine.screen, color, (offset_x + x * cell_height, offset_y + y * cell_height, cell_height, cell_height)) 

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
            item.X = item.X * self.engine.config.cellsize + self.engine.config.cellsize / 2
            item.Y = item.Y * self.engine.config.cellsize + self.engine.config.cellsize / 2
        
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

        targetX = (targetX * 2 + 1) * self.engine.config.cellsize + self.engine.config.cellsize / 2
        targetY = (targetY * 2 + 1) * self.engine.config.cellsize + self.engine.config.cellsize / 2

        self.engine.target = Target(targetX, targetY, self.engine.config) 
        self.target = self.engine.target
        self.target.open = False

        self.player.X = (startX * 2 + 1) * self.engine.config.cellsize + self.engine.config.cellsize / 2
        self.player.Y = (startY * 2 + 1) * self.engine.config.cellsize + self.engine.config.cellsize / 2
        
    def draw_maze(self):
        for y in range(max(0, int(self.player.Y // self.engine.config.cellsize - 10)), min(len(self.map), int(self.player.Y // self.engine.config.cellsize + 10))):
            for x in range(max(0, int(self.player.X // self.engine.config.cellsize - 10)), min(len(self.map[0]), int(self.player.X // self.engine.config.cellsize + 10))):              
                    renderx = (x * self.engine.config.cellsize - self.player.X + self.engine.screen.get_width() // 2)
                    rendery = (y * self.engine.config.cellsize - self.player.Y + self.engine.screen.get_height() // 2)
                    if(renderx + self.engine.config.cellsize < 0 or rendery + self.engine.config.cellsize < 0 or renderx > self.engine.screen.get_width() or rendery > self.engine.screen.get_height()):
                        continue
                    sprite = self.tilemap[y][x] if self.map[y][x] == 0 else self.engine.floor
                    scaled = self.pygame.transform.scale(sprite, (self.engine.config.cellsize, self.engine.config.cellsize))
                    self.screen.blit(scaled, (renderx, rendery))
                    # self.pygame.draw.rect(self.engine.screen, self.engine.config.light_gray, (renderx, rendery, self.engine.config.cellsize, self.engine.config.cellsize))

    def draw_items_overlay(self):
        dark_gray = (60, 60, 60, 68)  
        black = (20, 20, 20, 128)
        white = (255, 255, 255, 128)

        base_x = 20
        base_y = 20

        offset_x = base_x + 10

        overlay = self.pygame.Surface((380, 100), self.pygame.SRCALPHA)
        overlay.fill(black)  
        self.engine.screen.blit(overlay, (base_x - 5, base_y))  

        for item in self.picked_up_items:
            if(item.used):
                continue
            renderx = offset_x
            rendery = base_y + 10
            offset_x += 80 + 10
            item_sprite = item.texture
            scaled = self.pygame.transform.scale(item_sprite, (80, 80))
            self.screen.blit(scaled, (renderx, rendery))
            if(item.selected):
                sel_sprite = self.engine.selected_sprite
                scaled = self.pygame.transform.scale(sel_sprite, (80, 80))
                self.screen.blit(scaled, (renderx, rendery))

    def draw_items(self):
        for item in self.items:
            if(item.picked_up):
                continue
            renderx = (item.X - self.player.X + self.engine.screen.get_width() // 2)
            rendery = (item.Y - self.player.Y + self.engine.screen.get_height() // 2)
            if(renderx + self.engine.config.cellsize < 0 or rendery + self.engine.config.cellsize < 0 or renderx > self.engine.screen.get_width() or rendery > self.engine.screen.get_height()):
                continue
            sprite = item.texture.convert_alpha()
            radius = item.R()
            scaled = self.pygame.transform.scale(sprite, (radius * 2, radius * 2))
            self.screen.blit(scaled, (renderx - radius, rendery - radius))

    def draw_target(self):
        renderx = (self.target.X - self.player.X + self.engine.screen.get_width() // 2)
        rendery = (self.target.Y - self.player.Y + self.engine.screen.get_height() // 2)
        tradius = self.target.R()
        if(renderx + tradius < 0 or rendery + tradius < 0 or renderx > self.engine.screen.get_width() or rendery > self.engine.screen.get_height()):
            return
        sprite = self.target.sprites[self.target.open].convert_alpha()
        scaled = self.pygame.transform.scale(sprite, (tradius * 2, tradius * 2))
        self.screen.blit(scaled, (renderx - tradius, rendery - tradius))

    def draw_player(self):
        sprite = self.player.sprites[self.player.last_dir][0 if not self.player.moving else int((self.pygame.time.get_ticks() // 100)) % 4].convert_alpha()
        pradius = self.player.R()
        scaled = self.pygame.transform.scale(sprite, (pradius * 2, pradius * 2))
        self.screen.blit(scaled, (self.engine.screen.get_width() // 2 - pradius, self.engine.screen.get_height() // 2 - pradius))

    def draw_trails(self):
        radius = self.player.R()
        for trail in self.trails:
            x = trail[0]
            y = trail[1]
            renderx = (x - self.player.X + self.engine.screen.get_width() // 2)
            rendery = (y - self.player.Y + self.engine.screen.get_height() // 2)
            if(renderx + self.engine.config.cellsize < 0 or rendery + self.engine.config.cellsize < 0 or renderx > self.engine.screen.get_width() or rendery > self.engine.screen.get_height()):
                continue
            self.screen.blit(self.engine.paint, (renderx - radius, rendery - radius))

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

        left = newX - self.player.R()
        right = newX + self.player.R()
        top = newY - self.player.R()
        bottom = newY + self.player.R()

        if(left // self.engine.config.cellsize < 0 or top // self.engine.config.cellsize < 0 or right // self.engine.config.cellsize >= len(self.map[0]) or bottom // self.engine.config.cellsize >= len(self.map)):
            return False
        if(self.map[int(bottom // self.engine.config.cellsize)][int(right // self.engine.config.cellsize)] == 0 or 
           self.map[int(top // self.engine.config.cellsize)]   [int(left // self.engine.config.cellsize)]  == 0 or 
           self.map[int(top // self.engine.config.cellsize)]   [int(right // self.engine.config.cellsize)] == 0 or 
           self.map[int(bottom // self.engine.config.cellsize)][int(left // self.engine.config.cellsize)]  == 0):
            return False
        
        if(self.is_within_target_range([newX, newY]) and self.target.open):
            self.engine.page = self.engine.swap_to_score(self.pygame.time.get_ticks(), self.map, self.end, self.start)

        iradius = self.player.R()
        for item in self.items:
            if(item.picked_up):
                continue
            if((newX - item.X) * (newX - item.X) + (newY - item.Y) * (newY - item.Y) < (iradius + iradius) * (iradius + iradius)):
                item.picked_up = True
                self.picked_up_items.append(item)
                if(not self.any_items_selected()):
                    item.selected = True

        return True
    
    def any_items_selected(self):
        for item in self.picked_up_items:
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
            self.player.speed += self.player.speed / 3
            return True
        if(isinstance(item, Key)):
            if(self.is_within_target_range([self.player.X, self.player.Y])):
                self.target.open = True
                return True
        if(isinstance(item, Magnifying_Glass)):
            self.being_recalc()
            self.engine.config.cellsize = 200
            self.engine.config.obj_radius = 36
            self.finish_recalc()
            return True
        if(isinstance(item, Maze_Map)):
            if(item.is_in_use):
                self.draw_mini_map = False
                item.is_in_use = False
            else:
                self.draw_mini_map = True
                item.is_in_use = True
            return False
        return False
    
    def is_within_target_range(self, player_coords):
        pradius = self.player.R()
        tradius = self.target.R()
        return (player_coords[0] - self.target.X) * (player_coords[0] - self.target.X) + (player_coords[1] - self.target.Y) * (player_coords[1] - self.target.Y) + 64 < (pradius + tradius) * (pradius + tradius)

    def being_recalc(self):
        self.player.X = (self.player.X - self.engine.config.cellsize / 2) / self.engine.config.cellsize
        self.player.Y = (self.player.Y - self.engine.config.cellsize / 2) / self.engine.config.cellsize

        self.target.X = (self.target.X - self.engine.config.cellsize / 2) / self.engine.config.cellsize
        self.target.Y = (self.target.Y - self.engine.config.cellsize / 2) / self.engine.config.cellsize

        self.player.speed = self.engine.config.cellsize / self.player.speed

        for item in self.items:
            item.X = (item.X - self.engine.config.cellsize / 2) / self.engine.config.cellsize
            item.Y = (item.Y - self.engine.config.cellsize / 2) / self.engine.config.cellsize

    def finish_recalc(self):
        self.player.X = self.player.X * self.engine.config.cellsize + self.engine.config.cellsize / 2
        self.player.Y = self.player.Y * self.engine.config.cellsize + self.engine.config.cellsize / 2

        self.target.X = self.target.X * self.engine.config.cellsize + self.engine.config.cellsize / 2
        self.target.Y = self.target.Y * self.engine.config.cellsize + self.engine.config.cellsize / 2

        for item in self.items:
            item.X = item.X * self.engine.config.cellsize + self.engine.config.cellsize / 2
            item.Y = item.Y * self.engine.config.cellsize + self.engine.config.cellsize / 2

        self.player.speed = self.engine.config.cellsize / self.player.speed
    
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


