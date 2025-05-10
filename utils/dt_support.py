import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from datetime import datetime, timedelta
from utils import data_preparation, prep_support

def initialize_data():
    """Fetch and return prepared data from data preparation module"""
    result = data_preparation.data_prep()
    return {
        'processed_input': result['dataframe'],
        'time_picked': result['time_picked'],
        'route_coords': result['route_coords'],
        'type_of_vehicle': result['type_of_vehicle'],
        'restaurant_loc': result['restaurant_loc'],
        'delivery_loc': result['delivery_loc'],
        'osrm_data': {
            'duration': result['duration_osrm'],
            'distance': result['distance_osrm'],
            'speed': result['speed_osrm']
        }
    }

def generate_input_key(data):
    """Create unique key based on current inputs"""
    try:
        # Convert all components to strings before concatenation
        input_hash = str(hash(str(data['processed_input'].iloc[0].to_dict())))
        time_hash = str(hash(data['time_picked']))
        vehicle_hash = str(hash(data['type_of_vehicle']))
        
        return f"{input_hash}_{time_hash}_{vehicle_hash}"
    except Exception as e:
        st.error(f"Error generating input key: {str(e)}")
        # Return a fallback key if something fails
        return str(datetime.now().timestamp())

def handle_session_state(current_input_key):
    """Manage session state and reset when inputs change"""
    if 'last_input_key' not in st.session_state:
        st.session_state.update({
            'last_input_key': current_input_key,
            'show_map': False,
            'prediction_results': None,
            'delivery_map': None
        })
    elif st.session_state.last_input_key != current_input_key:
        st.session_state.update({
            'last_input_key': current_input_key,
            'show_map': False,
            'prediction_results': None,
            'delivery_map': None
        })

def create_delivery_map(route_coords, restaurant_loc, delivery_loc):
    """Create a Folium map with route and markers"""
    m = folium.Map(location=restaurant_loc, zoom_start=13)
    
    folium.PolyLine(
        route_coords,
        color='blue',
        weight=5,
        opacity=0.7,
        tooltip="Delivery Route"
    ).add_to(m)
    
    folium.Marker(
        restaurant_loc,
        popup="Restaurant",
        icon=folium.Icon(color='green', icon='utensils', prefix='fa')
    ).add_to(m)
    
    folium.Marker(
        delivery_loc,
        popup="Delivery Location",
        icon=folium.Icon(color='red', icon='flag', prefix='fa')
    ).add_to(m)
    
    m.fit_bounds([restaurant_loc, delivery_loc])
    return m

def initialize_map(data, current_input_key):
    """Initialize or update the delivery map"""
    if not st.session_state.delivery_map or st.session_state.last_input_key != current_input_key:
        st.session_state.delivery_map = create_delivery_map(
            data['route_coords'],
            data['restaurant_loc'],
            data['delivery_loc']
        )

def handle_prediction(data):
    """Handle prediction button click and calculations"""
    if st.button("🛵 Predict Delivery Time", help="Click to estimate delivery duration"):
        with st.spinner("🔮 Crystal ball gazing... Calculating your delivery ETA"):
            prediction = prep_support.make_prediction(data['processed_input'])
        
        deviation = 4.29  # Could be moved to config
        time_picked_dt = datetime.strptime(data['time_picked'], '%H:%M')
        predicted_minutes = float(prediction[0])
        
        st.session_state.prediction_results = {
            'predicted_minutes': predicted_minutes,
            'delivery_time': time_picked_dt + timedelta(minutes=predicted_minutes),
            'lower_bound': time_picked_dt + timedelta(minutes=predicted_minutes - deviation),
            'upper_bound': time_picked_dt + timedelta(minutes=predicted_minutes + deviation),
            'vehicle_type': data['type_of_vehicle']
        }

