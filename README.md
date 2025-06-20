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

**Module 5**:

Data Analysis using Power BI. 

Installations:
Installed Power BI Desktop.
Installed SQLite ODBC Driver.
Configured ODBC Data Source Name SmartSalesDSN
    Opened ODBC Data Sources (64-bit) from the Start Menu.
    Clicked the System DSN tab.
    Clicked Add → selected SQLite3 ODBC Driver → clicked Finish.
    Gave DSN Name SmartSalesDSN.
    Clicked Browse and selected database file, smart_sales.db . 
    Click OK to save.

PowerBI Setup 
    Clicked Get Data (top left) → Select ODBC from the list.
    Selected the DSN SmartSalesDSN.
    Selected the tables you want to analyze:
        Customer table
        Product table
        Sales table
    Clicked Load to bring the tables into Power BI.

- Utilizing SQL on PowerBI

In the Home tab, clicked Transform Data to open Power Query Editor.
In Power Query Editor, clicked Advanced Editor (top menu).
Executed below Query

let 
source = ODBC.Query("dsn=SMARtSalesDSN",
    "SELECT c.name, SUM(s.amount) AS total_spent
    FROM sale s
    JOIN customer c ON s.customer_id = c.customer_id
    GROUP BY c.name
    ORDER BY total_spent DESC;")
in 
source

![image](https://github.com/user-attachments/assets/2db0f9c7-82d7-4927-8db6-df8940175e6c)

Result: Table displaying Total Spent for each customer. 

![image](https://github.com/user-attachments/assets/565ecb1d-c7dd-4c3a-81eb-176a382cf30f)

In the Model View, Table connection displaying modified Sales Table. 

![image](https://github.com/user-attachments/assets/0cb9b940-cce4-4bcb-918e-250f6063e110)

Data Slicing

Transformed Data to show customer joining date in the range of Year, Quarter, Month

![image](https://github.com/user-attachments/assets/f1792508-4a47-4ee3-a575-0af9db0e5ac2)

Data Dicing

Transformed Product data to display products based on Category and Condition

![image](https://github.com/user-attachments/assets/4f7ba6f1-71a6-4fd6-ad9d-ad8c02e373c4)

Clustered Chart

Created Chart to display customers' rewards points accumulation based on Year, Quarter, and Month

![image](https://github.com/user-attachments/assets/136d1903-3aad-44a0-a7a4-8fa25147ac72)

Final Visualization dashboard after doing key data transformation activities. 

![image](https://github.com/user-attachments/assets/1c83bc7c-b6dd-427b-9f48-b962c2920ab4)

**Module 6**:

OLAP Cubing

- Under scripts/OLAP created a olap_cubing file: scripts/olap_cubing.py. 
- Utilized Sales Data from smart_sales.db to ingest data into olap cubing.
- Dimensions: PaymentType, Metrics: Total sale amount by payment type, total sales count by payment type.
- Data from new olap cubing results saved under \data\olap_cubing_outputs\multidimensional_olap_cube.csv.
![image](https://github.com/user-attachments/assets/08fe6a2d-01c2-48d8-9995-d996053611b2)

Analysis through OLAP Cubing

- Under scripts/OLAP created an olap_most_used_paymenttype file: scripts/olap_most_used_paymenttype.py. 
- Added functions to analyze sales data based on payment type used.
- Added functions to visualize the sales amount based on payment type used.4
  
![HighestAndLowestPaymentTypeRevenue](https://github.com/user-attachments/assets/8b95b126-c405-44ef-b559-057262f6cab6)

- Added the visualization result data to \data\results\sales_by_payment_type.png

![Sales_By_PaymentType](https://github.com/user-attachments/assets/f8052de5-df6e-425f-9ca3-33988729cd26)

**Module 7**:

Final Report – Custom BI Project 

Business Goal: 
Analyze sales of each product category per year and determine the highest performing category for each year.

Process:
- Created custom_scripts.py file under scripts/custom_scripts folder.
- Added function to load sales data from sales_prepared.csv file.
- Added function to slice ProductCategory column data and merge into the sales data file.
- Added function to aggregate data by ProductCategory and Year (extracted from SaleDate) and save into file under data/custom_outputs as   sales_by_product_category_and_year.csv.
- Added function to Visualize SalesAmount by ProductCategory and Year, and save the visualized data under folder data custom_project_results as sales_by_product_category_and_year.png.
- Added function to Visualize the top ProductCategory with the highest sales for each year, and save the visualized data under folder data/custom_project_results as top_category_per_year.png.

Results:
- Aggregrated Data with ProductCategory, Year, and SaleAmount.
![image](https://github.com/user-attachments/assets/77f8902b-0e4b-4619-9dc0-702ad1978553)

- Visualization of SalesAmount by ProductCategory and Year.
![image](https://github.com/user-attachments/assets/18326648-8d1b-4a57-91e4-dd5309cfeb25)

- Visualization of top ProductCategory per Year. 
![image](https://github.com/user-attachments/assets/15824658-031f-44a7-9178-33eba5a7e910)

