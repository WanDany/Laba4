import pygame
import numpy as np
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Matrix Operations with Interface")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Шрифт
font = pygame.font.Font(None, 28)

# Класс кнопки
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = GRAY

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        label = font.render(self.text, True, BLACK)
        screen.blit(label, (self.rect.x + 10, self.rect.y + 10))

    def check_click(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()

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

# Отображение матрицы на экране
def draw_matrix(matrix, position):
    x, y = position
    if isinstance(matrix, str):
        error_text = font.render(matrix, True, BLUE)
        screen.blit(error_text, (x, y))
    else:
        for row in range(matrix.shape[0]):
            for col in range(matrix.shape[1]):
                value = font.render(str(matrix[row, col]), True, BLUE)
                screen.blit(value, (x + col * 50, y + row * 50))

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

# Основные переменные и объекты
matrix_operations = MatrixOperations()
buttons = [
    Button(50, 400, 150, 40, "Сложение", set_addition),
    Button(220, 400, 150, 40, "Вычитание", set_subtraction),
    Button(390, 400, 150, 40, "Умножение", set_multiplication),
    Button(50, 460, 150, 40, "Транспонирование A", set_transpose),
    Button(220, 460, 150, 40, "Обратная A", set_inverse),
]

# Поля ввода значений матриц
input_boxes_a = [pygame.Rect(50 + (i % 2) * 50, 100 + (i // 2) * 50, 40, 40) for i in range(4)]
input_boxes_b = [pygame.Rect(300 + (i % 2) * 50, 100 + (i // 2) * 50, 40, 40) for i in range(4)]
input_values_a = ["0"] * 4
input_values_b = ["0"] * 4
active_box = None

# Основной цикл программы
running = True
while running:
    screen.fill(WHITE)

    # Отрисовка заголовков
    label_a = font.render("Matrix A", True, BLACK)
    label_b = font.render("Matrix B", True, BLACK)
    label_result = font.render("Result", True, BLACK)
    screen.blit(label_a, (50, 50))
    screen.blit(label_b, (300, 50))
    screen.blit(label_result, (550, 50))

    # Отображение матриц и кнопок
    draw_matrix(matrix_operations.matrix_a, (50, 100))
    draw_matrix(matrix_operations.matrix_b, (300, 100))
    if matrix_operations.result_matrix is not None:
        draw_matrix(matrix_operations.result_matrix, (550, 100))

    for button in buttons:
        button.draw()

    # Отображение полей ввода для матриц
    for i, box in enumerate(input_boxes_a):
        pygame.draw.rect(screen, DARK_GRAY if active_box == box else GRAY, box)
        value = font.render(input_values_a[i], True, BLACK)
        screen.blit(value, (box.x + 5, box.y + 5))

    for i, box in enumerate(input_boxes_b):
        pygame.draw.rect(screen, DARK_GRAY if active_box == box else GRAY, box)
        value = font.render(input_values_b[i], True, BLACK)
        screen.blit(value, (box.x + 5, box.y + 5))

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for button in buttons:
                button.check_click(pos)
            for i, box in enumerate(input_boxes_a + input_boxes_b):
                if box.collidepoint(pos):
                    active_box = box
                    break
            else:
                active_box = None
        elif event.type == pygame.KEYDOWN:
            if active_box is not None:
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
                elif event.key == pygame.K_RETURN:
                    # Обновить значения матриц после завершения ввода
                    try:
                        values_a = list(map(int, input_values_a))
                        values_b = list(map(int, input_values_b))
                        matrix_operations.set_matrix_values(values_a, values_b)
                    except ValueError:
                        pass

    pygame.display.flip()

pygame.quit()
sys.exit()
