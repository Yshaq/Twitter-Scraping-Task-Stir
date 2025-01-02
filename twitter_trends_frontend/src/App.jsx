import { useState } from 'react'
import './App.css'


function App() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const fetchData = async () => {
    setLoading(true); // Show "Loading" message
    setData(null); // Clear previous data

    try {
      const response = await fetch("http://localhost:5000");
      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }
      const jsonData = await response.json();
      setData(jsonData); // Store data to display
    } catch (error) {
      setData({ error: error.message });
    } finally {
      setLoading(false); // Hide "Loading" message
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      {
        !loading ?
        <button onClick={fetchData} style={{ padding: "10px 20px", fontSize: "16px" }}>
          Fetch Data
        </button>
        :
        <button style={{ padding: "10px 20px", fontSize: "16px" }} disabled>
          Fetch Data
        </button>

      }

      {loading && <p style={{ marginTop: "20px" }}>Loading...<br/> This typically takes upto 20 seconds.</p>}

      {data && (
        <div>
          <p style={{ marginTop: "50px" }}>These are the most happening topics as on {data['timestamp']}</p>
          <div>
          <ul>
            <li>{data['nameoftrend1']}</li>
            <li>{data['nameoftrend2']}</li>
            <li>{data['nameoftrend3']}</li>
            <li>{data['nameoftrend4']}</li>
            <li>{data['nameoftrend5']}</li>
          </ul>
          </div>
          <p>The IP Address used for this query was {data['ip']}</p>

          <p>Here's a JSON extract of this record from MongoDB:</p>
        <pre
          style={{
            marginTop: "20px",
            padding: "10px",
            backgroundColor: "#f0f0f0",
            textAlign: "left",
          }}
        >
          {JSON.stringify(data, null, 2)}
        </pre>
        </div>
      )}
    </div>
  );
}

export default App;

