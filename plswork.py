import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
FPS = 60
CAR_WIDTH, CAR_HEIGHT = 50, 100
TRACK_COLOR = (200, 200, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Customizable Mario Kart")

# Load character images (ensure the images are in your project directory)
try:
    MARIO_IMG = pygame.image.load("mario.jpg").convert_alpha()  # Mario image file
    LUIGI_IMG = pygame.image.load("luigi.png").convert_alpha()  # Luigi image file
    PEACH_IMG = pygame.image.load("peach.png").convert_alpha()  # Princess Peach image file
    BOWSER_IMG = pygame.image.load("bowser.jpg").convert_alpha()  # Bowser image file
    TOAD_IMG = pygame.image.load("toad.jpg").convert_alpha()  # Toad image file
except pygame.error as e:
    print(f"Error loading image: {e}. Make sure all character images are in the same directory.")
    pygame.quit()
    exit()

# Resize character images to fit on the car (adjust the size as needed)
CHARACTER_SIZE = (CAR_WIDTH, 50)
MARIO_IMG = pygame.transform.scale(MARIO_IMG, CHARACTER_SIZE)
LUIGI_IMG = pygame.transform.scale(LUIGI_IMG, CHARACTER_SIZE)
PEACH_IMG = pygame.transform.scale(PEACH_IMG, CHARACTER_SIZE)
BOWSER_IMG = pygame.transform.scale(BOWSER_IMG, CHARACTER_SIZE)
TOAD_IMG = pygame.transform.scale(TOAD_IMG, CHARACTER_SIZE)

CHARACTER_IMAGES = {
    "Mario": MARIO_IMG,
    "Luigi": LUIGI_IMG,
    "Peach": PEACH_IMG,
    "Bowser": BOWSER_IMG,
    "Toad": TOAD_IMG,
}
AVAILABLE_CHARACTERS = list(CHARACTER_IMAGES.keys())

# Define the car object
class Car:
    def __init__(self, x, y, color, character_name):
        self.x = x
        self.y = y
        self.speed = 5
        self.angle = 0
        self.color = color
        self.character_name = character_name
        self.character_surface = CHARACTER_IMAGES.get(character_name)
        self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA) # Make the car surface transparent
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, keys):
        # Using math module for trigonometric calculations
        if keys[pygame.K_a]:
            self.angle -= 5
        if keys[pygame.K_d]:
            self.angle += 5
        if keys[pygame.K_w]:
            # Convert angle to radians and use math.cos and math.sin for movement
            radians = math.radians(self.angle)
            self.x += self.speed * math.cos(radians)
            self.y -= self.speed * math.sin(radians)  # Minus because screen y-coordinates increase downwards
        if keys[pygame.K_s]:
            # Convert angle to radians and move backward
            radians = math.radians(self.angle)
            self.x -= self.speed * math.cos(radians)
            self.y += self.speed * math.sin(radians)

        self.rect.center = (self.x, self.y)

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, rotated_rect)

        # Draw the character on top of the car
        if self.character_surface:
            character_rect = self.character_surface.get_rect(center=self.rect.center)
            screen.blit(self.character_surface, character_rect)

# Set up the race track (oval-shaped track)
def draw_track():
    pygame.draw.ellipse(screen, TRACK_COLOR, (100, 100, 600, 400), 0)  # Outer part of the track
    pygame.draw.ellipse(screen, BLACK, (150, 150, 500, 300), 0)  # Inner part (track is the space between the two ellipses)

# Button class to handle button creation and detection
class Button:
    def __init__(self, text, x, y, width, height, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Car color and character customization screen with buttons
def customization_screen():
    running = True
    selected_color = (255, 0, 0)  # Default color: red
    selected_character_name = "Mario"  # Default character: Mario
    font = pygame.font.Font(None, 36)

    # Create buttons for color selection
    color_buttons = [
        Button("Red", 300, 150, 200, 50, (255, 0, 0), (255, 255, 255)),
        Button("Green", 300, 220, 200, 50, (0, 255, 0), (255, 255, 255)),
        Button("Blue", 300, 290, 200, 50, (0, 0, 255), (255, 255, 255)),
    ]

    # Create buttons for character selection
    character_buttons = [
        Button("Mario", 100, 150, 150, 50, (255, 0, 0), (255, 255, 255)),
        Button("Luigi", 100, 220, 150, 50, (0, 255, 0), (255, 255, 255)),
        Button("Peach", 100, 290, 150, 50, (255, 182, 193), (255, 255, 255)),
    ]

    start_button = Button("Start Race", 300, 400, 200, 50, (0, 0, 0), (255, 255, 255))

    while running:
        screen.fill(WHITE)
        draw_text("Customize Your Car", font, (255, 0, 0), 230, 50)

        # Draw color selection buttons
        for button in color_buttons:
            button.draw()

        # Draw character selection buttons
        for button in character_buttons:
            button.draw()

        # Draw start button
        start_button.draw()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if any button is clicked
                for button in color_buttons:
                    if button.is_clicked(mouse_pos):
                        # Get the color from the button's text
                        if button.text == "Red":
                            selected_color = (255, 0, 0)
                        elif button.text == "Green":
                            selected_color = (0, 255, 0)
                        elif button.text == "Blue":
                            selected_color = (0, 0, 255)

                for button in character_buttons:
                    if button.is_clicked(mouse_pos):
                        selected_character_name = button.text

                if start_button.is_clicked(mouse_pos):
                    return selected_color, selected_character_name

        pygame.display.update()
    pygame.quit()
    return None, None # In case the user quits before starting

# Utility function to draw text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Main game loop
def game_loop(player_color, player_character_name):
    if player_color is None or player_character_name is None:
        return # Exit if customization was not completed

    player_car = Car(WIDTH // 4, HEIGHT // 2, player_color, player_character_name)
    other_cars = []
    available_others = list(AVAILABLE_CHARACTERS)
    if player_character_name in available_others:
        available_others.remove(player_character_name)

    num_others = min(3, len(available_others)) # Create up to 3 other cars
    for i in range(num_others):
        other_character = random.choice(available_others)
        available_others.remove(other_character)
        other_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # Position other cars with some spacing
        x_pos = WIDTH // 2 + (i * (CAR_WIDTH * 2))
        y_pos = HEIGHT // 2
        other_car = Car(x_pos, y_pos, other_color, other_character)
        other_car.angle = 180 # Make them face the player initially
        other_cars.append(other_car)

    all_cars = [player_car] + other_cars

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)  # Clear screen
        draw_track()  # Draw the track

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle key inputs for the player
        keys = pygame.key.get_pressed()
        player_car.update(keys)

        # Draw all cars
        for car in all_cars:
            car.draw()

        # Update the screen
        pygame.display.update()

        # Maintain the frame rate
        clock.tick(FPS)

    pygame.quit()

# Run the game
def main():
    player_color, player_character_name = customization_screen()  # Get selected car color and character
    if player_color is not None and player_character_name is not None:
        game_loop(player_color, player_character_name)  # Start the race

if __name__ == "__main__":
    main()