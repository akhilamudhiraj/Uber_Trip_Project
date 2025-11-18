 Uber Trip Analysis Project

## Description
This project analyzes Uber trip data to gain insights into trip patterns, peak hours, trip durations, and locations. It uses Python, Pandas, Matplotlib, and Seaborn for data analysis and visualization.

## Folder Structure
- `data/` – Contains raw Uber trip datasets.
- `notebooks/` – Jupyter notebooks for EDA and analysis.
- `scripts/` – Python scripts for preprocessing, analysis, and plotting.
- `plots/` – Generated visualizations.
- `.venv/` – Virtual environment for project dependencies.
- `README.md` – Project overview and instructions.
- `requirements.txt` – Python dependencies.

## Features
- Exploratory Data Analysis (EDA) on Uber trip datasets
- Visualization of trip distribution, peak hours, and locations
- Summary statistics for trip durations and distances
- Identification of high-demand areas and time slots

## Dataset
The project uses Uber trip datasets for analysis.  
Path in the project: `data/uber_trip_data.csv`

## Installation
Clone the repository:
```bash
git clone https://github.com/akhilamudhiraj/Uber_Trip_Project.git
Navigate into the project folder:

bash
Copy code
cd Uber_Trip_Project
Create a virtual environment (if not already created):

bash
Copy code
python -m venv .venv
Activate the virtual environment:

Windows (PowerShell):

bash
Copy code
.\.venv\Scripts\Activate.ps1
Windows (CMD):

bash
Copy code
.venv\Scripts\activate.bat
Install the required libraries:

bash
Copy code
pip install -r requirements.txt
Usage
Run analysis scripts or Jupyter notebooks:

bash
Copy code
jupyter notebook notebooks/uber_analysis.ipynb
Visualizations will be saved in the plots/ folder
