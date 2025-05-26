"""
scripts/data_preparation/prepare_sales.py

This script reads data from the data/raw folder, cleans the data, 
and writes the cleaned version to the data/prepared folder.

Tasks:
- Remove duplicates
- Handle missing values
- Remove outliers
- Ensure consistent formatting

"""

#####################################
# Import Modules at the Top
#####################################

# Import from Python Standard Library
import pathlib
import sys

# Import from external packages (requires a virtual environment)
import pandas as pd

# Ensure project root is in sys.path for local imports (now 3 parents are needed)
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))

# Import local modules (e.g. utils/logger.py)
from utils.logger import logger  

# Optional: Use a data_scrubber module for common data cleaning tasks
from utils.data_scrubber import DataScrubber  


# Constants
SCRIPTS_DATA_PREP_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent  # Directory of the current script
SCRIPTS_DIR: pathlib.Path = SCRIPTS_DATA_PREP_DIR.parent 
PROJECT_ROOT: pathlib.Path = SCRIPTS_DIR.parent 
DATA_DIR: pathlib.Path = PROJECT_ROOT/ "data" 
RAW_DATA_DIR: pathlib.Path = DATA_DIR / "raw"  
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR / "prepared"  # place to store prepared data


# Ensure the directories exist or create them
DATA_DIR.mkdir(exist_ok=True)
RAW_DATA_DIR.mkdir(exist_ok=True)
PREPARED_DATA_DIR.mkdir(exist_ok=True)

#####################################
# Define Functions - Reusable blocks of code / instructions
#####################################

# TODO: Complete this by implementing functions based on the logic in the other scripts

def read_raw_data(file_name: str) -> pd.DataFrame:
    """
    Read raw data from CSV.

    Args:
        file_name (str): Name of the CSV file to read.
    
    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    logger.info(f"FUNCTION START: read_raw_data with file_name={file_name}")
    filepath = RAW_DATA_DIR.joinpath(file_name)
    df = pd.read_csv(filepath)
    logger.info(f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns")


    # TODO: OPTIONAL Add data profiling here to understand the dataset
    # Suggestion: Log the datatypes of each column and the number of unique values
    # Example:
    logger.info(f"Column datatypes: \n{df.dtypes}")
    logger.info(f"Number of unique values: \n{df.nunique()}")
    
    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame to clean.
    
    Returns:
        pd.DataFrame: DataFrame without duplicates.
    """
    logger.info(f"FUNCTION START: remove_duplicates with dataframe shape={df.shape}")
    columns_to_remove = ["CustomerID", "CampaignID"]
    df = df.drop_duplicates(subset=columns_to_remove, keep='first')
    logger.info(f"Removed duplicates based on columns {columns_to_remove}, new shape={df.shape}")
    return df

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame to clean.
    
    Returns:
        pd.DataFrame: DataFrame with missing values handled.
    """
    logger.info(f"FUNCTION START: handle_missing_values with dataframe shape={df.shape}")
    # Example: Fill missing values with the mean of the column

    missing_by_col = df.isna().sum()
    logger.info(f"Missing values by column before handling:\n{missing_by_col}")
    
    #Convert SaleAmount column to float64 if not already
    df['SaleAmount'] = df['SaleAmount'].astype('float64')
    logger.info(f"Converted SaleAmount to float64, current dtype: {df['SaleAmount'].dtype}")
    for column in df.select_dtypes(include=['float64', 'int64']).columns:
        logger.info(f"Handling missing values for column: {column}")
        mean_value = df[column].mean()
        round_times = 1  if column == 'CampaignID' else 2  # Round CampaignID to 1 decimal places, others to 2
        df[column].fillna(mean_value.round(round_times), inplace=True)
        logger.info(f"Filled missing values in {column} with mean value {mean_value}")
        df.loc[df[column] <= 0, column] = mean_value.round(round_times)  # Fill zero values with mean
        logger.info(f"Filled zero values in {column} with mean value {mean_value}")

    df['PaymentType'].fillna('Cash', inplace=True)  
    
    # Log missing values by column after handling
    missing_by_col = df.isna().sum()
    logger.info(f"Missing values by column after handling:\n{missing_by_col}")
    logger.info(f"{len(df)} records remaining after handling missing values.")
    return df

def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outliers from the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame to clean.
    
    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """
    logger.info(f"FUNCTION START: remove_outliers with dataframe shape={df.shape}")

    for column in df.select_dtypes(include=['float64', 'int64']).columns:
        mean = df[column].mean()
        std = df[column].std()
        threshold = 3 * std
        df = df[(df[column] >= (mean - threshold)) & (df[column] <= (mean + threshold))]
        logger.info(f"Removed outliers based on Sales, new shape={df.shape}")
    
    return df

def save_prepared_data(df: pd.DataFrame, file_name: str) -> pd.DataFrame:
    """
    Save cleaned data to CSV.

    Args:
        df (pd.DataFrame): Cleaned DataFrame.
        file_name (str): Name of the output file.
    
    Returns:
        pd.DataFrame: DataFrame that was saved.
    """
    logger.info(f"FUNCTION START: save_prepared_data with file_name={file_name}, dataframe shape={df.shape}")
    file_path = PREPARED_DATA_DIR.joinpath(file_name)
    df.to_csv(file_path, index=False)
    logger.info(f"Data saved to {file_path}")
    
    return df

#####################################
# Define Main Function - The main entry point of the script
#####################################

def main() -> None:
    """
    Main function for processing data.
    """
    logger.info("==================================")
    logger.info("STARTING prepare_sales_data.py")
    logger.info("==================================")

    logger.info(f"Root         : {PROJECT_ROOT}")
    logger.info(f"data/raw     : {RAW_DATA_DIR}")
    logger.info(f"data/prepared: {PREPARED_DATA_DIR}")
    logger.info(f"scripts      : {SCRIPTS_DIR}")

    input_file = "sales_data.csv"
    output_file = "sales_prepared.csv"
    
    # Read raw data
    df = read_raw_data(input_file)

    # Record original shape
    original_shape = df.shape

    # Log initial dataframe information
    logger.info(f"Initial dataframe columns: {', '.join(df.columns.tolist())}")
    logger.info(f"Initial dataframe shape: {df.shape}")
    
    # Clean column names
    original_columns = df.columns.tolist()
    df.columns = df.columns.str.strip()
    
    # Log if any column names changed
    changed_columns = [f"{old} -> {new}" for old, new in zip(original_columns, df.columns) if old != new]
    if changed_columns:
        logger.info(f"Cleaned column names: {', '.join(changed_columns)}")

    df = remove_duplicates(df)
    
    df = handle_missing_values(df)

    df = remove_outliers(df)

    df = save_prepared_data(df, output_file)
    
    logger.info("==================================")
    logger.info(f"Original shape: {original_shape}")
    logger.info(f"Cleaned shape:  {df.shape}")
    logger.info("==================================")
    logger.info("FINISHED prepare_sales_data.py")
    logger.info("==================================")

#####################################
# Conditional Execution Block 
# Ensures the script runs only when executed directly
# This is a common Python convention.
#####################################

if __name__ == "__main__":
    main()