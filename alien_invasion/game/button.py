from typing import TYPE_CHECKING

import pygame
import pygame.font
from pygame.color import Color

from game.images import load_image

if TYPE_CHECKING:
    from pygame.surface import Surface

    from game.screen import Screen


class Button:
    def __init__(self,
                 screen: "Screen",
                 image: "Surface",
                 position: tuple[int, int],
                 message: str,
                 button_color: Color | None = None,
                 text_color: Color | None = None,
                 hover_text_color: Color | None = None,
                 font: pygame.font.Font | None = None) -> None:
        self.screen = screen
        self.image = image
        self.message = message
        self.button_color = button_color or Color(176, 186, 231)
        self.text_color = text_color or Color(255, 255, 255)
        self.hover_text_color = hover_text_color or Color(150, 255, 255)
        self.font = font or pygame.font.SysFont("tahoma", 40)

        self.ellipse_rect = self.image.get_rect()
        self.ellipse_rect.centerx, self.ellipse_rect.centery = position
        self.prepare_message(message)

    def prepare_message(self, message: str) -> None:
        self.msg_image = self.font.render(message, True, self.text_color, self.button_color)  # noqa: FBT003
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.ellipse_rect.center

    def update(self) -> None:
        if not self.ellipse_rect.collidepoint(pygame.mouse.get_pos()):
            self.prepare_message(self.message)
            return

        self.msg_image = self.font.render(self.message, True, self.hover_text_color, self.button_color)  # noqa: FBT003
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.ellipse_rect.center

    def draw(self) -> None:
        self.screen.it.blit(self.image, self.ellipse_rect)
        self.screen.it.blit(self.msg_image, self.msg_image_rect)


class StartButton(Button):
    IMAGE = load_image("button.png")

    def __init__(self, screen: "Screen") -> None:
        position = (screen.rect.centerx, screen.rect.centery)
        super().__init__(screen=screen, image=self.IMAGE, position=position, message="Start")
