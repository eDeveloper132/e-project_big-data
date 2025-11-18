# EarthScape Climate Agency Analytics Platform

This repository contains the source code for the EarthScape Climate Agency Analytics Platform, a full-stack big data solution designed to monitor, process, and analyze climate change data.

## Project Overview

The platform provides a web-based dashboard for visualizing climate data, detecting anomalies, and predicting future trends. It is built with a scalable architecture suitable for handling large datasets.

- **Backend:** A Flask-based REST API that handles user authentication, data requests, and serves as a gateway to the processed data.
- **Frontend:** A responsive single-page dashboard built with HTML, Bootstrap 5, and Chart.js.
- **Big Data Processing:** A Hadoop MapReduce job developed using the `mrjob` library to process raw climate data.
- **Machine Learning:** A predictive model built with Scikit-Learn for trend analysis and anomaly detection.

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5, Chart.js
- **Data Processing:** `mrjob` (for Hadoop MapReduce)
- **Machine Learning:** `scikit-learn`, `pandas`, `numpy`
- **Database (Simulated):** MongoDB (for metadata), HDFS (for bulk data)

## Project Structure

```
.
├── backend/
│   ├── api/
│   ├── config/
│   └── app.py
├── frontend/
│   ├── src/
│   │   ├── css/style.css
│   │   └── js/script.js
│   └── index.html
├── hadoop_scripts/
│   ├── jobs/climate_analysis.py
│   └── ingest_data.py
├── ml_models/
│   └── src/climate_model.py
└── requirements.txt
```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd earthscape-climate-analytics
    ```

2.  **Create a virtual environment and activate it:**
    *We recommend using `uv`, a fast Python package installer.*
    ```bash
    uv venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

## Running the Project

1.  **Run the Backend Server:**
    The backend serves the frontend and provides the API.
    ```bash
    cd backend
    python app.py
    ```
    The application will be available at `http://127.0.0.1:5000`. Open this URL in your web browser.

2.  **Login Credentials:**
    Use the following mock credentials to log in:
    - **Username:** `admin`, **Password:** `admin_pass` (Administrator role)
    - **Username:** `analyst`, **Password:** `analyst_pass` (Analyst role)

3.  **Generate Dummy Data (Optional):**
    To simulate the data ingestion process, you can run the `ingest_data.py` script. This will create `dummy_climate_data.csv` and `sensor_data.json`.
    ```bash
    cd hadoop_scripts
    python ingest_data.py
    ```

4.  **Run the MapReduce Job (Simulation):**
    You can test the MapReduce job locally. It will process the generated CSV file and output the average temperature per region.
    ```bash
    cd hadoop_scripts/jobs
    python climate_analysis.py ../dummy_climate_data.csv
    ```

5.  **Train the Machine Learning Model (Simulation):**
    To train the ML model and see an example prediction, run the `climate_model.py` script.
    ```bash
    cd ml_models/src
    python climate_model.py
    ```
