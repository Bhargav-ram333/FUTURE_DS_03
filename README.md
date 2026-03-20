# FUTURE_DS_03
# Funnel Analysis Dashboard (Bank Marketing)

A Streamlit-based interactive dashboard to analyze marketing funnel performance using the Bank Marketing dataset. This project helps identify conversion rates, drop-off points, and high-performing segments.

---

## Project Overview

This project analyzes how users move through a marketing funnel:

Contacts → Leads → Customers

It answers key business questions:

* Where are users dropping off?
* Which channels perform best?
* How can conversions be improved?

---

## Features

* Funnel visualization (Contacts → Leads → Customers)
* Drop-off analysis at each stage
* Channel-wise conversion performance
* Monthly conversion trends
* Interactive filters (Job, Education, Age)
* Actionable insights

---

## Tech Stack

* Python
* Streamlit
* Pandas
* Plotly

---

## Dataset

The project uses the Bank Marketing Dataset from the UCI Machine Learning Repository.

* Contains customer campaign data
* Includes job, age, education, contact type, and conversion outcome

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-repo-link>
cd <your-repo-folder>
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run the Application

```bash
streamlit run app.py
```

---

## Project Structure

```
project/
│── app.py
│── bank-full.csv
│── requirements.txt
│── README.md
```

---

## Key Metrics

* Contact to Lead Conversion Rate
* Lead to Customer Conversion Rate
* Overall Conversion Rate
* Drop-off Percentage at Each Stage

---

## Insights

This dashboard helps:

* Identify high-performing marketing channels
* Detect major drop-off points in the funnel
* Understand customer segments
* Improve marketing strategy using data

---

## Deployment

This application can be deployed using Streamlit Community Cloud.

---

## Author

Bhargav Ram

---

## Future Improvements

* Campaign-level performance analysis
* Real-time data integration
* Machine learning-based predictions
* Exportable reports
