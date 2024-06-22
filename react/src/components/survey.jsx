// src/components/Survey.js
import React, { useState } from 'react';

const surveyData = {
  1: ["Qual a sua nota média?", "average"],
  2: ["Descreva sua experiência.", "text"],
  3: ["Qual sua escolha?", "multiple choice", {
    "a": "Opção 1",
    "b": "Opção 2",
    "c": "Opção 3",
    "d": "Opção 4"
  }]
};

const Survey = () => {
  const [responses, setResponses] = useState({});

  const handleInputChange = (id, value) => {
    setResponses({
      ...responses,
      [id]: value
    });
  };

  const renderQuestion = (id, question, type, choices = null) => {
    switch (type) {
      case 'average':
        return (
          <div key={id}>
            <label>{question}</label>
            <input
              type="number"
              step="0.1"
              value={responses[id] || ''}
              onChange={(e) => handleInputChange(id, e.target.value)}
            />
          </div>
        );
      case 'text':
        return (
          <div key={id}>
            <label>{question}</label>
            <textarea
              rows="5"
              cols="50"
              type="text"
              placeholder="Enter Text..."
              value={responses[id] || ''}
              onChange={(e) => handleInputChange(id, e.target.value)}
            />
          </div>
        );
      case 'multiple choice':
        return (
          <div key={id}>
            <label>{question}</label>
            {Object.entries(choices).map(([key, choice]) => (
              <div key={key}>
                <input
                  type="radio"
                  name={`question-${id}`}
                  value={key}
                  checked={responses[id] === key}
                  onChange={() => handleInputChange(id, key)}
                />
                {choice}
              </div>
            ))}
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <form>
      {Object.entries(surveyData).map(([id, [question, type, choices]]) =>
        renderQuestion(id, question, type, choices)
      )}
      <button type="button" onClick={() => console.log(responses)}>Submit</button>
    </form>
  );
};

export default Survey;
