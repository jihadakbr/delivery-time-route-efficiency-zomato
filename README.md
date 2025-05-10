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
![]()
### Insights

---
![]()
### Insights

---
![]()
### Insights

---
![]()
### Insights

---
![]()
### Insights

---
![]()
### Insights

---
![]()
### Insights

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
[Dashboard Image Placeholder]()

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact
For questions or collaborations, feel free to reach out:

- **Email**: [jihadakbr@gmail.com](mailto:jihadakbr@gmail.com)
- **LinkedIn**: [linkedin.com/in/jihadakbr](https://www.linkedin.com/in/jihadakbr)
- **Portfolio**: [jihadakbr.github.io](https://jihadakbr.github.io/)
