import pandas as pd
import streamlit as st
from utils import dash_support

def dashboard_page():
    st.title("📊 SmartDelivery Dashboard")
    st.markdown("<br>", unsafe_allow_html=True)


    ########## ML Model Metric section
    st.subheader('🔧 Machine Learning Model')
    
    # Create the metric
    data = {
        'Model': ['XGBoost'],
        'Deviation (RMSE)': ['±4.29 minutes'],
        'Interpretation': ['On average, predictions are off by 4.29 minutes.']
    }

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Display in Streamlit
    st.dataframe(df, hide_index=True)


    ########## Delivery routes section
    st.subheader('🧭 Delivery Routes Visualization')
    
    # Initialize cached map
    if 'cached_map' not in st.session_state:
        st.session_state.cached_map = None
    
    # Generate map if not cached
    if not st.session_state.cached_map:
        with st.spinner('Generating optimized route visualization...'):
            restaurant_locs, delivery_locs, routes = dash_support.load_route_data()
            st.session_state.cached_map = dash_support.generate_route_map(
                restaurant_locs,
                delivery_locs,
                routes
            )
    
    # Display cached map
    if st.session_state.cached_map:
        dash_support.render_map(st.session_state.cached_map)


    ########### Feature Importance section
    dash_support.show_feature_importance()


    ########### Traffic Levels section
    charts_df = pd.read_csv('saved_csv/charts.csv')
    dash_support.visualize_traffic_levels(charts_df)


    ########### Underperforming Drivers section
    # Create and transform data
    performance_df = dash_support.create_performance_df(charts_df)
    performance_df = dash_support.calculate_efficiency_metrics(performance_df)
    underperformers_table, underperformers_length = dash_support.generate_underperformers_table(performance_df)
    key_metrics = dash_support.generate_key_metrics(performance_df)
    
    # Display metrics
    st.subheader(f'🙁 Underperforming Drivers ({underperformers_length}/{len(performance_df)})')
    
    # Show underperformers table
    st.dataframe(
        underperformers_table,
        column_config={
            "speed_ratio": st.column_config.NumberColumn(
                "Speed Ratio",
                help="Actual speed vs OSRM predicted speed",
                format="%.2f"
            )
        }
    )
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Speed Ratio", f"{key_metrics['avg_speed_ratio']:.2f}")
        st.metric("Avg Vehicle Condition", f"{key_metrics['avg_vehicle_condition']:.1f}/3.0")
    with col2:
        st.metric("Slow Drivers (Speed Ratio < 0.5)", f"{key_metrics['speed_flag_pct']:.1f}%")
        st.metric("Avg Rating", f"{key_metrics['avg_rating']:.1f}/6.0")
    with col3:
        st.metric("Avg Time Taken", f"{key_metrics['avg_time_taken']:.0f} min")
        st.metric("Avg Expected Duration", f"{key_metrics['avg_osrm_duration']:.0f} min")


    ########### Recommended Actions section
    st.markdown("<br>", unsafe_allow_html=True)
    dash_support.display_recommendations()