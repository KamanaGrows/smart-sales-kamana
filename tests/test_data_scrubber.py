import unittest
import pandas as pd
from utils.data_scrubber import DataScrubber  
from utils.logger import logger  

class TestDataScrubber(unittest.TestCase):
    
    def setUp(self):
        # Sample data for testing
        self.data = {
            'ID': [1, 2, 3, 4, 5, 5, 6, 7],
            'Name': ["Ram", "Tom", "Jose", "Sam", "Bob", "Bob", "Kai", "Sai"],
            'Age': [20, 27, 44, 30, 57, 57, 47, 31]
        }
        self.df = pd.DataFrame(self.data)
        self.scrubber = DataScrubber(self.df)

    def test_convert_column_to_new_data_type(self):
        # Test converting 'ID' column to float
        self.scrubber.convert_column_to_new_data_type('ID', 'int')
        self.assertTrue(self.df['ID'].dtype == 'int')

    def test_drop_column(self):
        # Test dropping 'Age' column
        columns = ['Name']
        df = self.scrubber.drop_columns(columns=columns)
        logger.info(f"DataFrame after dropping columns {columns}:\n{df}")
        self.assertNotIn('Name', df.columns)

    def test_filter_column_outliers(self):      
        # Test filtering outliers in 'Age' column
        df = self.scrubber.filter_column_outliers('Age', 20, 50)
        logger.info(f"DataFrame after filtering outliers in 'Age':\n{df}")
        self.assertTrue(all(df['Age'] >= 20) and all(df['Age'] <= 50))

    def test_remove_duplicate_records(self):
        # Test removing duplicate records
        df = self.scrubber.remove_duplicate_records()
        logger.info(f"DataFrame after removing duplicates:\n{df}")
        self.assertEqual(len(df), 7)

    def test_handle_missing_data(self):
        df = self.scrubber.handle_missing_data(fill_value="N/A")
        self.assertFalse(df.isnull().values.any())

if __name__ == '__main__':
    unittest.main()