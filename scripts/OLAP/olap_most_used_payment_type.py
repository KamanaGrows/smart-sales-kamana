"""
Module 6: OLAP Goal Script (uses cubed results)
File: scripts/olap_goals_sales_by_weekday.py

This script uses our precomputed cubed data set to get the information 
we need to answer a specific business goal. 

GOAL: Analyze sales data to determine which day of the week 
consistently shows the lowest sales revenue. 

ACTION: This can help inform decisions about reducing operating hours 
or focusing marketing efforts on less profitable days.

PROCESS: 
Group transactions by the day of the week.
Sum SaleAmount for each day.
Identify the day with the lowest total revenue.

This example assumes a cube data set with the following column names (yours will differ).
DayOfWeek,product_id,customer_id,sale_amount_usd_sum,sale_amount_usd_mean,sale_id_count,sale_ids
Friday,101,1001,6344.96,6344.96,1,[582]
etc.
"""

import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import sys

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from utils.logger import logger  # noqa: E402

# Constants
OLAP_OUTPUT_DIR: pathlib.Path = pathlib.Path("data").joinpath("olap_cubing_outputs")
CUBED_FILE: pathlib.Path = OLAP_OUTPUT_DIR.joinpath("multidimensional_olap_cube.csv")
RESULTS_OUTPUT_DIR: pathlib.Path = pathlib.Path("data").joinpath("results")

# Create output directory for results if it doesn't exist
RESULTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_olap_cube(file_path: pathlib.Path) -> pd.DataFrame:
    """Load the precomputed OLAP cube data."""
    try:
        cube_df = pd.read_csv(file_path)
        logger.info(f"OLAP cube data successfully loaded from {file_path}.")
        return cube_df
    except Exception as e:
        logger.error(f"Error loading OLAP cube data: {e}")
        raise


def analyze_sales_by_paymenttype(cube_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total sales by payment type."""
    try:
        # Group by payment_type and sum the sales
        sales_by_paymenttype = (
            cube_df.groupby("payment_type")["sale_amount_sum"].sum().reset_index()
        )
        sales_by_paymenttype.rename(columns={"sale_amount_sum": "TotalSales"}, inplace=True)
        sales_by_paymenttype.sort_values(by="TotalSales", inplace=True)
        logger.info("Sales aggregated by payment_type successfully.")
        return sales_by_paymenttype
    except Exception as e:
        logger.error(f"Error analyzing sales by payment_type: {e}")
        raise


def identify_least_used_payment_type(sales_by_paymenttype: pd.DataFrame) -> str:
    """Identify the payment type with the lowest total sales revenue."""
    try:
        least_used_payment_type = sales_by_paymenttype.iloc[0]
        logger.info(
            f"Least used payment type: {least_used_payment_type['payment_type']} with revenue ${least_used_payment_type['TotalSales']:.2f}."
        )
        return least_used_payment_type["payment_type"]
    except Exception as e:
        logger.error(f"Error identifying least used payment type: {e}")
        raise

def identify_most_used_payment_type(sales_by_paymenttype: pd.DataFrame) -> str:
    """Identify the payment type with the highest total sales revenue."""
    try:
        most_used_payment_type = sales_by_paymenttype.iloc[-1]
        logger.info(
            f"Most used payment type: {most_used_payment_type['payment_type']} with revenue ${most_used_payment_type['TotalSales']:.2f}."
        )
        return most_used_payment_type["payment_type"]
    except Exception as e:
        logger.error(f"Error identifying most used payment type: {e}")
        raise

def visualize_sales_by_payment_type(sales_by_paymenttype: pd.DataFrame) -> None:
    """Visualize total sales by payment type."""
    try:
        plt.figure(figsize=(10, 6))
        plt.bar(
            sales_by_paymenttype["payment_type"],
            sales_by_paymenttype["TotalSales"],
            color="skyblue",
        )
        plt.title("Total Sales by Payment Type", fontsize=16)
        plt.xlabel("Payment Type", fontsize=12)
        plt.ylabel("Total Sales (USD)", fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the visualization
        output_path = RESULTS_OUTPUT_DIR.joinpath("sales_by_payment_type.png")
        plt.savefig(output_path)
        logger.info(f"Visualization saved to {output_path}.")
        plt.show()
    except Exception as e:
        logger.error(f"Error visualizing sales by payment type: {e}")
        raise


def main():
    """Main function for analyzing and visualizing sales data."""
    logger.info("Starting SALES_BY_PAYMENT_TYPE analysis...")

    # Step 1: Load the precomputed OLAP cube
    cube_df = load_olap_cube(CUBED_FILE)

    # Step 2: Analyze total sales by payment type
    sales_by_paymenttype = analyze_sales_by_paymenttype(cube_df)

    # Step 3: Identify the highest revenue by payment type
    least_used_payment_type = identify_least_used_payment_type(sales_by_paymenttype)
    logger.info(f"Least revenue by payment type: {least_used_payment_type}")
    logger.info("Close the Figure to complete this script.")

    # Step 4: Identify the most revenue by payment type
    most_used_payment_type = identify_most_used_payment_type(sales_by_paymenttype)
    logger.info(f"Most revenue by payment type: {most_used_payment_type}")
    logger.info("Close the Figure to complete this script.")

    # Step 5: Visualize total sales by payment type
    visualize_sales_by_payment_type(sales_by_paymenttype)
    logger.info("Analysis and visualization completed successfully.")


if __name__ == "__main__":
    main()