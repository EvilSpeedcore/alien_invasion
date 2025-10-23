from typing import TYPE_CHECKING

import pygame
import pygame.font

from game.images import load_image

if TYPE_CHECKING:
    from game.screen import Screen


class Button:

    def __init__(self, screen: "Screen", message: str) -> None:
        self.screen = screen
        self.screen_rect = screen.rect
        self.button_image = load_image("button1.png")
        self.button_color = (176, 186, 231)
        self.hover_text_color = (150, 255, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont("tahoma", 40)
        self.ellipse_rect = self.button_image.get_rect()
        self.ellipse_rect.centerx = self.screen_rect.centerx
        self.ellipse_rect.centery = self.screen_rect.centery
        self.prepare_message(message)

    def prepare_message(self, message: str) -> None:
        """Turn message to Surface subject.

        Args:
            :param str message: Button label.

        """
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
