import pygame


class Screen:

    def __init__(self, width: int, height: int) -> None:
        self.it = pygame.display.set_mode((width, height))
        self.rect = self.it.get_rect()
