from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
import pandas as pd
from werkzeug.utils import secure_filename
from tanglish_sentiment_mega import analyze_sentiment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    text_result = None
    text_input = ""
    error = None
    results = None
    positive_texts = []
    negative_texts = []
    neutral_texts = []
    download_ready = False

    if request.method == 'POST':
        if 'text_input' in request.form and request.form['text_input'].strip():
            text_input = request.form['text_input']
            text_result = analyze_sentiment(text_input)

        elif 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Process CSV
                try:
                    df = pd.read_csv(filepath)
                    text_column = request.form.get('text_column', 'text')

                    if text_column not in df.columns:
                        error = f"Column '{text_column}' not found in CSV. Available columns: {', '.join(df.columns)}"
                    else:
                        # Analyze sentiment for each row
                        df['sentiment'] = df[text_column].apply(analyze_sentiment)

                        # Split by sentiment for display
                        positive_df = df[df['sentiment'].str.contains('Positive')]
                        negative_df = df[df['sentiment'].str.contains('Negative')]
                        neutral_df = df[df['sentiment'].str.contains('Neutral')]

                        positive_texts = positive_df[[text_column, 'sentiment']].values.tolist()
                        negative_texts = negative_df[[text_column, 'sentiment']].values.tolist()
                        neutral_texts = neutral_df[[text_column, 'sentiment']].values.tolist()

                        # Save separate CSV files for each sentiment
                        if not positive_df.empty:
                            positive_df.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'positive_results.csv'), index=False)
                        if not negative_df.empty:
                            negative_df.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'negative_results.csv'), index=False)
                        if not neutral_df.empty:
                            neutral_df.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'neutral_results.csv'), index=False)

                        # Save complete results too
                        result_file = os.path.join(app.config['UPLOAD_FOLDER'], 'complete_results.csv')
                        df.to_csv(result_file, index=False)
                        download_ready = True

                except Exception as e:
                    error = f"Error processing CSV: {str(e)}"
            else:
                error = "Please upload a valid CSV file"

    return render_template('index.html',
                         text_result=text_result,
                         text_input=text_input,
                         error=error,
                         positive_texts=positive_texts,
                         negative_texts=negative_texts,
                         neutral_texts=neutral_texts,
                         download_ready=download_ready)

@app.route('/download_complete')
def download_complete():
    result_file = os.path.join(app.config['UPLOAD_FOLDER'], 'complete_results.csv')
    if os.path.exists(result_file):
        return send_file(result_file, as_attachment=True, download_name='sentiment_analysis_complete.csv')
    else:
        flash('No complete results file available')
        return redirect(url_for('index'))

@app.route('/download_positive')
def download_positive():
    result_file = os.path.join(app.config['UPLOAD_FOLDER'], 'positive_results.csv')
    if os.path.exists(result_file):
        return send_file(result_file, as_attachment=True, download_name='positive_sentiments.csv')
    else:
        flash('No positive results file available')
        return redirect(url_for('index'))

@app.route('/download_negative')
def download_negative():
    result_file = os.path.join(app.config['UPLOAD_FOLDER'], 'negative_results.csv')
    if os.path.exists(result_file):
        return send_file(result_file, as_attachment=True, download_name='negative_sentiments.csv')
    else:
        flash('No negative results file available')
        return redirect(url_for('index'))

@app.route('/download_neutral')
def download_neutral():
    result_file = os.path.join(app.config['UPLOAD_FOLDER'], 'neutral_results.csv')
    if os.path.exists(result_file):
        return send_file(result_file, as_attachment=True, download_name='neutral_sentiments.csv')
    else:
        flash('No neutral results file available')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
