import React, { useState, useEffect } from 'react';

const Survey = () => {
  const [surveyData, setSurveyData] = useState(null);
  const [responses, setResponses] = useState({});

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch('http://localhost:5000/answer_form');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const jsonData = await response.json();
      setSurveyData(jsonData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleInputChange = (questionKey, value) => {
    setResponses({
      ...responses,
      [questionKey]: value
    });
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://localhost:5000/answer_form', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(responses),
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const responseData = await response.json();
      console.log('Response from backend:', responseData);
      alert('Responses submitted successfully!');
    } catch (error) {
      console.error('Error submitting responses:', error);
      alert('Error submitting responses');
    }
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

  if (!surveyData) {
    return <p>Loading...</p>;
  }

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
