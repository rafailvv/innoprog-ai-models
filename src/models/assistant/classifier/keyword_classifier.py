from nltk.stem.snowball import RussianStemmer
import string

def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def stem_words(words):
    stemmer = RussianStemmer()
    return [stemmer.stem(word) for word in words]

def simple_tokenize(text):
    return text.split()

def classify_message_with_stemming_simple(message):
    task_keywords_stemmed = stem_words(["задача", "проблема", "решить", "помощь", "подсказка"])
    organizational_keywords_stemmed = stem_words(["запись", "расписание", "записаться", "прекратить", "занятие"])

    message_words_stemmed = stem_words(simple_tokenize(remove_punctuation(message.lower())))

    print(message_words_stemmed)

    if any(keyword in message_words_stemmed for keyword in task_keywords_stemmed):
        return "Подсказки по задачам"
    elif any(keyword in message_words_stemmed for keyword in organizational_keywords_stemmed):
        return "Организационные задачи"
    else:
        return "Все остальные"