# Funnel Analysis Dashboard (Bank Marketing)

Dashboard for analysation - https://futureds03-fgha97prhfnqvbe42wtzhu.streamlit.app/

This project is an interactive Streamlit dashboard for analyzing marketing funnel performance using the Bank Marketing dataset. It focuses on understanding user progression through key stages and identifying opportunities to improve conversion rates.

---

## Overview

The dashboard models a typical marketing funnel:

Contacts → Leads → Customers

It is designed to answer business-critical questions:

* Where do users drop off in the funnel?
* Which channels generate better conversions?
* What improvements can increase overall conversion?

---

## Features

* Funnel visualization of Contacts, Leads, and Customers
* Drop-off analysis between funnel stages
* Channel-wise conversion performance
* Monthly conversion trends
* Interactive filters for job, education, and age
* Data-driven insights for decision making

---

## Tech Stack

* Python
* Streamlit
* Pandas
* Plotly

---

## Dataset

This project uses the Bank Marketing Dataset from the UCI Machine Learning Repository.

Dataset highlights:

* Customer demographic information
* Marketing campaign interactions
* Contact type and duration
* Conversion outcome (subscription: yes/no)

---



## Project Structure

```
.
├── app.py
├── bank-full.csv
├── requirements.txt
├── README.md
```

---

## Key Metrics

* Contact to Lead Conversion Rate
* Lead to Customer Conversion Rate
* Overall Conversion Rate
* Drop-off Percentage

---

## Insights Generated

* Identification of high-performing marketing channels
* Detection of major drop-off points in the funnel
* Segment-based conversion understanding
* Recommendations for improving campaign performance

---

## Deployment

The application can be deployed on Streamlit Community Cloud by connecting the GitHub repository and selecting the main app file.

---

## Author

Bhargav Ram

---

## Future Enhancements

* Campaign-level deep dive analysis
* Integration with real-time marketing data
* Predictive modeling for conversion likelihood
* Exportable reports and dashboards

---

## License

This project is for educational and portfolio purposes.
