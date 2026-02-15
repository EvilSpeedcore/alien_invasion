from typing import TYPE_CHECKING

import pygame
import pygame.font
from pygame.color import Color

from game.images import load_image

if TYPE_CHECKING:
    from pygame.surface import Surface


class Button:
    IMAGE = load_image("button.png")

    def __init__(self,
                 surface: "Surface",
                 position: dict[str, tuple[int, int]],
                 message: str,
                 button_color: Color | None = None,
                 text_color: Color | None = None,
                 hover_text_color: Color | None = None,
                 font: pygame.font.Font | None = None) -> None:
        self.surface = surface
        self.image = self.IMAGE
        self.message = message
        self.button_color = button_color or Color(176, 186, 231)
        self.text_color = text_color or Color(255, 255, 255)
        self.hover_text_color = hover_text_color or Color(150, 255, 255)
        self.font = font or pygame.font.SysFont("tahoma", 40)

        self.ellipse_rect = self.image.get_rect(**position)
        self.prepare_message(message)

    def prepare_message(self, message: str) -> None:
        self.msg_image = self.font.render(message, True, self.text_color, self.button_color)  # noqa: FBT003
        self.msg_image_rect = self.msg_image.get_rect(center=self.ellipse_rect.center)

    def update(self, mouse_position: tuple[float, float] | None = None) -> None:
        if mouse_position is None:
            mouse_position = pygame.mouse.get_pos()

        if not self.ellipse_rect.collidepoint(mouse_position):
            self.prepare_message(self.message)
            return

        self.msg_image = self.font.render(self.message, True, self.hover_text_color, self.button_color)  # noqa: FBT003
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.ellipse_rect.center

    def draw(self) -> None:
        self.surface.blit(self.image, self.ellipse_rect)
        self.surface.blit(self.msg_image, self.msg_image_rect)
