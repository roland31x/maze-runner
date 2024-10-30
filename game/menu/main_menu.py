from game.page import Page

class MainMenu(Page):
    def __init__(self, engine):
        self.playhover = False
        self.generated = self.showcase()
        super().__init__(engine)

    def render(self):
        self.engine.screen.fill(self.engine.config.dark_gray)

        font = self.pygame.font.SysFont(None, 74)
        title_text = font.render('Maze Runner', True, self.engine.config.light_gray)
        title_rect = title_text.get_rect(center=(self.engine.screen.get_width() // 2, 100))
        self.engine.screen.blit(title_text, title_rect)

        button_font = self.pygame.font.SysFont(None, 50)
        button_text = button_font.render('Play', True, (255, 255, 255))
        button_color = (0, 80, 0) if not self.playhover else (0, 180, 0)
        button_rect = self.pygame.draw.rect(self.engine.screen, button_color, (self.engine.screen.get_width() // 2 - 100, self.engine.screen.get_height() // 2 + 220, 200, 100))
        text_rect = button_text.get_rect(center=button_rect.center)
        self.engine.screen.blit(button_text, text_rect)


        self.draw_showcase()
        self.draw_player()

    
    def handle_event(self, event):
        if(event.type == self.pygame.MOUSEBUTTONDOWN):
            if(event.button == 1):
                if(self.engine.screen.get_width() // 2 - 100 <= event.pos[0] <= self.engine.screen.get_width() // 2 + 100 and self.engine.screen.get_height() // 2 + 220 <= event.pos[1] <= self.engine.screen.get_height() // 2 + 320):
                    self.engine.page = self.engine.swap_to_map_gen()
        elif(event.type == self.pygame.MOUSEMOTION):
            if(self.engine.screen.get_width() // 2 - 100 <= self.pygame.mouse.get_pos()[0] <= self.engine.screen.get_width() // 2 + 100 and self.engine.screen.get_height() // 2 + 220 <= self.pygame.mouse.get_pos()[1] <= self.engine.screen.get_height() // 2 + 320):
                self.playhover = True
            else:
                self.playhover = False

    def draw_player(self):
        sprite = self.engine.player.sprites[2][int((self.pygame.time.get_ticks() // 100)) % 4].convert_alpha()
        scaled = self.pygame.transform.scale(sprite, (300, 300))
        self.screen.blit(scaled, (self.engine.screen.get_width() // 2 - 150, self.engine.screen.get_height() // 2 - 150))

    def draw_showcase(self):
        max_height = 400
        max_width = 400
        cell_height = max_height // len(self.generated)
        cell_width = max_width // len(self.generated[0])

        if(cell_height > cell_width):
            offset_x = self.engine.screen.get_width() / 2 - max_width / 2
            offset_y = self.engine.screen.get_height() / 2 - (len(self.generated) * cell_width) / 2
        else:
            offset_x = self.engine.screen.get_width() / 2 - (len(self.generated[0]) * cell_height) / 2
            offset_y = self.engine.screen.get_height() / 2 - max_height / 2

        for y in range(len(self.generated)):
            for x in range(len(self.generated[y])):
                color = self.engine.config.black  # Default to black for 0  
                if self.generated[y][x] == 1:
                    color = self.engine.config.light_gray  # h for 1
                self.pygame.draw.rect(self.engine.screen, color, (offset_x + x * cell_height, offset_y + y * cell_height, cell_height, cell_height))

    def showcase(self):
        maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, ],
                [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, ],
                [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, ],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, ],
                [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, ],
                [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, ],
                [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, ],
                [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, ],
                [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, ],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, ],
                [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, ],
                [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, ],
                [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, ],
                [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, ],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, ],
                [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, ],
                [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, ],
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, ],
                [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],]
        return maze