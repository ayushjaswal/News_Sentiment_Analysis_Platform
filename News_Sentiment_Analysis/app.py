from flask import Flask, request, jsonify
from News_Sentiment_Analysis.components.prediction_pipeline import PredictionPipeline
from News_Sentiment_Analysis.components.data_fetching_pipeline import NewsScraper
from flask_cors import CORS
import numpy as np
import os
import requests
os.environ["KERAS_BACKEND"] = "tensorflow"

app = Flask(__name__)
CORS(app)

prediction_pipeline = PredictionPipeline()
mining_pipeline = NewsScraper()

# @app.route("/summarize", methods=["POST"])
# def summarize():
#     """Summarize the given article."""
#     data = request.get_json()
#     article = data.get("article", "")
    
#     if not article:
#         return jsonify({"error": "No article provided"}), 400
    
#     summary = prediction_pipeline.summarize(article)
    
#     return jsonify({"summary": summary})

@app.route("/mine-article/<topic>", methods=['GET'])
def mine(topic):
    if not topic:
        return jsonify({"error": "No topic provided"})
    
    articles_data = mining_pipeline.scrape_site(topic)
    articles = articles_data['article'].tolist()  # Convert Series to list
    
    predictions = []
    summaries = []
    for article in articles:
        prediction = prediction_pipeline.predict(article)
        # Convert any non-serializable types to their serializable form
        if isinstance(prediction, np.ndarray):
            prediction = prediction.tolist()
        elif hasattr(prediction, 'to_dict'):
            prediction = prediction.to_dict()
        
        predictions.append(prediction)
        
        summary = requests.post("http://localhost:8081/predict", json={"article": article})
        summaries.append(summary.json())
    
    return jsonify({
        "articles": articles,
        "predictions": predictions,
        "summaries": summaries
    })

@app.route("/predict", methods=["POST"])
def predict():
    """Predict political bias for a given article."""
    data = request.get_json()
    article = data.get("article", "")
    
    if not article:
        return jsonify({"error": "No article provided"}), 400
    
    predictions = prediction_pipeline.predict(article)
    
    # Handle potential non-serializable objects
    if isinstance(predictions, np.ndarray):
        predictions = predictions.tolist()
    elif hasattr(predictions, 'to_dict'):
        predictions = predictions.to_dict()
    
    return jsonify(predictions)

if __name__ == "__main__":
    app.run(debug=True, port=8080)