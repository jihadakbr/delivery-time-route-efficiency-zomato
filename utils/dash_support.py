import os
import ast
import json
import folium
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from scipy import stats
from utils import prep_support


def load_route_data():
    """Load and return route data from CSV"""
    result_route = pd.read_csv("saved_csv/route_prod.csv")
    return (
        result_route['restaurant_locs'],
        result_route['delivery_locs'],
        result_route['routes']
    )

def parse_location(location_str):
    """Parse location string to coordinate list"""
    try:
        return ast.literal_eval(location_str) if isinstance(location_str, str) else location_str
    except:
        return None

def parse_route(route_str):
    """Parse route string to coordinate list"""
    try:
        return json.loads(route_str) if isinstance(route_str, str) else route_str
    except:
        try:
            return ast.literal_eval(route_str)
        except:
            return None

def create_map_markers(map_obj, restaurant_locs, delivery_locs, routes):
    """Add markers and routes to Folium map"""
    for i, (route_str, r_loc, d_loc) in enumerate(zip(routes, restaurant_locs, delivery_locs)):
        route = parse_route(route_str)
        if not route:
            continue
            
        # Add route path
        folium.PolyLine(
            route, 
            color='blue', 
            weight=3, 
            opacity=0.7,
            tooltip=f"Route {i+1}"
        ).add_to(map_obj)
        
        # Add restaurant marker
        if r_parsed := parse_location(r_loc):
            folium.Marker(
                location=r_parsed,
                popup=f"Restaurant {i+1}",
                icon=folium.Icon(color='green', icon='cutlery')
            ).add_to(map_obj)
            
        # Add delivery marker
        if d_parsed := parse_location(d_loc):
            folium.Marker(
                location=d_parsed,
                popup=f"Delivery {i+1}",
                icon=folium.Icon(color='red', icon='flag')
            ).add_to(map_obj)

def generate_route_map(restaurant_locs, delivery_locs, routes):
    """Generate Folium map with optimized routes"""
    map_obj = folium.Map(location=[21.5937, 78.9629], zoom_start=5)
    map_obj.get_root().width = "100%"
    map_obj.get_root().height = "600px"
    create_map_markers(map_obj, restaurant_locs, delivery_locs, routes)
    return map_obj

def render_map(map_obj):
    """Render Folium map in Streamlit with proper dimensions"""
    map_html = map_obj.get_root().render()
    map_html = map_html.replace(
        '<div class="folium-map" id="map_', 
        '<div class="folium-map" style="width:100%; height:600px" id="map_'
    )
    st.components.v1.html(map_html, height=600)

# Load feature column names with caching
@st.cache_data
def load_features_name():
    feature_columns_path = 'saved_csv/feature_columns.csv'
    if not os.path.exists(feature_columns_path):
        st.error("Feature columns file not found!")
        return None
    return pd.read_csv(feature_columns_path, header=None)[0].tolist()

