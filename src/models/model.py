import torch
from collections import OrderedDict
from transformers import MPNetPreTrainedModel, MPNetModel


class ESGify(MPNetPreTrainedModel):
    """Model for Classification ESG risks from text."""

    @staticmethod
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output
        input_mask_expanded = attention_mask.unsqueeze(-1)
        input_mask_expanded = input_mask_expanded.expand(
            token_embeddings.size()
        ).float()

        return torch.sum(
            token_embeddings * input_mask_expanded, 1
        ) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def __init__(self, config):
        super().__init__(config)

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
        outputs = self.mpnet(
            input_ids=input_ids, attention_mask=attention_mask
        )

        logits = self.classifier(
            ESGify.mean_pooling(outputs["last_hidden_state"], attention_mask)
        )

        logits = 1.0 / (1.0 + torch.exp(-logits))

        return logits
