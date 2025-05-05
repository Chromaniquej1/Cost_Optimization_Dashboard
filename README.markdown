# Company XYZ Benefits Optimization Project

This repository contains a Power BI dashboard, a Plotly Dash web application, and a cost analysis report for optimizing medical benefits costs for Company XYZ's 1000 employees. The project includes visualizations and actionable recommendations to reduce costs, particularly by promoting HSA and HMO plans over high-cost PPO plans.

## Repository Structure
- **Root Files**:
  - `PowerBI_Dashboard.pdf`: UI of the Power BI dashboard.
  - `Report_Cost_Optimization.pdf`: Comprehensive cost analysis report with recommendations.
  - `dashapp.pdf`: UI of the Plotly Dash web app.
  - `README.md`: This file, with setup instructions.
- **Folders**:
  - `Dash_webapp/`: Contains the Plotly Dash app files:
    - `benefits_dashboard.py`: Main Dash app script.
    - `data_employee.csv`: Dataset with employee attributes (job title, department, state, medical plan, costs).
    - `requirements.txt`: Python dependencies.
  - `powebi_dash/`: Contains Power BI files (e.g., `.pbix` file for the dashboard).

## Running the Plotly Dash App Locally

Follow these steps to set up and run the Plotly Dash app locally on your machine.

### Prerequisites
- **Python 3.10** (or compatible version).
- **pip** (Python package manager).
- **Git** (for cloning the repository).
- A web browser (e.g., Chrome, Firefox) to view the app.

### Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Chromaniquej1/benefits-dashboard.git
   cd benefits-dashboard
   ```

2. **Navigate to the Dash App Folder**:
   ```bash
   cd Dash_webapp
   ```

3. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   This installs `dash`, `plotly`, `pandas`, and `gunicorn` as specified in `requirements.txt`.

5. **Verify Dataset**:
   Ensure `data_employee.csv` is in the `Dash_webapp` folder. This file contains the employee data required by the app.

6. **Run the Dash App**:
   ```bash
   python benefits_dashboard.py
   ```
   The app will start in debug mode and display a URL (typically `http://127.0.0.1:8050`).

7. **Access the App**:
   Open your web browser and navigate to `http://127.0.0.1:8050`. You should see the dashboard with:
   - Key metric cards (e.g., total premium cost ~$300,000).
   - Filters for state and department (e.g., California, IT).
   - Charts (e.g., cost by state/plan, savings by department).
   - Savings calculator (~$352.32 per PPO-to-HSA switch).

8. **Stop the App**:
   Press `Ctrl+C` in the terminal to stop the server.

### Troubleshooting
- **Module Not Found**: Ensure dependencies are installed (`pip install -r requirements.txt`).
- **File Not Found**: Verify `data_employee.csv` is in `Dash_webapp/`.
- **Port Conflict**: If `8050` is in use, the app will suggest another port (e.g., `8051`).
- **Errors in Browser**: Check the terminal for error messages and confirm Python 3.10 is used (`python --version`).
- **Dependency Issues**: Upgrade pip (`pip install --upgrade pip`) and retry installation.

## Power BI Dashboard
The Power BI dashboard is in the `powebi_dash` folder, with its UI showcased in `PowerBI_Dashboard.pdf`. To view or edit:
1. Open the `.pbix` file in Power BI Desktop (download from [Microsoft](https://powerbi.microsoft.com/)).
2. Ensure the dataset (`data_employee.csv`) is accessible if needed for refresh.

## Cost Analysis Report
- **Report_Cost_Optimization.pdf**: Contains the full analysis and recommendations.


## Dash App UI
- **dashapp.pdf**: Displays the UI of the Plotly Dash app, including cards, filters, charts, and the savings calculator.


## Contact
For questions or issues, please open a GitHub issue or contact [jayantbiradar619@gmail.com].
