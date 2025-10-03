# Deployment Script for Tanglish Sentiment Analyzer
# This script helps deploy the Streamlit app to Streamlit Cloud

import streamlit as st
import os

# Check if we're running on Streamlit Cloud
if os.getenv('STREAMLIT_SHARING_MODE'):
    st.success("✅ App is deployed on Streamlit Cloud!")
else:
    st.info("ℹ️ To deploy this app:")

    st.markdown("""
    ## Deployment Steps:

    1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

    2. **Run locally:**
    ```bash
    streamlit run streamlit_app.py
    ```

    3. **Deploy to Streamlit Cloud:**
       - Push your code to GitHub
       - Go to [share.streamlit.io](https://share.streamlit.io)
       - Connect your GitHub repository
       - Set main file path: `sentiment/streamlit_app.py`
       - Click "Deploy"

    4. **Alternative deployment options:**
       - **Heroku**: Use `streamlit-heroku` package
       - **AWS/Azure/GCP**: Use container deployment
       - **Docker**: Create Dockerfile with Streamlit

    ## File Structure:
    ```
    sentiment/
    ├── streamlit_app.py      # Main Streamlit app
    ├── tanglish_sentiment_mega.py  # Sentiment analysis library
    ├── requirements.txt       # Python dependencies
    └── data/                  # Any data files
    ```
    """)

# Show app info
st.info("🧠 Tanglish Sentiment Analyzer - Ready for deployment!")
