from datetime import datetime

def get_file_content(filename):
    #Читает содержимое из указанного файла построчно.
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
        return None

def get_current_datetime():
    #Возвращает текущую дату и время в виде отформатированной строки.
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def format_content(content, lines_per_page, left_margin, filename):
    #Форматирует содержимое с заданным количеством строк на странице, отступом слева и информацией о файле.
   
    # Заголовок с именем файла и текущей датой и временем
    header = f"Файл: {filename} | Дата: {get_current_datetime()}\n" + "-" * 50 + "\n"
    formatted_content = header
    page_line_count = 0

    # Обработка каждой строки с добавлением отступа и постраничного разрыва
    for line in content:
        # Добавляем отступ слева и содержимое строки
        formatted_content += " " * left_margin + line

        # Увеличиваем счётчик строк для текущей страницы
        page_line_count += 1
        if page_line_count >= lines_per_page:
            # Добавляем разрыв страницы, если достигли заданного количества строк
            formatted_content += "\n--- Разрыв страницы ---\n"
            page_line_count = 0

    return formatted_content

def save_to_file(content, output_filename):
    #Сохраняет содержимое в указанный файл.
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Содержимое успешно сохранено в '{output_filename}'")
    except IOError as e:
        print(f"Не удалось записать файл '{output_filename}': {e}")

def main():
    # Запрашиваем имя исходного текстового файла
    filename = input("Введите имя текстового файла для форматирования: ")
    content = get_file_content(filename)
    if content is None:
        return

    # Запрашиваем у пользователя количество строк на странице и отступ слева
    try:
        lines_per_page = int(input("Введите количество строк на странице: "))
        left_margin = int(input("Введите количество пробелов для отступа слева: "))
    except ValueError:
        print("Ошибка ввода. Пожалуйста, введите числовые значения.")
        return

    # Форматируем содержимое файла
    formatted_content = format_content(content, lines_per_page, left_margin, filename)

    # Выбираем опцию вывода
    print("Выберите вариант вывода:")
    print("1. Печать на экран")
    print("2. Сохранить в другой файл")

    choice = input("Введите ваш выбор (1 или 2): ")

    if choice == '1':
        # Выводим отформатированное содержимое на экран
        print("\nВывод форматированного содержимого на экран:\n")
        print(formatted_content)
    elif choice == '2':
        # Сохраняем отформатированное содержимое в новый файл
        output_filename = input("Введите имя выходного файла: ")
        save_to_file(formatted_content, output_filename)
    else:
        print("Неверный выбор.")

if __name__ == "__main__":
    main()
