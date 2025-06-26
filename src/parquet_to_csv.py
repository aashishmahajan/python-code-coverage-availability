import pandas as pd

def parquet_to_csv(parquet_file_path, csv_file_path, **kwargs):
    """
    Converts a Parquet file to a CSV file.

    Args:
        parquet_file_path (str): The path to the input Parquet file.
        csv_file_path (str): The path to the output CSV file.
        **kwargs: Additional arguments to pass to pandas.DataFrame.to_csv()
                  (e.g., sep, encoding, index, header).
    """
    try:
        # Read the Parquet file into a Pandas DataFrame
        df = pd.read_parquet(parquet_file_path, engine='pyarrow')

        # Write the DataFrame to a CSV file
        # index=False prevents pandas from writing the DataFrame index as a column in the CSV
        df.to_csv(csv_file_path, index=False, **kwargs)

        print(f"Successfully converted '{parquet_file_path}' to '{csv_file_path}'")
    except FileNotFoundError:
        print(f"Error: Parquet file not found at '{parquet_file_path}'")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

# Example usage:
#input_parquet = "your_data.parquet"  # Replace with your Parquet file path
#output_csv = "your_data.csv"        # Replace with your desired CSV output path

# Create a dummy parquet file for demonstration
#data = {'col1': [1, 2, 3], 'col2': ['A', 'B', 'C'], 'col3': [True, False, True]}
#df_dummy = pd.DataFrame(data)
#df_dummy.to_parquet(input_parquet, engine='pyarrow')

# parquet_to_csv(input_parquet, output_csv)

# You can also specify additional CSV writing options, for example:
# parquet_to_csv(input_parquet, "your_data_tab_separated.csv", sep='\t', encoding='utf-8')
