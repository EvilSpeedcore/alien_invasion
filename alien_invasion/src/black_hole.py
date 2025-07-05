import random
from os import path

import pygame
from pygame.sprite import Sprite

from images import load_image
from paths import Paths


class BlackHole(Sprite):
    """Parent class, which represent BlackHoles spawn at last boss stage."""

    IMAGE_DIR = 'black_hole'

    def __init__(self, ai_settings, screen, ship):
        """Initialize black hole.

        Args:
            :param ai_settings: Instance of Settings class.
            :param screen: Display Surface..
            :param ship: Instance of Ship class.

        """
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # List, which will contain loaded images.
        self.images = []

        # List for names of images in directory.
        self.rt_list = ['black_hole_1.png', 'black_hole_2.png', 'black_hole_3.png', 'black_hole_4.png',
                        'black_hole_5.png', 'black_hole_6.png', 'black_hole_7.png', 'black_hole_8.png',
                        'black_hole_9.png', 'black_hole_10.png', 'black_hole_11.png', 'black_hole_12.png']

        # To make an animated black hole, we store several loaded images in list to iterate through it later.
        self.prepare_images()

        # load of black hole image to display it as static image.
        self.image = load_image('black_hole/black_hole_1.png')

        # Rectangular area of the image.
        self.rect = self.image.get_rect()

        # Black holes spawns in random area of screen from allowed coordinates.
        self.banned_coordinates_x_1 = [x for x in range(int(ship.centerx - 100.0), int(ship.centerx + 106.0))]
        self.banned_coordinates_x_2 = [x for x in range(int(self.screen_rect.centerx - 150.0),
                                                        int(self.screen_rect.centerx + 150.0))]
        self.banned_coordinates_x = list(set(self.banned_coordinates_x_1 + self.banned_coordinates_x_2))
        self.available_coordinates_x = [x for x in range(100, self.screen_rect.right - 100) if
                                        x not in self.banned_coordinates_x]
        self.banned_coordinates_y_1 = [y for y in range(int(ship.centery - 100.0), int(ship.centery + 106.0))]
        self.banned_coordinates_y_2 = [y for y in range(int(self.screen_rect.centery - 150.0),
                                                        int(self.screen_rect.centery + 150.0))]
        self.banned_coordinates_y = list(set(self.banned_coordinates_y_1 + self.banned_coordinates_y_2))
        self.available_coordinates_y = [y for y in range(100, self.screen_rect.bottom - 100) if
                                        y not in self.banned_coordinates_y]
        self.rect.centerx = random.choice(self.available_coordinates_x)
        self.rect.centery = random.choice(self.available_coordinates_y)

        # Black hole animation step counter.
        self.rt_image_number = 0

    def draw_black_hole(self):
        """Draw black hole on screen."""
        self.screen.blit(self.image, self.rect)

    def prepare_images(self):
        """Add loaded images to list."""
        for image in self.rt_list:
            self.images.append(load_image(f'{self.IMAGE_DIR}/{image}'))

    def update(self):
        """Change image of black hole to make animation effect."""
        hp_image = self.images[self.rt_image_number]
        self.image = hp_image.copy()
