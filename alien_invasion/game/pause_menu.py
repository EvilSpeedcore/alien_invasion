from typing import TYPE_CHECKING

import pygame

from game.button import Button

if TYPE_CHECKING:
    from game.screen import Screen


class PauseMenu:

    def __init__(self, screen: "Screen") -> None:
        self.screen = screen

        self.size, self.radius = 350, 20
        self.menu_color = (173, 235, 235, 255)
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

        font = pygame.font.SysFont("tahoma", size=40)
        self.text_surface = font.render("PAUSED", True, (255, 255, 255))  # noqa: FBT003
        self.text_rect = self.text_surface.get_rect(midtop=(self.rect.centerx, 20))
        self.back_to_menu_button = Button(surface=self.surface,
                                          position={"midtop": (self.rect.centerx, 100)},
                                          message="Menu")

    def update(self) -> None:
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surface, self.menu_color, self.rect, border_radius=self.radius)
        self.surface.blit(self.text_surface, self.text_rect)
        self.back_to_menu_button.draw()
        self.screen.it.blit(
            self.surface,
            (self.screen.rect.centerx - self.size / 2,
             self.screen.rect.centery - self.size / 2),
        )
