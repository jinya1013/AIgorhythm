import pygame

from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario

windowSize = 640, 480


def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    display_size = screen.get_size()
    game_surface = pygame.Surface(windowSize)
    max_frame_rate = 60
    dashboard = Dashboard("./img/font.png", 8, game_surface)
    sound = Sound()
    level = Level(game_surface, sound, dashboard)
    menu = Menu(game_surface, dashboard, level, sound)

    while not menu.start:
        menu.update()
        # Scale and blit to full screen
        scaled_surface = pygame.transform.scale(game_surface, display_size)
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    mario = Mario(0, 0, level, game_surface, dashboard, sound)
    clock = pygame.time.Clock()

    while not mario.restart:
        pygame.display.set_caption(
            "Super Mario running with {:d} FPS".format(int(clock.get_fps()))
        )
        if mario.pause:
            mario.pauseObj.update()
        else:
            level.drawLevel(mario.camera)
            dashboard.update()
            mario.update()
        # Scale and blit to full screen
        scaled_surface = pygame.transform.scale(game_surface, display_size)
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        clock.tick(max_frame_rate)
    return "restart"


if __name__ == "__main__":
    exitmessage = "restart"
    while exitmessage == "restart":
        exitmessage = main()
