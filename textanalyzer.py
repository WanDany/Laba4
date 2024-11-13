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

    # Подсчет общего количества слов и предложений
    total_words = len(words)
    total_sentences = len(sentences)

    # Нахождение самого часто встречающегося слова
    most_common_word = word_counts.most_common(1)[0]

    # Вывод результатов на экран
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

    print(f"\nОбщее количество слов в тексте: {total_words}")
    print(f"Общее количество предложений в тексте: {total_sentences}")
    print(f"Самое часто встречающееся слово: {most_common_word[0]} (встретилось {most_common_word[1]} раз)")

    # Запись результатов в файл
    write_results_to_file(sorted_repeated_words, sorted_unique_words, shortest_word, longest_word, shortest_sentence, longest_sentence, total_words, total_sentences, most_common_word)

# Функция для записи результатов в новый текстовый файл
def write_results_to_file(repeated_words, unique_words, shortest_word, longest_word, shortest_sentence, longest_sentence, total_words, total_sentences, most_common_word):
    # Открытие нового файла для записи
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

    print("\nРезультаты анализа сохранены в файл 'text_analysis_results.txt'.")

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
