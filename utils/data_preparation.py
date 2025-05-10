import pandas as pd
import streamlit as st
from utils import prep_support

def data_prep():
    tab1, tab2 = st.columns(2) 

    with tab1:
        delivery_person_age = st.number_input("Driver's Age (Years)", min_value=15, max_value=50, value=39)
        delivery_person_ratings = st.number_input("Driver's Rating", min_value=1.0, max_value=6.0, value=4.9, step=0.1, format="%0.1f")
        restaurant_location_latitude = st.number_input("Restaurant Location Latitude", min_value=8.400000, max_value=37.600000, value=18.994049, step=0.000001, format="%0.6f")
        restaurant_location_longitude = st.number_input("Restaurant Location Longitude", min_value=68.700000, max_value=97.400000, value=72.825203, step=0.000001, format="%0.6f")
        delivery_location_latitude = st.number_input("Delivery Location Latitude", min_value=8.400000, max_value=37.600000, value=19.074049, step=0.000001, format="%0.6f")
        delivery_location_longitude = st.number_input("Delivery Location Longitude", min_value=68.700000, max_value=97.400000, value=72.905203, step=0.000001, format="%0.6f")
        vehicle_condition = st.number_input("Vehicle Condition (0=Excellent, 3=Poor)", min_value=0, max_value=3, value=0)
        multiple_deliveries = st.number_input("Number of Multiple Deliveries", min_value=0, max_value=3, value=1)
        weather_conditions = st.selectbox("Weather Conditions", options=["Cloudy", "Fog", "Sandstorms", "Stormy", "Sunny", "Windy"], index=3) # Stormy
        road_traffic_density = st.selectbox("Traffic Level", options=["Low", "Medium", "High", "Jam"], index=3) # Jam

    with tab2:
        type_of_order = st.selectbox("Order Type", options=["Buffet", "Drinks", "Meal", "Snack"], index=3) # Snack
        type_of_vehicle = st.selectbox("Vehicle Type", options=["Bicycle", "Electric Scooter", "Motorcycle", "Scooter"], index=2) # Motorcycle
        festival = st.selectbox("Is It a Festival?", options=["Yes", "No", "Unknown"], index=1) # No
        city = st.selectbox("City Type", options=["Metropolitan", "Semi-Urban", "Urban"], index=0) # Metropolitan
        order_day_of_week = st.selectbox("Order Day", options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], index=0) # Monday
        order_month = st.selectbox("Order Month", options=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], index=3) # April
        time_ordered_hour = st.number_input("Order Time (Hour)", min_value=0, max_value=23, value=21, step=1)
        time_picked_hour = st.number_input("Pick-Up Time (Hour)", min_value=0, max_value=23, value=21, step=1)
        time_picked_mins = st.number_input("Pick-Up Time (Minutes)", min_value=0, max_value=59, value=25, step=1)
        
    # Combine time_picked_hour and time_picked_mins into a single time variable
    time_picked = f"{int(time_picked_hour):02d}:{int(time_picked_mins):02d}"

    route_data = prep_support.get_osrm_route_data(
        restaurant_location_longitude, restaurant_location_latitude,
        delivery_location_longitude, delivery_location_latitude
    )
    
    if route_data:
        # Convert coordinates to [lat,lon] for Folium
        route_coords = [[lat, lon] for [lon, lat] in route_data['coordinates']]
        
        # Create and display map
        restaurant_loc = [restaurant_location_latitude, restaurant_location_longitude]
        delivery_loc = [delivery_location_latitude, delivery_location_longitude]
                
        duration_osrm = route_data['duration']/60 # in minutes
        speed_osrm = (route_data['distance']/1000)/(route_data['duration']/3600) # in km/h
        distance_osrm = route_data['distance']/1000 # in km

    else:
        st.error("Failed to get route data. Please check your locations.")

    # Create a DataFrame for numerical features
    df = pd.DataFrame({
        'Delivery_person_Age': [float(delivery_person_age)],
        'Delivery_person_Ratings': [delivery_person_ratings],
        'Delivery_location_latitude': [delivery_location_latitude],
        'Delivery_location_longitude': [delivery_location_longitude],
        'Vehicle_condition': [vehicle_condition],
        'multiple_deliveries': [float(multiple_deliveries)],
        'duration_osrm': [duration_osrm],
        'speed_osrm': [speed_osrm]
    })

    # Apply one-hot encoding to categorical variables
    df = prep_support.one_hot_encode(df, 'Weather_conditions', ["Cloudy", "Fog", "Sandstorms", "Stormy", "Sunny", "Windy"], weather_conditions)
    df = prep_support.one_hot_encode(df, 'Road_traffic_density', ["High", "Jam", "Low", "Medium"], road_traffic_density)
    df = prep_support.one_hot_encode(df, 'Type_of_order', ["Buffet", "Drinks", "Meal", "Snack"], type_of_order)
    df = prep_support.one_hot_encode(df, 'Type_of_vehicle', ["bicycle", "electric_scooter", "motorcycle", "scooter"], type_of_vehicle)
    df = prep_support.one_hot_encode(df, 'Festival', ["No", "Unknown", "Yes"], festival)
    df = prep_support.one_hot_encode(df, 'City', ["Metropolitian", "Semi-Urban", "Urban"], city)

    # Transform categorical variables to numerical for Cylical Encoding
    df = prep_support.transform_datetime_features(df, order_day_of_week, order_month, time_ordered_hour, time_picked_hour)

    # Apply cyclical encoding to datetime features
    df = prep_support.cyclical_encode(df, 'Order_DayOfWeek', 7)
    df = prep_support.cyclical_encode(df, 'Order_Month', 12)
    df = prep_support.cyclical_encode(df, 'Time_Orderd_Hour', 24)
    df = prep_support.cyclical_encode(df, 'Time_Order_picked_Hour', 24)

    # Drop unnecessary columns to avoid multicollinearity and original numerical columns used for encoding
    df = prep_support.drop_unnecessary_columns(df)

    # Validates and reorders DataFrame columns based on a saved feature columns list
    df = prep_support.validate_and_reorder_columns(df)

    return {
        'dataframe': df,
        'time_picked': time_picked,
        'route_coords': route_coords,
        'type_of_vehicle': type_of_vehicle,
        'restaurant_loc': restaurant_loc, 
        'delivery_loc': delivery_loc,
        'duration_osrm': duration_osrm,
        'speed_osrm': speed_osrm,
        'distance_osrm': distance_osrm
    }