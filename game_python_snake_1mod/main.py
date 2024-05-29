import pygame, sys, random, string
import pygame.freetype
from pygame.math import Vector2
from datetime import datetime, timedelta

pygame.init()

FONT_MATRIX = 'assets/Fonts/matrix.ttf'
FONT_MATRIX_NUMBERS = 'assets/Fonts/miltown_.ttf'

try:
    title_font = pygame.font.Font(FONT_MATRIX, 60)
except FileNotFoundError:
    print("Fuente no encontrada.")

try:
    score_font = pygame.font.Font(FONT_MATRIX_NUMBERS, 40)
except FileNotFoundError:
    print("Fuente no encontrada.")

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)
GREEN_MATRIX = (0, 255, 0)
DARK_GRAY = (17, 17, 17)

cell_size = 20
number_of_cells = 25

OFFSET = 75


class OstacleAzul2:

    def __init__(self, snake_body, *positions):
        self.position = self.generate_random_pos(snake_body, *positions)

    def draw(self):
        ostacle_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        screen.blit(ostacle_azul_surface, ostacle_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells -1)
        y = random.randint(0, number_of_cells -1)
        return Vector2(x, y)
    
    def generate_random_pos(self, snake_body, *positions):
        position = self.generate_random_cell()
        snake_positions = [segment[0] for segment in snake_body]

        while position in snake_positions or position == positions:
            position = self.generate_random_cell()
        return position


class OstacleAzul:

    def __init__(self, snake_body, food_position, ostacle_shaco_position):
        self.position = self.generate_random_pos(snake_body, food_position, ostacle_shaco_position)

    def draw(self):
        ostacle_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        screen.blit(ostacle_azul_surface, ostacle_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells -1)
        y = random.randint(0, number_of_cells -1)
        return Vector2(x, y)
    
    def generate_random_pos(self, snake_body, food_position, ostacle_shaco_position):
        position = self.generate_random_cell()
        snake_positions = [segment[0] for segment in snake_body]  # Extraer solo las posiciones de las tuplas

        while position in snake_positions or position == food_position or position == ostacle_shaco_position:
            position = self.generate_random_cell()
        return position


class OstacleShaco:

    def __init__(self, snake_body, food_position):
        self.position = self.generate_random_pos(snake_body, food_position)

    def draw(self):
        ostacle_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        screen.blit(ostacle_shaco_surface, ostacle_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells -1)
        y = random.randint(0, number_of_cells -1)
        return Vector2(x, y)
    
    def generate_random_pos(self, snake_body, food_position):
        position = self.generate_random_cell()
        snake_positions = [segment[0] for segment in snake_body]

        while position in snake_positions or position == food_position:
            position = self.generate_random_cell()
        return position


