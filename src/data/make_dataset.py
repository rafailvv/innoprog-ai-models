import json
import re

import numpy as np
import pandas as pd
import os
# Assuming ADMIN_ID is a constant representing the admin's identifier in the chat.
ADMIN_ID = 'user5790141925'


def give_conversation(path_file):
    # Load the data from the provided JSON file path.
    with open(path_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    messages = []
    users = set()

    # Extract message details and collect unique user IDs.
    for msg in data['messages']:
        users.add(msg['from_id'])
        # Initialize a dictionary to store message details.
        temp_dict = {
            'id': msg['id'],
            'from': msg['from_id'],
            'text': " ".join(t['text'] for t in msg['text_entities']).strip(),
            'date': msg['date_unixtime']
        }
        messages.append(temp_dict)

    grouped = []
    text_temp = ''

    # Group messages by sender to combine sequential messages from the same user.
    for idx, message in enumerate(messages):
        if idx < len(messages) - 1 and message['from'] == messages[idx + 1]['from']:
            text_temp += message['text'] + " "
        else:
            text_temp += message['text']
            grouped.append({
                'id': message['id'],
                'from': message['from'],
                'text': re.sub(r'\s+', ' ', text_temp).strip(),
                'date': message['date']
            })
            text_temp = ''

    # Convert the grouped messages into a pandas DataFrame.
    df = pd.DataFrame(grouped)

    # Filter questions and answers based on the sender's ID.
    questions = df[df['from'] != ADMIN_ID]['text'].tolist()
    answers = df[df['from'] == ADMIN_ID]['text'].tolist()

    # Create a DataFrame containing questions and their corresponding answers.
    qa_df = pd.DataFrame({
        'question': questions[:len(answers)],
        'answer': answers
    })

    return qa_df
PATH = "../../data/"
all_df = []
for file in os.listdir(PATH + "raw"):
    all_df.append(give_conversation(PATH + f'raw/{file}').replace('', np.nan).dropna())
dataset_df = pd.concat(all_df, ignore_index=True)
dataset_df.to_csv(PATH + "interim/dataset.csv")