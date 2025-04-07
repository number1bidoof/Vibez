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
FINISH_LINE = pygame.Rect(WIDTH // 2 - 5, 100, 10, 100)
LAPS_TO_WIN = 3

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Customizable Mario Kart")

# Load character images
try:
    MARIO_IMG = pygame.image.load("mario.jpg").convert_alpha()
    LUIGI_IMG = pygame.image.load("luigi.png").convert_alpha()
    PEACH_IMG = pygame.image.load("peach.png").convert_alpha()
    BOWSER_IMG = pygame.image.load("bowser.jpg").convert_alpha()
    TOAD_IMG = pygame.image.load("toad.jpg").convert_alpha()
except pygame.error as e:
    print(f"Error loading image: {e}. Make sure all character images are in the same directory.")
    pygame.quit()
    exit()

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

class Car:
    def __init__(self, x, y, color, character_name):
        self.x = x
        self.y = y
        self.speed = 5
        self.angle = 0
        self.color = color
        self.character_name = character_name
        self.character_surface = CHARACTER_IMAGES.get(character_name)
        self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.laps = 0
        self.passed_finish = False

    def update(self, keys):
        if keys.get(pygame.K_a, False):
            self.angle -= 5
        if keys.get(pygame.K_d, False):
            self.angle += 5
        if keys.get(pygame.K_w, False):
            radians = math.radians(self.angle)
            self.x += self.speed * math.cos(radians)
            self.y -= self.speed * math.sin(radians)
        if keys.get(pygame.K_s, False):
            radians = math.radians(self.angle)
            self.x -= self.speed * math.cos(radians)
            self.y += self.speed * math.sin(radians)

        self.rect.center = (self.x, self.y)

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, rotated_rect)

        if self.character_surface:
            character_rect = self.character_surface.get_rect(center=self.rect.center)
            screen.blit(self.character_surface, character_rect)

def draw_track():
    pygame.draw.ellipse(screen, TRACK_COLOR, (100, 100, 600, 400), 0)
    pygame.draw.ellipse(screen, BLACK, (150, 150, 500, 300), 0)
    pygame.draw.rect(screen, (255, 255, 0), FINISH_LINE)

def constrain_car_position(car):
    # Define the track boundary using the ellipse's position and size
    track_rect = pygame.Rect(100, 100, 600, 400)
    # Restrict the car to the track area
    if not track_rect.collidepoint(car.rect.centerx, car.rect.centery):
        # If the car is outside the track, stop movement
        car.x = max(min(car.x, track_rect.right - CAR_WIDTH), track_rect.left + CAR_WIDTH)
        car.y = max(min(car.y, track_rect.bottom - CAR_HEIGHT), track_rect.top + CAR_HEIGHT)

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

def game_mode_selection():
    font = pygame.font.Font(None, 36)
    mode_buttons = [
        Button("Multiplayer", 300, 200, 200, 50, (100, 100, 255), WHITE),
        Button("Race Against AI", 300, 300, 200, 50, (100, 255, 100), BLACK),
    ]

    while True:
        screen.fill(WHITE)
        draw_text("Select Game Mode", font, (0, 0, 0), 270, 100)

        for button in mode_buttons:
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in mode_buttons:
                    if button.is_clicked(mouse_pos):
                        return button.text

        pygame.display.update()

