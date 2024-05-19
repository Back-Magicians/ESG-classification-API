import os
import sys
from collections import OrderedDict

import numpy as np
import torch
from transformers import MPNetPreTrainedModel, MPNetModel, AutoTokenizer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.example import ARTICLE_TEXT


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output
    input_mask_expanded = attention_mask.unsqueeze(-1)
    input_mask_expanded = input_mask_expanded.expand(token_embeddings.size()).float()

    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )


class ESGify(MPNetPreTrainedModel):
    """Model for Classification ESG risks from text."""

    def __init__(self, config):
        """ """
        super().__init__(config)
        # Instantiate Parts of model
        self.mpnet = MPNetModel(config, add_pooling_layer=False)
        self.id2label = config.id2label
        self.label2id = config.label2id
        self.classifier = torch.nn.Sequential(
            OrderedDict(
                [
                    ("norm", torch.nn.BatchNorm1d(768)),
                    ("linear", torch.nn.Linear(768, 512)),
                    ("act", torch.nn.ReLU()),
                    ("batch_n", torch.nn.BatchNorm1d(512)),
                    ("drop_class", torch.nn.Dropout(0.2)),
                    ("class_l", torch.nn.Linear(512, 47)),
                ]
            )
        )

    def forward(self, input_ids, attention_mask):
        # Feed input to mpnet model
        outputs = self.mpnet(input_ids=input_ids, attention_mask=attention_mask)

        # mean pooling dataset and eed input to classifier to compute logits
        logits = self.classifier(
            mean_pooling(outputs["last_hidden_state"], attention_mask)
        )

        # apply sigmoid
        logits = 1.0 / (1.0 + torch.exp(-logits))

        return logits


model = ESGify.from_pretrained("ai-lab/ESGify")
tokenizer = AutoTokenizer.from_pretrained("ai-lab/ESGify")

text = ARTICLE_TEXT

model = ESGify.from_pretrained("ai-lab/ESGify")
tokenizer = AutoTokenizer.from_pretrained("ai-lab/ESGify")

texts = [text]
to_model = tokenizer.batch_encode_plus(
    texts,
    add_special_tokens=True,
    max_length=512,
    return_token_type_ids=False,
    padding="max_length",
    truncation=True,
    return_attention_mask=True,
    return_tensors="pt",
)
results = model(**to_model)

for i in torch.topk(results, k=3).indices.tolist()[0]:
    print(f"{model.id2label[i]}: {np.round(results.flatten()[i].item(), 3)}")
