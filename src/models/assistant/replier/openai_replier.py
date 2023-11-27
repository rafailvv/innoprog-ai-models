from openai import OpenAI

api_key = 'YOUR_API_KEY'

def reply_message(additional_information):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Представь, что ты чат ассистент образовательной школы."\
                                    "Тебе на вход будет подаваться информация, которую нужно сообщить ученику."\
                                    "В ответ составь корректное, вежливое, подбадривающее сообщение."\
                                    "Включи в него лаконично данную для перефразирования информацию."},
        {"role": "user", "content": additional_information},
    ]
    )

    # Extract and print the model's reply
    return completion.choices[0].message.content