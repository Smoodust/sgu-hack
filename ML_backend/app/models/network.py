import onnx
import onnxruntime as rt
from tokenizers import Tokenizer


class BertLikeONNX:
    def __init__(self, model_uri: str, k: int = 5):
        self.k = k
        self.session = rt.InferenceSession(
            model_uri,
            providers=rt.get_available_providers(),
        )
        self.tokenizer = Tokenizer.from_file(
            "tokenizer.json"
        )
        self.tokenizer.enable_truncation(max_length=512)

    def __call__(self, text: str):
        output = self.tokenizer.encode(text)
        preds = self.session.run(
            None,
            {
                "input_ids": output.ids,
                "attention_mask": output.attention_mask
            }
        )[0]
        return preds
