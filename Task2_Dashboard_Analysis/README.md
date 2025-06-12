# Task 2 – Descriptive and Predictive Analysis with Interactive Dashboard

## 📄 Overview

This task performs **Descriptive** and **Predictive** analysis on a sales dataset and displays the insights via an **interactive dashboard** built with **Plotly Dash**.
The dashboard provides filters, visualizations, and a live sales prediction form powered by a trained machine learning model.

---

## 📂 Directory Structure


Task2_Dashboard_Analysis/

├── data/

│   └── sales_data_sample.csv           # Dataset (from Kaggle)

├── model/

│   ├── sales_model.pkl                 # Trained ML model

│   ├── le_product.pkl                  # LabelEncoder for PRODUCTLINE

│   └── le_country.pkl                  # LabelEncoder for COUNTRY

├── eda_notebook.ipynb                 # Data exploration + model building

├── dashboard_app.py                   # Final dashboard application

├── README.md                          # This documentation



## 🔮 Predictive Analysis

A **Random Forest Regression model** is trained to predict `SALES` based on:

**Features used**:

- `QUANTITYORDERED`
- `PRICEEACH`
- `MSRP`
- `DISCOUNT` (engineered)
- `UNIT_PROFIT` (engineered)
- `IS_BIG_ORDER` (engineered: quantity > 30 → 1)
- Encoded `COUNTRY` and `PRODUCTLINE`

**Model Performance**:

- R² Score: ~0.88
- MAE: ₹315

Model saved as `sales_model.pkl` and used in the dashboard for real-time predictions.

---

## 🧪 Sample Prediction

Using:

- Quantity Ordered: `10`
- Price Each: `100`
- MSRP: `120`
- Product Line: `Motorcycles`

The prediction output will display something like:

> 📈 **Predicted Sales: ₹1056.47**

---

## 💻 How to Run the Dashboard

##### 1. Clone Repo

* git clone
* cd Task1_CRUD_Sales

##### 2.Install Dependencies

* pip install -r requirements.txt

##### 3. Launch the Dashboard

* python dashboard_app.py

##### 4.will start a local server at:

* http://127.0.0.1:8050/

## 📑 File Descriptions

### ✅ `eda_notebook.ipynb`

* Performs full data cleaning
* Feature engineering
* Exploratory graphs (bar, pie, heatmap)
* Trains `RandomForestRegressor` on selected features
* Saves:
  * `sales_model.pkl`
  * `le_product.pkl` (LabelEncoder for PRODUCTLINE)
  * `le_country.pkl` (LabelEncoder for COUNTRY)

# Dashboard Analysis

### 📊 Enterprise Sales Analytics Suite

An interactive, production-grade dashboard built with **Dash** and  **Plotly** , delivering real-time business intelligence and AI-driven sales predictions. This dashboard provides deep insights into sales trends, performance metrics, product analysis, and customer behavior across global markets.

## 🚀 Features

### 🔹 Real-Time KPIs

* **Total Revenue** ,  **Orders** ,  **Average Order Value** , **Profit** updated live.
* Interactive filters to instantly reflect business performance.

### 🔹 Interactive Visualizations

* 📈  **Main Trend Chart** : Revenue, Profit, and Sales Volume over time.
* 🎯  **Performance Gauges** : Profit Margin and Fulfillment Rate.
* 🏪  **Product Treemap** : Breakdown by product line.
* 🌍  **Geographic Sales Map** : Sales heatmap by country.
* 🕒  **Temporal Heatmap** : Analyze sales patterns across weekdays and months.

### 🔹 AI-Powered Sales Prediction

* Predict sales using inputs like Quantity, Price, MSRP, Market, and Product Line.
* Shows confidence intervals, profit margin analysis, and deal quality indicators.

### 🔹 Advanced UX/UI Design

* Modern **dark-themed** UI with smooth animations, icons, and custom components.
* Sticky sidebar with filters and alert system.
* Data table with filtering, sorting, and conditional formatting.

##### 🧠 Technologies Used


| Category       | Tools/Frameworks                                                                   |
| -------------- | ---------------------------------------------------------------------------------- |
| Dashboard      | [Dash](https://dash.plotly.com/), [Plotly]                                            |
| ML Integration | joblib, Scikit-learn                                                              |
| UI Components  | [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) |
| Visualization  | Plotly Express, Plotly Graph Objects                                               |
| Styling        | Custom CSS, Google Fonts (Inter), FontAwesome                                      |


##### 📊 Insights Provided

| Metric            | Description                                |
| ----------------- | ------------------------------------------ |
| Total Revenue     | Aggregated sales value                     |
| Orders            | Number of transactions                     |
| Profit & Margin   | Calculated from MSRP and discounts         |
| Sales Volume      | Units sold                                 |
| Geographic Spread | Sales across countries                     |
| Product Share     | Treemap of product lines                   |
| Temporal Trends   | Day-Month heatmaps                         |
| Prediction        | Forecasted sales using business parameters |



## 📌 Filters Available

* **Time Aggregation** : Daily, Weekly, Monthly, Quarterly, Yearly
* **Date Range** : Select specific time span
* **Product Lines**
* **Countries (Markets)**
* **Customer Segment** : Low, Medium, High, Premium

---

## 📥 Data Table

At the bottom of the dashboard:

* Displays latest 50 transactions
* Sortable, searchable, and filterable
* Color-coded rows for profit margins

---

## 🎯 Ideal Use Cases

* Business sales monitoring dashboards
* Executive performance overviews
* Market-specific product strategy
* Predictive insights and what-if scenario testing

---

## 📌 Notes

* If `sales_model.pkl`, `le_product.pkl`, or `le_country.pkl` are missing, the app will simulate data.
* Optimized for modern browsers and supports responsive layouts.

## 👤 Author

**Mayur Subhash Gholap**

*Engineer & Full Stack Developer with AI/ML Experience*

---

## 📝 License

This project is open-source and free to use under the MIT License.
