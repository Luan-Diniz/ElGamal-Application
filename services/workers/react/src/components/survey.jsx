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

  const handleSubmit = () => {
    const formattedResponses = {};
    Object.entries(surveyData).forEach(([questionKey, [id]]) => {
      formattedResponses[`${id}`] = responses[questionKey];
    });

    const jsonContent = JSON.stringify(formattedResponses, null, 2);

    // Create a blob and trigger a download
    const blob = new Blob([jsonContent], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'responses.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  const renderQuestion = (questionKey, [id, type, choices = null]) => {
    switch (type) {
      case 'average':
        return (
          <div key={id}>
            <h3>{questionKey}</h3>
            <input
              type="number"
              step="0.1"
              placeholder="Digite o valor..."
              value={responses[questionKey] || ''}
              onChange={(e) => handleInputChange(questionKey, e.target.value)}
            />
          </div>
        );
      case 'text':
        return (
          <div key={id}>
            <h3>{questionKey}</h3>
            <textarea
              rows="5"
              cols="50"
              type="text"
              placeholder="Digite o texto..."
              value={responses[questionKey] || ''}
              onChange={(e) => handleInputChange(questionKey, e.target.value)}
            />
          </div>
        );
      case 'multiple choice':
        return (
          <div key={id}>
            <h3>{questionKey}</h3>
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
      <h3></h3>
      <button type="button" onClick={handleSubmit}>Submit</button>
    </form>
  );
};

export default Survey;
