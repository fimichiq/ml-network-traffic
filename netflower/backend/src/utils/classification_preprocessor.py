import numpy as np
import os
import pandas as pd
import pickle
from config import CONVERT_FOLDER, UTILS_FOLDER

# Columns to exclude before classification
ID_COLUMNS = ["Flow ID", "Src IP", "Timestamp", "Dst IP"]

# 79 features expected by scaler (in correct order)
FEATURE_COLUMNS = [
    'Src Port', 'Dst Port', 'Protocol', 'Flow Duration', 'Tot Fwd Pkts',
    'Tot Bwd Pkts', 'TotLen Fwd Pkts', 'TotLen Bwd Pkts', 'Fwd Pkt Len Max',
    'Fwd Pkt Len Min', 'Fwd Pkt Len Mean', 'Fwd Pkt Len Std', 'Bwd Pkt Len Max',
    'Bwd Pkt Len Min', 'Bwd Pkt Len Mean', 'Bwd Pkt Len Std', 'Flow Byts/s',
    'Flow Pkts/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max',
    'Flow IAT Min', 'Fwd IAT Tot', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max',
    'Fwd IAT Min', 'Bwd IAT Tot', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max',
    'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags',
    'Bwd URG Flags', 'Fwd Header Len', 'Bwd Header Len', 'Fwd Pkts/s',
    'Bwd Pkts/s', 'Pkt Len Min', 'Pkt Len Max', 'Pkt Len Mean', 'Pkt Len Std',
    'Pkt Len Var', 'FIN Flag Cnt', 'SYN Flag Cnt', 'RST Flag Cnt', 'PSH Flag Cnt',
    'ACK Flag Cnt', 'URG Flag Cnt', 'CWE Flag Count', 'ECE Flag Cnt',
    'Down/Up Ratio', 'Pkt Size Avg', 'Fwd Seg Size Avg', 'Bwd Seg Size Avg',
    'Fwd Byts/b Avg', 'Fwd Pkts/b Avg', 'Fwd Blk Rate Avg', 'Bwd Byts/b Avg',
    'Bwd Pkts/b Avg', 'Bwd Blk Rate Avg', 'Subflow Fwd Pkts', 'Subflow Fwd Byts',
    'Subflow Bwd Pkts', 'Subflow Bwd Byts', 'Init Fwd Win Byts',
    'Init Bwd Win Byts', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean',
    'Active Std', 'Active Max', 'Active Min', 'Idle Mean', 'Idle Std', 'Idle Max',
    'Idle Min'
]


class ClassificationPreprocessor:
    """
    Preprocessor for preparing CICFlowMeter data for classification.

    Pipeline:
    1. Load CSV
    2. Replace inf/nan with 0
    3. Extract ID columns (Flow ID, Src IP, Dst IP, Timestamp)
    4. Select only features (79 columns)
    5. Normalization (log1p / square)
    6. Standardization (StandardScaler)
    7. Dimensionality reduction (PCA)
    """

    def __init__(self, netflow_file: str):
        """
        :param netflow_file: CSV filename from CONVERT_FOLDER
        """
        self.netflow_path = os.path.join(CONVERT_FOLDER, netflow_file)

        if not os.path.isfile(self.netflow_path):
            raise FileNotFoundError(f"File {netflow_file} does not exist in {CONVERT_FOLDER}")

        # Load scaler and PCA
        self.scaler = pickle.load(open(os.path.join(UTILS_FOLDER, 'scaler.pkl'), 'rb'))
        self.pca = pickle.load(open(os.path.join(UTILS_FOLDER, 'pca.pkl'), 'rb'))

    def preprocess(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Preprocesses data to classification-ready format.

        :return: tuple (X_pca, id_columns)
            - X_pca: DataFrame with 30 PCA components, ready for classification
            - id_columns: DataFrame with ID columns (Flow ID, Src IP, Dst IP, Timestamp)
        """
        # 1. Load CSV
        df = pd.read_csv(self.netflow_path)

        # 2. Replace inf/nan with 0
        df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

        # 3. Extract ID columns
        id_columns = df[ID_COLUMNS].copy()

        # 4. Select only features (in correct order)
        X = df[FEATURE_COLUMNS].copy()

        # 5. Normalization
        X = self._normalize(X)

        # 6. Standardization
        X_scaled = pd.DataFrame(
            self.scaler.transform(X),
            columns=FEATURE_COLUMNS
        )

        # 7. PCA
        X_pca = pd.DataFrame(
            self.pca.transform(X_scaled),
            columns=[f'PC{i+1}' for i in range(self.pca.n_components_)]
        )

        return X_pca, id_columns

    def _normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize data:
        - skewness > 0 or column 'Src Port': log1p
        - skewness < 0: square
        """
        df_norm = df.copy()
        for col in df.columns:
            skew = df[col].skew()
            if skew > 0 or col == "Src Port":
                df_norm[col] = np.log1p(df[col].clip(lower=-0.99))
            elif skew < 0:
                df_norm[col] = df[col] ** 2
        return df_norm
