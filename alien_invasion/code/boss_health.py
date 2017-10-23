import pygame
from pygame.sprite import Sprite
from os import path


class BossHealth(Sprite):
    """Parent class, which represents health and shield bar of boss."""
    def __init__(self, ai_settings, screen):
        """Initialize boss health.

        Args:
            :param ai_settings: Instance of Settings class.
            :param screen: Display Surface.

        """
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        # Directory which stores black hole images.
        self.img_dir = None

        # List, which will contain loaded images.
        self.hp_images = []

        # List for names of images in directory.
        self.hp_list = []

    def prepare_images(self):
        """Add loaded images to list."""
        for hp in self.hp_list:
            self.hp_images.append(pygame.image.load(path.join(self.img_dir, hp)))


class GreenBossHealth(BossHealth):
    """Child class of BossHealth class, which represents health and shield of green boss."""

    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings, screen)
        self.img_dir = path.join('images', 'green_boss_hp')
        self.hp_list = ['1_hp.png', '2_hp.png', '3_hp.png', '4_hp.png', '5_hp.png',
                        '6_hp.png', '7_hp.png', '8_hp.png', '9_hp.png', '10_hp.png',
                        '1_shield.png', '2_shield.png', '3_shield.png', '4_shield.png', '5_shield.png',
                        '6_shield.png', '7_shield.png', '8_shield.png', '9_shield.png', '10_shield.png']

        # Load of image, which represents health bar of undamaged boss.
        self.image = pygame.image.load('images/green_boss_hp/10_hp.png')

        # Rectangular area of the image.
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()

        # To make an dynamic health bar, we store several loaded images in list to iterate through it later.
        self.prepare_images()


class RedBossHealth(BossHealth):
    """Child class of BossHealth class, which represents health and shield of red boss."""
    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings, screen)
        self.img_dir = path.join('images', 'red_boss_hp')
        self.hp_list = ['1_hp.png', '2_hp.png', '3_hp.png', '4_hp.png', '5_hp.png',
                        '6_hp.png', '7_hp.png', '8_hp.png', '9_hp.png', '10_hp.png',
                        '1_shield.png', '2_shield.png', '3_shield.png', '4_shield.png', '5_shield.png']
        self.image = pygame.image.load('images/red_boss_hp/10_hp.png')
        self.rect = self.image.get_rect()
        self.prepare_images()


class BlueBossHealth(BossHealth):
    """Child class of BossHealth class, which represents health and shield of blue boss."""
    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings, screen)
        self.img_dir = path.join('images', 'blue_boss_hp')
        self.hp_list = ['1_hp.png', '2_hp.png', '3_hp.png', '4_hp.png', '5_hp.png',
                        '6_hp.png', '7_hp.png', '8_hp.png', '9_hp.png', '10_hp.png',
                        '1_shield.png', '2_shield.png', '3_shield.png', '4_shield.png', '5_shield.png',
                        '6_shield.png', '7_shield.png', '8_shield.png', '9_shield.png', '10_shield.png']
        self.image = pygame.image.load('images/blue_boss_hp/10_hp.png')
        self.rect = self.image.get_rect()
        self.prepare_images()
