import React from 'react';
import { Sparkles } from 'lucide-react';
import { ExpectedData } from '../types';

type NewsCardProps = {
  summary: string;
  prediction: ExpectedData;
  index: number;
};

const getSentimentColor = (sentiment: string, type: string) => {
  if (type === 'political') {
    if (sentiment.toLowerCase().includes('left')) return 'text-blue-600 bg-blue-50';
    if (sentiment.toLowerCase().includes('center')) return 'text-purple-600 bg-purple-50';
    if (sentiment.toLowerCase().includes('right')) return 'text-red-600 bg-red-50';
  }
  
  if (type === 'framing') {
    if (sentiment.toLowerCase().includes('negative')) return 'text-red-600 bg-red-50';
    if (sentiment.toLowerCase().includes('neutral')) return 'text-amber-600 bg-amber-50';
    if (sentiment.toLowerCase().includes('positive')) return 'text-green-600 bg-green-50';
  }
  
  if (type === 'sensational') {
    if (sentiment.toLowerCase().includes('low')) return 'text-green-600 bg-green-50';
    if (sentiment.toLowerCase().includes('high')) return 'text-red-600 bg-red-50';
  }
  
  return 'text-gray-600 bg-gray-50';
};

const NewsCard: React.FC<NewsCardProps> = ({ summary, prediction, index }) => {
  return (
    <div 
      className="flex flex-col md:flex-row gap-6 p-6 border border-gray-100 rounded-xl shadow-sm bg-white backdrop-blur transition-all duration-500 hover:shadow-md"
      style={{
        opacity: 0,
        animation: `fadeIn 0.5s ease-out ${0.1 + index * 0.15}s forwards`,
        transform: 'translateY(20px)',
      }}
    >
      <div className="md:w-1/2">
        <div className="flex items-center gap-2 mb-3">
          <Sparkles size={18} className="text-amber-500" />
          <h3 className="text-lg font-semibold text-gray-800">News Summary</h3>
        </div>
        <p className="text-gray-600 leading-relaxed">{summary}</p>
      </div>
      
      <div className="md:w-1/2">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">Sentiment Analysis</h3>
        
        <div className="space-y-3">
          <div className="space-y-1">
            <p className="text-sm text-gray-500">Political Bias</p>
            <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(prediction.pol_model, 'political')}`}>
              {prediction.pol_model}
            </div>
          </div>
          
          <div className="space-y-1">
            <p className="text-sm text-gray-500">Framing Bias</p>
            <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(prediction.frame_model, 'framing')}`}>
              {prediction.frame_model}
            </div>
          </div>
          
          <div className="space-y-1">
            <p className="text-sm text-gray-500">Sensationalism Level</p>
            <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(prediction.sens_and_opin, 'sensational')}`}>
              {prediction.sens_and_opin}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NewsCard;