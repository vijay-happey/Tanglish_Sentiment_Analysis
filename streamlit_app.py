import streamlit as st
import pandas as pd
import os
import tempfile
from tanglish_sentiment_mega import analyze_sentiment

# Set page configuration
st.set_page_config(
    page_title="Tanglish Sentiment Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #1f77b4;
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .sentiment-positive {
        color: #28a745;
        font-weight: bold;
    }
    .sentiment-negative {
        color: #dc3545;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: #6c757d;
        font-weight: bold;
    }
    .results-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 2px solid;
    }
    .results-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    .results-column {
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ddd;
    }
    .positive-column {
        background-color: #d4edda;
        border-color: #c3e6cb;
    }
    .negative-column {
        background-color: #f8d7da;
        border-color: #f5c6cb;
    }
    .neutral-column {
        background-color: #fff3cd;
        border-color: #ffeaa7;
    }
    .sentence-item {
        background: white;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        border-left: 4px solid;
    }
    .positive-item {
        border-color: #28a745;
    }
    .negative-item {
        border-color: #dc3545;
    }
    .neutral-item {
        border-color: #6c757d;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header"><h1>🧠 Tanglish Sentiment Analyzer</h1><p>Analyze sentiment in Tamil+English mixed sentences (Tanglish)</p></div>',
                unsafe_allow_html=True)

    # Create tabs for different modes
    tab1, tab2 = st.tabs(["📝 Text Input Mode", "📁 CSV Upload Mode"])

    with tab1:
        st.markdown('<h2 class="section-header">📝 Text Input Mode</h2>', unsafe_allow_html=True)

        # Text input
        text_input = st.text_area(
            "Enter your Tanglish text:",
            placeholder="Enter your Tanglish sentence here... e.g., 'Semma awesomeu da! Vera level magizhchi.'",
            height=100
        )

        if st.button("Analyze Sentiment", type="primary"):
            if text_input.strip():
                with st.spinner("Analyzing sentiment..."):
                    result = analyze_sentiment(text_input)
                    st.success("Analysis Complete!")

                    # Display result in a styled box
                    sentiment_class = result.split(' ')[0].lower()
                    st.markdown(f"""
                        <div class="results-box sentiment-{sentiment_class}">
                            <h3>Analysis Result</h3>
                            <p style="font-size: 1.2rem;">{result}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Please enter some text to analyze.")

    with tab2:
        st.markdown('<h2 class="section-header">📁 CSV Upload Mode</h2>', unsafe_allow_html=True)

        # File upload
        uploaded_file = st.file_uploader(
            "Upload CSV file:",
            type=['csv'],
            help="CSV file should contain a text column (default: 'text')"
        )

        # Column name input
        text_column = st.text_input(
            "Text column name:",
            value="text",
            placeholder="text"
        )

        if uploaded_file is not None:
            if st.button("Analyze CSV", type="primary"):
                with st.spinner("Processing CSV file..."):
                    try:
                        # Read CSV
                        df = pd.read_csv(uploaded_file)

                        if text_column not in df.columns:
                            st.error(f"Column '{text_column}' not found in CSV. Available columns: {', '.join(df.columns)}")
                        else:
                            # Analyze sentiment for each row
                            df['sentiment'] = df[text_column].apply(analyze_sentiment)

                            # Split by sentiment for display
                            positive_df = df[df['sentiment'].str.contains('Positive')]
                            negative_df = df[df['sentiment'].str.contains('Negative')]
                            neutral_df = df[df['sentiment'].str.contains('Neutral')]

                            # Store results in session state for downloads
                            st.session_state.positive_df = positive_df
                            st.session_state.negative_df = negative_df
                            st.session_state.neutral_df = neutral_df
                            st.session_state.complete_df = df

                            st.success("CSV Analysis Complete!")

                            # Display results
                            display_csv_results(positive_df, negative_df, neutral_df, text_column)

                    except Exception as e:
                        st.error(f"Error processing CSV: {str(e)}")
        else:
            st.info("Please upload a CSV file to get started.")

def display_csv_results(positive_df, negative_df, neutral_df, text_column):
    """Display CSV analysis results in a grid layout"""
    st.markdown('<h3 class="section-header">📊 Analysis Results</h3>', unsafe_allow_html=True)

    # Create columns for different sentiment types
    col1, col2 = st.columns(2)

    with col1:
        # Positive results
        st.markdown("""
            <div class="results-column positive-column">
                <h4>😀 Positive Sentences</h4>
            </div>
        """, unsafe_allow_html=True)

        if not positive_df.empty:
            for _, row in positive_df.iterrows():
                st.markdown(f"""
                    <div class="sentence-item positive-item">
                        <p><strong>{row[text_column]}</strong></p>
                        <p class="sentiment-positive">{row['sentiment']}</p>
                    </div>
                """, unsafe_allow_html=True)

        # Negative results
        st.markdown("""
            <div class="results-column negative-column">
                <h4>😞 Negative Sentences</h4>
            </div>
        """, unsafe_allow_html=True)

        if not negative_df.empty:
            for _, row in negative_df.iterrows():
                st.markdown(f"""
                    <div class="sentence-item negative-item">
                        <p><strong>{row[text_column]}</strong></p>
                        <p class="sentiment-negative">{row['sentiment']}</p>
                    </div>
                """, unsafe_allow_html=True)

    with col2:
        # Neutral results
        st.markdown("""
            <div class="results-column neutral-column">
                <h4>😐 Neutral Sentences</h4>
            </div>
        """, unsafe_allow_html=True)

        if not neutral_df.empty:
            for _, row in neutral_df.iterrows():
                st.markdown(f"""
                    <div class="sentence-item neutral-item">
                        <p><strong>{row[text_column]}</strong></p>
                        <p class="sentiment-neutral">{row['sentiment']}</p>
                    </div>
                """, unsafe_allow_html=True)

    # Download buttons
    st.markdown('<h3 class="section-header">📥 Download Results</h3>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📄 Complete Results", use_container_width=True):
            csv_data = st.session_state.complete_df.to_csv(index=False)
            st.download_button(
                label="Download Complete CSV",
                data=csv_data,
                file_name="sentiment_analysis_complete.csv",
                mime="text/csv",
                key="complete_download"
            )

    with col2:
        if not positive_df.empty and st.button("😀 Positive Only", use_container_width=True):
            csv_data = positive_df.to_csv(index=False)
            st.download_button(
                label="Download Positive CSV",
                data=csv_data,
                file_name="positive_sentiments.csv",
                mime="text/csv",
                key="positive_download"
            )

    with col3:
        if not negative_df.empty and st.button("😞 Negative Only", use_container_width=True):
            csv_data = negative_df.to_csv(index=False)
            st.download_button(
                label="Download Negative CSV",
                data=csv_data,
                file_name="negative_sentiments.csv",
                mime="text/csv",
                key="negative_download"
            )

    with col4:
        if not neutral_df.empty and st.button("😐 Neutral Only", use_container_width=True):
            csv_data = neutral_df.to_csv(index=False)
            st.download_button(
                label="Download Neutral CSV",
                data=csv_data,
                file_name="neutral_sentiments.csv",
                mime="text/csv",
                key="neutral_download"
            )

if __name__ == "__main__":
    main()
