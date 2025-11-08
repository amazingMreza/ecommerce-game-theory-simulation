# file: data_loader.py

import pandas as pd

def load_and_preprocess_data(file_path: str) -> pd.DataFrame:
    
    print("--- Task I: Data Preparation ---")

    try:
        df = pd.read_excel(file_path)
        print(f"Successfully loaded data from '{file_path}'.")
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
        exit()

    print("\nInitial data information:")
    df.info()
    print("\nInitial first five rows:")
    print(df.head())
    print("-" * 50)

    print("\nStarting preprocessing...")
    initial_rows = len(df)

    df.dropna(subset=['Customer ID'], inplace=True)
    print(f"Number of rows after deleting null customer id: {len(df)}")

    df.drop_duplicates(inplace=True)
    print(f"Rows after removing duplicate rows: {len(df)}")

    df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]
    print(f"Number of rows after removing invalid values ​​(negative numbers and prices): {len(df)}")

    df['Customer ID'] = df['Customer ID'].astype(int)

    final_rows = len(df)
    print("\nPreprocessing complete!")
    print(f"Total rows removed: {initial_rows - final_rows}")
    print(f"Final number of rows: {final_rows}")
    print("-" * 50)

    print("\nTop 10 products by total quantity sold:")
    product_analysis = df.groupby('StockCode').agg(
        mean_price=('Price', 'mean'),
        total_quantity=('Quantity', 'sum')
    ).sort_values(by='total_quantity', ascending=False)
    print(product_analysis.head(10))
    print("-" * 50)

    return df



if __name__ == '__main__':
    file_path_to_test = 'online_retail_II.xlsx'
    
    print(f"--- TESTING '{__file__}' ---")
    print(f"Attempting to load and process data from: {file_path_to_test}")
    
    cleaned_dataframe = load_and_preprocess_data(file_path_to_test)
    
    if cleaned_dataframe is not None:
        print("\n--- TEST SUCCEEDED ---")
        print("The function returned a DataFrame. Here are its final info and first 5 rows:")
        cleaned_dataframe.info()
        print(cleaned_dataframe.head())
    else:
        print("\n--- TEST FAILED ---")
        print("The function did not return a DataFrame.")
