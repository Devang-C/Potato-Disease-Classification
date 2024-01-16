from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_ENDPOINT = "http://localhost:8040/predict"  # Update with your API endpoint

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was submitted with the form
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        # Check if the file has a name
        if file.filename == '':
            return render_template('index.html', error='No selected file')

        # Make a request to your FastAPI endpoint
        files = {'file': (file.filename, file.read())}
        response = requests.post(API_ENDPOINT, files=files)

        # Parse the response
        result = response.json()

        return render_template('index.html', result=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,port=5050)
