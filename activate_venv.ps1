# PowerShell script to activate virtual environment
Write-Host "Activating virtual environment for Sentiment Analysis project..." -ForegroundColor Green

# Navigate to project directory
Set-Location -Path $PSScriptRoot

# Try to activate using different methods
try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "Virtual environment activated successfully!" -ForegroundColor Green
}
catch {
    Write-Host "PowerShell execution policy might be blocking the script. Using alternative method..." -ForegroundColor Yellow
    & ".\venv\Scripts\activate.bat"
}

Write-Host ""
Write-Host "Available commands:" -ForegroundColor Cyan
Write-Host "  - python app.py (for Flask app)" -ForegroundColor White
Write-Host "  - streamlit run streamlit_app.py (for Streamlit app)" -ForegroundColor White
Write-Host "  - python tanglish_sentiment_mega.py (for sentiment analysis)" -ForegroundColor White
Write-Host "  - jupyter notebook (to run Jupyter notebooks)" -ForegroundColor White
Write-Host ""