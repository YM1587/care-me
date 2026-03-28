import React, { useState } from 'react';
import { Activity, HeartPulse, Thermometer, Wind, User, AlertCircle, Phone, Stethoscope, Droplets, ArrowRight } from 'lucide-react';
import './App.css';

const DEFAULT_STATE = {
  age: 45,
  sex: "Female",
  arrival_mode: 1, // 1=Walk-in, 3=Ambulance
  injury: 1, // 1=No, 2=Yes
  chief_complain: "chest pain",
  mental_state: 1, // 1=Alert, 4=Unresponsive
  pain: 1, // 0=No, 1=Yes
  nrs_pain: 7, // 0-10
  sbp: 140,
  dbp: 90,
  hr: 88,
  rr: 18,
  temp: 37.1,
  spo2: 98
};

function App() {
  const [formData, setFormData] = useState(DEFAULT_STATE);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    let parsedValue = value;
    
    if (type === 'number') {
      parsedValue = parseFloat(value) || 0;
    } else if (name === 'injury' || name === 'pain' || name === 'arrival_mode' || name === 'mental_state') {
      parsedValue = parseInt(value, 10);
    }
    
    setFormData(prev => ({
      ...prev,
      [name]: parsedValue
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to connect to triage AI server');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getUrgencyColor = (recommendation) => {
    switch(recommendation) {
      case 'Emergency': return 'emergency';
      case 'Urgent': return 'urgent';
      case 'Non-Urgent': return 'non-urgent';
      default: return 'neutral';
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-brand">
          <HeartPulse size={32} className="brand-icon" />
          <h1>CareMe Triage Assistant</h1>
        </div>
        <div className="header-status">
          <span className="status-dot"></span> AI Active
        </div>
      </header>

      <main className="dashboard">
        <section className="input-panel glass-panel">
          <h2><User size={20}/> Patient Information</h2>
          <form onSubmit={handleSubmit} className="triage-form">
            
            <div className="form-group-row">
              <div className="input-group">
                <label>Age</label>
                <input type="number" name="age" value={formData.age} onChange={handleInputChange} min="0" max="120" required />
              </div>
              <div className="input-group">
                <label>Sex</label>
                <select name="sex" value={formData.sex} onChange={handleInputChange}>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                </select>
              </div>
            </div>

            <div className="form-group-row">
              <div className="input-group">
                <label>Chief Complaint</label>
                <input type="text" name="chief_complain" value={formData.chief_complain} onChange={handleInputChange} required />
              </div>
            </div>

            <div className="form-group-row">
              <div className="input-group">
                <label>Arrival Mode</label>
                <select name="arrival_mode" value={formData.arrival_mode} onChange={handleInputChange}>
                  <option value={1}>Walk-in</option>
                  <option value={2}>Car</option>
                  <option value={3}>Ambulance</option>
                  <option value={7}>Other</option>
                </select>
              </div>
              <div className="input-group">
                <label>Mental State</label>
                <select name="mental_state" value={formData.mental_state} onChange={handleInputChange}>
                  <option value={1}>Alert (Normal)</option>
                  <option value={2}>Verbal Response</option>
                  <option value={3}>Pain Response</option>
                  <option value={4}>Unresponsive</option>
                </select>
              </div>
            </div>

            <div className="form-group-row">
              <div className="input-group">
                <label>Injury / Trauma</label>
                <select name="injury" value={formData.injury} onChange={handleInputChange}>
                  <option value={1}>No</option>
                  <option value={2}>Yes</option>
                </select>
              </div>
              <div className="input-group">
                <label>Pain Scope</label>
                <div className="pain-inputs">
                  <select name="pain" value={formData.pain} onChange={handleInputChange}>
                    <option value={0}>No Pain</option>
                    <option value={1}>Pain Present</option>
                  </select>
                  {formData.pain === 1 && (
                    <input type="number" name="nrs_pain" title="Pain Scale (0-10)" placeholder="0-10" value={formData.nrs_pain} onChange={handleInputChange} min="0" max="10" />
                  )}
                </div>
              </div>
            </div>

            <div className="vitals-section">
              <h3><Activity size={18}/> Vitals</h3>
              <div className="vitals-grid">
                <div className="input-group vital-group">
                  <label><HeartPulse size={14}/> SBP</label>
                  <input type="number" name="sbp" value={formData.sbp} onChange={handleInputChange} />
                </div>
                <div className="input-group vital-group">
                  <label><HeartPulse size={14} className="faded"/> DBP</label>
                  <input type="number" name="dbp" value={formData.dbp} onChange={handleInputChange} />
                </div>
                <div className="input-group vital-group">
                  <label><Activity size={14}/> Heart Rate</label>
                  <input type="number" name="hr" value={formData.hr} onChange={handleInputChange} />
                </div>
                <div className="input-group vital-group">
                  <label><Wind size={14}/> Resp Rate</label>
                  <input type="number" name="rr" value={formData.rr} onChange={handleInputChange} />
                </div>
                <div className="input-group vital-group">
                  <label><Thermometer size={14}/> Temp (°C)</label>
                  <input type="number" name="temp" value={formData.temp} onChange={handleInputChange} step="0.1" />
                </div>
                <div className="input-group vital-group">
                  <label><Droplets size={14}/> SpO2 (%)</label>
                  <input type="number" name="spo2" value={formData.spo2} onChange={handleInputChange} />
                </div>
              </div>
            </div>

            <button type="submit" disabled={loading} className="analyze-btn">
              {loading ? <span className="loader"></span> : <span><Stethoscope size={18}/> Run AI Assessment</span>}
            </button>
          </form>
        </section>

        <section className={`result-panel glass-panel ${result ? getUrgencyColor(result.final_recommendation) : ''}`}>
          {error && (
            <div className="error-box">
              <AlertCircle size={24}/>
              <p>{error}</p>
            </div>
          )}

          {!result && !error && !loading && (
            <div className="empty-state">
              <HeartPulse size={48} className="empty-icon" />
              <h3>Awaiting Patient Data</h3>
              <p>Fill out the assessment form and run the AI algorithm to generate a triage recommendation.</p>
            </div>
          )}

          {loading && (
            <div className="empty-state">
              <span className="large-loader"></span>
              <h3>Consulting CareMe AI...</h3>
            </div>
          )}

          {result && (
            <div className="results-content animate-pop">
              <h2>Recommendation</h2>
              <div className={`recommendation-badge ${getUrgencyColor(result.final_recommendation)}`}>
                {result.final_recommendation}
              </div>
              
              <div className="metrics-row">
                <div className="metric-box">
                  <span>AI Confidence</span>
                  <strong>{(result.confidence_score * 100).toFixed(1)}%</strong>
                </div>
                <div className="metric-box model-raw">
                  <span>Raw Model Class</span>
                  <strong>{result.original_ml_prediction}</strong>
                </div>
              </div>

              {result.alerts && result.alerts.length > 0 && (
                <div className="alerts-container">
                  <h4><AlertCircle size={16}/> Clinical Overrides & Alerts</h4>
                  <ul>
                    {result.alerts.map((alert, idx) => (
                      <li key={idx} className={alert.includes('CRITICAL') ? 'critical-alert' : 'warning-alert'}>
                        {alert}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="probabilities">
                <h4>Probability Breakdown</h4>
                <div className="prob-bar-container">
                  <div className="prob-label">Emergency</div>
                  <div className="prob-track">
                    <div className="prob-fill emergency" style={{width: `${result.probabilities["Emergency"] * 100}%`}}></div>
                  </div>
                  <div className="prob-pct">{(result.probabilities["Emergency"] * 100).toFixed(1)}%</div>
                </div>
                <div className="prob-bar-container">
                  <div className="prob-label">Urgent</div>
                  <div className="prob-track">
                    <div className="prob-fill urgent" style={{width: `${result.probabilities["Urgent"] * 100}%`}}></div>
                  </div>
                  <div className="prob-pct">{(result.probabilities["Urgent"] * 100).toFixed(1)}%</div>
                </div>
                <div className="prob-bar-container">
                  <div className="prob-label">Non-Urgent</div>
                  <div className="prob-track">
                    <div className="prob-fill non-urgent" style={{width: `${result.probabilities["Non-Urgent"] * 100}%`}}></div>
                  </div>
                  <div className="prob-pct">{(result.probabilities["Non-Urgent"] * 100).toFixed(1)}%</div>
                </div>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
