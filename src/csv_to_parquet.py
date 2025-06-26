import pandas as pd

def csv_to_parquet(csv_file_path, parquet_file_path, **kwargs):
    """
    Converts a CSV file to a Parquet file.

    Args:
        csv_file_path (str): The path to the input CSV file.
        parquet_file_path (str): The path to the output Parquet file.
        **kwargs: Additional arguments to pass to pandas.read_csv()
                  (e.g., sep, encoding, header).
    """
    try:
        # Read the CSV file into a Pandas DataFrame
        # We assume common CSV parameters, but you can pass more via kwargs for read_csv
        df = pd.read_csv(csv_file_path, **kwargs)

        # Write the DataFrame to a Parquet file
        df.to_parquet(parquet_file_path, engine='pyarrow', index=False)

        print(f"Successfully converted '{csv_file_path}' to '{parquet_file_path}'")
    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_file_path}'")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

# Example usage (assuming 'your_data.csv' exists from the previous conversion)
input_csv = "your_data.csv"
output_parquet = "your_data_reconverted.parquet"

# Example: Create a dummy CSV file if 'your_data.csv' doesn't exist
try:
    with open(input_csv, 'w') as f:
        f.write("col1,col2,col3\n1,A,True\n2,B,False\n3,C,True\n")
except Exception as e:
    print(f"Could not create dummy CSV: {e}")

csv_to_parquet(input_csv, output_parquet)

# You can also specify additional CSV reading options, for example:
# csv_to_parquet("your_data_tab_separated.csv", "output.parquet", sep='\t')
