import pygame
import os
from .page import Page
from .pages import *
from .player import Player, Target
from .config import Config

class Engine:
    def __init__(self):
        self.page : Page = None
        self.config = Config()
        self.default()

    def default(self):
        self.config.default()
        self.player = 0
        self.score = 0
        self.level = 0
        self.mapX = self.config.sizeX
        self.mapY = self.config.sizeY
        self.player = Player("Player", self.config.player_speed, self.config)
        self.target = Target(self.mapX - 1, self.mapY - 1, self.config)

    def start(self):     
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.pygame = pygame
        self.paint = pygame.image.load('game/models/paint.png').convert_alpha()
        self.floor = pygame.image.load('game/models/floor.png').convert_alpha()
        self.selected_sprite = pygame.image.load('game/models/selected.png').convert_alpha()
        self.map_overlay = pygame.image.load('game/models/map_overlay.png').convert_alpha()
        self.walltiles = self.wall_tile_init()
        self.page = self.swap_to_main_menu()
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.page.handle_event(event)

            self.page.render()
            pygame.display.flip()
            self.clock.tick(60)      

    def stop(self):
        self.running = False

    def swap_to_maze(self, maze, tilemap):
        #print("Swapping to maze")
        page = Maze(self, maze, tilemap)
        return page

    def swap_to_score(self, score, maze, target, starting):
        #print("Swapping to score")
        page = Score(self, score, maze, target, starting)
        return page

    def swap_to_main_menu(self):
        #print("Swapping to main menu")
        page = MainMenu(self)
        return page

    def swap_to_map_gen(self):
        #print("Swapping to map gen")
        page = MapGen(self)
        return page
    
    def wall_tile_init(self):
        walltiles = {}
            
        for u in range(0,2):
            for d in range(0,2):
                for l in range(0,2):
                    for r in range(0,2):
                        if(os.path.exists('game/models/wall_' + str(u) + '_' + str(r) + '_' + str(d) + '_' + str(l) + '.png')):
                            walltiles[(u,r,d,l)] = pygame.image.load('game/models/wall_' + str(u) + '_' + str(r) + '_' + str(d) + '_' + str(l) + '.png').convert_alpha()
                            
        return walltiles    
        
        

def InitializeGame():
    return Engine()