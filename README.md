Agentic AI Manufacturing Data Integration Platform
🤖 Agentic AI Manufacturing Integration is an interactive AI-powered system that integrates production ERP/MES data with CMM quality measurements to deliver comprehensive manufacturing analytics and actionable insights.

🚀 Project Overview
Manufacturing data often lives in silos: production systems track order and machine data while CMM systems capture quality measurements separately.

This platform demonstrates a true agentic AI approach that autonomously:

Discovers semantic relationships between these disparate datasets (schema mapping)

Integrates and merges data based on those relationships

Calculates key quality metrics like pass/fail rates

Provides traceability of defects to production lots

Detects anomalies in measurement deviations using statistical methods

All results are presented through a modern, tabbed, and user-friendly dashboard built with Streamlit and Plotly.

🎯 Key Features
File Uploads or Sample Data: Upload your own ERP and CMM CSV files or use the provided sample data to get started quickly

AI-Powered Schema Mapping: Automatically identify which columns correspond between production and quality data sources

Seamless Data Integration: Merge datasets based on AI-discovered relationships to create a unified dataset for analysis

Quality Analytics Dashboard: Interactive charts and tables showing pass/fail rates overall and by machine, shift, and plant

Traceability: Defects linked back to specific production lots for root cause analysis

Anomaly Detection: Identify measurements with unusually high deviations beyond tolerance thresholds

Export Options: Download unified datasets, defective lots, anomalies, and reporting summaries easily

📂 Data Description
Production Data (ERP/MES)
Production order IDs, Part IDs, Lot IDs

Machine and operator information

Production timestamps, quantities, and shifts

CMM Data (Quality Measurements)
Measurement IDs, Component IDs

Feature measurements with nominal and tolerance values

Pass/fail quality results

Measurement timestamps and inspector info

🏗️ Architecture & Tools
Python 3.8+: Backend & data processing

Pandas: Data manipulation

NumPy: Numeric computations

Streamlit: Web UI framework

Plotly: Interactive data visualization

Agentic AI: AI-driven schema mapping and analysis automation

💡 Setup & Usage
Install dependencies
bash
pip install -r requirements.txt
Run the dashboard
bash
streamlit run streamlit_app_ultimate.py
Workflow:
Upload your production and CMM CSV files or click Use Sample Data.

The system automatically maps schemas, integrates data, and runs all analyses.

Navigate tabs to explore AI-discovered mappings, integrated data preview, quality analytics, and anomaly detection.

Export datasets and reports directly from the UI.

📈 Benefits & Impact
Reduces manual data integration time from days to minutes

Enables real-time identification and traceability of defects

Provides data-driven insights for continuous quality improvement

Demonstrates scalable, autonomous AI methodology for manufacturing analytics

🦾 Next Steps & Roadmap
Incorporate real-time data streaming & IoT sensor inputs

Add predictive ML models for early defect detection

Integrate computer vision for visual quality inspection

Deploy on scalable cloud infrastructure

Extend schema mapping with language models (OpenAI API) if desired

👨‍💻 About
Developed as a Machine Learning application prototype demonstrating agentic AI principles within discrete manufacturing analytics.
