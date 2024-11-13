import re
from collections import Counter
import tkinter as tk
from tkinter import filedialog, messagebox

def analyze_text(file_path):
    try:
        # Чтение текста из файла
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Разделение на слова и предложения
        words = re.findall(r'\b\w+\b', text.lower())
        sentences = re.split(r'(?<=[.!?]) +', text)

        # Статистика по словам
        word_counts = Counter(words)

        # Слова, которые встречаются более одного раза
        repeated_words = {word: count for word, count in word_counts.items() if count > 1}
        sorted_repeated_words = sorted(repeated_words.items())

        # Слова, которые встречаются только один раз
        unique_words = [word for word, count in word_counts.items() if count == 1]
        sorted_unique_words = sorted(unique_words)

        # Самое короткое и самое длинное слово
        shortest_word = min(words, key=len)
        longest_word = max(words, key=len)

        # Самое короткое и самое длинное предложение
        shortest_sentence = min(sentences, key=len)
        longest_sentence = max(sentences, key=len)

        # Подсчет общего количества слов и предложений
        total_words = len(words)
        total_sentences = len(sentences)

        # Нахождение самого часто встречающегося слова
        most_common_word = word_counts.most_common(1)[0]

        # Формирование результата
        result = f"Слова, которые встречаются более одного раза:\n"
        for word, count in sorted_repeated_words:
            result += f"{word}: {count}\n"

        result += "\nСлова, которые встречаются только один раз:\n"
        for word in sorted_unique_words:
            result += f"{word}\n"

        result += f"\nСамое короткое слово: {shortest_word}\n"
        result += f"Самое длинное слово: {longest_word}\n"
        result += f"\nСамое короткое предложение: {shortest_sentence}\n"
        result += f"Самое длинное предложение: {longest_sentence}\n"
        result += f"\nОбщее количество слов в тексте: {total_words}\n"
        result += f"Общее количество предложений в тексте: {total_sentences}\n"
        result += f"Самое часто встречающееся слово: {most_common_word[0]} (встретилось {most_common_word[1]} раз)\n"

        # Отображение результата в текстовом поле
        text_output.delete(1.0, tk.END)  # Очистка текстового поля перед выводом
        text_output.insert(tk.END, result)

        # Запись результатов в файл
        write_results_to_file(sorted_repeated_words, sorted_unique_words, shortest_word, longest_word, shortest_sentence, longest_sentence, total_words, total_sentences, most_common_word)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось обработать файл: {e}")

# Функция для записи результатов в новый текстовый файл
def write_results_to_file(repeated_words, unique_words, shortest_word, longest_word, shortest_sentence, longest_sentence, total_words, total_sentences, most_common_word):
    with open("text_analysis_results.txt", 'w', encoding='utf-8') as file:
        file.write("Слова, которые встречаются более одного раза:\n")
        for word, count in repeated_words:
            file.write(f"{word}: {count}\n")

        file.write("\nСлова, которые встречаются только один раз:\n")
        for word in unique_words:
            file.write(f"{word}\n")

        file.write(f"\nСамое короткое слово: {shortest_word}\n")
        file.write(f"Самое длинное слово: {longest_word}\n")

        file.write(f"\nСамое короткое предложение: {shortest_sentence}\n")
        file.write(f"Самое длинное предложение: {longest_sentence}\n")

        file.write(f"\nОбщее количество слов в тексте: {total_words}\n")
        file.write(f"Общее количество предложений в тексте: {total_sentences}\n")
        file.write(f"Самое часто встречающееся слово: {most_common_word[0]} (встретилось {most_common_word[1]} раз)\n")

    messagebox.showinfo("Успех", "Результаты анализа сохранены в файл 'text_analysis_results.txt'.")

# Функция для выбора файла
def select_file():
    file_path = filedialog.askopenfilename(
        title="Выберите текстовый файл",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        analyze_text(file_path)
    else:
        messagebox.showwarning("Предупреждение", "Файл не выбран.")

# Создание главного окна
root = tk.Tk()
root.title("Анализ текста")

# Настройка интерфейса
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

btn_select_file = tk.Button(frame, text="Выбрать файл", command=select_file)
btn_select_file.pack()

# Создаем текстовое поле с прокруткой
text_frame = tk.Frame(frame)
text_frame.pack()

# Прокрутка
scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL)

# Текстовое поле для отображения результатов
text_output = tk.Text(text_frame, width=80, height=20, wrap=tk.WORD, yscrollcommand=scrollbar.set)
text_output.pack(side=tk.LEFT)

# Привязываем прокрутку к текстовому полю
scrollbar.config(command=text_output.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()
