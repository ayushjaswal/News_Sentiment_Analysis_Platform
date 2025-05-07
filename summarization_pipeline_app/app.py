from flask import Flask, request, jsonify
from summarization_pipeline_app.data_summarization import DataSummarization
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

summarization_pipeline = DataSummarization()

@app.route("/predict", methods=['POSt'])
def mine():
    data = request.get_json()
    article = data.get("article", "")
    summary = summarization_pipeline.summarize(article=article)
    return jsonify(summary)

if __name__ == "__main__":
    app.run(debug=True, port=8081)