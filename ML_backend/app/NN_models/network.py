from typing import cast
import onnx
import onnxruntime as rt
import numpy as np
from tokenizers import Tokenizer


class BertLikeONNX:
    """A class to handle ONNX model inference for BERT-like text embeddings."""

    def __init__(self, model_uri: str) -> None:
        """
        Initialize the ONNX model session and tokenizer.
        
        Args:
            model_uri: Path to the ONNX model file
        """

        self.session = rt.InferenceSession(
            model_uri,
            providers=rt.get_available_providers(),
        )
        self.tokenizer = Tokenizer.from_file(
            "NN_models/tokenizer.json"
        )
        self.tokenizer.enable_truncation(max_length=512)

    def __call__(self, text: str):
        """
        Process text and generate embedding.
        
        Args:
            text: Input text to process
            
        Returns:
            Embedding vector
        """

        output = self.tokenizer.encode(text)
        inputs_ids = np.expand_dims(np.array(output.ids), axis=0).astype("int64")
        attention_mask = np.expand_dims(np.array(output.attention_mask), axis=0).astype("int64")
        preds = self.session.run(
            ['final_output'],
            {
                "input_ids": inputs_ids,
                "attention_mask": attention_mask
            }
        )[0][0]
        return cast(np.ndarray, preds)


logs_embedder = BertLikeONNX("NN_models/embedder.onnx")