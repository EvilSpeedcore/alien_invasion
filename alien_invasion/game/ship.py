from game.images import load_image


class Ship:
    """Class, which represents playable character in game - ship."""
    def __init__(self, ai_settings, screen):
        """Initialize ship.

        Args:
            :param ai_settings: Instance of Settings class.
            :param screen: Display Surface.

        """
        self.screen = screen
        self.ai_settings = ai_settings

        # Instead of rotation of one ship image, we upload several images for each ship direction.
        self.original_image = load_image('ship_up.png')
        self.original_image_up_right = load_image('ship_up_right.png')
        self.original_image_up_left = load_image('ship_up_left.png')
        self.original_image_down_right = load_image('ship_down_right.png')
        self.original_image_down_left = load_image('ship_down_left.png')
        self.original_image_right = load_image('ship_right.png')
        self.original_image_left = load_image('ship_left.png')
        self.original_image_down = load_image('ship_down.png')
        self.image = self.original_image

        # Get the rectangular area of the image.
        self.rect = self.image.get_rect()

        self.screen_rect = screen.get_rect()

        # Set starting position of ship at the center of screen.
        self.rect.centerx = self.screen_rect.centerx 
        self.rect.centery = self.screen_rect.centery

        # Current ship position.
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # Flags to check if ship moving in one or another direction.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Default ship direction.
        self.current_ship_rotation = "up"

        # Direction in which ship currently moving.
        self.desirable_ship_rotation = None

    def update(self):
        """Update ship position depending on movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def center_ship(self):
        """Set ship position on center of the screen."""
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.centery

    def prepare_for_boss(self):
        """Set ship position below boss position."""
        self.centerx = self.screen_rect.centerx
        self.centery = 700
             
    def blitme(self):
        """Draw ship."""
        self.screen.blit(self.image, self.rect)
