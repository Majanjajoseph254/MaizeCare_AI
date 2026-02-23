from geopy.distance import geodesic
import pandas as pd

def find_nearest_miller(user_lat, user_lon, csv_path='data/millers.csv'):
    """Finds the closest miller from the CSV based on user GPS."""
    df = pd.read_csv(csv_path)
    
    # Calculate distance for each miller
    def calculate_dist(row):
        miller_coords = (row['lat'], row['lon'])
        user_coords = (user_lat, user_lon)
        return geodesic(user_coords, miller_coords).km

    df['distance_km'] = df.apply(calculate_dist, axis=1)
    
    # Sort by nearest and return the top one
    nearest = df.sort_values(by='distance_km').iloc[0]
    return nearest.to_dict()