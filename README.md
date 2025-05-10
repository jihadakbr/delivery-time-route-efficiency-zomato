# SmartDelivery: Optimizing Zomato's Operations with Predictive Analytics & Route Efficiency

---

## Table of Contents
1. [Dataset Overview](#dataset-overview)  
2. [Project Background](#project-background)  
3. [Business Objective](#business-objective)  
4. [Data Understanding](#data-understanding)  
5. [Project Overview](#project-overview)  
6. [Data Preprocessing](#data-preprocessing)  
7. [Findings and Results](#findings-and-results)  
8. [Recommendations](#recommendations)  
9. [Dashboard](#dashboard)  
10. [License](#license)  
11. [Contact](#contact)  

---

## Dataset Overview

| No. | Column Name                      | Description                                                      |
|-----|----------------------------------|------------------------------------------------------------------|
| 1   | ID                               | Unique identifier for each delivery.                            |
| 2   | Delivery_person_ID               | Unique identifier for each delivery person.                     |
| 3   | Delivery_person_Age              | Age of the delivery person.                                     |
| 4   | Delivery_person_Ratings          | Ratings assigned to the delivery person.                        |
| 5   | Restaurant_latitude              | Latitude of the restaurant.                                     |
| 6   | Restaurant_longitude             | Longitude of the restaurant.                                    |
| 7   | Delivery_location_latitude       | Latitude of the delivery location.                              |
| 8   | Delivery_location_longitude      | Longitude of the delivery location.                             |
| 9   | Order_Date                       | Date of the order.                                              |
| 10  | Time_Ordered                     | Time the order was placed.                                      |
| 11  | Time_Order_picked                | Time the order was picked up for delivery.                      |
| 12  | Weather_conditions               | Weather conditions at the time of delivery.                     |
| 13  | Road_traffic_density             | Density of road traffic during delivery.                        |
| 14  | Vehicle_condition                | Condition of the delivery vehicle.                              |
| 15  | Type_of_order                    | Type of order (e.g., dine-in, takeaway, delivery).              |
| 16  | Type_of_vehicle                  | Type of vehicle used for delivery.                              |
| 17  | Multiple_deliveries              | Indicator of whether multiple deliveries were made in the same trip. |
| 18  | Festival                         | Indicator of whether the delivery coincided with a festival.    |
| 19  | City                             | City where the delivery took place.                             |
| 20  | Time_taken (min)                 | Time taken for delivery in minutes.                             |

---

## Project Background

- **Skyrocketing Expectations**: Customers demanded faster, more reliable deliveries.  
- **Rising Costs**: Inefficient routing and delivery delays inflated operational expenses.  
- **Inconsistent Performance**: Poor routing led to delays, dissatisfied customers, and mounting inefficiencies.  

---

## Business Objective

1. **Predictive Analytics**: Build a machine learning model to accurately forecast delivery times.  
2. **Route Optimization**: Utilize the OSRM (Open Source Routing Machine) API for precise distance and duration estimates, improving delivery efficiency.  
3. **Delivery Performance Analysis**: Identify underperforming drivers by analyzing factors such as actual delivery times, ratings, vehicle conditions, and more.  

---

## Data Understanding

- **Source**: [Kaggle – Zomato Delivery Operations Analytics Dataset](https://www.kaggle.com/datasets/saurabhbadole/zomato-delivery-operations-analytics-dataset/data).  
- **Details**: 46,000 orders from February to April 2022 across India.  
- **Components**: Includes order details, driver profiles, delivery, and restaurant location data. 

---

## Project Overview
![Project Overview Diagram](https://raw.githubusercontent.com/jihadakbr/time-delivery-route-efficiency-zomato/refs/heads/main/assets/images/workflow-diagram-delivery-time.png)

The project was deployed using Streamlit and structured as follows:
```
time-delivery-route-efficiency-zomato/
├── smartdelivery_app.py    # Main entry point
├── custom_pages/
│   ├── home.py             # Landing page
│   ├── dashboard.py        # Main dashboard
│   ├── contact.py          # Contact information
│   └── overview.py         # Project overview (diagram)
├── utils/
│   ├── dash_support.py     # Dashboard functions
│   ├── data_preparation.py # Data preprocessing
│   ├── dt_support.py       # Delivery time functions
│   └── prep_support.py     # Preprocessing support functions
├── app/
│   └── delivery_time.py    # Time delivery prediction app
├── saved_models/           # Trained model binaries
├── saved_csv/              # Preprocessed CSV files
└── assets/                 # Static files (images, styles, JS)
```

Streamlit link: [time-delivery-route-efficiency-zomato.streamlit.app](https://time-delivery-route-efficiency-zomato.streamlit.app/)
<br>
<br>
<br>
The project files on GitHub are:
- `Predictive Analytics & Route Efficiency - Presentation.pdf` — PowerPoint presentation in PDF format
- `Predictive Analytics & Route Efficiency.ipynb` — Applying end-to-end machine learning steps for Zomato dataset

---

## Data Preprocessing

### Step 1: Fetch OSRM API (Local)
- Retrieved distance, duration, and route coordinates for precise routing information.

### Step 2: Fetch OpenStreetMap API
- Filled missing values in the "City" column using OpenStreetMap data.

### Step 3: Fetch Weather API
- Addressed missing values in the "Weather_conditions" column using weather API data.

### Step 4: Remove Anomalous Locations
- Identified and removed anomalous delivery or restaurant locations (e.g., coordinates in the ocean).

### Step 5: Convert Data Types
- Reformatted the "Order_Date" column to the date data type for consistency.

### Step 6: Address Outliers
- Removed entries with improbable speeds, such as above 150 km/h or below 3 km/h, to ensure data reliability.

---

## Findings and Results

### Best Model: XGBoost
- Achieved a Root Mean Squared Error (RMSE) of **4.29 minutes**, accurately predicting delivery times. 
- Considering the standard deviation of actual delivery times (~9 minutes), this is a highly reliable result.

---
![Machine Learning Models Comparison](https://raw.githubusercontent.com/jihadakbr/time-delivery-route-efficiency-zomato/refs/heads/main/assets/images/machine-learning-models-comparison.png)
### Insights:
- The best machine learning model: XGBoost. with RMSE 4.29 minutes. The actual time taken by drivers from the restaurant to the
delivery location was successfully predicted using an XGBoost machine learning model, achieving an average prediction error (RMSE) of approximately 4.29 minutes. This is a strong result, considering the standard deviation of the actual delivery times is around 9 minutes.
- Additionally, I generated a projected best route using the OSRM API and visualized it on a Folium map. This allows us to better understand the driver’s actual route and provides more accurate estimates of both distance and travel time.

---
![Actual vs Predicted Delivery Times](https://raw.githubusercontent.com/jihadakbr/time-delivery-route-efficiency-zomato/refs/heads/main/assets/images/actual-vs-predicted-delivery-times.png)
### Insights:
- The graph comparing actual and predicted delivery times shows a strong linear relationship, closely following the line y = x.
- The red line represents this ideal relationship, indicating that, on average, the model’s predicted delivery times accurately reflect the actual delivery times.

---
![XGBoost Top 10 Important Features](https://raw.githubusercontent.com/jihadakbr/time-delivery-route-efficiency-zomato/refs/heads/main/assets/images/xgboost-top-10-important-features.png)
### Insights:
- The top three most impactful factors influencing the actual time taken from the driver to the customer are Road_traffic_density_low, Road_traffic_density_jam, and Multiple_deliveries.
- This suggests that low road traffic density helps reduce delivery time, while traffic jams significantly increase it. Additionally, assigning multiple deliveries to a single driver also contributes to longer delivery times, as demonstrated by the partial dependence plot in the Jupyter Notebook.

---
![Distribution of Traffic Levels by Hour](https://raw.githubusercontent.com/jihadakbr/time-delivery-route-efficiency-zomato/refs/heads/main/assets/images/distribution-of-traffic-levels-by-hour.png)
### Insights:
Insight
- Traffic density trends:
   - Low: Late night to morning (22:16–11:15).
   - High: Midday (11:16–15:15).
   - Medium: Evening rush (15:16–19:15).
   - Jam: Night (19:16–22:15).
- Most orders occur between 17:00–23:00, aligning with peak traffic hours.

---
![Speed Ratio vs Ratings](https://raw.githubusercontent.com/jihadakbr/time-delivery-route-efficiency-zomato/refs/heads/main/assets/images/speed-ratio-vs-ratings.png)
### Insights:
- OSRM parameters for the car profile were used as the baseline to assess driver performance.
- Since drivers may use a variety of vehicles (Motorcycle, Bicycle, Electric Scooter, and Scooter), and one driver can switch between vehicle types, I used a speed ratio threshold of below 0.5 to identify underperforming drivers.
- Additionally, drivers were also considered underperforming if their actual travel time deviated by more than 2 standard deviations (approximately ±4 minutes) from the mean. For example, if the average actual time is 26 minutes, drivers with times above 30 minutes or below 22 minutes were flagged.

---
![Actual Time vs Expected Duration](https://raw.githubusercontent.com/jihadakbr/time-delivery-route-efficiency-zomato/refs/heads/main/assets/images/actual-time-vs-expected-duration.png)
### Insights:
- Similar to the previous slide, this shows the expected travel duration from the OSRM API using the car profile as the baseline. I flagged drivers as slower than expected if their actual travel time was less than 50% of the OSRM expected duration.
- Based on this threshold, most drivers (in the green-shaded area) were faster than expected, while a few (in the redshaded area) were slower than expected.

---
![Underperforming Drivers Report](https://raw.githubusercontent.com/jihadakbr/time-delivery-route-efficiency-zomato/refs/heads/main/assets/images/underperforming-drivers-report.png)
### Insights:
- This report summarizes the underperforming drivers. I identified underperforming drivers based on the following criteria:
   - Rating below 0.35
   - Speed ratio below 0.5
   - Actual travel time deviating by more than 2 standard deviations from the mean
   - Poor vehicle condition (a score greater than 2 on a 0–3 scale, where 0 indicates good condition)

---

## Recommendations

1. **Optimize Delivery Routes**
   - Utilize OSRM route projections to minimize delays caused by traffic or multiple deliveries.

2. **Schedule Optimization**
   - Adjust staffing and schedules to handle peak demand (17:00–23:00) efficiently and capitalize on low-traffic periods (late night to morning).

3. **Enhance Driver Performance**
   - Implement targeted training programs for underperforming drivers and maintain vehicle conditions for better efficiency.

---

## Dashboard
![]()
![]()
![]()
![]()
![]()
![]()
![]()
![]()
![]()
![]()
![]()
![]()

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact
For questions or collaborations, feel free to reach out:

- **Email**: [jihadakbr@gmail.com](mailto:jihadakbr@gmail.com)
- **LinkedIn**: [linkedin.com/in/jihadakbr](https://www.linkedin.com/in/jihadakbr)
- **Portfolio**: [jihadakbr.github.io](https://jihadakbr.github.io/)
