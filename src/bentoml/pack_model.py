import pickle
import bentoml 

from config import settings

"""
This file is only ran when a new model has been trained and confirmed to used for deployment.
"""

if __name__ == "__main__":
    filename = f"assets/{settings.pickle_model_name}.pkl"
    loaded_model = pickle.load(open(filename, 'rb'))
    print(f"[SUCCESS]: Loaded model from {filename} \n")

    # put model into bentoml store
    saved_model = bentoml.sklearn.save_model(
        name=settings.bento_model_name, 
        model=loaded_model,
        signatures={
        "predict": {
            "batchable": True,
        }}
    )
    print(f"[SUCCESS]: Saved model to {settings.bento_model_name}")


