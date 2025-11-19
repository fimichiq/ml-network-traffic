import numpy as np
import os
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

NETFLOWS_FOLDER: str = "../../shared-files/Netflows/"
ID_COLUMNS = ["Flow ID", "Src IP", "Timestamp", "Dst IP"]


def replace_nans(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function with purpose of replacing missing data with 0.
    Historically it has proven that missing values in those dfs are just
    numbers too big to read.

    :param df: pandas dataframe containing data to process
    """
    df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    return df


def pop_columns(df: pd.DataFrame, columns: list) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Function to pop columns which do not participate in classification

    :param df: pandas dataframe containing data to process
    :param columns: list of column names to drop
    """
    df = df.drop("Label")
    popped_columns = df[columns]
    df = df.drop(columns=columns)
    return df, popped_columns

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to normalize the data.
    The left skewness is being normalized by squaring the numbers.
    The right skewness is being normalized by logarithmizing the numbers.

    :param df: pandas dataframe containing data to normalize
    """
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    df_norm = df.copy()
    for col in numeric_columns:
        if df[col].skew() > 0 or col == "Src Port":
            df_norm[col] = np.log1p(df[col].clip(lower=-0.99))  # Ensures log1p always gets valid input
        elif df[col].skew() < 0:
            df_norm[col] = df[col] ** 2  # Can cause overflow
    return df_norm


class Preprocessor:
    """
    Class responsible for preprocessing data based on mode which is being used.

    Possible modes are:
        - multiclass: processing focuses on filling missing values and scaling the data
        - binary: as above also, changes labels from type of attack (ex. DDoS) to simple ATTACK; Also used for unary case

    """

    def __init__(self, netflow_file: str, binary: bool = False):
        """

        :param netflow_file: filename pointing on file with dataset to work on
        :param binary: bool pointing that training/classification should be binary
        """
        self.netflow_file = os.path.join(NETFLOWS_FOLDER, netflow_file)

        if os.path.isfile(self.netflow_file):
            raise Exception(f"File {netflow_file} does not exists!")

        self.binary = binary

    def preprocess_train(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Function preprocess data for training/partial training.

        Keeps Label since it is assumed that it contains valid classes.

        returns
        """
        df = pd.read_csv(self.netflow_file)

        df = replace_nans(df)

        df = normalize(df)

        # Training the model; The label is needed; Drop ID_COLUMNS
        df = df.drop(columns=ID_COLUMNS, axis=1)
        x = df.drop(columns=["Label"], axis=1)
        y = df["Label"]

        # bin & unary
        if self.binary:
            y = y.apply(lambda l: 0 if l == "BENIGN" else 1)

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

        scaler = StandardScaler()

        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)

        pca = PCA(n_components=13)

        x_train = pca.fit_transform(x_train)
        x_test = pca.transform(x_test)

        return x_train, x_test, y_train, y_test

    def preprocess_classify(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Function preprocess data for classification.

        Mirrors process which was taken for trained data.
        Drops Label since it is not needed.

        Uses StandardScaler and PCA

        returns two DataFrames:
        1. preprocessed x
        2. columns to be attached after classification for identification of flows
        """
        df = pd.read_csv(self.netflow_file)

        df = replace_nans(df)

        df = normalize(df)
        # Pop unnecessary columns for machine learning model; Attach them later for identification of flows
        x, id_cols = pop_columns(df, columns=ID_COLUMNS)

        # Classifying with model; Label is not defined - drop; Need ID_COLUMNS
        x = x.drop(columns=["Label"], axis=1)

        scaler = StandardScaler()

        x = scaler.transform(x)

        pca = PCA(n_components=13)

        x = pca.transform(x)

        return x, id_cols





