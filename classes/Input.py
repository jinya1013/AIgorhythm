import os
import random
import sys

import numpy as np
import pygame
from pygame.locals import K_LEFT, K_LSHIFT, K_RIGHT, K_SPACE, K_UP, K_h, K_k, K_l

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

prograssion_indices = [0, 2, 4, 5, 7, 9, 11]


def freq_to_note(freq):
    if freq == 0:
        return None, None
    A4 = 440.0
    n = int(round(12 * np.log2(freq / A4)))
    note_number = n + 69
    octave = note_number // 12 - 1
    note_index = note_number % 12
    return NOTE_NAMES[note_index], octave


class Input:
    def __init__(self, entity):
        self.mouseX = 0
        self.mouseY = 0
        self.entity = entity
        # self.targetKeyIndex = random.randint(0, 11)
        self.targetKeyIndex = 0
        self.targetNote = NOTE_NAMES[self.targetKeyIndex]

        self.counter = 0

    def checkForInput(self):
        events = pygame.event.get()
        self.checkForKeyboardInput()
        self.checkForFileInput()
        self.checkForMouseInput(events)
        self.checkForQuitAndRestartInputEvents(events)

    def checkForKeyboardInput(self):
        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[K_LEFT] or pressedKeys[K_h] and not pressedKeys[K_RIGHT]:
            self.entity.traits["goTrait"].direction = -1
        elif pressedKeys[K_RIGHT] or pressedKeys[K_l] and not pressedKeys[K_LEFT]:
            self.entity.traits["goTrait"].direction = 1
        else:
            self.entity.traits["goTrait"].direction = 0

        isJumping = pressedKeys[K_SPACE] or pressedKeys[K_UP] or pressedKeys[K_k]
        self.entity.traits["jumpTrait"].jump(isJumping)

        self.entity.traits["goTrait"].boost = pressedKeys[K_LSHIFT]

    def checkForMouseInput(self, events):
        mouseX, mouseY = pygame.mouse.get_pos()
        if self.isRightMouseButtonPressed(events):
            self.entity.levelObj.addKoopa(
                mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
            )
            self.entity.levelObj.addGoomba(
                mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
            )
            self.entity.levelObj.addRedMushroom(
                mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
            )
        if self.isLeftMouseButtonPressed(events):
            self.entity.levelObj.addCoin(
                mouseX / 32 - self.entity.camera.pos.x, mouseY / 32
            )

    def checkForQuitAndRestartInputEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (
                event.key == pygame.K_ESCAPE or event.key == pygame.K_F5
            ):
                self.entity.pause = True
                self.entity.pauseObj.createBackgroundBlur()

    def isLeftMouseButtonPressed(self, events):
        return self.checkMouse(events, 1)

    def isRightMouseButtonPressed(self, events):
        return self.checkMouse(events, 3)

    def checkMouse(self, events, button):
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP and e.button == button:
                return True
        return False

    def checkForFileInput(self):
        with open("pitch.txt", "r") as f:
            file_content = f.readlines()

        if file_content:
            (
                pitch,
                magnitude,
                note,
                octave,
            ) = file_content[-1].split(",")
            print(f"pitch: {pitch}, magnitude: {magnitude}, note: {note}")
            # if float(magnitude) > 30:
            #     if float(pitch) > 700:
            #         self.entity.traits["jumpTrait"].jump(True)
            #     else:
            #         pass
            #     if float(pitch) > 500:
            #         self.entity.traits["goTrait"].direction = 1
            # else:
            #     self.entity.traits["goTrait"].direction = 0
            if float(magnitude) > 0.7:
                print(
                    f"note: {note}, targetNote: {self.targetNote}, note == targetNote: {note == self.targetNote}"
                )
                if note == self.targetNote:
                    self.entity.traits["jumpTrait"].jump(True)
            self.entity.traits["goTrait"].direction = 1

            # target note
            font = pygame.font.Font(None, 30)
            if self.counter % 480 == 0:
                self.targetNote = NOTE_NAMES[
                    (
                        self.targetKeyIndex
                        + prograssion_indices[(self.counter // 30) % 7]
                    )
                    % 12
                ]

            # Draw TARGET note with background and border
            text_surf = font.render(f"TARGET: {self.targetNote}", True, (0, 0, 0))
            text_rect = text_surf.get_rect(
                bottomleft=(10, self.entity.screen.get_height() - 10)
            )
            # Background
            bg_rect = text_rect.inflate(10, 6)
            pygame.draw.rect(self.entity.screen, (255, 255, 200), bg_rect)
            # Border
            pygame.draw.rect(self.entity.screen, (0, 0, 0), bg_rect, 2)
            self.entity.screen.blit(text_surf, text_rect)

            # Draw CURRENT note with background and border
            font = pygame.font.Font(None, 30)
            text_surf = font.render(f"CURRENT: {note}", True, (0, 0, 0))
            text_rect = text_surf.get_rect(
                bottomleft=(10, self.entity.screen.get_height() - 35)
            )
            bg_rect = text_rect.inflate(10, 6)
            pygame.draw.rect(self.entity.screen, (220, 240, 255), bg_rect)
            pygame.draw.rect(self.entity.screen, (0, 0, 0), bg_rect, 2)
            self.entity.screen.blit(text_surf, text_rect)

            # Draw guiding arrow at top right with background
            if note in NOTE_NAMES and self.targetNote in NOTE_NAMES:
                note_idx = NOTE_NAMES.index(note)
                target_idx = NOTE_NAMES.index(self.targetNote)
                arrow_font = pygame.font.Font(None, 50)
                if note_idx < target_idx:
                    # Draw up arrow
                    arrow_surf = arrow_font.render("GO UP!!", True, (0, 128, 0))
                elif note_idx > target_idx:
                    # Draw down arrow
                    arrow_surf = arrow_font.render("GO DOWN!!", True, (200, 0, 0))
                else:
                    arrow_surf = None
                if arrow_surf:
                    screen_width = self.entity.screen.get_width()
                    screen_height = self.entity.screen.get_height()
                    arrow_rect = arrow_surf.get_rect(
                        bottomright=(screen_width - 20, screen_height - 20)
                    )
                    bg_rect = arrow_rect.inflate(20, 10)
                    pygame.draw.rect(self.entity.screen, (255, 255, 200), bg_rect)
                    pygame.draw.rect(self.entity.screen, (0, 0, 0), bg_rect, 2)
                    self.entity.screen.blit(arrow_surf, arrow_rect)

            pygame.display.update()

        self.counter += 1


if __name__ == "__main__":
    a = []
    with open(os.path.join("file.txt"), mode="r") as f:
        for line in f.readlines():
            a.extend(line.split())

    breakpoint()
