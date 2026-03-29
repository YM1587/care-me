import React, { useState } from 'react';
import { Activity, HeartPulse, Thermometer, Wind, User, AlertCircle, Stethoscope, Droplets, ShieldAlert, ShieldCheck, AlertTriangle, Info, Cpu, ClipboardCheck } from 'lucide-react';
import './App.css';

const DEFAULT_STATE = {
  age: null,
  age_group: 1, // Default to 19-40
  sex: "Female",
  arrival_mode: 1,
  injury: 1,
  chief_complain: "",
  mental_state: 1,
  pain: 1,
  nrs_pain: 0,
  sbp: 120,
  dbp: 80,
  hr: 75,
  rr: 16,
  temp: 36.6,
  spo2: 98
};

const SCENARIO_DATA = {
  1: {
    title: "Safe & Stable",
    desc: "Awaiting standard monitoring. Clinical findings support routine care.",
    icon: <ShieldCheck size={28} />,
    colorClass: "non-urgent"
  },
  2: {
    title: "Safety Re-evaluation Required",
    desc: "Vitals show borderline instability. Manual clinical reassessment strongly advised.",
    icon: <AlertTriangle size={28} />,
    colorClass: "recheck"
  },
  3: {
    title: "Critical - High Urgency",
    desc: "Immediate clinical intervention requested. Life-threatening thresholds breached.",
    icon: <ShieldAlert size={28} />,
    colorClass: "emergency"
  },
  4: {
    title: "Complex Emergency",
    desc: "System flags high-risk ambiguity with physiological markers. Senior consult advised.",
    icon: <AlertCircle size={28} />,
    colorClass: "complex"
  }
};

