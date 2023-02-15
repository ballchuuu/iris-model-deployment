import pandas as pd
from sklearn.linear_model import LogisticRegression

from utils import train_test_split_by_species
from utils import train_model

if __name__ == "__main__":
    df = pd.read_csv("../data/Iris.csv")

    # Train test split
    X = df.drop(["Species", "Id"], axis=1)
    y = df["Species"]
    X_train, X_test, y_train, y_test = train_test_split_by_species(X=X, y=y, test_size=0.25)

    # initialise model
    model = LogisticRegression()

    # train model and save weights to pickle file
    model = train_model(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test, model=model, model_name="log_reg")