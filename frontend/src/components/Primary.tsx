import React, { useState } from "react";
import { Send, Sparkles, ArrowRight } from "lucide-react";
import axios from "axios";
import { config, path } from "../path";
import { useNavigate } from "react-router-dom";
import { ExpectedData } from "../types";

const SentimentBar = ({ value, options }: {
    value: string,
    options: { value: string; label: string; color: string; textColor: string }[]
}) => {
    const activeIndex = options.findIndex(opt => opt.value === value);
    
    return (
        <div className="relative flex items-center justify-between w-full mt-3">
            <div className="absolute w-full h-[1px] bg-gray-200/50"></div>
            <div className="relative flex justify-between w-full">
                {options.map((option, idx) => (
                    <div
                        key={idx}
                        className={`flex flex-col items-center transition-all duration-300 ease-in-out
                            ${idx === activeIndex ? 'scale-110 transform' : 'opacity-60'}`}
                    >
                        <div
                            className={`w-3 h-3 rounded-full transition-all duration-300 
                                ${idx === activeIndex
                                    ? `${option.color} shadow-lg shadow-${option.color}/20`
                                    : 'bg-gray-200'
                                }`}
                        />
                        <span className={`text-xs mt-2 font-medium transition-all duration-300
                            ${idx === activeIndex ? option.textColor : 'text-gray-400'}`}>
                            {option.label}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
};

const Primary = () => {
    const [data, setData] = useState<ExpectedData>();
    const [article, setArticle] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const response = await axios.post(`${path}/predict`, { article }, config);
            const result = await response.data;
            setData(result);
        } catch (error) {
            console.error("Error analyzing article:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const sentimentConfigs = {
        political: [
            { value: "left", label: "Left", color: "bg-blue-500", textColor: "text-blue-500" },
            { value: "center", label: "Center", color: "bg-purple-500", textColor: "text-purple-500" },
            { value: "right", label: "Right", color: "bg-red-500", textColor: "text-red-500" }
        ],
        framing: [
            { value: "negative", label: "Negative", color: "bg-red-500", textColor: "text-red-500" },
            { value: "neutral", label: "Neutral", color: "bg-yellow-500", textColor: "text-yellow-600" },
            { value: "positive", label: "Positive", color: "bg-green-500", textColor: "text-green-500" }
        ],
        sensational: [
            { value: "low", label: "Low", color: "bg-green-500", textColor: "text-green-500" },
            { value: "high", label: "High", color: "bg-red-500", textColor: "text-red-500" }
        ]
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex flex-col items-center justify-center p-6">
            <div className="w-full max-w-2xl space-y-6">
                {/* Header */}
                <div className="text-center space-y-4">
                    <h1 className="text-4xl font-bold text-gray-800">
                        News Sentiment Analysis
                    </h1>
                    <button 
                        onClick={() => navigate("/latest-news")}
                        className="inline-flex items-center cursor-pointer gap-2 px-4 py-2 text-sm font-medium text-amber-700 bg-amber-50 rounded-full hover:bg-amber-100 transition-all duration-300 group"
                    >
                        Get Latest News
                        <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
                    </button>
                </div>

                {/* Input Form */}
                <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-lg border border-white/50 p-6">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <textarea
                            className="w-full h-40 px-4 py-3 rounded-xl bg-white/50 border border-gray-100 outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-300 resize-none placeholder:text-gray-400"
                            placeholder="Paste your article here for analysis..."
                            value={article}
                            onChange={(e) => setArticle(e.target.value)}
                        />
                        <button
                            type="submit"
                            disabled={isLoading || !article.trim()}
                            className={`w-full flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-medium transition-all duration-300
                                ${isLoading || !article.trim()
                                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                    : 'bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:shadow-lg hover:shadow-blue-500/20 hover:-translate-y-0.5'
                                }`}
                        >
                            {isLoading ? (
                                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
                            ) : (
                                <>
                                    <Send className="w-4 h-4" />
                                    Analyze
                                </>
                            )}
                        </button>
                    </form>
                </div>

                {/* Results */}
                {data && (
                    <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-lg border border-white/50 p-6 animate-fade-in">
                        <div className="flex items-center gap-2 mb-6">
                            <Sparkles className="w-5 h-5 text-amber-500" />
                            <h2 className="text-xl font-semibold text-gray-800">Analysis Results</h2>
                        </div>
                        <div className="space-y-8">
                            <div className="space-y-2">
                                <h3 className="text-sm font-medium text-gray-600">Political Bias</h3>
                                <SentimentBar value={data.pol_model} options={sentimentConfigs.political} />
                            </div>

                            <div className="space-y-2">
                                <h3 className="text-sm font-medium text-gray-600">Framing</h3>
                                <SentimentBar value={data.frame_model} options={sentimentConfigs.framing} />
                            </div>

                            <div className="space-y-2">
                                <h3 className="text-sm font-medium text-gray-600">Sensationalism Level</h3>
                                <SentimentBar value={data.sens_and_opin} options={sentimentConfigs.sensational} />
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Primary;