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
                 button_color: Color,
                 text_color: Color,
                 hover_text_color: Color,
                 font: pygame.font.Font) -> None:
        self.screen = screen
        self.button_image = image
        self.button_color = button_color
        self.text_color = text_color
        self.hover_text_color = hover_text_color
        self.font = font
        self.ellipse_rect = self.button_image.get_rect()
        self.ellipse_rect.centerx, self.ellipse_rect.centery = position
        self.prepare_message(message)

    def prepare_message(self, message: str) -> None:
        """Turn message to Surface subject."""
        if self.ellipse_rect.collidepoint(pygame.mouse.get_pos()):
            self.msg_image = self.font.render(message, True, self.hover_text_color, self.button_color)  # noqa: FBT003
            self.msg_image_rect = self.msg_image.get_rect()
            self.msg_image_rect.center = self.ellipse_rect.center
        else:
            self.msg_image = self.font.render(message, True, self.text_color, self.button_color)  # noqa: FBT003
            self.msg_image_rect = self.msg_image.get_rect()
            self.msg_image_rect.center = self.ellipse_rect.center

    def draw_button(self) -> None:
        """Draw button with text on screen."""
        self.screen.it.blit(self.button_image, self.ellipse_rect)
        self.screen.it.blit(self.msg_image, self.msg_image_rect)


class StartButton(Button):
    IMAGE = load_image("button1.png")

    def __init__(self, screen: "Screen") -> None:
        super().__init__(screen=screen,
                         image=self.IMAGE,
                         position=(screen.rect.centerx, screen.rect.centery),
                         message="Start",
                         button_color=Color(176, 186, 231),
                         text_color=Color(255, 255, 255),
                         hover_text_color=Color(150, 255, 255),
                         font=pygame.font.SysFont("tahoma", 40))
