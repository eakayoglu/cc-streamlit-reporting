# Coffee Shop Reporting Dashboard

Welcome to the Coffee Shop Reporting Dashboard project! This dashboard is designed to provide insightful visualizations and reports based on sales data. It leverages Streamlit for the web interface, Pandas for data manipulation, and Plotly for creating interactive charts.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Interactive Filters**: Easily filter data using the built-in UI.
- **Visual Reports**: Generate bar charts for sales by category, sub-category, and month.
- **Multiple Tabs**: Navigate through different tabs for various reports.
- **File Upload**: Upload Excel files to visualize custom data.
- **Responsive Layout**: Optimized for different screen sizes.

## Installation

To get started with the Coffee Shop Reporting Dashboard, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/eakayoglu/cc-streamlit-reporting.git
    cd cc
    ```

2. **Create a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Activate the virtual environment:**
    ```sh
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Run the Streamlit app:**
    ```sh
    streamlit run app.py
    ```

3. **Upload your Excel file**: Once the app is running, upload your Excel file to visualize the data.

## File Structure

```
cc-streamlit-reporting/
├── app.py
├── requirements.txt
├── README.md
└── venv/
```

- `app.py`: The main application file containing the Streamlit app code.
- `requirements.txt`: A list of Python packages required to run the app.
- `README.md`: This file.
- `venv/`: The virtual environment directory.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
