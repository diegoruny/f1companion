class Car:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 30))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))