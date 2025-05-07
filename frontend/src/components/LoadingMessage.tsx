import React, { useState, useEffect } from 'react';

type LoadingMessageProps = {
  messages?: string[];
  typingSpeed?: number;
  delayBetweenMessages?: number;
};

const defaultMessages = [
  "Finding latest articles...",
  "Analyzing sentiments and biases...",
  "Summarizing content...",
  "Good things take time...",
  "Almost ready..."
];

const LoadingMessage: React.FC<LoadingMessageProps> = ({
  messages = defaultMessages,
  typingSpeed = 50,
  delayBetweenMessages = 1000,
}) => {
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
  const [displayedText, setDisplayedText] = useState('');

  useEffect(() => {
    const currentMessage = messages[currentMessageIndex];

    // If not fully typed, keep typing
    if (displayedText.length < currentMessage.length) {
      const timeoutId = setTimeout(() => {
        setDisplayedText(currentMessage.substring(0, displayedText.length + 1));
      }, typingSpeed);
      return () => clearTimeout(timeoutId);
    } else {
      // After typing a message, wait then go to the next message
      const delayTimeout = setTimeout(() => {
        setDisplayedText('');
        setCurrentMessageIndex((prev) => (prev + 1) % messages.length);
      }, delayBetweenMessages);
      return () => clearTimeout(delayTimeout);
    }
  }, [displayedText, currentMessageIndex, messages, typingSpeed, delayBetweenMessages]);

  return (
    <div className="min-h-[24px] text-gray-600 font-medium">
      {displayedText}
      <span className="animate-pulse">|</span>
    </div>
  );
};

export default LoadingMessage;
