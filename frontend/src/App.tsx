import { useState } from 'react'
import './App.css'

function App() {
  const [code, setCode] = useState('')
  const [feedback, setFeedback] = useState('')

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://localhost:8081/api/review', {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain' },
        body: code
      })
      const data = await response.json()
      setFeedback(data.feedback)
    } catch (error) {
      console.error('Review error:', error)
      setFeedback('Error: Unable to get review.')
    }
  }

  return (
    <div style={{
      padding: '20px',
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#ffffff',
      minHeight: '100vh',
      color: '#333'
    }}>
      <h1 style={{
        textAlign: 'center',
        color: '#333',
        fontSize: '28px',
        marginBottom: '30px',
        fontWeight: '300'
      }}>
        AI Code Review Assistant
      </h1>
      <div style={{ maxWidth: '700px', margin: '0 auto' }}>
        <div style={{
          marginBottom: '20px',
          padding: '20px',
          border: '1px solid #e1e1e1',
          borderRadius: '8px',
          backgroundColor: '#f9f9f9'
        }}>
          <label style={{
            display: 'block',
            marginBottom: '10px',
            fontSize: '16px',
            fontWeight: 'bold'
          }}>
            Paste your code here:
          </label>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Enter your code..."
            rows={12}
            style={{
              width: '100%',
              padding: '12px',
              border: '1px solid #ccc',
              borderRadius: '4px',
              fontFamily: 'monospace',
              fontSize: '14px',
              resize: 'vertical',
              boxSizing: 'border-box'
            }}
          />
        </div>
        <div style={{ textAlign: 'center', marginBottom: '30px' }}>
          <button
            onClick={handleSubmit}
            style={{
              padding: '12px 24px',
              backgroundColor: '#007bff',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'background-color 0.3s'
            }}
            onMouseOver={(e) => (e.target as HTMLButtonElement).style.backgroundColor = '#0056b3'}
            onMouseOut={(e) => (e.target as HTMLButtonElement).style.backgroundColor = '#007bff'}
          >
            Review Code
          </button>
        </div>
        {feedback && (
          <div style={{
            padding: '20px',
            border: '1px solid #e1e1e1',
            borderRadius: '8px',
            backgroundColor: '#f9f9f9',
            whiteSpace: 'pre-wrap',
            fontSize: '14px',
            lineHeight: '1.5'
          }}>
            <h3 style={{ marginTop: 0, color: '#333' }}>AI Feedback:</h3>
            {feedback}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
