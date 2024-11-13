import pygame
import numpy as np
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Matrix Operations with Resizable UI")

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
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False

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

# Класс для работы с матрицами
class MatrixOperations:
    def __init__(self):
        self.matrix_a = np.zeros((2, 2), dtype=int)
        self.matrix_b = np.zeros((2, 2), dtype=int)
        self.result_matrix = None
        self.operation = None

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

    def clear_result(self):
        self.result_matrix = None

# Отображение матрицы на экране
def draw_matrix(matrix, position, title, input_boxes=None, input_values=None):
    x, y = position
    title_text = font.render(title, True, DARK_GRAY)
    screen.blit(title_text, (x, y - 30))

    if isinstance(matrix, str):
        error_text = font.render(matrix, True, BLUE)
        screen.blit(error_text, (x, y))
    else:
        for row in range(matrix.shape[0]):
            for col in range(matrix.shape[1]):
                rect = pygame.Rect(x + col * 60, y + row * 60, 50, 50)
                pygame.draw.rect(screen, LIGHT_GRAY, rect)
                pygame.draw.rect(screen, DARK_GRAY, rect, 2)
                
                value_text = input_values[row * 2 + col] if input_values else str(matrix[row, col])
                color = BLACK if matrix[row, col] != 0 else DARK_GRAY
                value_surface = font.render(value_text, True, color)
                screen.blit(value_surface, (rect.x + (rect.width - value_surface.get_width()) // 2,
                                            rect.y + (rect.height - value_surface.get_height()) // 2))
                if input_boxes:
                    input_boxes[row * 2 + col].update(rect)

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
    Button(50, 400, 150, 40, "Сложение", set_addition),
    Button(220, 400, 150, 40, "Вычитание", set_subtraction),
    Button(390, 400, 150, 40, "Умножение", set_multiplication),
    Button(50, 460, 150, 40, "Транспонирование A", set_transpose),
    Button(220, 460, 150, 40, "Обратная A", set_inverse),
    Button(390, 460, 150, 40, "Очистить результат", clear_result)
]

# Поля ввода значений матриц
input_boxes_a = [pygame.Rect(50 + (i % 2) * 60, 100 + (i // 2) * 60, 50, 50) for i in range(4)]
input_boxes_b = [pygame.Rect(300 + (i % 2) * 60, 100 + (i // 2) * 60, 50, 50) for i in range(4)]
input_values_a = ["0"] * 4
input_values_b = ["0"] * 4
active_box = None

# Основной цикл программы
running = True
while running:
    screen.fill(WHITE)

    # Отрисовка матриц и кнопок
    draw_matrix(matrix_operations.matrix_a, (50, 100), "Matrix A", input_boxes_a, input_values_a)
    draw_matrix(matrix_operations.matrix_b, (300, 100), "Matrix B", input_boxes_b, input_values_b)
    if matrix_operations.result_matrix is not None:
        draw_matrix(matrix_operations.result_matrix, (550, 100), "Result")

    # Отображение кнопок
    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        button.check_hover(mouse_pos)
        button.draw()

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for button in buttons:
                button.check_click(pos)
            for i, box in enumerate(input_boxes_a + input_boxes_b):
                if box.collidepoint(pos):
                    active_box = box
                    if i < 4:
                        input_values_a[i] = ""
                    else:
                        input_values_b[i - 4] = ""
                    break
            else:
                active_box = None
        elif event.type == pygame.KEYDOWN and active_box is not None:
            index = (input_boxes_a + input_boxes_b).index(active_box)
            if event.key == pygame.K_BACKSPACE:
                if index < 4:
                    input_values_a[index] = input_values_a[index][:-1]
                else:
                    input_values_b[index - 4] = input_values_b[index - 4][:-1]
            elif event.unicode.isdigit() or (event.unicode == '-' and len(input_values_a[index]) == 0):
                if index < 4:
                    input_values_a[index] += event.unicode
                else:
                    input_values_b[index - 4] += event.unicode

            # Преобразуем значения в массивы для матриц
            values_a = [int(val) if val else 0 for val in input_values_a]
            values_b = [int(val) if val else 0 for val in input_values_b]
            matrix_operations.set_matrix_values(values_a, values_b)

    pygame.display.flip()

pygame.quit()
sys.exit()
