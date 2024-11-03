from game.page import Page
from numpy import random

class MapGen(Page):
    def __init__(self, engine):
        super().__init__(engine)
        self.cd = 6
        self.tilemap = []
        self.newMap(self.engine.mapX, self.engine.mapY)
        
    def render(self):
        self.engine.screen.fill(self.engine.config.dark_gray)
        # Render the title
        font = self.pygame.font.SysFont(None, 55)
 
        gen_title = 'Generating Maze'
        if(self.cd < 6):
            gen_title = 'Starting in ' + str(self.cd)
            if(self.cd == 1):
                # for row in self.generated:
                #     toprint = "["
                #     for cell in row:
                #         toprint += str(cell) + ", "
                #     toprint += "],"
                #     print(toprint)
                # print("")
                self.engine.page = self.engine.swap_to_maze(self.generated, self.tilemap)

        title = font.render(gen_title, True, self.engine.config.light_gray)
        self.engine.screen.blit(title, (self.engine.screen.get_width() // 2 - title.get_rect().width // 2, 110))

        # Calculate the loading bar dimensions
        bar_width = self.engine.screen.get_width() - 100
        bar_height = 50
        bar_x = 50
        bar_y = self.engine.screen.get_height() - 100 - bar_height // 2

        # Calculate the progress
        progress = self.done / self.needed if self.needed > 0 else 0
        fill_width = int(bar_width * progress)

        # Draw the loading bar background
        self.pygame.draw.rect(self.engine.screen, self.engine.config.white, (bar_x, bar_y, bar_width, bar_height))

        # Draw the filled part of the loading bar
        self.pygame.draw.rect(self.engine.screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))

        self.draw_maze()
        
    def draw_maze(self):
        max_height = 400
        max_width = 400
        cell_height = max_height // len(self.generated)
        cell_width = max_width // len(self.generated[0])

        if(cell_height < cell_width):
            offset_x = self.engine.screen.get_width() / 2 - (len(self.generated[0]) * cell_height) / 2
            offset_y = self.engine.screen.get_height() / 2 - (len(self.generated) * cell_height) / 2
        else:
            offset_x = self.engine.screen.get_width() / 2 - (len(self.generated[0]) * cell_width) / 2
            offset_y = self.engine.screen.get_height() / 2 - (len(self.generated) * cell_width) / 2

        cell_height = min(cell_height, cell_width)

        for y in range(len(self.generated)):
            for x in range(len(self.generated[y])):
                color = self.engine.config.black  # Default to black for 0
                if self.generated[y][x] == 1:
                    color = self.engine.config.light_gray  # Blue for 1
                elif self.generated[y][x] == 2:
                    color = (255, 0, 0)  # Red for 2
                self.pygame.draw.rect(self.engine.screen, color, (offset_x + x * cell_height, offset_y + y * cell_height, cell_height, cell_height))    
        
    def newMap(self, width, height) -> list:
        a_width = width * 2 + 1
        a_height = height * 2 + 1
        dirs = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        self.generated = [[0 for x in range(a_width)] for u in range(a_height)]
        self.tilemap = [[0 for x in range(a_width)] for u in range(a_height)]

        #print(len(self.generated))
        self.done = 0
        self.needed = width * height

        targetX = random.randint(0, width)
        targetY = random.randint(0, height)

        targetX = 2 * targetX + 1
        targetY = 2 * targetY + 1

        targetswapped = False

        while(self.done < self.needed - 1):
            #print("main loop")
            startX = random.randint(0, width - 1)
            startY = random.randint(0, height - 1)

            startX = 2 * startX + 1
            startY = 2 * startY + 1

            while((startX == targetX and startY == targetY) or self.generated[startY][startX] == 1):
                #print("starting point")
                if(self.needed - self.done < 4):
                    for y in range(0, height):
                        for x in range(0, width):
                            if(self.generated[2 * y + 1][2 * x + 1] == 0):
                                startX = x
                                startY = y
                                #print("new start: " + str(startX) + ", " + str(startY))
                else:                   
                    startX = random.randint(0, width)
                    startY = random.randint(0, height)

                startX = 2 * startX + 1
                startY = 2 * startY + 1
                #print("ah start: " + str(startX) + ", " + str(startY))      

            self.generated[startY][startX] = 2
            stack = []

            nextX = startX
            nextY = startY

            while((nextX != targetX or nextY != targetY) and self.generated[nextY][nextX] != 1):
                #print("random walk")

                if(len(stack) >= max(width, height) and not targetswapped):
                    targetX = nextX
                    targetY = nextY
                    targetswapped = True
                    break

                nextmove = random.randint(0, 4)

                if(len(stack) > 0):
                    if((stack[len(stack) - 1][2] + 2) % 4 == nextmove):
                        #print("don't walk where you came from")
                        continue

                nextX = startX + 2 * dirs[nextmove][1]
                nextY = startY + 2 * dirs[nextmove][0]

                self.render()
                self.pygame.event.pump()
                self.pygame.display.flip()

                # for row in self.generated:
                #     print("".join(str(cell) for cell in row))

                # print("")

                if(nextX >= 0 and nextX < a_width and nextY >= 0 and nextY < a_height):
                    if(self.generated[nextY][nextX] != 2):
                        self.generated[startY + dirs[nextmove][0]][startX + dirs[nextmove][1]] = 2
                        if(self.generated[nextY][nextX] == 0):
                            self.generated[nextY][nextX] = 2
                        stack.append([startY, startX, nextmove])
                        startX = nextX
                        startY = nextY
                    elif(self.generated[nextY][nextX] == 2):
                        while(startX != nextX or startY != nextY):
                            #print("backtrack")
                            self.generated[startY][startX] = 0
                            past = stack.pop()
                            self.generated[startY - dirs[past[2]][0]][startX - dirs[past[2]][1]] = 0
                            startX = past[1]
                            startY = past[0]
                else:
                    nextX = startX
                    nextY = startY
            

            
            for y in range(a_height):
                for x in range(a_width):
                    if(self.generated[y][x] == 2):
                        self.generated[y][x] = 1
            self.done += len(stack)

        self.done += 1

        for y in range(0, a_height):
            for x in range(0, a_width):
                if(self.generated[y][x] == 1):
                    continue
                wall = [0, 0, 0, 0]
                for dir in dirs:
                    if(y + dir[1] >= 0 and y + dir[1] < a_height and x + dir[0] >= 0 and x + dir[0] < a_width):
                        if(self.generated[y + dir[1]][x + dir[0]] == 0):
                            wall[dirs.index(dir)] = 1
                sprite = self.engine.walltiles[(wall[0], wall[1], wall[2], wall[3])].convert_alpha()
                self.tilemap[y][x] = sprite         
 

        for countdown in range(0, 5):
            self.cd = 5 - countdown

            self.render()
            self.pygame.event.pump()
            self.pygame.display.flip()

            self.pygame.time.delay(100)

        

        

