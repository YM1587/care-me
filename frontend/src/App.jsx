import React, { useState } from 'react';
import { Activity, HeartPulse, Thermometer, Wind, User, AlertCircle, Stethoscope, Droplets, ShieldAlert, Clock } from 'lucide-react';
import './App.css';

const DEFAULT_STATE = {
  age: null,
  age_group: 1, // Default to 19-40
  sex: "Female",
  arrival_mode: 1,
  injury: 1,
  mental_state: 1,
  pain: 1,
  nrs_pain: 7,
  sbp: 140,
  dbp: 90,
  hr: 88,
  rr: 18,
  temp: 37.1,
  spo2: 98
};

function App() {
  const [formData, setFormData] = useState(DEFAULT_STATE);
  const [ageType, setAgeType] = useState('range'); // 'exact' or 'range'
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    let parsedValue = value;
    
    if (type === 'number') {
      parsedValue = value === '' ? null : parseFloat(value);
    } else if (['injury', 'pain', 'arrival_mode', 'mental_state', 'age_group'].includes(name)) {
      parsedValue = value === '' ? null : parseInt(value, 10);
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

    // Prepare data (clear exact age if using range, or vice versa if we had exact)
    const submissionData = { ...formData };
    if (ageType === 'range') {
      submissionData.age = null;
    } else {
      submissionData.age_group = null;
    }

    try {
      const response = await fetch('http://localhost:8000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(submissionData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Failed to connect to triage AI server' }));
        throw new Error(errorData.detail || 'Server error');
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
      case 'Critical': return 'emergency';
      case 'Non-critical': return 'non-urgent';
      default: return 'neutral';
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-brand">
          <HeartPulse size={32} className="brand-icon" />
          <h1>CareMe Triage Assistant <span className="v2-badge">v2.1</span></h1>
        </div>
        <div className="header-status">
          <span className="status-dot"></span> AI Engines Active
        </div>
      </header>

      <main className="dashboard">
        <section className="input-panel glass-panel">
          <h2><User size={20}/> Patient Triage Form</h2>
          <form onSubmit={handleSubmit} className="triage-form">
            
            <div className="form-group-row">
              <div className="input-group">
                <label>Age Input Type</label>
                <div className="age-toggle">
                  <button type="button" className={ageType === 'range' ? 'active' : ''} onClick={() => setAgeType('range')}>Range</button>
                  <button type="button" className={ageType === 'exact' ? 'active' : ''} onClick={() => setAgeType('exact')}>Exact</button>
                </div>
              </div>
            </div>

            <div className="form-group-row">
              <div className="input-group">
                <label>{ageType === 'exact' ? 'Exact Age' : 'Estimated Age Range'}</label>
                {ageType === 'exact' ? (
                  <input type="number" name="age" value={formData.age ?? ''} onChange={handleInputChange} min="0" max="120" placeholder="Years" required />
                ) : (
                  <select name="age_group" value={formData.age_group ?? ''} onChange={handleInputChange} required>
                    <option value={0}>Pediatric (0-18)</option>
                    <option value={1}>Young Adult (19-40)</option>
                    <option value={2}>Middle Aged (41-65)</option>
                    <option value={3}>Senior (66+)</option>
                  </select>
                )}
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
                <label>Pain Context</label>
                <div className="pain-inputs">
                  <select name="pain" value={formData.pain} onChange={handleInputChange}>
                    <option value={0}>No Pain</option>
                    <option value={1}>Pain Present</option>
                  </select>
                  {formData.pain === 1 && (
                    <input type="number" name="nrs_pain" title="NRS Pain Scale (0-10)" placeholder="0-10" value={formData.nrs_pain ?? ''} onChange={handleInputChange} min="0" max="10" />
                  )}
                </div>
              </div>
            </div>

            <div className="vitals-section">
              <h3><Activity size={18}/> Vitals Assessment</h3>
              <div className="vitals-grid">
                <div className="input-group vital-group">
                  <label><HeartPulse size={14}/> SBP</label>
                  <input type="number" name="sbp" value={formData.sbp ?? ''} onChange={handleInputChange} required />
                </div>
                <div className="input-group vital-group">
                  <label><HeartPulse size={14} className="faded"/> DBP</label>
                  <input type="number" name="dbp" value={formData.dbp ?? ''} onChange={handleInputChange} required />
                </div>
                <div className="input-group vital-group">
                  <label><Activity size={14}/> Heart Rate</label>
                  <input type="number" name="hr" value={formData.hr ?? ''} onChange={handleInputChange} required />
                </div>
                <div className="input-group vital-group">
                  <label><Wind size={14}/> Resp Rate</label>
                  <input type="number" name="rr" value={formData.rr ?? ''} onChange={handleInputChange} required />
                </div>
                <div className="input-group vital-group">
                  <label><Thermometer size={14}/> Temp (°C)</label>
                  <input type="number" name="temp" value={formData.temp ?? ''} onChange={handleInputChange} step="0.1" required />
                </div>
                <div className="input-group vital-group">
                  <label><Droplets size={14}/> SpO2 (%)</label>
                  <input type="number" name="spo2" value={formData.spo2 ?? ''} placeholder="Auto (98%)" onChange={handleInputChange} />
                </div>
              </div>
            </div>

            <button type="submit" disabled={loading} className="analyze-btn">
              {loading ? <span className="loader"></span> : <span><Stethoscope size={18}/> Run Multi-Model Assessment</span>}
            </button>
          </form>
        </section>

        <section className={`result-panel glass-panel ${result ? getUrgencyColor(result.final_recommendation) : ''}`}>
          {error && (
            <div className="error-box animate-shake">
              <AlertCircle size={24}/>
              <p>{error}</p>
            </div>
          )}

          {!result && !error && !loading && (
            <div className="empty-state">
              <HeartPulse size={48} className="empty-icon" />
              <h3>Awaiting Diagnostics</h3>
              <p>Complete the patient assessment to generate AI recommendations and risk scores.</p>
            </div>
          )}

          {loading && (
            <div className="empty-state">
              <span className="large-loader"></span>
              <h3>Consulting Urgency & Risk Models...</h3>
            </div>
          )}

          {result && (
            <div className="results-content animate-pop">
              <div className="results-header">
                <h2>Clinical Recommendation</h2>
                <div className={`recommendation-badge ${getUrgencyColor(result.final_recommendation)}`}>
                  {result.final_recommendation === 'Critical' ? '🚨 Critical' : '✅ Non-critical'}
                </div>
              </div>
              
              <div className="metrics-row">
                <div className="metric-box">
                  <span>Urgency Confidence</span>
                  <strong>{(result.confidence_score * 100).toFixed(1)}%</strong>
                </div>
                <div className="metric-box">
                  <span>Mistriage Risk</span>
                  <strong className={result.mistriage_risk_alert ? 'text-danger' : ''}>
                    {(result.risk_score * 100).toFixed(1)}%
                  </strong>
                </div>
              </div>

              {result.mistriage_risk_alert && (
                <div className="mistriage-risk-panel">
                  <ShieldAlert size={20} />
                  <div>
                    <h4>High Mistriage Risk Detected</h4>
                    <p>The models suggest a potential mismatch between clinical presentation and automated classification. Extreme caution advised.</p>
                  </div>
                </div>
              )}

              {result.alerts && result.alerts.length > 0 && (
                <div className="alerts-container">
                  <h4><AlertCircle size={16}/> Clinical Safety Overrides</h4>
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
                <h4>Urgency Probability Distribution</h4>
                {['Critical', 'Non-critical'].map(label => (
                  <div className="prob-bar-container" key={label}>
                    <div className="prob-label">{label}</div>
                    <div className="prob-track">
                      <div 
                        className={`prob-fill ${getUrgencyColor(label)}`} 
                        style={{width: `${(result.probabilities[label] || 0) * 100}%`}}
                      ></div>
                    </div>
                    <div className="prob-pct">{((result.probabilities[label] || 0) * 100).toFixed(1)}%</div>
                  </div>
                ))}
              </div>

              {result.influential_features && result.influential_features.length > 0 && (
                <div className="influential-factors">
                  <h4>Key Risk Factors</h4>
                  <div className="factors-row">
                    {result.influential_features.map((f, i) => (
                      <div key={i} className={`factor-tag ${f.risk.toLowerCase()}`}>
                        {f.name}: {f.value}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
