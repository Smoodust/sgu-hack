import numpy as np
import onnx
import onnxruntime as rt


class NetworkONNX:
    def __init__(self, model_uri: str = "models:/multivae/1", k: int = 5):
        self.k = k
        self.session = rt.InferenceSession(
            model_uri,
            providers=rt.get_available_providers(),
        )
        self.input_name = self.session.get_inputs()[0].name
        self.input_shape = self.session.get_inputs()[0].shape 

    def __call__(self, feature):
        feature = np.asarray(feature, dtype=np.float32)
        
        if len(feature.shape) == 1:
            feature = feature.reshape(1, -1)
            
        preds = self.session.run(None, {self.input_name: feature})[0]
        return np.argpartition(preds, -self.k)[-self.k :].tolist()


model = NetworkONNX(model_uri="models/multivae.onnx")
