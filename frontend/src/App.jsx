import { useState } from 'react'
import './App.css'

function App() {
  const [loading, setLoading] = useState(false);

  const triggerCalendarEvent = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/create-test-event', {
        method: 'POST',
      });
      const data = await response.json();
      alert("Event Created! Check your Google Calendar.");
      console.log(data);
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Google Calendar Integration</h1>
      <button 
        onClick={triggerCalendarEvent} 
        disabled={loading}
        style={{ padding: '10px 20px', cursor: 'pointer' }}
      >
        {loading ? 'Processing...' : 'Click to Create Event'}
      </button>
    </div>
  );
}

export default App;