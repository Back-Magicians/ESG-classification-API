import torch
import numpy as np
from transformers import AutoTokenizer

from src.models.model import ESGify


def predict_pretrained(text: str):
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

    model_result = model(**to_model)
    result = {}

    for i in torch.topk(model_result, k=3).indices.tolist()[0]:
        result[model.id2label[i]] = np.round(
            model_result.flatten()[i].item(), 3
        )

    return result
