import React, { useState, useEffect } from 'react';

const Survey = () => {
  const [surveyData, setSurveyData] = useState(null);
  const [responses, setResponses] = useState({});

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch('http://localhost:5000/answer_form'); // Fetch data from Flask endpoint
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const jsonData = await response.json(); // Parse JSON response
      console.log('Response JSON data:', jsonData); // Log the JSON data
      setSurveyData(jsonData); // Set surveyData state with fetched JSON data
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

  const handleSubmit = () => {
    // Adjust submission logic based on your requirements
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
              placeholder="Enter Text..."
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
      <button type="button" onClick={handleSubmit}>Submit</button>
    </form>
  );
};

export default Survey;
