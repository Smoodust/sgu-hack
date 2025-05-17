import onnx
import onnxruntime as rt
import numpy as np
from tokenizers import Tokenizer


class BertLikeONNX:
    def __init__(self, model_uri: str):
        self.session = rt.InferenceSession(
            model_uri,
            providers=rt.get_available_providers(),
        )
        self.tokenizer = Tokenizer.from_file(
            "NN_models/tokenizer.json"
        )
        self.tokenizer.enable_truncation(max_length=512)

    def __call__(self, text: str):
        output = self.tokenizer.encode(text)
        preds = self.session.run(
            ['final_output'],
            {
                "input_ids": np.expand_dims(np.array(output.ids), axis=0).astype("int64"),
                "attention_mask": np.expand_dims(np.array(output.attention_mask), axis=0).astype("int64")
            }
        )[0]
        return preds[0]


logs_embedder = BertLikeONNX("NN_models/embedder.onnx")