import streamlit as st

def home_page():
    st.title("SmartDelivery: Optimizing Zomato's Operations with Predictive Analytics & Route Efficiency")
    st.markdown("""
    **Welcome to SmartDelivery!**
    
     ***Disclaimer**: The following story is fictional and created solely to illustrate the challenges addressed by this project.*

    #### 🎬 The Background: Navigating Complexity in Indian Food Delivery

    Zomato's delivery network in India faced escalating challenges despite booming order volumes:  
    ⚡ **Skyrocketing Expectations**: Customers demanded faster, more reliable deliveries.  
    💰 **Rising Costs**: Inefficient routing and delivery delays inflated operational expenses.  
    🛵 **Inconsistent Performance**: Poor routing led to delays, dissatisfied customers, and mounting inefficiencies.  
                
    To maintain its competitive edge, Zomato needed a data-driven transformation—a comprehensive framework to 
    predict delivery times, optimize routes, and analyze delivery performance in order to streamline operations and exceed customer expectations.
    """)

    _, col, _ = st.columns([1, 2, 1])  # Adjust ratios for spacing
    with col:
        # Display image
        st.image("assets/images/zomato-driver-illustration.png", caption="Zomato's Driver Illustration, created by ChatGPT")

    st.markdown("""
    #### 🎯 The Mission: Smarter Delivery, Happier Customers
    
    This project aims to empower Zomato with actionable insights and cutting-edge technology to tackle these challenges head-on. This mission includes:  
    📊 **Predictive Analytics**: Build a machine learning model to accurately forecast delivery times.  
    🗺️ **Route Optimization**: Leverage the OSRM (Open Source Routing Machine) API to calculate precise distances, estimated delivery durations, and the most efficient routes for riders.  
    📋 **Delivery Performance Analysis**: Identify underperforming drivers by analyzing factors such as actual delivery times, ratings, average speeds, vehicle conditions, and total completed deliveries.

    This project merges predictive analytics, route optimization, and performance evaluation to enhance Zomato’s delivery operations, delighting customers while reducing costs.
    
    *It was powered by the Zomato Delivery Operations Analytics dataset, comprising over 46,000 orders from various regions of India, spanning February to April 2022, sourced from 
    [Kaggle](https://www.kaggle.com/datasets/saurabhbadole/zomato-delivery-operations-analytics-dataset/data).* 
    """)