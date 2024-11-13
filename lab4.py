import tkinter as tk  # Импортируем модуль для создания графического интерфейса
from tkinter import filedialog, messagebox  # Импортируем диалоговые окна для выбора файлов и сообщений об ошибках
from datetime import datetime  # Импортируем модуль для работы с датой и временем
import os  # Импортируем модуль для работы с операционной системой (для получения имени файла)

# Основные стили для ретро-интерфейса
BG_COLOR = "#3e2212"  # Темно-коричневый цвет фона для всего окна
BUTTON_BG = "#8b5a2b"  # Цвет фона кнопок
TEXT_COLOR = "#FFFFFF"  # Белый цвет текста
FRAME_COLOR = "#8b5a2b"  # Цвет рамок элементов управления
INFO_BG = "#7A4B32"  # Цвет фона верхней панели с информацией
FONT = ("Courier New", 11, "bold")  # Шрифт, используемый для текста в интерфейсе (пиксельный стиль)

def get_file_content(filename):
     #Читает содержимое из указанного файла построчно.
    try:
        # Открываем файл для чтения с кодировкой utf-8
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()  # Читаем все строки из файла и возвращаем их в виде списка
    except FileNotFoundError:
        # Если файл не найден, показываем сообщение об ошибке
        messagebox.showerror("Ошибка", f"Файл '{filename}' не найден.")
        return None  # Возвращаем None, если файл не найден

def get_current_datetime():
     #Возвращает текущую дату и время в виде отформатированной строки.
    now = datetime.now()  # Получаем текущее время
    return now.strftime("%Y-%m-%d %H:%M:%S")  # Форматируем время в строку вида "ГГГГ-ММ-ДД ЧЧ:ММ:СС"

def format_content(content, left_margin):
     #Форматирует содержимое с заданным отступом слева, без информации о файле и дате.
    
    formatted_content = ""  # Переменная для хранения отформатированного содержимого
    for line in content:
        formatted_content += " " * left_margin + line  # Добавляем отступ и строку в итоговое содержимое
    return formatted_content  # Возвращаем отформатированное содержимое

def display_content(limit_lines=True):
    """Отображает содержимое в основной области текста, либо ограниченное количество строк, либо все строки."""
    filename_text = file_label.cget("text")  # Получаем текст из метки с названием файла
    filename = filename_text.split(" | ")[0].replace("Файл: ", "").strip()  # Извлекаем только имя файла из текста метки

    if filename == "Файл не выбран":  # Если файл не выбран, выводим предупреждение
        messagebox.showwarning("Ошибка", "Файл не выбран!")
        return

    content = get_file_content(filename)  # Получаем содержимое выбранного файла
    if content is None:  # Если файл не был прочитан (например, не найден), выходим
        return

    try:
        lines_per_page = int(lines_entry.get())  # Получаем количество строк для отображения с поля ввода
        left_margin = int(margin_entry.get())  # Получаем отступ слева с поля ввода
    except ValueError:
        # Если введены некорректные данные, выводим сообщение об ошибке
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите числовые значения для строк на странице и отступа слева.")
        return

    formatted_content = format_content(content, left_margin)  # Форматируем содержимое с заданным отступом
    
    if limit_lines:
        # Ограничиваем количество строк, выводимых на экран
        lines_to_display = formatted_content.splitlines()[:lines_per_page]
        display_text = "\n".join(lines_to_display)
    else:
        # Если не ограничиваем, выводим все строки
        display_text = formatted_content

    text_area.config(state=tk.NORMAL)  # Включаем возможность редактировать текстовое поле
    text_area.delete(1.0, tk.END)  # Очищаем текущее содержимое текстового поля
    text_area.insert(tk.END, display_text)  # Вставляем новое содержимое в текстовое поле
    text_area.config(state=tk.NORMAL)  # Снова разрешаем редактирование текста

def save_content():
    #Сохраняет отформатированное содержимое в указанный файл.
    filename = file_label.cget("text")  # Получаем название файла из метки
    if filename == "Файл не выбран":  # Если файл не выбран, выводим предупреждение
        messagebox.showwarning("Ошибка", "Файл не выбран!")
        return

    content = text_area.get(1.0, tk.END)  # Получаем текст из текстового поля

    # Открываем диалоговое окно для сохранения файла
    output_filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if output_filename:  # Если файл выбран для сохранения
        try:
            # Открываем файл для записи и сохраняем содержимое
            with open(output_filename, 'w', encoding='utf-8') as file:
                file.write(content)
            messagebox.showinfo("Сохранение", f"Содержимое успешно сохранено в '{output_filename}'")  # Уведомляем пользователя о сохранении
        except IOError as e:
            # Если возникла ошибка при записи, выводим сообщение об ошибке
            messagebox.showerror("Ошибка", f"Не удалось записать файл '{output_filename}': {e}")

