import React, { useEffect, useState } from "react";
import axios from "axios";
import { Loader } from "lucide-react";
import LoadingMessage from "./LoadingMessage";
import NewsCard from "./NewsCard";
import { NewsData } from "../types";
import { config, path } from "../path";

const LatestNews: React.FC = () => {
  const [news, setNews] = useState<NewsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const topic = "bbc_news"; // You can make this dynamic later

  useEffect(() => {
    const fetchNews = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        const res = await axios.get(`${path}/mine-article/${topic}`, config);
        setNews(res.data);
      } catch (error) {
        console.error("Error fetching news:", error);
        setError("Failed to load news. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchNews();
  }, [topic]);

  return (
    <div className="py-12 px-4 max-w-5xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">
          Latest World News
        </h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Get the latest news with advanced sentiment and bias analysis
        </p>
      </div>

      {isLoading ? (
        <div className="flex flex-col items-center justify-center py-20 space-y-6">
          <div className="relative">
            <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-gray-900"></div>
            <Loader className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-gray-700" size={24} />
          </div>
          
          <div className="text-center">
            <LoadingMessage />
          </div>
        </div>
      ) : error ? (
        <div className="bg-red-50 border border-red-200 text-red-600 rounded-lg p-6 text-center">
          <p className="font-medium">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition"
          >
            Try Again
          </button>
        </div>
      ) : news ? (
        <div className="space-y-6">
          {news.summaries.map((summary, idx) => (
            <NewsCard 
              key={idx}
              summary={summary}
              prediction={news.predictions[idx]}
              index={idx}
            />
          ))}
        </div>
      ) : (
        <div className="text-center text-gray-600">No news articles found.</div>
      )}
    </div>
  );
};

export default LatestNews;