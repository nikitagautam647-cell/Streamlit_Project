# Streamlit Project

A lightweight Streamlit application for interactive data exploration and visualization. This repository includes the app source code, dependency requirements, and usage instructions for running the project locally.

## Table of Contents

- [Introduction](#introduction)
- [Dataset / Inputs](#dataset--inputs)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Results / Output](#results--output)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

This project is a Streamlit web application that provides an interactive logistics dashboard for Nassau Candy Co. It includes filters, KPI cards, and multi-tab analytics for performance overview, delay risk analysis, delivery efficiency, and smart recommendations.

## Dataset / Inputs

- The app uses an Excel dataset named `streamlit excel.xlsx`.
- The data contains order, shipment, and logistics metrics including lead time, sales, gross profit, state, ship mode, and delay status.
- If you want to run this locally, keep the Excel file in the project root next to `app.py`.

## Tech Stack

- Python
- Streamlit
- pandas
- plotly (or other visualization library if used)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nikitagautam647-cell/Streamlit_Project.git
   cd Streamlit_Project
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:

   ```powershell
   . .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

## Usage

Run the Streamlit application from the project root:

```bash
python -m streamlit run app.py
```

Then open the URL shown in your browser, typically `http://localhost:8501`.

### Deployed App

View the live dashboard here:

https://appproject-fztzy8a96wsxcxtuh6x5hr.streamlit.app/

## Features

- Interactive Streamlit interface
- Easy local setup and execution
- Modular project structure for quick updates
- Placeholder for data analysis or visualization workflows

## Results / Output

- The app displays a rich dashboard with KPI cards, interactive filters, and multiple analytics tabs.
- Tabs include `Performance Overview`, `Delay Risk Analysis`, `Delivery Efficiency`, and `Smart Recommendations`.
- The hosted dashboard is available at the deployment link above.

## Project Structure

```
Streamlit_Project/
├── app.py
├── requirements.txt
├── README.md
└── run-project.md
```

- `app.py` — Main Streamlit application script.
- `requirements.txt` — Python dependencies required to run the app.
- `README.md` — Project overview and setup instructions.
- `run-project.md` — Additional project execution notes.

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request with a clear description.

## License

This project is available under the [MIT License](LICENSE).

## Contact

For questions or feedback, please open an issue in the repository.

- Name: Nikita Gautam
- Email: nikitagautm647@gmail.com
