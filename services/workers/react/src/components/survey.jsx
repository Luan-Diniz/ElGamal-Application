// src/components/Survey.js
import React, { useState } from 'react';

const surveyData = {
  "Questão 1": [1, "average"],
  "Questão 2": [2, "text"],
  "Questão 3": [3, "multiple choice",
    {
      "a": ["Escolha 1", 3],
      "b": ["Escolha 2", 5],
      "c": ["Escolha 3", 7],
      "d": ["Escolha 4", 11]
    }
  ]
};

const Survey = () => {
  const [responses, setResponses] = useState({});

  const handleInputChange = (questionKey, value) => {
    setResponses({
      ...responses,
      [questionKey]: value
    });
  };

  const renderQuestion = (questionKey, [id, type, choices = null]) => {
    switch (type) {
      case 'average':
        return (
          <div key={id}>
            <label>{questionKey}</label>
            <input
              type="number"
              step="0.1"
              value={responses[questionKey] || ''}
              onChange={(e) => handleInputChange(questionKey, e.target.value)}
            />
          </div>
        );
      case 'text':
        return (
          <div key={id}>
            <label>{questionKey}</label>
            <textarea
              rows="5"
              cols="50"
              type="text"
              placeholder="Enter Text..."
              value={responses[questionKey] || ''}
              onChange={(e) => handleInputChange(questionKey, e.target.value)}
            />
          </div>
        );
      case 'multiple choice':
        return (
          <div key={id}>
            <label>{questionKey}</label>
            {Object.entries(choices).map(([key, [choiceText, choiceValue]]) => (
              <div key={key}>
                <input
                  type="radio"
                  name={`question-${id}`}
                  value={choiceValue}
                  checked={responses[questionKey] === choiceValue}
                  onChange={() => handleInputChange(questionKey, choiceValue)}
                />
                {choiceText}
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
      {Object.entries(surveyData).map(([questionKey, questionData]) =>
        renderQuestion(questionKey, questionData)
      )}
      <button type="button" onClick={() => console.log(responses)}>Submit</button>
    </form>
  );
};

export default Survey;
