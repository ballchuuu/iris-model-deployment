from typing import Union
import sqlite3
import datetime
import pickle

# EDA
import pandas as pd
import matplotlib.pyplot as plt

# Data Preparation
import sklearn
from sklearn.model_selection import train_test_split

# Model Training
from sklearn.metrics import accuracy_score


def train_test_split_by_species(
    X: pd.DataFrame, 
    y: pd.Series, 
    test_size: float = 0.25,
    random_state: int = 42) -> Union[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    
    """
    Function performs train test split by species to ensure that each species has some rows in train set and test set
    Outputs: X_train, X_test, y_train, y_test
    
    Note: As the dataset here is small, validation set is not used.
    """

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    stratify=y, 
                                                    test_size=test_size,
                                                    random_state=random_state)

    print(f"Number of train rows: {len(X_train)}")
    print(f"Number of test rows: {len(X_test)}")
    return X_train, X_test, y_train, y_test


def push_metric_to_db(db_name:str, model_name: str, train_acc: float, test_acc: float) -> bool:
    """
    Creates a simple table in sqlite db that tracks the metric of each model trained. 
    Cols: id, model_name, timestamp, accuracy_metric

    Output: Boolean on whether the metric was pushed to db and model id 
    """

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    metric_table_name = "iris_model_metric"
   
    try:
        # create metric table if it does not exist
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {metric_table_name} (id INTEGER PRIMARY KEY, model_name TEXT, updated_at TIMESTAMP, test_acc FLOAT, train_acc FLOAT);
        """
        c.execute(create_query)

        # update table with new metric
        timestamp = datetime.datetime.now()
        insert_query = f"""
        INSERT INTO '{metric_table_name}' (model_name, updated_at, test_acc, train_acc)
        VALUES (?, ?, ?, ?);
        """
        c.execute(insert_query, (model_name, timestamp, test_acc, train_acc))
        conn.commit()

        # get model id (to save model weights with unique name)
        model_ver_query = f"""
        SELECT 
            id
        FROM 
            {metric_table_name}
        ORDER BY updated_at DESC
        LIMIT 1
        """
        c.execute(model_ver_query)
        sql_result = c.fetchone()
        model_ver = sql_result[0]

    except Exception as e:
        print("[ERROR]: Failed to update table")
        print(str(e))

        # default model version is 0
        return False, 0
        
    finally:
        c.close()
        conn.close()

    return True, model_ver 
    

def train_model(
    X_train: pd.DataFrame, 
    X_test: pd.DataFrame, 
    y_train: pd.Series, 
    y_test: pd.Series,
    model: sklearn.base.BaseEstimator,
    model_name: str,
    db_name: str = "../../data/database.sqlite") -> sklearn.base.BaseEstimator:

    """
    Function is model agnostic and takes in any sklearn model for training. 
    After training the weights are saved in the form of a pickle file with the metrics saved to the SQLite database
    Outputs: model (i.e. trained_model) 
    """

    # train given model
    model.fit(X_train,y_train)

    # obtain predictions for test set
    train_prediction = model.predict(X_train)
    test_prediction = model.predict(X_test)
    train_acc, test_acc = accuracy_score(y_train, train_prediction), accuracy_score(y_test, test_prediction)
    print("[SUCCESS]: Completed model training \n")

    # push model metrics to database and return model version
    pushed_bool, model_ver = push_metric_to_db(db_name=db_name, model_name=model_name, train_acc=train_acc, test_acc=test_acc)
    if not pushed_bool:
        print("[ERROR]: Unable to update metrics table with model training results")
    else:
        print(f"[SUCCESS]: Pushed model metrics to {db_name} for model: {model_name}")
        print(f"Train acc: {train_acc}, Test acc: {test_acc} \n")

    # save model to pickle file under assets: filename is a combination of model_name + model_id to uniquely differentiate the weights
    filename = f"../../src/bentoml/assets/{model_name}_{model_ver}.pkl"
    pickle.dump(model, open(filename, 'wb'))
    print(f"[SUCCESS]: Saved model weights to {filename} in the assets folder")

    return model


