import pygame
import time
import numpy as np

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Matrix Operations Animation")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Шрифт
font = pygame.font.Font(None, 36)

# Класс для отображения и анимации операций с матрицами
class MatrixAnimator:
    def __init__(self, matrix_a, matrix_b):
        self.matrix_a = matrix_a
        self.matrix_b = matrix_b
        self.result_matrix = None

    def draw_matrix(self, matrix, position):
        x, y = position
        for row in range(matrix.shape[0]):
            for col in range(matrix.shape[1]):
                value = font.render(str(matrix[row, col]), True, BLUE)
                screen.blit(value, (x + col * 50, y + row * 50))

    def animate_operation(self, operation):
        screen.fill(WHITE)
        
        # Выбор операции
        if operation == 'addition':
            self.result_matrix = self.matrix_a + self.matrix_b
        elif operation == 'subtraction':
            self.result_matrix = self.matrix_a - self.matrix_b
        elif operation == 'multiplication':
            self.result_matrix = self.matrix_a.dot(self.matrix_b)
        elif operation == 'transpose_a':
            self.result_matrix = self.matrix_a.T
        elif operation == 'inverse_a':
            self.result_matrix = np.linalg.inv(self.matrix_a)
        else:
            print("Unsupported operation")
            return
        
        # Отображение матриц
        self.draw_matrix(self.matrix_a, (50, 100))
        self.draw_matrix(self.matrix_b, (300, 100))
        
        # Показ результата с задержкой
        for row in range(self.result_matrix.shape[0]):
            for col in range(self.result_matrix.shape[1]):
                time.sleep(0.3)
                value = font.render(str(self.result_matrix[row, col]), True, BLACK)
                screen.blit(value, (550 + col * 50, 100 + row * 50))
                pygame.display.flip()

# Пример матриц для анимации
matrix_a = np.array([[2, 3], [1, 4]])
matrix_b = np.array([[1, 2], [3, 4]])

# Создание аниматора
animator = MatrixAnimator(matrix_a, matrix_b)

# Основной цикл программы
running = True
while running:
    screen.fill(WHITE)
    
    # Запускаем анимацию умножения (можно сменить на другую операцию)
    animator.animate_operation('multiplication')
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
