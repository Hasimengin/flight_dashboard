# Analysing Domestic Commercial Airline Traffic Delays

## Objective
This repository allows users to interactively analyse the **BTS Marketing Carrier On-Time Performance** dataset from **2018 to 2025**.

## Input Dataset
The on-time performance dataset was downloaded from the **Bureau of Transportation Statistics (BTS)** website.

- Source: https://www.transtats.bts.gov/
- Time span: **2018 to 2025**
- Original size: **56M+ records**
- Sample used in this project: **2M records**, selected randomly

The full dataset can be downloaded [here](https://drive.google.com/file/d/1n7_2Sbc1j0IRJhlT-ezSAm2lY2Q3oZGB/view?usp=drive_link).

## File Dictionary

### `data_download.py`
Python script used to download data from the BTS website.

### `data_download_with_ui_automation.py`
Python script designed to download data from the BTS website through UI automation using the Playwright library.It has some bugs.

### `flight_anlaysis_report.ipynb`
Jupyter notebook with three sections that allow users to analyse flight data interactively.

### `On_Time_Marketing_Carrier_On_Time_Performance_update_sample_v2.parquet`
Subset of the flight data used in `flight_anlaysis_report.ipynb`.

### `usa_airport_locations.csv`
CSV file containing airport coordinates used to map airports in the United States.  
The dataset was downloaded from [here](https://www.arcgis.com/home/item.html?id=cba647d88bcb4c819b01dcfba019c456).

### `L_UNIQUE_CARRIERS.csv`
CSV file containing the list of airline carriers. It is used to map carrier codes to full carrier names in the `On_Time_Marketing_Carrier_On_Time_Performance_update_sample_v2.parquet` dataset.

## User Manual

You can run `flight_anlaysis_report.ipynb` in two different ways:

- Local setup
- GitHub Codespaces

---

## Local Setup

You can clone this repository to your computer and run the notebook locally. The instructions below assume that you have **VS Code** installed.

### macOS

1. Open the **Terminal** app.
2. Navigate to the folder where you want to store the project:

   ```bash
    cd yourprojectpath
   ```
3. Clone the repository:

   ```bash
   git clone https://github.com/Hasimengin/flight_dashboard.git
   ```

4. Open the project in VS Code:

   ```bash
   code .
   ```

5. Open a new terminal session in VS Code.
6. Move into the project directory:

   ```bash
   cd flight_dashboard
   ```

7. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

8. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

9. Install dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

10. Open `flight_anlaysis_report.ipynb` and run each section from top to bottom.

You can then use the interactive dashboard with your own inputs.

### Windows (PowerShell)

1. Open **PowerShell**.
2. Navigate to the folder where you want to store the project:

   ```powershell
   cd yourprojectpath
   ```

3. Clone the repository:

   ```powershell
   git clone https://github.com/Hasimengin/flight_dashboard.git
   ```

4. Open VS Code.
5. Open a new PowerShell session in VS Code.
6. Move into the project directory:

   ```powershell
   cd flight_dashboard
   ```

7. Create a virtual environment:

   ```powershell
   python3 -m venv venv
   ```

8. Activate the virtual environment:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

9. Install dependencies from `requirements.txt`:

   ```powershell
   pip install -r requirements.txt
   ```

10. Open `flight_anlaysis_report.ipynb` and run each section from top to bottom.

You can then use the interactive dashboard with your own inputs.

---

## GitHub Codespaces

You can also run the notebook in **GitHub Codespaces**.

1. Open the repository in your browser while logged into your GitHub account:

   ```text
   https://github.com/Hasimengin/flight_dashboard
   ```

2. On the repository page, click **Code**.
3. Select the **Codespaces** tab.
4. Click **Create codespace on main**.

A VS Code environment will launch in the browser.

The Codespaces environment is already configured through the `.devcontainer` setup, so dependencies should be installed automatically without needing to create a virtual environment manually.

5. Open the dashboard notebook.
6. Run the cells from top to bottom.

If you get a Python interpreter error:

- Press `Ctrl + Shift + P`
- Search for **Python: Select Interpreter**
- Choose the correct Python interpreter for the Codespace

After that, rerun the notebook cells.

---

## Repository Link

```text
https://github.com/Hasimengin/flight_dashboard.git
```