def ai_move(car):
    car.angle -= 1
    radians = math.radians(car.angle)
    car.x += car.speed * math.cos(radians)
    car.y -= car.speed * math.sin(radians)
    car.rect.center = (car.x, car.y)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def main():
    # Character and color selection inside main()
    running = True
    selected_color = (255, 0, 0)  # Default color: Red
    selected_character_name = "Mario"  # Default character: Mario
    font = pygame.font.Font(None, 36)

    # Color selection buttons
    color_buttons = [
        Button("Red", 300, 150, 200, 50, (255, 0, 0), (255, 255, 255)),
        Button("Green", 300, 220, 200, 50, (0, 255, 0), (255, 255, 255)),
        Button("Blue", 300, 290, 200, 50, (0, 0, 255), (255, 255, 255)),
    ]

    # Character selection buttons
    character_buttons = [
        Button("Mario", 100, 150, 150, 50, (255, 0, 0), (255, 255, 255)),
        Button("Luigi", 100, 220, 150, 50, (0, 255, 0), (255, 255, 255)),
        Button("Peach", 100, 290, 150, 50, (255, 182, 193), (255, 255, 255)),
        Button("Bowser", 100, 360, 150, 50, (255, 165, 0), (255, 255, 255)),
        Button("Toad", 100, 430, 150, 50, (255, 255, 255), (0, 0, 0)),
    ]

    # Start button
    start_button = Button("Start Race", 300, 500, 200, 50, (0, 0, 0), (255, 255, 255))

    while running:
        screen.fill((255, 255, 255))  # White background

        draw_text("Customize Your Car", font, (0, 0, 0), 230, 50)

        for button in color_buttons + character_buttons + [start_button]:
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Handle color selection
                for button in color_buttons:
                    if button.is_clicked(mouse_pos):
                        if button.text == "Red":
                            selected_color = (255, 0, 0)
                        elif button.text == "Green":
                            selected_color = (0, 255, 0)
                        elif button.text == "Blue":
                            selected_color = (0, 0, 255)

                # Handle character selection
                for button in character_buttons:
                    if button.is_clicked(mouse_pos):
                        selected_character_name = button.text

                # Start race
                if start_button.is_clicked(mouse_pos):
                    mode = game_mode_selection()
                    game_loop(selected_color, selected_character_name, mode)

        pygame.display.update()

    pygame.quit()

def game_loop(player_color, player_character_name, mode):
    if player_color is None or player_character_name is None:
        return

    player_car = Car(WIDTH // 4, HEIGHT // 2, player_color, player_character_name)
    all_cars = [player_car]

    if mode == "Multiplayer":
        p2_color = (0, 255, 255)
        p2_char = "Luigi" if player_character_name != "Luigi" else "Peach"
        player2 = Car(WIDTH // 4, HEIGHT // 2 + 120, p2_color, p2_char)
        all_cars.append(player2)

    elif mode == "Race Against AI":
        available_others = list(AVAILABLE_CHARACTERS)
        if player_character_name in available_others:
            available_others.remove(player_character_name)

        num_others = min(3, len(available_others))
        for i in range(num_others):
            other_character = random.choice(available_others)
            available_others.remove(other_character)
            other_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            x_pos = WIDTH // 2 + (i * CAR_WIDTH * 2)
            y_pos = HEIGHT // 2
            other_car = Car(x_pos, y_pos, other_color, other_character)
            other_car.angle = 180
            all_cars.append(other_car)

    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 48)

    while running:
        screen.fill(WHITE)
        draw_track()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player_car.update({k: keys[k] for k in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]})

        if mode == "Multiplayer":
            player2 = all_cars[1]
            player2.update({k: keys[k] for k in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]})

        elif mode == "Race Against AI":
            for ai_car in all_cars[1:]:
                ai_move(ai_car)

        # Constrain cars within the track
        constrain_car_position(player_car)

        if mode == "Multiplayer":
            player2 = all_cars[1]
            constrain_car_position(player2)

        elif mode == "Race Against AI":
            for ai_car in all_cars[1:]:
                constrain_car_position(ai_car)

        # Check if player car crosses finish line
        if FINISH_LINE.collidepoint(player_car.rect.center):
            if not player_car.passed_finish:
                player_car.laps += 1
                player_car.passed_finish = True
                print(f"{player_car.character_name} completed lap {player_car.laps}")
        else:
            player_car.passed_finish = False

        # Check if player has won
        if player_car.laps >= LAPS_TO_WIN:
            draw_text("You Win!", font, (0, 255, 0), WIDTH // 2 - 100, HEIGHT // 2)
            pygame.display.update()
            pygame.time.wait(3000)
            running = False

        for car in all_cars:
            car.draw()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
