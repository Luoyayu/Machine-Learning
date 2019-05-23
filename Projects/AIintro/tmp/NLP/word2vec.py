# -*- coding:utf-8 -*-

# word2vec pytorch implement
# (1) skip-gram 无任何优化

import logging
import numpy as np
import torch
from torch.nn import functional as F
import torch.optim as optim

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

corpus = [
    'he is a king',
    'she is a queen',
    'he is a man',
    'she is a woman',
    'warsaw is poland capital',
    'berlin is germany capital',
    'paris is france capital',
]

# token encode & build vocabulary indices
tokenized_corpus = [x.split() for x in corpus]
logger.info(tokenized_corpus)

# unique & keep order
vocabulary = np.array(tokenized_corpus).reshape(1, -1).squeeze(0)
tmp_set = set()
vocabulary = [x for x in vocabulary if not (x in tmp_set or tmp_set.add(x))]
del tmp_set

logger.info(vocabulary)

word2idx = {w: idx for (idx, w) in enumerate(vocabulary)}
idx2word = {idx: w for (idx, w) in enumerate(vocabulary)}

logger.info(word2idx)
logger.info(idx2word)

# build center words & context words
# assume context Windows equal to 2

windows_size = 2
idx_pairs = []

for sentence in tokenized_corpus:
    indices = [word2idx[word] for word in sentence]
    for center_word_pos in range(len(indices)):
        for w in range(-windows_size, windows_size + 1):
            context_word_pos = center_word_pos + w
            if context_word_pos < 0 or context_word_pos >= len(indices) or \
                    center_word_pos == context_word_pos:
                continue
            context_word_idx = indices[context_word_pos]
            idx_pairs.append((indices[center_word_pos], context_word_idx))

idx_pairs = np.array(idx_pairs)
logger.info(idx_pairs)
for i, (center_word_idx, context_word_idx) in enumerate(idx_pairs):
    if i < 5:
        logger.info((idx2word[center_word_idx], idx2word[context_word_idx]))

# we interest in predict context word by center word, so the probability P(context|center;θ)
# now we have the target: max \prod_{center} \prod_{context} P(context|center, θ)
# we have to optimize θ make the likelihood maximum
# transform to
# min -1/|V| \sum_{center} \sum_{context} log P(context|center, θ)
# P(context|center) = exp(u_{context}^T v_{center}) / \sum_{w\in V}exp(u_w^T v_center)
# u and v are vectors, the scalar product of given center and context pair become bigger as they are more similar

vocabulary_size = len(vocabulary)
embedding_dims = 5


def get_input_layer(word_idx):
    x = torch.zeros(vocabulary_size, dtype=torch.float64)
    x[word_idx] = 1.0
    return x


W1 = torch.randn(embedding_dims, vocabulary_size, dtype=torch.float64, requires_grad=True)
output = torch.randn(vocabulary_size, embedding_dims, dtype=torch.float64, requires_grad=True)
num_epochs = 100

lr = 0.001
optimizer = optim.Adam([W1, output], lr=lr)

for epoch in range(num_epochs):
    loss_val = 0
    for data, target in idx_pairs:
        x = get_input_layer(data)
        y_true = torch.tensor(np.array([target]), dtype=torch.long)

        z1 = torch.matmul(W1, x)
        z2 = torch.matmul(output, z1)

        log_softmax = F.log_softmax(z2, dim=0)
        loss = F.nll_loss(log_softmax.view(1, -1), y_true)
        loss_val += loss.item()
        loss.backward()
        optimizer.step()

    if epoch % 10 == 0:
        logger.info(f"epoch [{epoch}]: {loss_val / len(idx_pairs)}")

print(output)
print(torch.nn.CosineSimilarity(dim=0)(output[word2idx["king"]], output[word2idx["queen"]]).item())
print(torch.nn.CosineSimilarity(dim=0)(output[word2idx["he"]], output[word2idx["she"]]).item())