function App() {
  const [formData, setFormData] = useState(DEFAULT_STATE);
  const [ageType, setAgeType] = useState('range');
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
    setFormData(prev => ({ ...prev, [name]: parsedValue }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    const submissionData = { ...formData };
    if (ageType === 'range') {
      submissionData.age = null;
    } else {
      submissionData.age_group = null;
    }

    try {
      const response = await fetch('http://localhost:8000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(submissionData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Service unavailable' }));
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

  const protocol = result?.clinical_protocol;
  const ai = result?.ai_insights;
  const currentScenario = protocol ? SCENARIO_DATA[protocol.scenario_id] : null;

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-brand">
          <HeartPulse size={36} className="brand-icon" />
          <div className="brand-text">
            <h1>CareMe</h1>
            <p>Clinically-Safe AI Brain for Emergency Support</p>
          </div>
        </div>
        <div className="header-status">
          <span className="status-dot"></span> Active Intelligence
        </div>
      </header>

      <main className="dashboard">
        <section className="input-panel glass-panel">
          <h2><User size={20}/> Triage Input Console</h2>
          <form onSubmit={handleSubmit} className="triage-form">
            
            {/* MODULE 1: PATIENT DEMOGRAPHICS */}
            <div className="form-module">
              <div className="module-header">
                <User size={14}/> Patient Demographics
              </div>
              <div className="module-content">
                <div className="form-group-row">
                  <div className="input-group">
                    <label>Biological Sex</label>
                    <select name="sex" value={formData.sex} onChange={handleInputChange}>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                    </select>
                  </div>
                  <div className="input-group">
                    <label>Age Entry Mode</label>
                    <div className="age-toggle">
                      <button type="button" className={ageType === 'range' ? 'active' : ''} onClick={() => setAgeType('range')}>Group</button>
                      <button type="button" className={ageType === 'exact' ? 'active' : ''} onClick={() => setAgeType('exact')}>Exact</button>
                    </div>
                  </div>
                </div>
                <div className="form-group-row">
                  <div className="input-group full-width">
                    <label>{ageType === 'exact' ? 'Exact Age (Years)' : 'Estimated Age Group'}</label>
                    {ageType === 'exact' ? (
                      <input type="number" name="age" value={formData.age ?? ''} onChange={handleInputChange} min="0" max="110" placeholder="Enter age..." required />
                    ) : (
                      <select name="age_group" value={formData.age_group ?? ''} onChange={handleInputChange} required>
                        <option value={0}>Pediatric (0-18)</option>
                        <option value={1}>Young Adult (19-40)</option>
                        <option value={2}>Middle Aged (41-65)</option>
                        <option value={3}>Senior (66+)</option>
                      </select>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* MODULE 2: CLINICAL ASSESSMENT */}
            <div className="form-module">
              <div className="module-header">
                <Stethoscope size={14}/> Clinical Assessment
              </div>
              <div className="module-content">
                <div className="form-group-row">
                  <div className="input-group full-width">
                    <label>Chief Complaint (Optional)</label>
                    <input type="text" name="chief_complain" value={formData.chief_complain} onChange={handleInputChange} placeholder="Unresponsive / Unknown..." />
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
                    <label>Level of Consciousness</label>
                    <select name="mental_state" value={formData.mental_state} onChange={handleInputChange}>
                      <option value={1}>1: Alert</option>
                      <option value={2}>2: Verbal</option>
                      <option value={3}>3: Pain</option>
                      <option value={4}>4: Unresponsive</option>
                    </select>
                  </div>
                </div>
                <div className="form-group-row">
                  <div className="input-group">
                    <label>Injury / Trauma</label>
                    <select name="injury" value={formData.injury} onChange={handleInputChange}>
                      <option value={1}>Non-traumatic</option>
                      <option value={2}>Traumatic Injury</option>
                    </select>
                  </div>
                  <div className="input-group">
                    <label>Pain Scale (NRS)</label>
                    <div className="pain-inputs">
                      <select name="pain" value={formData.pain} onChange={handleInputChange}>
                        <option value={0}>No Pain</option>
                        <option value={1}>Painful</option>
                      </select>
                      {formData.pain === 1 && (
                        <input type="number" name="nrs_pain" placeholder="0-10" value={formData.nrs_pain ?? ''} onChange={handleInputChange} min="0" max="10" />
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* MODULE 3: VITALS CONSOLE */}
            <div className="form-module">
              <div className="module-header">
                <Activity size={14}/> Vitals Console
              </div>
              <div className="module-content">
                <div className="vitals-grid">
                  {[
                    { label: 'SBP', name: 'sbp', icon: <HeartPulse size={12}/>, alert: formData.sbp < 90 || formData.sbp > 180 },
                    { label: 'DBP', name: 'dbp', icon: <HeartPulse size={12} className="faded"/> },
                    { label: 'HR', name: 'hr', icon: <Activity size={12}/>, alert: formData.hr > 130 || formData.hr < 40 },
                    { label: 'RR', name: 'rr', icon: <Wind size={12}/>, alert: formData.rr > 30 || formData.rr < 8 },
                    { label: 'Temp', name: 'temp', icon: <Thermometer size={12}/>, alert: formData.temp > 38.5 || formData.temp < 35.5 },
                    { label: 'SpO2', name: 'spo2', icon: <Droplets size={12}/>, alert: formData.spo2 < 92 }
                  ].map(v => (
                    <div className="input-group" key={v.name}>
                      <label className={v.alert ? 'text-urgent' : ''}>{v.label}</label>
                      <input type="number" name={v.name} value={formData[v.name] ?? ''} onChange={handleInputChange} step={v.name === 'temp' ? '0.1' : '1'} required={v.name !== 'spo2'} />
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <button type="submit" disabled={loading} className="analyze-btn">
              {loading ? <span className="loader"></span> : <span><Cpu size={18}/> Run Clinical Analysis Engine</span>}
            </button>
          </form>
        </section>

        <section className="result-container-split">
          {error && <div className="error-box animate-shake"><AlertCircle size={24}/><p>{error}</p></div>}
          
          {!result && !error && !loading && (
            <div className="empty-state-split glass-panel">
              <Cpu size={48} className="empty-icon" />
              <h3>Awaiting Triage Data</h3>
              <p>The system will segregate AI Risk Intelligence from Safety Override Protocols once analyzed.</p>
            </div>
          )}

          {loading && (
            <div className="empty-state-split glass-panel">
              <span className="large-loader"></span>
              <h3>Synching Decision Engines...</h3>
            </div>
          )}

          {result && (
            <>
              {/* CARD 1: AI DIAGNOSTIC INTELLIGENCE */}
              <div className="ai-intelligence-card glass-panel animate-pop">
                <div className="card-header">
                  <div className="header-icon"><Cpu size={20}/></div>
                  <h3>AI Diagnostic Intelligence</h3>
                </div>
                
                <div className="ai-stats-row">
                  <div className="ai-stat-box">
                    <span>XGBoost Urgency</span>
                    <strong className={ai.prediction === 'Critical' ? 'text-danger' : 'text-success'}>
                      {ai.prediction}
                    </strong>
                  </div>
                  <div className="ai-stat-box">
                    <span>Confidence Score</span>
                    <strong>{(ai.confidence * 100).toFixed(1)}%</strong>
                  </div>
                </div>

                <div className="risk-profile-section">
                  <div className="risk-header">
                    <span>Safety Risk Profile</span>
                    <span className={`risk-badge ${ai.risk_label.toLowerCase()}`}>{ai.risk_label} RISK</span>
                  </div>
                  <div className="risk-progress">
                    <div className="risk-progress-fill" style={{width: `${(ai.mistriage_risk * 100)}%`}}></div>
                  </div>
                  <p className="risk-caption">Based on Random Forest mistake-detection model.</p>
                </div>

                <div className="prob-distribution">
                  <span>Class Probabilities</span>
                  <div className="prob-bars">
                    {Object.entries(ai.probabilities).map(([key, val]) => (
                      <div className="p-bar-item" key={name}>
                        <div className="p-bar-label">{key}</div>
                        <div className="p-bar-track"><div className={`p-bar-fill ${key.toLowerCase()}`} style={{width: `${val * 100}%`}}></div></div>
                        <div className="p-bar-val">{(val * 100).toFixed(0)}%</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* CARD 2: CLINICAL SAFETY VALIDATION */}
              <div className={`clinical-safety-card glass-panel animate-pop ${currentScenario.colorClass}`}>
                <div className="card-header">
                  <div className="header-icon"><ClipboardCheck size={20}/></div>
                  <h3>Clinical Safety Protocol (SATS-Aligned)</h3>
                </div>

                <div className="final-recommendation-zone">
                  <div className={`recommendation-box ${currentScenario.colorClass}`}>
                    <div className="scenario-icon">{currentScenario.icon}</div>
                    <div className="scenario-text">
                      <h4>{currentScenario.title}</h4>
                      <p>{protocol.final_recommendation}</p>
                    </div>
                  </div>
                </div>

                <div className="rules-segregation">
                  {Object.keys(protocol.rule_breaches).length > 0 && (
                    <div className="findings-group critical">
                      <div className="findings-label"><AlertCircle size={14}/> SATS Level 1 Breaches (Red)</div>
                      <div className="findings-list">
                        {Object.entries(protocol.rule_breaches).map(([key, val]) => (
                          <div className="finding-item" key={key}><strong>{key}:</strong> {val}</div>
                        ))}
                      </div>
                    </div>
                  )}

                  {Object.keys(protocol.rule_warnings).length > 0 && (
                    <div className="findings-group urgent">
                      <div className="findings-label"><AlertTriangle size={14}/> Clinical Warnings (Orange)</div>
                      <div className="findings-list">
                        {Object.entries(protocol.rule_warnings).map(([key, val]) => (
                          <div className="finding-item" key={key}><strong>{key}:</strong> {val}</div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div className="nurse-instruction-box">
                   <div className="instruction-header"><Info size={16}/> Nurse Action Plan</div>
                   <p>{protocol.alerts[0]}</p>
                </div>
              </div>
            </>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
