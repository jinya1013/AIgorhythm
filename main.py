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
    screen = pygame.display.set_mode(windowSize)
    max_frame_rate = 60
    dashboard = Dashboard("./img/font.png", 8, screen)
    sound = Sound()
    level = Level(screen, sound, dashboard)
    menu = Menu(screen, dashboard, level, sound)

    while not menu.start:
        menu.update()

    mario = Mario(0, 0, level, screen, dashboard, sound)
    clock = pygame.time.Clock()

    # target_note = "C#"

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

        # try:
        #     note_text = f"NOTE: {target_note}"

        #     font_size = 8
        #     x_pos = 10
        #     y_pos = windowSize[1] - font_size - 10

        #     dashboard.draw_text(note_text, x_pos, y_pos)

        # except AttributeError:
        # font = pygame.font.Font(None, 30)
        # text_surf = font.render(f"NOTE: {target_note}", True, (255, 255, 255))
        # text_rect = text_surf.get_rect(bottomleft=(10, windowSize[1] - 10))
        # screen.blit(text_surf, text_rect)
        # pygame.display.update()
        clock.tick(max_frame_rate)
    return "restart"


if __name__ == "__main__":
    exitmessage = "restart"
    while exitmessage == "restart":
        exitmessage = main()
