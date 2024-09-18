import pandas as pd
import pyproj
import os
from pyproj import Transformer

# Constants
CSV_FILE_PATH = os.path.join('data', '2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv')
OUTPUT_FILE_PATH = os.path.join('data', 'preprocessed_coverage_data.csv')

# Create a transformer object
transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)

def lamber93_to_gps(x, y):
	return transformer.transform(x, y)

def preprocess():
    # Load CSV data
    df = pd.read_csv(
        CSV_FILE_PATH,
        sep=';',
        header=0,  # Assume first row is header
        names=['ProviderCode', 'X', 'Y', '2G', '3G', '4G'],
        usecols=[0, 1, 2, 3, 4, 5],
        dtype={'ProviderCode': int, 'X': float, 'Y': float, '2G': int, '3G': int, '4G': int}
    )

    # Map provider codes to names
    provider_map = {
        20801: 'Orange',
        20810: 'SFR',
        20815: 'Free',
        20820: 'Bouygues Telecom'
    }

    # Add ProviderName column to DataFrame
    df['ProviderName'] = df['ProviderCode'].map(provider_map)

    # Convert coordinates
    df['Longitude'], df['Latitude'] = lamber93_to_gps(df['X'].values, df['Y'].values)

    # Save preprocessed data
    df.to_csv(OUTPUT_FILE_PATH, index=False)

    print("Preprocessing complete. Data saved to:", OUTPUT_FILE_PATH)

if __name__ == '__main__':
    preprocess()