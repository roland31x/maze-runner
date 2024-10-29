from game.page import Page

class Score(Page):
    def __init__(self, engine, score, maze, end, start):
        self.score = score
        self.maze = maze
        self.end = end
        self.start = start
        super().__init__(engine)

    def render(self):

        self.engine.screen.fill(self.engine.config.dark_gray)

        font = self.pygame.font.SysFont(None, 65)
        title = font.render('Game Over', True, (0, 0, 0))
        self.engine.screen.blit(title, (self.engine.screen.get_width() // 2 - title.get_rect().width // 2, 60))

        minutes = self.score // 60000
        seconds = (self.score - (minutes * 60000)) // 1000
        milliseconds = self.score - (minutes * 60000) - (seconds * 1000)

        timestr = str(minutes) + ":" if minutes > 0 else "" + str(seconds) + "." + str(milliseconds)

        font = self.pygame.font.SysFont(None, 45)
        score_text = font.render('Time: ' + timestr, True, (0, 0, 0))
        self.engine.screen.blit(score_text, (self.engine.screen.get_width() // 2 - score_text.get_rect().width // 2, 120))

        self.draw_maze()

        font = self.pygame.font.SysFont(None, 30)
        score_text = font.render('Press ENTER to return to the main menu', True, (0, 0, 0))
        self.engine.screen.blit(score_text, (self.engine.screen.get_width() // 2 - score_text.get_rect().width // 2, 600))

    def draw_maze(self):
            max_height = 400
            max_width = 400
            cell_height = max_height // len(self.maze)
            cell_width = max_width // len(self.maze[0])

            if(cell_height < cell_width):
                offset_x = self.engine.screen.get_width() / 2 - (len(self.maze[0]) * cell_height) / 2
                offset_y = self.engine.screen.get_height() / 2 - (len(self.maze) * cell_height) / 2
            else:
                offset_x = self.engine.screen.get_width() / 2 - (len(self.maze[0]) * cell_width) / 2
                offset_y = self.engine.screen.get_height() / 2 - (len(self.maze) * cell_width) / 2

            cell_height = min(cell_height, cell_width)

            offset_y += 20

            self.pygame.draw.rect(self.engine.screen, self.engine.config.white, (offset_x - 5, offset_y - 5, cell_width * len(self.maze[0]) + 10, cell_height * len(self.maze) + 10))

            for y in range(len(self.maze)):
                for x in range(len(self.maze[y])):
                    color = (30, 30, 30)  # Default to black for 0
                    if self.maze[y][x] == 1:
                        color = (180, 180, 180)  # Blue for 1
                    elif self.maze[y][x] == 2:
                        color = (255, 0, 0)  # Red for 2
                    self.pygame.draw.rect(self.engine.screen, color, (offset_x + x * cell_height, offset_y + y * cell_height, cell_height, cell_height))

            # for trail in self.trails:
            #     for x, y in trail:
            #         self.pygame.draw.rect(self.engine.screen, (0, 255, 0), (offset_x + x * cell_height, offset_y + y * cell_height, cell_height, cell_height))

            self.draw_player(cell_height, offset_x, offset_y)
            self.draw_target(cell_height, offset_x, offset_y)

    def draw_player(self, size, offset_x, offset_y):
        sprite = self.engine.player.sprites[2][0].convert_alpha()
        scaled = self.pygame.transform.scale(sprite, (size, size))
        self.screen.blit(scaled, (offset_x + self.start[0] * size, offset_y + self.start[1] * size, size, size))
        #print("Drawing player at " + str(self.start[0]) + ", " + str(self.start[1]))

    def draw_target(self, size, offset_x, offset_y):
        sprite = self.engine.target.sprites[1].convert_alpha()
        scaled = self.pygame.transform.scale(sprite, (size, size))
        self.screen.blit(scaled, (offset_x + self.end[0] * size, offset_y + self.end[1] * size, size, size))
        #print("Drawing target at " + str(self.end[0]) + ", " + str(self.end[1]))


    def handle_event(self, event):
        if(event.type == self.pygame.KEYDOWN):
            if(event.key == self.pygame.K_RETURN):
                self.engine.page = self.engine.swap_to_main_menu()