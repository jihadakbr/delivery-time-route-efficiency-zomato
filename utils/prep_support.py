import os
import joblib
import requests
import numpy as np
import pandas as pd
import streamlit as st

@st.cache_resource
def load_model(model_filename: str):
    """
    Load a model from the specified filename.

    Args:
        model_filename (str): The filename of the saved model.

    Returns:
        The loaded model object.
    
    Raises:
        ValueError: If the model file exists but cannot be loaded.
        FileNotFoundError: If the model file does not exist.
    """
    model_path = f'saved_models/{model_filename}'
    
    if os.path.exists(model_path):
        try:
            # Assuming the model was saved directly, not as a dictionary
            return joblib.load(model_path)
        except Exception as e:
            raise ValueError(f"Error loading model from {model_path}: {e}")
    else:
        raise FileNotFoundError(f"No model found at {model_path}")

def one_hot_encode(df, column_base, categories, selected_value):
    """
    One-hot encode a categorical variable and add the resulting columns to the DataFrame.
    
    Parameters:
    - df: DataFrame to which columns will be added.
    - column_base: Base name for the new columns (e.g., 'Weather_conditions').
    - categories: List of possible categories for the variable.
    - selected_value: The selected value of the variable (input from the user).
    
    Returns:
    - DataFrame with the new one-hot encoded columns.
    """
    for category in categories:
        col_name = f"{column_base}_{category}"
        df[col_name] = [1 if selected_value == category else 0]
    return df

def cyclical_encode(df, column_name, period):
    """
    Apply cyclical encoding to a numerical column using sine and cosine transformations.
    
    Parameters:
    - df: DataFrame containing the column to encode.
    - column_name: Name of the column to encode.
    - period: Period of the cyclic feature (e.g., 7 for days of the week, 12 for months).
    
    Returns:
    - DataFrame with the new sine and cosine columns added.
    """
    df[f'{column_name}_sin'] = np.sin(2 * np.pi * df[column_name] / period)
    df[f'{column_name}_cos'] = np.cos(2 * np.pi * df[column_name] / period)
    return df

def transform_datetime_features(df, order_day_of_week, order_month, time_ordered_hour, time_picked_hour):
    """
    Transforms datetime features into numerical representations.
    
    Args:
        df (pd.DataFrame): The dataframe to transform
        order_day_of_week (str): Day of the week (e.g., "Monday")
        order_month (str): Month name (e.g., "January")
        time_ordered_hour (int): Hour when order was placed (0-23)
        time_picked_hour (int): Hour when order was picked (0-23)
        
    Returns:
        pd.DataFrame: Transformed dataframe with numerical datetime features
    """
    # Mapping days of the week to numerical values
    day_of_week_map = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2, 
        "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
    }

    # Mapping months to numerical values
    month_map = {
        "January": 1, "February": 2, "March": 3, "April": 4, 
        "May": 5, "June": 6, "July": 7, "August": 8, 
        "September": 9, "October": 10, "November": 11, "December": 12
    }
    
    # Convert to numerical values
    order_day_numeric = day_of_week_map[order_day_of_week]
    order_month_numeric = month_map[order_month]

    # Add numerical features to dataframe
    df['Order_DayOfWeek'] = [float(order_day_numeric)]
    df['Order_Month'] = [float(order_month_numeric)]
    df['Time_Orderd_Hour'] = [float(time_ordered_hour)]
    df['Time_Order_picked_Hour'] = [float(time_picked_hour)]
    
    return df

def drop_unnecessary_columns(df):
    """
    Drops columns that could cause multicollinearity or are original numerical columns
    used for encoding.
    
    Args:
        df (pd.DataFrame): The dataframe to process
        
    Returns:
        pd.DataFrame: Dataframe with specified columns removed
    """
    drop_columns = [
        'Weather_conditions_Cloudy', 
        'Road_traffic_density_High', 
        'Type_of_order_Buffet',
        'Type_of_vehicle_bicycle', 
        'Festival_No', 
        'City_Metropolitian',
        'Order_DayOfWeek', 
        'Order_Month', 
        'Time_Orderd_Hour', 
        'Time_Order_picked_Hour'
    ]
    
    # Only drop columns that actually exist in the dataframe
    columns_to_drop = [col for col in drop_columns if col in df.columns]
    
    return df.drop(columns=columns_to_drop)

def validate_and_reorder_columns(df, feature_columns_path='saved_csv/feature_columns.csv'):
    """
    Validates and reorders DataFrame columns based on a saved feature columns list.
    
    Args:
        df (pd.DataFrame): The DataFrame to validate and reorder
        feature_columns_path (str): Path to the CSV file containing the reference column order
        
    Returns:
        pd.DataFrame: DataFrame with validated and reordered columns
    """
    # Load the feature columns order
    feature_columns = pd.read_csv(feature_columns_path, header=None)[0].tolist()

    # Check for missing or extra columns
    missing_cols = set(feature_columns) - set(df.columns)
    if missing_cols:
        print(f"Warning: Missing columns: {missing_cols}")
    
    extra_cols = set(df.columns) - set(feature_columns)
    if extra_cols:
        print(f"Warning: Extra columns: {extra_cols}")

    # Reorder columns to match the reference order (keeping only common columns)
    common_cols = [col for col in feature_columns if col in df.columns]
    return df[common_cols]

def get_osrm_route_data(start_lon, start_lat, end_lon, end_lat):
    """
    Get complete route data from OSRM in one API call
    Returns: {
        'duration': seconds (minimum 1 second to prevent division by zero),
        'distance': meters,
        'coordinates': [[lon,lat], ...] or None if error
    }
    """
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=full&geometries=geojson"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data.get('code') == 'Ok':
            route = data['routes'][0]
            # Ensure duration is never zero by using max(1, duration)
            return {
                'duration': max(1, route['duration']),  # Minimum 1 second
                'distance': route['distance'],
                'coordinates': route['geometry']['coordinates']
            }
        return None
    except Exception as e:
        st.error(f"OSRM API Error: {str(e)}")
        return None

def make_prediction(processed_input):
    # Model Path
    model_filename = 'XGBoost_20250508_151557.pkl'

    # Loading the model using joblib
    model = load_model(model_filename)

    # Reshape input for prediction
    input_array = np.array(processed_input).reshape(1, -1)

    # Make prediction
    prediction = model.predict(input_array)
    
    return prediction