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

### Data retrieval: Use the "mysql-connector-python" library to connect to the MySQL database and fetch the data into a Pandas dataframe.

