from transformers import pipeline
from dotenv import load_dotenv
import os

os.environ["TF_USE_LEGACY_KERAS"] = "1"

load_dotenv()  # Load environment variables from .env file if you need to access keys

class DataSummarization:
    def __init__(self):
        self.current_calls = 0
        self.remember_summaries = []
        # Using Hugging Face's pre-trained model for summarization
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize(self, article):
        # Summarize the article using BART
        summary = self.summarizer(article, max_length=100, min_length=60, do_sample=False)[0]['summary_text']
        
        # Increment call count and store summary
        self.current_calls += 1
        print(f"CURRENT CALLS: {self.current_calls}")
        
        # Append the summary to remember history
        self.remember_summaries.append({
            'index': self.current_calls,
            'article': article,
            'summary': summary
        })
        
        return summary
    
    def print_history(self):
        for i in self.remember_summaries:
            print(f"Summary {i['index']}")
            print("="*20, end="\n")
            print(i['summary'])
            print("\n")
    

if __name__ == "__main__":
    ds = DataSummarization()
    article = """This past week, travellers in Rome may have spotted cardinals frequenting their favourite restaurants. Just before the last papal election in 2013, Italian media reported that many of these men were making the time to visit a particular neighbourhood favourite, Al Passetto di Borgo, a family-run eatery located 200m from Saint Peter's Basilica, where Cardinal Donald William Wuerl is known to order the lasagna and Francesco Coccopalmerio (allegedly the most-voted Italian cardinal in 2013) likes the grilled squid. Cardinals may feel some urgency to get in a good meal or two because, during the conclave beginning on 7 May, in which 135 cardinals will hold a secret election for a new pope in the Vatican's Sistine Chapel, they'll be entirely secluded from the rest of the world for an indefinite period of time. Voting, sleeping and eating all take place in tightly controlled sequestration."""

    # Summarize the article
    response = ds.summarize(article)
    
    # Output the summary
    print("SUMMARY:")
    print(response)

    # Print summary history
    ds.print_history()