def show_feature_importance():
    """
    Displays an interactive horizontal bar chart of top 10 feature importances using Streamlit and Plotly.
    
    Parameters:
    - model: Trained model object with feature_importances_ attribute
    - feature_columns: List of feature names
    """

    st.subheader('🔑 XGBoost - Top 10 Important Features')

    feature_columns = load_features_name()

    model_filename = 'XGBoost_20250508_151557.pkl'

    try:
        model = prep_support.load_model(model_filename)
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        st.stop()

    # Input validation
    if feature_columns is None:
        st.error("Error: Feature names not provided.")
        return
    if len(feature_columns) == 0:
        st.error("Error: Empty feature list provided.")
        return
    if not hasattr(model, 'feature_importances_'):
        st.warning("Warning: This model type doesn't support feature importances!")
        return
    if len(feature_columns) != len(model.feature_importances_):
        st.error(f"Mismatch error: Got {len(feature_columns)} features but expected {len(model.feature_importances_)}")
        return

    # Create feature importance DataFrame
    feat_imp = pd.DataFrame({
        'Feature': feature_columns,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False).head(10)

    # Create interactive visualization
    fig = px.bar(
        feat_imp,
        x='Importance',
        y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale='Viridis',
        text='Importance',
        height=500
    )

    # Visual formatting
    fig.update_layout(
        xaxis_title='',
        yaxis_title='',
        hovermode='y',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis={
            'categoryorder': 'total ascending',
            'tickfont': dict(size=14)
        },
        xaxis=dict(
            showticklabels=False,
            ticks='',
            showgrid=False
        ),
        margin=dict(t=20, b=0)
    )

    fig.update_traces(
        texttemplate='%{text:.3f}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=0.5,
        textfont=dict(
            size=14,
            color='black'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

def visualize_traffic_levels(charts_df):
    """Display traffic levels by hour visualization as a modular component."""

    st.subheader('🚦 Traffic Levels by Hour')

    # Convert to categorical with specified order
    traffic_order = ['Low', 'Medium', 'High', 'Jam']
    charts_df['Road_traffic_density'] = pd.Categorical(
        charts_df['Road_traffic_density'],
        categories=traffic_order,
        ordered=True
    )

    # Convert to datetime and extract hour
    charts_df['Hour_picked'] = pd.to_datetime(
        charts_df['Time_Order_picked'],
        format='%H:%M',
        errors='coerce'
    ).dt.hour

    # Drop rows with invalid times (if any)
    charts_df = charts_df.dropna(subset=['Hour_picked'])

    # Group by hour and traffic level
    traffic_by_hour = charts_df.groupby(
        ['Hour_picked', 'Road_traffic_density'], observed=False
    ).size().reset_index(name='Count')

    # Sort by hour to ensure correct order
    traffic_by_hour = traffic_by_hour.sort_values('Hour_picked')

    # Create formatted hour labels
    traffic_by_hour['Hour'] = traffic_by_hour['Hour_picked'].apply(lambda x: f"{int(x)}:00")

    # Create visualization
    fig = px.bar(
        traffic_by_hour,
        x='Hour',
        y='Count',
        color='Road_traffic_density',
        category_orders={'Road_traffic_density': traffic_order},
        color_discrete_map={
            'Low': '#1f77b4',    # Blue
            'Medium': '#2ca02c', # Green
            'High': '#ff7f0e',   # Orange
            'Jam': '#d62728'     # Red
        },
        title='',
        labels={
            'Road_traffic_density': 'Traffic Level',
            'Count': 'Number of Orders',
            'Hour': 'Hour of Day'
        }
    )

    # Update layout for better styling with larger fonts
    fig.update_layout(
        barmode='stack',
        xaxis_title='',
        yaxis_title='Number of Orders',
        legend_title='Traffic Level',
        xaxis=dict(
            tickmode='array',
            tickvals=traffic_by_hour['Hour'],
            title='',
            tickangle=0,
            tickfont=dict(size=14)  # Increase x-axis tick font size
        ),
        yaxis=dict(
            gridcolor='lightgray',
            gridwidth=0.5,
            title_font=dict(size=16),  # Increase y-axis title font size
            tickfont=dict(size=14)     # Increase y-axis tick font size
        ),
        legend=dict(
            font=dict(size=14),       # Increase legend text font size
            title_font=dict(size=16)   # Increase legend title font size
        ),
        plot_bgcolor='white',
        hovermode='x unified',
        height=600,
        margin=dict(t=20, b=0)
    )

    # Add custom hover template
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Order: %{y}')

    # Display the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

def create_performance_df(charts_df):
    """Create aggregated performance dataframe"""
    return charts_df.groupby('Delivery_person_ID').agg({
        'Delivery_person_Ratings': 'mean',
        'Time_taken (min)': 'mean',
        'Vehicle_condition': 'mean',
        'speed_actual': 'mean',
        'speed_osrm': 'mean',
        'duration_osrm': 'mean',
        'distance_osrm_km': 'mean',
        'multiple_deliveries': 'mean',
        'ID': 'count'
    }).rename(columns={
        'ID': 'Total_Deliveries',
        'duration_osrm': 'Avg_OSRM_Duration',
        'distance_osrm_km': 'Avg_OSRM_Distance'
    }).reset_index()

def calculate_efficiency_metrics(performance_df):
    """Calculate efficiency metrics and flags"""
    df = performance_df.copy()
    
    # Calculate metrics
    df['speed_ratio'] = df['speed_actual'] / df['speed_osrm']
    df['time_zscore'] = np.abs(stats.zscore(df['Time_taken (min)']))
    df['speed_flag'] = np.where(df['speed_ratio'] < 0.5, 1, 0)
    
    # Create flags
    df['Underperformer'] = np.where(
        (df['time_zscore'] > 2) |
        (df['speed_flag'] == 1) |
        (df['Delivery_person_Ratings'] < 3.5) |
        (df['Vehicle_condition'] > 2),
        'Yes', 'No'
    )
    
    # Advanced flags
    df['Advanced_Flag'] = np.where(
        (df['speed_ratio'] > 0.5) & (df['Underperformer'] == 'Yes'),
        'High Speed, Long Time Taken',
        df['Underperformer']
    )
    df['Advanced_Flag'] = df['Advanced_Flag'].replace({
        'Yes': 'Needs Improvement',
        'No': 'Meets Expectations'
    })
    
    return df

def generate_underperformers_table(performance_df):
    """Generate table of underperforming drivers"""
    underperformers = performance_df[performance_df['Underperformer'] == 'Yes']
    return (underperformers[[
        'Delivery_person_ID',
        'Delivery_person_Ratings',
        'Time_taken (min)',
        'speed_ratio',
        'Vehicle_condition'
    ]].round(2).head(10),
        len(underperformers)
    )

def generate_key_metrics(performance_df):
    """Generate key performance metrics"""
    return {
        'avg_speed_ratio': performance_df['speed_ratio'].mean(),
        'speed_flag_pct': performance_df['speed_flag'].mean() * 100,
        'avg_time_taken': performance_df['Time_taken (min)'].mean(),
        'avg_osrm_duration': performance_df['Avg_OSRM_Duration'].mean(),
        'avg_vehicle_condition': performance_df['Vehicle_condition'].mean(),
        'avg_rating': performance_df['Delivery_person_Ratings'].mean()
    }

def display_recommendations():
    # Title 
    st.subheader("💡 Recommended Actions")
    
    data = [
    {"Strategy": "🚦 Optimize Delivery Routes", 
     "Key Actions": "Use OSRM API for route planning to avoid traffic and multi-delay bottlenecks"},
    
    {"Strategy": "⏰ Optimize Delivery Schedule", 
     "Key Actions": "Shift deliveries to low-traffic hours (night/morning), staff up for peak (17:00-23:00)"},
    
    {"Strategy": "🚀 Improve Driver Performance", 
     "Key Actions": "Targeted training for underperforming drivers based on metrics"}
     ]

    # Display the table
    st.dataframe(
        data,
        column_config={
            'Strategy': st.column_config.TextColumn("♟️ Strategy", width="auto"),
            'Key Actions': st.column_config.TextColumn("✅ Key Actions", width="auto")
        },
        hide_index=True,
        use_container_width=True
    )
    
    
