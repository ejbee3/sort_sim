import pygame

class Bar_Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width, height))
        self.image.fill((137, 137, 137))
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 6
        self.is_smallest = False
        self.is_sorted = False
    
    def update(self, dir):
        self.rect.x += self.speed * dir

    def recolor(self, color):
        self.image.fill(color)
    

class Button(pygame.Rect):
    def __init__(self, left, top, width, height, text, color, text_color):
        super().__init__(left, top, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, screen, font):
        # Draw the button rectangle
        pygame.draw.rect(screen, self.color, self)
        # Render the text
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos):
        # Check if the mouse position is within the button
        return self.collidepoint(mouse_pos)
        