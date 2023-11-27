from openai import OpenAI

threshold = 3
api_key = 'YOUR_API_KEY'

def classify_message(trial=0):
    if trial >= 3:
        # three trials did not produce necessary result
        return 3
    
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Представь, что ты классификационная модель. Тебе нужно классифицировать данный текст в одну из трех категорий."\
                                    "Отвечай только номер категории и ни слова больше. "\
                                    "Список категорий: "\
                                    "1. помощь с задачей (запросы подсказок для задач) "\
                                    "2. организационные вопросы (вопросы по поводу расписания и занятий)"\
                                    "3. другое. Если у тебя нет высокой уверенности в ответе, то отправляй запрос в третью категорию"},
        {"role": "user", "content": "Дайте подсказку по задаче"},
    ]
    )

    # Extract and print the model's reply
    result = completion.choices[0].message.content
    if len(result) > 1:
        return classify_message(trial=trial+1)
    else:
        return int(result[0])