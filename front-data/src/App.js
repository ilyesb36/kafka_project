import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://localhost:3001/data');
      const jsonData = await response.json();
      setData(jsonData);
    };

    const intervalId = setInterval(fetchData, 5000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h2>Données Kafka</h2>
        {data.map((item, index) => (
          <div key={index}>
            <p>{item.value}</p>
          </div>
        ))}
      </header>
    </div>
  );
}

export default App;