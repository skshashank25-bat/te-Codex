import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { marked } from 'marked';
import './styles.css';

const workflows = [
  { value: '', label: 'Auto-detect' },
  { value: 'api_endpoint', label: 'API Endpoint Finder' },
  { value: 'api_error', label: 'API Error Troubleshooter' },
  { value: 'python_script', label: 'Python Script Debugger' },
  { value: 'transaction_script', label: 'Transaction JS/Selenium Helper' },
];

function App() {
  const [input, setInput] = useState('');
  const [workflow, setWorkflow] = useState('');
  const [answer, setAnswer] = useState('');
  const [detected, setDetected] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function submit() {
    setLoading(true);
    setError('');
    setAnswer('');
    try {
      const res = await fetch('http://localhost:8000/agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_input: input,
          workflow: workflow || null,
        }),
      });
      if (!res.ok) throw new Error(`Backend returned ${res.status}`);
      const data = await res.json();
      setDetected(data.workflow);
      setAnswer(data.answer_markdown);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>ThousandEyes AI Support Agent</h1>
      <p className="subtitle">API v7 endpoint finder, API error troubleshooter, Python reviewer, and Transaction JS/Selenium helper.</p>

      <label>Workflow</label>
      <select value={workflow} onChange={e => setWorkflow(e.target.value)}>
        {workflows.map(w => <option key={w.value} value={w.value}>{w.label}</option>)}
      </select>

      <label>Customer ask / error / script</label>
      <textarea
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Paste customer API ask, HTTP error, Python script, or ThousandEyes Transaction script..."
      />

      <button onClick={submit} disabled={loading || input.length < 3}>{loading ? 'Analyzing...' : 'Analyze'}</button>

      {error && <div className="error">{error}</div>}
      {detected && <div className="detected">Detected workflow: <strong>{detected}</strong></div>}
      {answer && <section className="answer" dangerouslySetInnerHTML={{ __html: marked(answer) }} />}
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);
