# Tanglish Sentiment Analysis - Virtual Environment Setup

## Virtual Environment Created Successfully! 🎉

Your Python virtual environment has been set up with all the necessary dependencies for your sentiment analysis project.

## Activation Instructions

### Method 1: Using Batch File (Recommended for Windows)
```cmd
activate_venv.bat
```

### Method 2: Using PowerShell Script
```powershell
.\activate_venv.ps1
```

### Method 3: Manual Activation
```cmd
# Command Prompt / PowerShell
.\venv\Scripts\activate.bat

# Or for PowerShell (if execution policy allows)
.\venv\Scripts\Activate.ps1
```

## Installed Packages

### Core Dependencies
- **streamlit** (1.50.0) - Web app framework
- **flask** (3.1.2) - Web framework
- **pandas** (2.3.3) - Data manipulation
- **numpy** (2.3.3) - Numerical computing
- **matplotlib** (3.10.6) - Data visualization

### Additional Packages
- **requests** - HTTP requests
- **werkzeug** - WSGI utilities
- And many more supporting libraries...

## Running Your Applications

Once the virtual environment is activated, you can run:

### Streamlit App
```cmd
streamlit run streamlit_app.py
```

### Flask App
```cmd
python app.py
```

### Sentiment Analysis Module
```cmd
python tanglish_sentiment_mega.py
```

### Jupyter Notebooks
```cmd
# Install Jupyter first (optional)
pip install jupyter ipykernel

# Then run
jupyter notebook
```

## Adding New Packages

To install additional packages in your virtual environment:

```cmd
# Make sure virtual environment is activated first
pip install package_name

# To save to requirements.txt
pip freeze > requirements.txt
```

## Deactivating the Virtual Environment

When you're done working, you can deactivate the virtual environment:

```cmd
deactivate
```

## Virtual Environment Location

Your virtual environment is located at:
```
c:\Users\vijay\OneDrive\Documents\Projects\sen\sentiment\venv\
```

## Troubleshooting

### PowerShell Execution Policy Error
If you get an execution policy error when trying to activate in PowerShell:

1. Run PowerShell as Administrator
2. Execute: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
3. Or use the batch file activation method instead

### Python Not Found
Make sure you're using the virtual environment's Python:
```cmd
.\venv\Scripts\python.exe your_script.py
```

## Project Structure

Your sentiment analysis project includes:
- `app.py` - Flask web application
- `streamlit_app.py` - Streamlit web application  
- `tanglish_sentiment_mega.py` - Core sentiment analysis logic
- Various Jupyter notebooks for experiments
- Data files for training and testing

Happy coding! 🚀