def display_prediction_results():
    """Display prediction results if available"""
    if st.session_state.prediction_results:
        results = st.session_state.prediction_results
        st.subheader("🚀 Delivery ETA")
        st.success(f"""
            ⏱️ Approximately **{results['predicted_minutes']:.0f} minutes** 
            (by {results['vehicle_type'].lower()})  
            ✨ Arriving by **{results['delivery_time'].strftime('%H:%M')}** 
            (between {results['lower_bound'].strftime('%H:%M')} - {results['upper_bound'].strftime('%H:%M')})
        """)

def handle_map_buttons(data):
    """Handle map visibility toggle and display"""
    col1, col2 = st.columns([2, 2])
    with col1:
        if st.session_state.show_map:
            if st.button("❌ Hide Map"):
                st.session_state.show_map = False
                st.rerun()
        else:
            if st.button("🗺️ Show Map"):
                st.session_state.show_map = True
                st.rerun()
    
    if st.session_state.show_map:
        display_map_data(data)

def display_map_data(data):
    """Display map and related OSRM data"""
    st.info(f"""
        🕒 Estimated time from OpenStreetMap APIs (by car): {data['osrm_data']['duration']:.1f} minutes  
        📏 Estimated distance from OpenStreetMap APIs (by car): {data['osrm_data']['distance']:.1f} km  
        ⚡ Estimated speed from OpenStreetMap APIs (by car): {data['osrm_data']['speed']:.1f} km/h
    """)
    st_folium(
        st.session_state.delivery_map,
        width='100%',
        height=700,
        key="delivery_map_display",
        returned_objects=[]
    )

def display_sample_data_table():
    """Display sample driver data in formatted table"""
    try:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader('👩 Sample of the Driver')
        st.markdown("<br>", unsafe_allow_html=True)
        
        data = {
            'Features': [
                "Driver's Age (Years)", "Driver's Ratings", "Restaurant Location Latitude", 
                "Restaurant Location Longitude", "Delivery Location Latitude", 
                "Delivery Location Longitude", "Vehicle Condition (0=Excellent, 3=Poor)", 
                "Number of Multiple Deliveries", "Weather Conditions", 
                "Traffic Level", "Order Type", "Vehicle Type", 
                "Is It a Festival?", "City Type", "Order Day", 
                "Order Month", "Order Time (Hour)", "Pick-Up Time (Hour)", 
                "Pick-Up Time (Minutes)", "Actual Delivery Time (Minutes)",
            ],
            'Driver 1': [
                39.0, 4.9, 18.994049, 72.825203, 19.074049, 72.905203, 0, 1, 
                'Stormy', 'Jam', 'Snack', 'motorcycle', 'No', 'Metropolitian', 
                'Monday', 'April', 21, 21, 25, 36
            ],
            'Driver 2': [
                31.0, 4.7, 17.430448, 78.418213, 17.460448, 78.448213, 1, 1, 
                'Cloudy', 'Low', 'Meal', 'scooter', 'No', 'Metropolitian', 
                'Thursday', 'March', 23, 23, 30, 18
            ]
        }
        
        # Create DataFrame with explicit dtype specification
        df = pd.DataFrame({
            'Features': pd.Series(data['Features'], dtype='string'),
            'Driver 1': pd.Series(data['Driver 1'], dtype='string'),
            'Driver 2': pd.Series(data['Driver 2'], dtype='string')
        })
        
        # Highlight the last row
        def highlight_row(row):
            return ['background-color: yellow' if row.name == len(df)-1 else '' 
                   for _ in row]
        
        styled_df = df.style.apply(highlight_row, axis=1)
        
        # Display with explicit Arrow compatibility
        st.dataframe(
            styled_df,
            height=740,
            use_container_width=True,
            hide_index=False,
            column_config={
                "Features": st.column_config.TextColumn("Features"),
                "Driver 1": st.column_config.TextColumn("Driver 1"),
                "Driver 2": st.column_config.TextColumn("Driver 2")
            }
        )
        
    except Exception as e:
        st.error(f"Error displaying sample data: {str(e)}")
        # Fallback display
        st.dataframe(pd.DataFrame(data), height=740, use_container_width=True)