def select_file():
    #Открывает проводник для выбора файла и отображает путь к файлу.
    filename = filedialog.askopenfilename(title="Выберите текстовый файл", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if filename:  # Если файл выбран
        filename_only = os.path.basename(filename)  # Извлекаем только имя файла из полного пути
        file_label.config(text=f"Файл: {filename_only} | Дата: {get_current_datetime()}")  # Обновляем метку с названием файла и текущей датой
        display_content()  # Отображаем содержимое файла в текстовом поле

# Настройка графического интерфейса
root = tk.Tk()  # Создаем главное окно приложения
root.title("Интерфейс в стиле Zelda")  # Устанавливаем заголовок окна
root.config(bg=BG_COLOR)  # Устанавливаем цвет фона главного окна

# Верхняя информационная панель
info_frame = tk.Frame(root, bg=INFO_BG, bd=4, relief="ridge")  # Создаем фрейм для верхней панели с информацией
info_frame.pack(pady=10, padx=10, fill="x", ipadx=5, ipady=5)  # Размещаем фрейм на экране

# Информация о файле
file_label = tk.Label(info_frame, text="Файл не выбран", font=FONT, bg=INFO_BG, fg=TEXT_COLOR)  # Создаем метку для отображения информации о файле
file_label.pack(side="top", pady=5)  # Размещаем метку на панели

# Основная область текста
text_area_frame = tk.Frame(root, bg=FRAME_COLOR, bd=4, relief="ridge")  # Создаем фрейм для области текста
text_area_frame.pack(padx=10, pady=10, fill="both", expand=True)  # Размещаем фрейм на экране

# Добавление прокрутки
scrollbar = tk.Scrollbar(text_area_frame)  # Создаем полосу прокрутки
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Размещаем полосу прокрутки справа

# Основное текстовое поле
text_area = tk.Text(text_area_frame, wrap=tk.WORD, font=FONT, fg=TEXT_COLOR, bg=BG_COLOR, state=tk.DISABLED, yscrollcommand=scrollbar.set)  # Создаем текстовое поле для отображения содержимого
text_area.pack(expand=True, fill='both', padx=5, pady=5)  # Размещаем текстовое поле на экране

scrollbar.config(command=text_area.yview)  # Настроим полосу прокрутки для работы с текстом

# Нижняя панель с кнопками
button_frame = tk.Frame(root, bg=BG_COLOR)  # Создаем фрейм для кнопок
button_frame.pack(pady=10)  # Размещаем фрейм с кнопками на экране

# Кнопки на одной строке
select_button = tk.Button(button_frame, text="Выбрать файл", command=select_file, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT)  # Кнопка для выбора файла
select_button.grid(row=0, column=0, padx=5, pady=5)  # Размещаем кнопку

display_button = tk.Button(button_frame, text="Показать ограниченное количество строк", command=lambda: display_content(limit_lines=True), bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT)  # Кнопка для отображения ограниченного количества строк
display_button.grid(row=0, column=1, padx=5, pady=5)

display_all_button = tk.Button(button_frame, text="Показать все строки", command=lambda: display_content(limit_lines=False), bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT)  # Кнопка для отображения всех строк
display_all_button.grid(row=0, column=2, padx=5, pady=5)

save_button = tk.Button(button_frame, text="Сохранить в файл", command=save_content, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT)  # Кнопка для сохранения содержимого в файл
save_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5)  # Размещаем кнопку на следующей строке

# Поле для ввода количества строк на странице с обводкой
input_frame = tk.Frame(button_frame, bg=FRAME_COLOR, bd=2, relief="solid")  # Создаем фрейм для ввода данных
input_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5)  # Размещаем фрейм

lines_label = tk.Label(input_frame, text="Количество строк:", font=FONT, bg=FRAME_COLOR, fg=TEXT_COLOR)  # Метка для ввода количества строк
lines_label.grid(row=0, column=0, padx=5, pady=5)  # Размещаем метку

lines_entry = tk.Entry(input_frame, font=FONT, fg=TEXT_COLOR, bg=BG_COLOR)  # Поле ввода для количества строк
lines_entry.grid(row=0, column=1, padx=5, pady=5)  # Размещаем поле ввода
lines_entry.insert(0, "10")  # Вставляем значение по умолчанию

margin_label = tk.Label(input_frame, text="Отступ слева:", font=FONT, bg=FRAME_COLOR, fg=TEXT_COLOR)  # Метка для ввода отступа
margin_label.grid(row=1, column=0, padx=5, pady=5)  # Размещаем метку

margin_entry = tk.Entry(input_frame, font=FONT, fg=TEXT_COLOR, bg=BG_COLOR)  # Поле ввода для отступа
margin_entry.grid(row=1, column=1, padx=5, pady=5)  # Размещаем поле ввода
margin_entry.insert(0, "4")  # Вставляем значение по умолчанию

root.mainloop()  # Запускаем главный цикл обработки событий интерфейса
