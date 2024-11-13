import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

def get_file_content(filename):
    """Читает содержимое из указанного файла построчно."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл '{filename}' не найден.")
        return None

def get_current_datetime():
    """Возвращает текущую дату и время в виде отформатированной строки."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def format_content(content, left_margin, filename):
    """
    Форматирует содержимое с заданным отступом слева и информацией о файле.
    """
    header = f"Файл: {filename} | Дата: {get_current_datetime()}\n" + "-" * 50 + "\n"
    formatted_content = header

    for line in content:
        formatted_content += " " * left_margin + line

    return formatted_content

def display_content(limit_lines=True):
    """Отображает содержимое в новом окне, либо ограниченное число строк, либо все строки."""
    filename = file_entry.get()
    content = get_file_content(filename)
    if content is None:
        return

    try:
        lines_per_page = int(lines_entry.get())
        left_margin = int(margin_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите числовые значения для строк на странице и отступа слева.")
        return

    # Форматируем содержимое с учетом отступа слева
    formatted_content = format_content(content, left_margin, filename)
    
    # Ограничиваем количество строк, если выбран режим отображения ограниченного количества строк
    if limit_lines:
        lines_to_display = formatted_content.splitlines()[:lines_per_page]
        display_text = "\n".join(lines_to_display)
    else:
        display_text = formatted_content

    # Открытие нового окна для отображения текста
    display_window = tk.Toplevel(root)
    display_window.title("Отформатированное содержимое")
    text_area = tk.Text(display_window, wrap=tk.WORD, font=("Courier", 10))
    text_area.insert(tk.END, display_text)
    text_area.config(state=tk.DISABLED)
    text_area.pack(expand=True, fill='both')

def save_content():
    """Сохраняет отформатированное содержимое в указанный файл."""
    filename = file_entry.get()
    content = get_file_content(filename)
    if content is None:
        return

    try:
        left_margin = int(margin_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите числовое значение для отступа слева.")
        return

    formatted_content = format_content(content, left_margin, filename)
    output_filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if output_filename:
        try:
            with open(output_filename, 'w', encoding='utf-8') as file:
                file.write(formatted_content)
            messagebox.showinfo("Сохранение", f"Содержимое успешно сохранено в '{output_filename}'")
        except IOError as e:
            messagebox.showerror("Ошибка", f"Не удалось записать файл '{output_filename}': {e}")

def select_file():
    """Открывает проводник для выбора файла и отображает путь к файлу."""
    filename = filedialog.askopenfilename(title="Выберите текстовый файл", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if filename:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filename)

# Настройка графического интерфейса
root = tk.Tk()
root.title("Форматирование документов")

# Поле выбора файла
file_label = tk.Label(root, text="Выберите файл:")
file_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
file_entry = tk.Entry(root, width=40)
file_entry.grid(row=0, column=1, padx=10, pady=10)
file_button = tk.Button(root, text="Обзор...", command=select_file)
file_button.grid(row=0, column=2, padx=10, pady=10)

# Поле для ввода количества строк на странице
lines_label = tk.Label(root, text="Количество строк на странице:")
lines_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
lines_entry = tk.Entry(root, width=10)
lines_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Поле для ввода отступа слева
margin_label = tk.Label(root, text="Отступ слева (пробелы):")
margin_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
margin_entry = tk.Entry(root, width=10)
margin_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Кнопки для вывода на экран и сохранения в файл
display_button = tk.Button(root, text="Показать ограниченное количество строк", command=lambda: display_content(limit_lines=True))
display_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

display_all_button = tk.Button(root, text="Показать все строки", command=lambda: display_content(limit_lines=False))
display_all_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

save_button = tk.Button(root, text="Сохранить в файл", command=save_content)
save_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
