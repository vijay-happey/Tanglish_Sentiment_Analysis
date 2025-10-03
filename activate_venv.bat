@echo off
echo Activating virtual environment for Sentiment Analysis project...
call venv\Scripts\activate.bat
echo Virtual environment activated!
echo You can now run:
echo   - python app.py (for Flask app)
echo   - streamlit run streamlit_app.py (for Streamlit app)
echo   - python tanglish_sentiment_mega.py (for sentiment analysis)
echo.
cmd /k