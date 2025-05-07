## How to run this repo

- You would be required to create two different python environment, one for summarization pipeline and one for the main app
- This is done to avoid the dependency issue at the moment untill the keras 3 support is available for transformers which is being utilized in the summarization pipeline
- Download the models from [here](https://drive.google.com/drive/folders/1b7I5FNh5_Wa1AwV_4d4aJEcYtDxQweKt?usp=sharing) Extract the models in the models folder inside `News_Sentiment_Analysis` folder
- Activate and run the corrosponding applications in their enviroments using `python app.py` command
- Install frontend dependencies using `pnpm install` or any other dependency manager of your choice
- Start frontend using `pnpm run dev` or `<yourmanager> run dev`
- Use the app

## Important Points and Justifications

- GloVe embeddings (e.g., `glove.6B.100d.txt`) are not provided to reduce repository size. Please download them from GloVe and place them appropriately. You can download the embeddings from the following link: [Download GloVe Embeddings](https://nlp.stanford.edu/projects/glove/)

- Models are compressed and then provided separately to decrease the repo size as git wasn't allowing big sized files to be pushed.
- Data used while training is not provided however sources are listed in this readme


## Sources for data

- Political Bias: Dataset by Mayoban Saxena [Download Here](https://www.kaggle.com/datasets/mayobanexsantana/political-bias)
- Framing Bias: Dataset by Shivam Ralli [Download Here](https://www.kaggle.com/datasets/hoshi7/news-sentiment-dataset?resource=download) and Dataset by Ankur Sinha [Download Here](https://www.kaggle.com/datasets/ankurzing/sentiment-analysis-for-financial-news)
- Sensationalism and Opinionism (fake news): Dataset by Sadman Sakib Mahi [Download Here](https://www.kaggle.com/datasets/sadmansakibmahi/fake-news-detection-dataset-with-pre-trained-model) 