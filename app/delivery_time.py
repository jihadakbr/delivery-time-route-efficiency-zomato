import streamlit as st
from utils import dt_support

def delivery_time_page():
    """Main function to handle the delivery time prediction page"""
    try:
        st.title("📈 Predict Delivery Time")
        
        st.write("""
                **Welcome to the Delivery Time Prediction Tool!**

                Eager to know how long a delivery might take? This smart tool helps you estimate delivery times by simply entering a few driver details. 
                It's quick, easy, and designed to help you plan better. Just fill in the form below, and let the tool do the rest!
                 """)

        # Data preparation and initialization
        try:
            data = dt_support.initialize_data()
            current_input_key = dt_support.generate_input_key(data)
        except Exception as e:
            st.error("Failed to initialize data")
            st.stop()
        
        # Session state management
        dt_support.handle_session_state(current_input_key)
        
        # Map initialization
        try:
            dt_support.initialize_map(data, current_input_key)
        except Exception as e:
            st.warning("Could not initialize map")
        
        # Prediction handling
        dt_support.handle_prediction(data)
        
        # UI components
        dt_support.display_prediction_results()
        dt_support.handle_map_buttons(data)
        dt_support.display_sample_data_table()

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.error("Please refresh the page and try again")