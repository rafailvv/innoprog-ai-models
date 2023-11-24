###

# Package includes model parameters and functions to launch the model 

###

import torch.nn as nn
import torch
import os

def predict(
        model,
        text,
        length
):
    predictions = []
    with torch.no_grad():
        model.eval()  # evaluation mode

        # forward pass and loss calculation
        outputs = model(text)


        _, predicted = torch.max(outputs.data, 1)
        predictions += predicted[:length].detach().cpu().tolist()

    return predictions


class Model(nn.Module):
    def __init__(self,
                 input_dim,
                 embedding_dim,
                 hidden_dim,
                 output_dim,
                 n_layers,
                 bidirectional,
                 dropout):

        super(Model, self).__init__()

        self.word_embeddings = nn.Embedding(input_dim, embedding_dim, padding_idx=1)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, bidirectional = bidirectional)
        self.hidden2tag = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, output_dim)

    def forward(self, x):
        embeds = self.word_embeddings(x)
        lstm_out, _ = self.lstm(embeds)
        tag_space = self.hidden2tag(lstm_out)

        return tag_space
    

DIR = os.path.abspath(os.curdir)

# DIR = DIR.replace(' ', '\ ')
DIR = DIR.split('/')
PATH = '/'.join(DIR)
PATH += '/models/complexity-prediction-model/best.pt'


INPUT_DIM = 81 # max of formula + 1
EMBEDDING_DIM = 128
HIDDEN_DIM = 64
OUTPUT_DIM = 11 # 5 possible points
N_LAYERS = 2
BIDIRECTIONAL = False
DROPOUT = 0.25
max_size = 50
PAD_IDX = 1

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = Model(INPUT_DIM, EMBEDDING_DIM, HIDDEN_DIM, OUTPUT_DIM, N_LAYERS, BIDIRECTIONAL, DROPOUT).to(device)
dict_state = torch.load(PATH)
model.load_state_dict(dict_state)
model.eval()