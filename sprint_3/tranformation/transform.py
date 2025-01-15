import pandas as pd
import numpy as np
from typing import Dict
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from CSV file."""
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except pd.errors.EmptyDataError:
        logging.error("The CSV file is empty.")
        raise

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataframe."""
    # Drop duplicates
    df.drop_duplicates(inplace=True)
    
    # Handle missing values
    df['weight'].fillna(df['weight'].mean(), inplace=True)
    df['size'].fillna(df['size'].mode()[0], inplace=True)
    
    # Convert 'size' to numeric
    size_map = {'XS': 1, 'S': 2, 'M': 3, 'L': 4, 'XL': 5, '2XL': 6, '3XL': 7}
    df['size_numeric'] = df['size'].map(size_map)
    
    logging.info("Data cleaning completed.")
    return df

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create new features."""
    # Calculate BMI (using size as a proxy for height)
    df['bmi'] = df['weight'] / ((df['size_numeric'] * 0.1) ** 2)
    
    # Categorize BMI
    df['bmi_category'] = pd.cut(df['bmi'], 
                                bins=[0, 18.5, 25, 30, 100],
                                labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    
    # Extract domain from email
    df['email_domain'] = df['email'].str.split('@').str[1]
    
    logging.info("Feature engineering completed.")
    return df

def enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    """Enrich data with external information."""
    # Add continent based on country (simplified mapping)
    continent_map = {
        'China': 'Asia', 'Nigeria': 'Africa', 'Portugal': 'Europe', 'Sweden': 'Europe',
        'Liberia': 'Africa', 'Brazil': 'South America', 'France': 'Europe',
        'Philippines': 'Asia', 'Indonesia': 'Asia', 'Egypt': 'Africa',
        'Ethiopia': 'Africa', 'Russia': 'Europe', 'Ireland': 'Europe',
        'Colombia': 'South America', 'Saudi Arabia': 'Asia', 'Argentina': 'South America',
        'Tanzania': 'Africa', 'Ukraine': 'Europe', 'Bolivia': 'South America',
        'United States': 'North America', 'Poland': 'Europe', 'Bangladesh': 'Asia',
        'Peru': 'South America', 'Venezuela': 'South America', 'Macedonia': 'Europe',
        'Mexico': 'North America', 'Ivory Coast': 'Africa', 'Greece': 'Europe',
        'Germany': 'Europe', 'Bulgaria': 'Europe', 'South Africa': 'Africa',
        'Cameroon': 'Africa', 'Czech Republic': 'Europe', 'Angola': 'Africa',
        'Chad': 'Africa'
    }
    df['continent'] = df['country'].map(continent_map)
    
    # Add fictional GDP per capita data
    gdp_data = {
        'China': 10500, 'Nigeria': 2000, 'Portugal': 23000, 'Sweden': 51000,
        'Liberia': 700, 'Brazil': 8750, 'France': 40000, 'Philippines': 3500,
        'Indonesia': 4000, 'Egypt': 3000, 'Ethiopia': 1000, 'Russia': 11000,
        'Ireland': 94000, 'Colombia': 6000, 'Saudi Arabia': 23000, 'Argentina': 10000,
        'Tanzania': 1100, 'Ukraine': 3700, 'Bolivia': 3500, 'United States': 65000,
        'Poland': 15000, 'Bangladesh': 2000, 'Peru': 6500, 'Venezuela': 3200,
        'Macedonia': 6000, 'Mexico': 9000, 'Ivory Coast': 2300, 'Greece': 17500,
        'Germany': 46000, 'Bulgaria': 10000, 'South Africa': 6000, 'Cameroon': 1500,
        'Czech Republic': 23000, 'Angola': 2000, 'Chad': 700
    }
    df['gdp_per_capita'] = df['country'].map(gdp_data)
    
    logging.info("Data enrichment completed.")
    return df

def main():
    input_file = 'MOCK_DATA.csv'
    output_file = 'PROCESSED_DATA.csv'
    
    try:
        # Load data
        df = load_data(input_file)
        
        # Process data
        df = clean_data(df)
        df = engineer_features(df)
        df = enrich_data(df)
        
        # Save processed data
        df.to_csv(output_file, index=False)
        logging.info(f"Processed data saved to {output_file}")
        
        # Print summary statistics
        print(df.describe())
        print("\nSample of processed data:")
        print(df.head())
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()