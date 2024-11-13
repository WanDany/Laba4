import re
from collections import Counter
from tkinter import Tk, filedialog

def analyze_text(file_path):
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

    # Вывод результатов
    print("Слова, которые встречаются более одного раза:")
    for word, count in sorted_repeated_words:
        print(f"{word}: {count}")

    print("\nСлова, которые встречаются только один раз:")
    for word in sorted_unique_words:
        print(word)

    print(f"\nСамое короткое слово: {shortest_word}")
    print(f"Самое длинное слово: {longest_word}")

    print(f"\nСамое короткое предложение: {shortest_sentence}")
    print(f"Самое длинное предложение: {longest_sentence}")

# Функция для выбора файла
def select_file():
    # Открытие диалогового окна для выбора файла
    Tk().withdraw()  # Скрыть основное окно Tkinter
    file_path = filedialog.askopenfilename(
        title="Выберите текстовый файл",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        analyze_text(file_path)
    else:
        print("Файл не выбран.")

# Запуск программы
select_file()
