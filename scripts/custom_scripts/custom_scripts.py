import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pathlib
import sys

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from utils.logger import logger  # noqa: E402

# Constants
DATA_DIR: pathlib.Path = pathlib.Path("data")   
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR / "prepared"
CUSTOM_OUTPUT_DIR: pathlib.Path = pathlib.Path("data").joinpath("custom_outputs")
RESULTS_OUTPUT_DIR: pathlib.Path = pathlib.Path("data").joinpath("custom_project_results")

# Create output directory for results if it doesn't exist
CUSTOM_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load data
def load_data(file_name: str) -> pd.DataFrame:
    """Load prepared sales data from CSV."""
    try:
        file_path = PREPARED_DATA_DIR.joinpath(file_name)
        df = pd.read_csv(file_path)
        logger.info(f"Data successfully loaded from {file_path}.")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

# Aggregate data
def aggregate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales data by product category and Year."""
    logger.info("Aggregating sales data by product category and Year...")
    logger.info(f"Data shape before aggregation: {df.shape}")
    df['Year'] = pd.to_datetime(df['SaleDate']).dt.to_period('Y')  # Convert sale_date to Year
    df['SaleAmount'] = df['SaleAmount'].astype(float).round(2)  # Ensure sale_amount is float
    df['ProductCategory'] = df['ProductCategory'].astype(str)  # Ensure product_category is string
    logger.info(f"Data shape after aggregation: {df.shape}")
    # Group by product_category and Year, summing the sale_amount
    df = df.groupby(['ProductCategory', 'Year'])['SaleAmount'].sum().reset_index()
    return df

# Save Aggregated Data
def save_aggregated_data(df: pd.DataFrame, file_name: str) -> None:
    """Save the aggregated data to CSV."""
    try:
        file_path = CUSTOM_OUTPUT_DIR.joinpath(file_name)
        df.to_csv(file_path, index=False)
        logger.info(f"Aggregated data saved to {file_path}.")
        return df
    except Exception as e:
        logger.error(f"Error saving aggregated data: {e}")
        raise

# Create visualization
def visualize_sales_by_product_category_and_year(df: pd.DataFrame) -> None:
    """Visualize sales amount by product category and Year."""
    logger.info("Creating visualization for sales amount by product category and Year...")
    try:
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x='ProductCategory', y='SaleAmount', hue='Year')
        plt.title('Sales Amount by Product Category and Year')
        plt.xlabel('Product Category')
        plt.ylabel('Sales Amount')
        plt.legend(title='Year')
        plt.xticks(rotation=45)
        plt.tight_layout()
        # Save the visualization
        output_path = RESULTS_OUTPUT_DIR.joinpath("sales_by_product_category_and_year.png")
        plt.savefig(output_path)
        logger.info(f"Visualization saved to {output_path}.")
        plt.show()
        logger.info("Visualization created successfully.")
    except Exception as e:
        logger.error(f"Error creating visualization: {e}")
        raise

def visualize_top_category_per_year(df: pd.DataFrame) -> None:
    """Visualize the top product category with the highest sales for each year."""
    logger.info("Creating visualization for top category per year...")
    try:
        # Group by Year and ProductCategory, then sum sales
        grouped = df.groupby(['Year', 'ProductCategory'])['SaleAmount'].sum().reset_index()

        # Get top category per year
        top_category_per_year = (
            grouped.sort_values(['Year', 'SaleAmount'], ascending=[True, False])
                   .groupby('Year')
                   .head(1)
        )
        logger.info("Top categories per year:")
        logger.info(top_category_per_year)
        # Plot
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(
            data=top_category_per_year,
            x='Year',
            y='SaleAmount',
            hue='ProductCategory'
        )

        plt.title('Top Product Category per Year by Sales')
        plt.xlabel('Year')
        plt.ylabel('Total Sales Amount')
        plt.legend(title='Product Category', loc='upper right')
        plt.tight_layout()
        output_path = RESULTS_OUTPUT_DIR.joinpath("top_category_per_year.png")
        plt.savefig(output_path)
        logger.info(f"Top category per year visualization saved to {output_path}.")
        plt.show()
    except Exception as e:
        logger.error(f"Error creating top category per year visualization: {e}")
        raise

def main():
    """Main function for analyzing and visualizing sales data."""
    logger.info("Starting SALES_BY_PRODUCT_CATEGORY_AND_YEAR analysis...")

    # Step 1: Load sales data
    sales_df = load_data("sales_prepared.csv")
    logger.info(f"Sales data loaded with shape: {sales_df.shape}")

    # Step 2: Load product data and merge with sales data
    product_df = load_data("products_prepared.csv")
    logger.info(f"Product data loaded with shape: {product_df.shape}")
    
    #Step 3: Rename columns for clarity and merged product data with sales data
    product_df = product_df.rename(columns={'category': 'ProductCategory', 'productid': 'ProductID'})    
    sales_df = sales_df.merge(product_df[['ProductID', 'ProductCategory']], on='ProductID', how='left')
    logger.info(f"Sales data merged with product data. New shape: {sales_df.shape}")

    # Step 4: Aggregate data
    df = aggregate_data(sales_df)
    logger.info(f"Aggregated data shape: {df.shape}")

    # Step 5: Save the aggregated data
    df = save_aggregated_data(df, "sales_by_product_category_and_year.csv")
    logger.info("Aggregated data saved successfully.")

    # Step 6: Visualize sales by product category and Year
    visualize_sales_by_product_category_and_year(df)
    logger.info("Analysis and visualization completed successfully.")

    # Step 7: Visualize top product categories by year
    visualize_top_category_per_year(df)
    logger.info("Top product categories visualization completed successfully.")

if __name__ == "__main__":
    main()