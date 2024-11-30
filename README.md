# File and Folder Cleanup Tool with Progress

This tool helps you delete files and folders older than a specific date, with a progress tracker. It is built using Streamlit for the user interface.

## screenshot
![Screenshot](screenshot_1.png)
![Screenshot](screenshot_2.png)
## Core Functionality

- **Input Folder Path**: Allows the user to specify the folder path to scan for files and folders.
- **Date Threshold**: Users can select a date threshold. Files and folders older than this date will be deleted.
- **Progress Tracker**: Displays the progress of the deletion process, showing the current file or folder being deleted.
- **Completion Status**: Shows the total number of files and folders deleted once the process is complete.

## Setup

### Prerequisites

- Python 3.6 or higher
- Streamlit library

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/easy_delete.git
    cd easy_delete
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. **Start the Streamlit application**:
    ```bash
    streamlit run easy_delete.py
    ```

2. **Open your web browser** and navigate to `http://localhost:8501` to access the application.

### Usage

1. **Enter the folder path** you want to scan.
2. **Select the date threshold** for deletion.
3. **Click the "Start Deletion" button** to begin the deletion process.
4. **Monitor the progress** of the deletion process through the progress bar and status text.
5. **View the total files and folders deleted** at the top of the interface once the process is complete.


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Streamlit for providing an easy-to-use framework for building web applications in Python.