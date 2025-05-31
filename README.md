# smart-sales-kamana

**Module 1:
**
Initial Tools Setup including VS-Code, Python and Github

**Module 2:
**
Created Project Repository in Github.
Created .gitignore and requirements.txt files.
Created raw/data folder and added csv files holding data to be used.
Created utils folder and added logger.py file which would generate logs.
Created logs folder and added project_log.log file which would display logs.
Created scripts folder and added data_prep.py files. 

**Module 3:
**
Created functions for collecting and cleaning data from csv files. 
Data cleaning functions including handling missing values, removing duplicates and outliers were designed and saved under scripts/data_preparation folder. 
Data_preparation file was individually created for each data file. Example: prepare_products_data.py, and prepare_sales_data.py
After executing the data_preparation files, new prepared csv data should be seen under data/prepared folder.

Notes: 
Use command .\.venv\scripts\activate from your project folder to activate Virtual Environment. 
Use command python .\scripts\data_preparation\prepare_customers_data.py to run data cleaning functions for each data_preparation file created. 

**Module 4:
**
Data Warehouse creating functions implemented in etl_to_dw.py file to retrieve clean prepared data and load to dw.
The file is created under scripts\create_dw folder, which when executed creates new database names smart_sales.db under data\dw consisting of three new tables customer, product and sales.

Customer Table:
![image](https://github.com/user-attachments/assets/dc842c7b-34ca-411c-8479-083a4b2c5f24)

Product Table:
![image](https://github.com/user-attachments/assets/e9503bff-665e-4993-ad91-578613161855)

Sale Table:

![image](https://github.com/user-attachments/assets/00cc6f5d-cbfe-41a3-8e3f-0c3bad8b415b)

