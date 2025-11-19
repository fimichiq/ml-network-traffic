import pandas as pd

class CSVReader:
    """
    Class responsible for reading CSV files.
    """
    def __init__(self):
        self.df_after_read = None
        self.df_after_preprocess = None
    
    def read(self, csv_file: str):
        """
        Function responsible for reading CSV files into pandas data frame. 
        Also saves data frame to self.df_after_read.
        :param csv_file: Path to the CSV file to be read.
        :return: returns data frame created from CSV file.
        """
        df = pd.read_csv(csv_file)
        self.df_after_read = df
        return df
        
