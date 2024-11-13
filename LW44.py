import pygame
import numpy as np
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Matrix Operations with Animations and Resizable UI")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (50, 50, 50)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 149, 237)

# Шрифт
font = pygame.font.Font(None, 32)
button_font = pygame.font.Font(None, 24)

# Класс кнопки
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.relative_pos = (x, y)
        self.relative_size = (width, height)
        self.text = text
        self.action = action
        self.hovered = False
        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(
            int(self.relative_pos[0] * SCREEN_WIDTH),
            int(self.relative_pos[1] * SCREEN_HEIGHT),
            int(self.relative_size[0] * SCREEN_WIDTH),
            int(self.relative_size[1] * SCREEN_HEIGHT)
        )

    def draw(self):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        label = button_font.render(self.text, True, WHITE)
        screen.blit(label, (self.rect.x + (self.rect.width - label.get_width()) // 2,
                            self.rect.y + (self.rect.height - label.get_height()) // 2))

    def check_click(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

# Класс для полей ввода значений
class InputBox:
    def __init__(self, x, y, size):
        self.relative_pos = (x, y)
        self.relative_size = size
        self.text = "0"
        self.active = False
        self.update_rect()

    def update_rect(self):
        box_size = int(self.relative_size * min(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = pygame.Rect(
            int(self.relative_pos[0] * SCREEN_WIDTH),
            int(self.relative_pos[1] * SCREEN_HEIGHT),
            box_size, box_size
        )

    def draw(self):
        pygame.draw.rect(screen, LIGHT_GRAY, self.rect)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 2 if self.active else 1)
        value_surface = font.render(self.text, True, BLACK)
        screen.blit(value_surface, (self.rect.x + (self.rect.width - value_surface.get_width()) // 2,
                                    self.rect.y + (self.rect.height - value_surface.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit() or (event.unicode == '-' and not self.text):
                self.text += event.unicode

# Класс для работы с матрицами
class MatrixOperations:
    def __init__(self):
        self.matrix_a = np.zeros((2, 2), dtype=int)
        self.matrix_b = np.zeros((2, 2), dtype=int)
        self.result_matrix = None
        self.animation_step = 0

    def set_matrix_values(self, values_a, values_b):
        self.matrix_a = np.array(values_a).reshape((2, 2))
        self.matrix_b = np.array(values_b).reshape((2, 2))

    def perform_operation(self, operation):
        if operation == 'addition':
            self.result_matrix = self.matrix_a + self.matrix_b
        elif operation == 'subtraction':
            self.result_matrix = self.matrix_a - self.matrix_b
        elif operation == 'multiplication':
            self.result_matrix = self.matrix_a.dot(self.matrix_b)
        elif operation == 'transpose_a':
            self.result_matrix = self.matrix_a.T
        elif operation == 'inverse_a':
            try:
                self.result_matrix = np.linalg.inv(self.matrix_a)
            except np.linalg.LinAlgError:
                self.result_matrix = "Non-invertible matrix"
        self.animation_step = 0

    def animate_result(self):
        if isinstance(self.result_matrix, np.ndarray):
            self.animation_step += 1
            if self.animation_step >= self.result_matrix.size:
                self.animation_step = self.result_matrix.size
            return self.animation_step < self.result_matrix.size
        return False

    def clear_result(self):
        self.result_matrix = None
        self.animation_step = 0

# Функции для кнопок
def set_addition():
    matrix_operations.perform_operation('addition')

def set_subtraction():
    matrix_operations.perform_operation('subtraction')

def set_multiplication():
    matrix_operations.perform_operation('multiplication')

def set_transpose():
    matrix_operations.perform_operation('transpose_a')

def set_inverse():
    matrix_operations.perform_operation('inverse_a')

def clear_result():
    matrix_operations.clear_result()

# Основные переменные и объекты
matrix_operations = MatrixOperations()
buttons = [
    Button(0.06, 0.83, 0.18, 0.06, "Сложение", set_addition),
    Button(0.28, 0.83, 0.18, 0.06, "Вычитание", set_subtraction),
    Button(0.50, 0.83, 0.18, 0.06, "Умножение", set_multiplication),
    Button(0.06, 0.92, 0.18, 0.06, "Транспонирование A", set_transpose),
    Button(0.28, 0.92, 0.18, 0.06, "Обратная A", set_inverse),
    Button(0.50, 0.92, 0.18, 0.06, "Очистить результат", clear_result)
]

# Поля ввода значений матриц
input_boxes_a = [InputBox(0.06 + (i % 2) * 0.1, 0.15 + (i // 2) * 0.1, 0.08) for i in range(4)]
input_boxes_b = [InputBox(0.38 + (i % 2) * 0.1, 0.15 + (i // 2) * 0.1, 0.08) for i in range(4)]

# Основной цикл программы
running = True
while running:
    screen.fill(WHITE)

    # Перерисовываем кнопки и обновляем их позиции
    for button in buttons:
        button.update_rect()
        button.draw()

    # Отображение полей ввода
    for box in input_boxes_a + input_boxes_b:
        box.update_rect()
        box.draw()

    # Отрисовка результата
    if matrix_operations.result_matrix is not None:
        if matrix_operations.animate_result():
            for i, row in enumerate(matrix_operations.result_matrix):
                for j, val in enumerate(row):
                    if i * 2 + j < matrix_operations.animation_step:
                        pos_x = int((0.7 + j * 0.1) * SCREEN_WIDTH)
                        pos_y = int((0.15 + i * 0.1) * SCREEN_HEIGHT)
                        rect = pygame.Rect(pos_x, pos_y, int(0.08 * SCREEN_WIDTH), int(0.08 * SCREEN_HEIGHT))
                        pygame.draw.rect(screen, LIGHT_GRAY, rect)
                        pygame.draw.rect(screen, DARK_GRAY, rect, 2)
                        val_surface = font.render(str(val), True, BLACK)
                        screen.blit(val_surface, (rect.x + (rect.width - val_surface.get_width()) // 2,
                                                  rect.y + (rect.height - val_surface.get_height()) // 2))
        else:
            for i, row in enumerate(matrix_operations.result_matrix):
                for j, val in enumerate(row):
                    pos_x = int((0.7 + j * 0.1) * SCREEN_WIDTH)
                    pos_y = int((0.15 + i * 0.1) * SCREEN_HEIGHT)
                    rect = pygame.Rect(pos_x, pos_y, int(0.08 * SCREEN_WIDTH), int(0.08 * SCREEN_HEIGHT))
                    pygame.draw.rect(screen, LIGHT_GRAY, rect)
                    pygame.draw.rect(screen, DARK_GRAY, rect, 2)
                    val_surface = font.render(str(val), True, BLACK)
                    screen.blit(val_surface, (rect.x + (rect.width - val_surface.get_width()) // 2,
                                              rect.y + (rect.height - val_surface.get_height()) // 2))

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for button in buttons:
                button.check_click(pos)
            for box in input_boxes_a + input_boxes_b:
                box.handle_event(event)
        elif event.type == pygame.KEYDOWN:
            for box in input_boxes_a + input_boxes_b:
                box.handle_event(event)

    # Преобразование значений для матриц
    values_a = [int(box.text) if box.text else 0 for box in input_boxes_a]
    values_b = [int(box.text) if box.text else 0 for box in input_boxes_b]
    matrix_operations.set_matrix_values(values_a, values_b)

    pygame.display.flip()

pygame.quit()
sys.exit()
