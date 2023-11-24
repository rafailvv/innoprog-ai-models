from utils import *
import numpy as np

# input_history - list of user's grade for previous len(input_history) tasks 
# recommended len(input_history) >= 3
input_history = [10, 12, 10]

increase_complexity = True
next_complexity = None
k = 1 # factor
m = np.mean(input_history)
max_dev = max(abs(el - m) for el in input_history)

if increase_complexity: next_complexity = int(m + k * max_dev)
else: next_complexity = int(m)


input_history.append(next_complexity)

prev_tensor  = torch.Tensor(input_history).long()
complexity_padding = torch.Tensor([0] * (max_size - len(input_history))).long()
to_predict = torch.concat((prev_tensor, complexity_padding))

l = predict(model, to_predict, len(input_history))
print(l)