# PhonePe-Pulse-Data-Visualization


## Introduction
PhonePe Pulse is a feature offered by the Indian digital payments platform called PhonePe.

PhonePe Pulse provides users with insights and trends related to their digital transactions and usage patterns on the PhonePe app. It offers personalized analytics, including spending patterns, transaction history, and popular merchants among PhonePe users.

This feature aims to help users track their expenses, understand their financial behavior, and make informed decisions.


## Problem Statement
The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics.The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.


## Approach

### Data extraction: 
Clone the Github using scripting to fetch the data from the Phonepe pulse Github repository and store it in a suitable format such as CSV or JSON.

### Data transformation: 
Use Python, along with libraries such as Pandas, to manipulate and pre-process the data. 
This may include cleaning the data, handling missing values, and transforming the data into a format suitable for analysis and visualization.

### Database insertion: 
Use the "mysql-connector-python" library in Python to connect to a MySQL database and insert the transformed data using SQL commands.

### Dashboard creation: 
Use the Streamlit and Plotly libraries in Python to create an interactive and visually appealing dashboard. 
Plotly's built-in geo map functions can be used to display the data on a map and 
Streamlit can be used to create a user-friendly interface with multiple dropdown options for users to select different facts and figures to display.

### Data retrieval: 
Use the "mysql-connector-python" library to connect to the MySQL database and fetch the data into a Pandas dataframe.


## Tools used

1. Github cloning
2. Python
3. Pandas
4. MYSQL database
5. Streamlit
6. PLotly

## Key skills

1. Data extraction and processing
2. Database management
3. Visualization and dashboard creation
4. Geo visualization
5. Dynamic updating


## Dashboard Overview

This dashboard has three main sections :

### Home

This section contains about the PhonePe and PhonePe pulse data which is used for data analysis.

### Data Visualization 

This section contains two parts Country Analysis and State Analysis

#### 1. Country Analysis

This section has the live geo visualization dashboard that displays information and insights about the transaction, Insurance and users data for Country analysis.

#### 2. State Analysis

This section has different visualizations and facts and figures that displays information and insights for State level analysis for transaction, Insurance and users data.


### Top Insights

This section contains dashboard that have 10 different dropdown options for users to select different facts to display for valuable insights and information about the data, making it a valuable tool for data analysis and decision-making.


### References

**Dataset** : https://github.com/PhonePe/pulse#readme

**Inspired From** : https://www.phonepe.com/pulse/explore/transaction/2022/4/