class Food:

    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells -1)
        y = random.randint(0, number_of_cells -1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        snake_positions = [segment[0] for segment in snake_body]

        while position in snake_positions:
            position = self.generate_random_cell()
        return position


class Snake:
    
    def __init__(self):
        pygame.freetype.init()
        self.font = pygame.freetype.Font(FONT_MATRIX, 24)
        self.body = [(Vector2(6, 9), self.generate_random_letter()), 
                     (Vector2(5, 9), self.generate_random_letter()), 
                     (Vector2(4, 9), self.generate_random_letter())]
        self.direction = Vector2(1, 0)
        self.add_segment = False
        self.eat_sound = pygame.mixer.Sound("assets/Sounds/ration.mp3")
        self.wall_hit_sound = pygame.mixer.Sound("assets/Sounds/Metal_Gear_Solid_Game_Over.mp3")

    def generate_random_letter(self):
        return random.choice(string.ascii_uppercase)

    def draw(self):
        for segment, letter in self.body:
            segment_pos = (OFFSET + segment.x * cell_size, 
                           OFFSET + segment.y * cell_size)
            self.font.render_to(screen, segment_pos, letter, GREEN_MATRIX)

    def update(self):
        new_head_pos = self.body[0][0] + self.direction
        new_head_letter = self.generate_random_letter()
        self.body.insert(0, (new_head_pos, new_head_letter))

        if not self.add_segment:
            self.body.pop()
        else:
            self.add_segment = False

    def reset(self):
        self.body = [(Vector2(6, 9), self.generate_random_letter()), 
                     (Vector2(5, 9), self.generate_random_letter()), 
                     (Vector2(4, 9), self.generate_random_letter())]
        self.direction = Vector2(1, 0)


class Game:

    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.ostacle_shaco = OstacleShaco(self.snake.body, self.food.position)
        self.ostacle_azul = OstacleAzul(self.snake.body, self.food.position, self.ostacle_shaco.position)
        self.ostacle_azul_2 = OstacleAzul2(self.snake.body, self.food.position, self.ostacle_shaco.position, self.ostacle_azul.position)
        self.ostacle_azul_2_2 = OstacleAzul2(
            self.snake.body,
            self.food.position,
            self.ostacle_shaco.position,
            self.ostacle_azul.position,
            self.ostacle_azul_2.position
            )
        self.ostacle_azul_2_3 = OstacleAzul2(
            self.snake.body,
            self.food.position,
            self.ostacle_shaco.position,
            self.ostacle_azul.position,
            self.ostacle_azul_2.position,
            self.ostacle_azul_2_2.position
            )
        self.ostacle_azul_2_4 = OstacleAzul2(
            self.snake.body,
            self.food.position,
            self.ostacle_shaco.position,
            self.ostacle_azul.position,
            self.ostacle_azul_2.position,
            self.ostacle_azul_2_2.position,
            self.ostacle_azul_2_3.position
            )
        self.ostacle_azul_2_5 = OstacleAzul2(
            self.snake.body,
            self.food.position,
            self.ostacle_shaco.position,
            self.ostacle_azul.position,
            self.ostacle_azul_2.position,
            self.ostacle_azul_2_2.position,
            self.ostacle_azul_2_3.position,
            self.ostacle_azul_2_4.position
            )
        self.state = "STOPPED"
        self.score = 0
        self.level = 0
        self.start_time = None  # Inicio del temporizador
        self.elapsed_time = 0  # Tiempo transcurrido
        self.previous_level = 1  # Almacena el nivel anterior
        self.level_sounds = [
            pygame.mixer.Sound("assets/Sounds/matrix2_intro_level1.mp3"),
            pygame.mixer.Sound("assets/Sounds/matrix3_menu_level2.mp3"),
            pygame.mixer.Sound("assets/Sounds/matrix2_rod_level3.mp3"),
            pygame.mixer.Sound("assets/Sounds/matrix1_7_level4.mp3"),
            pygame.mixer.Sound("assets/Sounds/matrix1_2_level5.mp3"),
            pygame.mixer.Sound("assets/Sounds/matrix1_clubbed_level6.mp3"),
            pygame.mixer.Sound("assets/Sounds/matrix2_chetau_level7.mp3"),
            pygame.mixer.Sound("assets/Sounds/deep_sea_level8.mp3"),
            pygame.mixer.Sound("assets/Sounds/hardcore_level9.mp3"),
            pygame.mixer.Sound("assets/Sounds/levelup_mario.mp3")
        ]

    def draw(self):
        self.food.draw()
        self.snake.draw()

        if self.level >= 2:
            self.ostacle_shaco.draw()

        if self.level >= 4:
            self.ostacle_azul.draw()

        if self.level >= 5:
            self.ostacle_azul_2.draw()

        if self.level >= 6:
            self.ostacle_azul_2_2.draw()

        if self.level >= 7:
            self.ostacle_azul_2_3.draw()

        if self.level >= 8:
            self.ostacle_azul_2_4.draw()

        if self.level >= 9:
            self.ostacle_azul_2_5.draw()


    def update(self):
        if self.state == "RUNNING":

            level_scores = [0, 5, 10, 25, 50, 100, 150, 250, 400]
            old_level = self.level

            if self.score in level_scores:

                self.level_up()

            # Verificar si el nivel ha cambiado
            if old_level != self.level:

                self.level_up_actions()

            self.snake.update()
            self.check_collision_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()
            self.check_collision_ostacle_shaco()
            self.check_collision_ostacle_azul()
            self.check_collision_ostacle_azul_2()
            self.check_collision_ostacle_azul_2_2()
            self.check_collision_ostacle_azul_2_3()
            self.check_collision_ostacle_azul_2_4()
            self.check_collision_ostacle_azul_2_5()

    def check_collision_food(self):
        if self.snake.body[0][0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            self.snake.eat_sound.play()

            if self.level >= 3:
                self.ostacle_shaco.position = self.ostacle_shaco.generate_random_pos(self.snake.body, self.ostacle_shaco.position)
            
            if self.level >= 4:
                self.ostacle_azul.position = self.ostacle_azul.generate_random_pos(self.snake.body, self.ostacle_shaco.position, self.ostacle_azul.position)
            
            if self.level >= 5:
                self.ostacle_azul_2.position = self.ostacle_azul_2.generate_random_pos(self.snake.body, self.food.position, self.ostacle_shaco.position, self.ostacle_azul.position)

            if self.level >= 6:
                self.ostacle_azul_2_2.position = self.ostacle_azul_2.generate_random_pos(
                    self.snake.body,
                    self.food.position,
                    self.ostacle_shaco.position,
                    self.ostacle_azul.position,
                    self.ostacle_azul_2.position
                )

            if self.level >= 7:
                self.ostacle_azul_2_3.position = self.ostacle_azul_2.generate_random_pos(
                    self.snake.body,
                    self.food.position,
                    self.ostacle_shaco.position,
                    self.ostacle_azul.position,
                    self.ostacle_azul_2.position,
                    self.ostacle_azul_2_2.position
                )

            if self.level >= 8:
                self.ostacle_azul_2_4.position = self.ostacle_azul_2.generate_random_pos(
                    self.snake.body,
                    self.food.position,
                    self.ostacle_shaco.position,
                    self.ostacle_azul.position,
                    self.ostacle_azul_2.position,
                    self.ostacle_azul_2_2.position,
                    self.ostacle_azul_2_3.position
                )

            if self.level >= 9:
                self.ostacle_azul_2_5.position = self.ostacle_azul_2.generate_random_pos(
                    self.snake.body,
                    self.food.position,
                    self.ostacle_shaco.position,
                    self.ostacle_azul.position,
                    self.ostacle_azul_2.position,
                    self.ostacle_azul_2_2.position,
                    self.ostacle_azul_2_3.position,
                    self.ostacle_azul_2_4.position
                )

            print("eat")

    def check_collision_ostacle_shaco(self):
        if self.level >= 2:
            if self.snake.body[0][0] == self.ostacle_shaco.position:
                self.game_over()
                print("Shaco")
    
    def check_collision_ostacle_azul(self):
        if self.level >= 4:
            if self.snake.body[0][0] == self.ostacle_azul.position:
                self.game_over()
                print("blue 0")

    def check_collision_ostacle_azul_2(self):
        if self.level >= 5:
            if self.snake.body[0][0] == self.ostacle_azul_2.position:
                self.game_over()
                print("blue 1")

    def check_collision_ostacle_azul_2_2(self):
        if self.level >= 6:
            if self.snake.body[0][0] == self.ostacle_azul_2_2.position:
                self.game_over()
                print("blue 2")

    def check_collision_ostacle_azul_2_3(self):
        if self.level >= 7:
            if self.snake.body[0][0] == self.ostacle_azul_2_3.position:
                self.game_over()
                print("blue 3")

    def check_collision_ostacle_azul_2_4(self):
        if self.level >= 8:
            if self.snake.body[0][0] == self.ostacle_azul_2_4.position:
                self.game_over()
                print("blue 4")
    
    def check_collision_ostacle_azul_2_5(self):
        if self.level >= 9:
            if self.snake.body[0][0] == self.ostacle_azul_2_5.position:
                self.game_over()
                print("blue 5")

    def check_collision_with_edges(self):
        if self.snake.body[0][0].x == number_of_cells or self.snake.body[0][0].x == -1:
            self.game_over()
            print("wall")

        if self.snake.body[0][0].y == number_of_cells or self.snake.body[0][0].y == -1:
            self.game_over()
            print("wall")

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"
        self.score = 0
        self.level = 0
        pygame.mixer.stop()
        self.snake.wall_hit_sound.play()

    def check_collision_with_tail(self):
        headless_body = [body[0] for body in self.snake.body[1:]]
        
        if self.snake.body[0][0] in headless_body:
            self.game_over()
            print("tail")
    
    def level_up(self):
        level_scores = {
            0: 1, 5: 2, 10: 3, 25: 4,
            50: 5, 100: 6, 150: 7,
            250: 8, 400: 9
        }

        for score, level in level_scores.items():
            if self.score >= score:
                self.level = level
    
    def level_up_actions(self):
        pygame.mixer.stop()

        if self.level > 1:

            self.level_sounds[9].play()

        if self.level <= 9:

            self.level_sounds[self.level - 1].play(loops=-1)

        self.previous_level = self.level


def format_time(seconds):
    return str(timedelta(seconds=seconds))


screen = pygame.display.set_mode((2*OFFSET + cell_size*number_of_cells, 2*OFFSET + cell_size*number_of_cells))

pygame.display.set_caption("Retro Snake                 1º Mod Matrix                 By: MagoOscuro91")

clok = pygame.time.Clock()

game = Game()

food_surface = pygame.image.load("assets/Graphics/pastilla_roja.png")
ostacle_shaco_surface = pygame.image.load("assets/Graphics/pastilla_shaco.png")
ostacle_azul_surface = pygame.image.load("assets/Graphics/pastilla_azul.png")

#m Velocidad maxima 50 ms, velocidad base 200 ms, -20 ms cada level.
def get_speed(level):

    base_speed = 200
    return max(50, base_speed - (level - 1) * 20)


SNAKE_UPDATE = pygame.USEREVENT

pygame.time.set_timer(SNAKE_UPDATE, get_speed(game.level))

start_time = None
elapsed_time = timedelta()

last_key_time = 0
min_time_between_keys = 100  # 500 ms, equivalente a 0.5 segundos


while True:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():

        if event.type == SNAKE_UPDATE:
            game.update()

            if game.state == "RUNNING":
                game.elapsed_time = (datetime.now() - game.start_time).total_seconds() #


        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            
            if game.state == "STOPPED":
                game.state = "RUNNING"
                game.start_time = datetime.now()  # Iniciar el temporizador
            
            pygame.time.set_timer(SNAKE_UPDATE, get_speed(game.level))

            if current_time - last_key_time >= min_time_between_keys:

                last_key_time = current_time 

                if (event.key == pygame.K_UP or event.key == pygame.K_w) and game.snake.direction != Vector2(0, 1):
                    game.snake.direction = Vector2(0, -1)

                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and game.snake.direction != Vector2(0, -1):
                    game.snake.direction = Vector2(0, 1)

                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and game.snake.direction != Vector2(1, 0):
                    game.snake.direction = Vector2(-1, 0)

                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and game.snake.direction != Vector2(-1, 0):
                    game.snake.direction = Vector2(1, 0)

                # Teclas para ir al nivel especifico para un desarollo comodo.
                if event.key == pygame.K_9:
                    game.level = 9
                    game.score = 401

                if event.key == pygame.K_8:
                    game.level = 8
                    game.score = 251
                
                if event.key == pygame.K_7:
                    game.level = 7
                    game.score = 151

                if event.key == pygame.K_6:
                    game.level = 6
                    game.score = 101

                if event.key == pygame.K_5:
                    game.level = 5
                    game.score = 51
            
            if game.level != game.previous_level:
                pygame.time.set_timer(SNAKE_UPDATE, get_speed(game.level))
                game.previous_level = game.level

    screen.fill(DARK_GRAY)

    pygame.draw.rect(screen, GREEN_MATRIX,
                    (OFFSET-5, OFFSET-5, cell_size*number_of_cells+10, cell_size*number_of_cells+10), 5)

    game.draw()

    ### Surfaces ###

    # Textos Surface (Crear superficie).
    title_surface = title_font.render("Retro Snake Matrix", True, GREEN_MATRIX)
    title_score_surface = title_font.render("Score", True, GREEN_MATRIX)
    title_level_surface = title_font.render("Level", True, GREEN_MATRIX)
    # Numeros Surface.
    score_surface = score_font.render(str(game.score), True, GREEN_MATRIX)
    level_surface = score_font.render(str(game.level), True, GREEN_MATRIX)
    time_surface = score_font.render(format_time(int(game.elapsed_time)), True, GREEN_MATRIX)

    ### Display Surfaces ###

    # Textos Display Surface (La superfice de visualización | Posicion).
    screen.blit(title_surface, (OFFSET+7, 15))
    screen.blit(title_score_surface, (OFFSET-50, OFFSET + cell_size*number_of_cells +20))
    screen.blit(title_level_surface, (OFFSET+375, OFFSET + cell_size*number_of_cells +20))
    # Numeros Display Surface.
    screen.blit(score_surface, (OFFSET+98, OFFSET + cell_size*number_of_cells +12))
    screen.blit(level_surface, (OFFSET+525, OFFSET + cell_size*number_of_cells +12))
    screen.blit(time_surface, (OFFSET+185, OFFSET + cell_size*number_of_cells +12))

    pygame.display.update()

    clok.tick(60) # 60 FPS.
