import React, { useState } from 'react';
import {
  Activity, HeartPulse, Thermometer, Wind, AlertCircle,
  Stethoscope, Droplets, ShieldAlert, ShieldCheck, AlertTriangle,
  Info, Cpu, ClipboardCheck, Eye, EyeOff, User, Lock, LogOut,
  Plus, Globe
} from 'lucide-react';
import './App.css';

/* ─── MOCK AUTH ─────────────────────────────────────────── */
const USERS = {
  'careme': { password: 'admin123', name: 'Care Me Admin', role: 'Nurse / Charge Nurse', dept: 'Emergency' },
  'admin': { password: 'admin', name: 'Admin', role: 'Administrator', dept: 'Clinical' },
};

/* ─── DEFAULT STATE ─────────────────────────────────────── */
const DEFAULT_STATE = {
  age: null, age_group: 1, sex: '', arrival_mode: '',
  injury: 1, chief_complain: '', mental_state: 1, pain: 0,
  nrs_pain: 0, sbp: 120, dbp: 80, hr: 75, rr: 16, temp: 36.6, spo2: 98,
};

const SCENARIO_DATA = {
  1: { title: 'Safe & Stable', desc: 'Awaiting standard monitoring.', icon: <ShieldCheck size={28} />, colorClass: 'non-urgent' },
  2: { title: 'Safety Re-evaluation Required', desc: 'Vitals show borderline instability. Reassessment advised.', icon: <AlertTriangle size={28} />, colorClass: 'recheck' },
  3: { title: 'Critical - High Urgency', desc: 'Immediate clinical intervention requested.', icon: <ShieldAlert size={28} />, colorClass: 'emergency' },
  4: { title: 'Complex Emergency', desc: 'High-risk ambiguity detected. Senior consult advised.', icon: <AlertCircle size={28} />, colorClass: 'complex' },
};

const CHIEF_COMPLAINTS = [
  'Chest Pain','Shortness of Breath','Abdominal Pain','Head Injury',
  'Altered Mental Status','Fever','Seizure','Stroke Symptoms',
  'Trauma / Fall','Allergic Reaction','Cardiac Arrest','Other',
];

/* ══════════════════════════════════════════════════════
   LOGIN PAGE
══════════════════════════════════════════════════════ */
function LoginPage({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPw, setShowPw] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true); setError('');
    setTimeout(() => {
      const u = USERS[username.trim().toLowerCase()];
      if (u && u.password === password) onLogin({ username: username.trim(), ...u });
      else setError('Invalid username or password.');
      setLoading(false);
    }, 600);
  };

  return (
    <div className="login-root">
      {/* LEFT hero */}
      <div className="login-hero">
        <div className="hero-overlay" />
        {/* Floating medical illustration */}
        <div className="hero-img-wrap">
          <img
            src="https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=900&q=80"
            alt="Medical triage care"
            className="hero-main-img"
          />
          <div className="hero-img-badge">
            <HeartPulse size={18} />
            <span>AI-Powered Triage</span>
          </div>
          <div className="hero-img-stat">
            <Activity size={14} />
            <span>Real-time vitals analysis</span>
          </div>
        </div>

        <div className="hero-brand">
          <div className="brand-pill"><Plus size={16}/></div>
          <span className="hero-brand-name">Care Me</span>
          <span className="hero-brand-sub">CLINICAL TRIAGE · AI</span>
        </div>
        <div className="hero-body">
          <h2>Smarter triage.<br/>Better outcomes.</h2>
          <p>AI-powered clinical decision support that analyses patient vitals in real time — giving your team the clarity to act fast and confidently.</p>
          <div className="hero-chips">
            <span>Real-time scoring</span>
            <span>Explainable AI</span>
            <span>Role-based access</span>
          </div>
        </div>
      </div>

      {/* RIGHT form */}
      <div className="login-panel">
        <div className="login-panel-inner">
          <div className="login-logo">
            <div className="brand-pill blue"><Plus size={16}/></div>
            <span className="login-logo-text">Care Me</span>
          </div>
          <h1 className="login-heading">Welcome back.</h1>
          <p className="login-desc">Sign in to the Care Me triage dashboard.</p>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="lf-field">
              <label>USERNAME</label>
              <div className="lf-wrap">
                <User size={15} className="lf-icon"/>
                <input type="text" placeholder="e.g. careme" value={username} onChange={e=>setUsername(e.target.value)} required/>
              </div>
            </div>
            <div className="lf-field">
              <label>PASSWORD</label>
              <div className="lf-wrap">
                <Lock size={15} className="lf-icon"/>
                <input type={showPw?'text':'password'} placeholder="Your password" value={password} onChange={e=>setPassword(e.target.value)} required/>
                <button type="button" className="lf-eye" onClick={()=>setShowPw(p=>!p)}>
                  {showPw?<EyeOff size={15}/>:<Eye size={15}/>}
                </button>
              </div>
            </div>
            {error && <div className="lf-error">{error}</div>}
            <button type="submit" className="lf-btn" disabled={loading}>
              {loading?<span className="lf-spin"/>:'Sign In'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════════
   TRIAGE DASHBOARD
══════════════════════════════════════════════════════ */
function TriageDashboard({ user, onLogout }) {
  const [formData, setFormData] = useState(DEFAULT_STATE);
  const [ageType, setAgeType] = useState('exact');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    let v = value;
    if (type==='number') v = value===''?null:parseFloat(value);
    else if (['injury','pain','arrival_mode','mental_state','age_group'].includes(name)) v = value===''?null:parseInt(value,10);
    setFormData(prev=>({...prev,[name]:v}));
  };

  const handleSubmit = async () => {
    setLoading(true); setError(null); setResult(null);
    const body = {...formData};
    if (ageType==='range') body.age=null; else body.age_group=null;
    try {
      const res = await fetch('http://localhost:8000/api/predict',{
        method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)
      });
      if (!res.ok) { const d=await res.json().catch(()=>({detail:'Service unavailable'})); throw new Error(d.detail||'Server error'); }
      setResult(await res.json());
    } catch(err){ setError(err.message); } finally { setLoading(false); }
  };

  const protocol = result?.clinical_protocol;
  const ai = result?.ai_insights;
  const scenario = protocol ? SCENARIO_DATA[protocol.scenario_id] : null;

  return (
    <div className="dash-root">
      {/* NAV */}
      <nav className="dash-nav">
        <div className="nav-left">
          <div className="brand-pill nav-pill"><Plus size={14}/></div>
          <span className="nav-brand">Care Me</span>
          <div className="nav-sep"/>
          <div className="nav-user-block">
            <div className="nav-avatar"/>
            <div className="nav-user-info">
              <span className="nav-uname">{user.name}</span>
              <span className="nav-dept">{user.dept}</span>
            </div>
            <span className="nav-role">{user.role}</span>
          </div>
        </div>
        <div className="nav-right">
          <button className="nav-triage-btn">Triage</button>
          <button className="nav-signout" onClick={onLogout}><LogOut size={13}/> Sign Out</button>
        </div>
      </nav>

      {/* PAGE HEADER */}
      <div className="page-header">
        <h1>Patient Triage Assessment</h1>
        <p>Care Me AI Engine · Dual-Model (Urgency + Mistriage Risk) · KTAS-Aligned</p>
      </div>

      {/* GRID */}
      <div className="dash-grid">

        {/* LEFT: Demographics + Vitals (scrollable) */}
        <div className="dash-col dash-col-left">
          {/* Demographics */}
          <div className="dash-card">
            <div className="dc-header">
              <div className="dc-icon blue"><User size={14}/></div>
              <span>Patient Demographics</span>
            </div>

            <div className="df-row">
              <div className="df-field full">
                <label>AGE (yrs) <span className="req">*</span></label>
                <div className="age-row">
                  <div className="age-toggle">
                    <button type="button" className={ageType==='exact'?'active':''} onClick={()=>setAgeType('exact')}>Exact</button>
                    <button type="button" className={ageType==='range'?'active':''} onClick={()=>setAgeType('range')}>Range</button>
                  </div>
                  {ageType==='exact'
                    ? <input type="number" name="age" placeholder="Enter exact age" value={formData.age??''} onChange={handleChange} min={0} max={120}/>
                    : <select name="age_group" value={formData.age_group??''} onChange={handleChange}>
                        <option value={0}>Pediatric (0–18)</option>
                        <option value={1}>Young Adult (19–40)</option>
                        <option value={2}>Middle Aged (41–65)</option>
                        <option value={3}>Senior (66+)</option>
                      </select>
                  }
                </div>
              </div>
            </div>

            <div className="df-row two">
              <div className="df-field">
                <label>SEX <span className="req">*</span></label>
                <select name="sex" value={formData.sex} onChange={handleChange}>
                  <option value="">Select...</option>
                  <option>Male</option><option>Female</option><option>Other</option>
                </select>
              </div>
              <div className="df-field">
                <label>ARRIVAL MODE <span className="req">*</span></label>
                <select name="arrival_mode" value={formData.arrival_mode} onChange={handleChange}>
                  <option value="">Select...</option>
                  <option value={1}>Walk-in</option><option value={2}>Car</option>
                  <option value={3}>Ambulance</option><option value={7}>Other</option>
                </select>
              </div>
            </div>

            <div className="df-row">
              <div className="df-field full">
                <label>MENTAL STATE <span className="req">*</span></label>
                <select name="mental_state" value={formData.mental_state} onChange={handleChange}>
                  <option value="">Select...</option>
                  <option value={1}>1: Alert (Stable)</option><option value={2}>2: Verbal (Review)</option>
                  <option value={3}>3: Pain (Critical)</option><option value={4}>4: Unresponsive (Critical)</option>
                </select>
              </div>
            </div>

            <div className="df-row">
              <div className="df-field full">
                <label>INJURY / TRAUMA <span className="req">*</span></label>
                <div className="radio-pair">
                  {[{label:'Yes',val:2},{label:'No',val:1}].map(o=>(
                    <label key={o.val} className={`radio-opt ${formData.injury===o.val?'sel':''}`}>
                      <span className="r-dot"/>
                      <input type="radio" name="injury" value={o.val} checked={formData.injury===o.val} onChange={handleChange}/>
                      {o.label}
                      <span className="r-check"/>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Vitals */}
          <div className="dash-card">
            <div className="dc-header">
              <div className="dc-icon teal"><Activity size={14}/></div>
              <span>Vital Signs</span>
            </div>
            <div className="vitals-grid">
              {[
                {label:'SYSTOLIC BP',sub:'(mmHg)',name:'sbp',step:1,alert:formData.sbp<90||formData.sbp>180},
                {label:'DIASTOLIC BP',sub:'(mmHg)',name:'dbp',step:1},
                {label:'HEART RATE',sub:'(bpm)',name:'hr',step:1,alert:formData.hr>130||formData.hr<40},
                {label:'RESP RATE',sub:'(brpm)',name:'rr',step:1,alert:formData.rr>30||formData.rr<8},
                {label:'TEMPERATURE',sub:'(°C)',name:'temp',step:0.1,alert:formData.temp>39||formData.temp<35},
                {label:'SpO2',sub:'(%)',name:'spo2',step:1,alert:formData.spo2<90},
              ].map(v=>(
                <div className="df-field" key={v.name}>
                  <label className={v.alert?'lbl-alert':''}>{v.label} <span className="label-sub">{v.sub}</span> <span className="req">*</span></label>
                  <input type="number" name={v.name} value={formData[v.name]??''} onChange={handleChange} step={v.step} className={v.alert?'inp-alert':''}/>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* MIDDLE: Clinical Presentation */}
        <div className="dash-col dash-col-mid">
          <div className="dash-card clinical-card">
            <div className="dc-header amber-hdr">
              <div className="dc-icon amber-icon"><AlertTriangle size={14}/></div>
              <span>Clinical Presentation</span>
            </div>

            <div className="df-field">
              <label>CHIEF COMPLAINT <span className="req">*</span></label>
              <select name="chief_complain" value={formData.chief_complain} onChange={handleChange}>
                <option value="">Select...</option>
                {CHIEF_COMPLAINTS.map(c=><option key={c} value={c}>{c}</option>)}
              </select>
            </div>

            <div className="df-field" style={{marginTop:'1.25rem'}}>
              <label>PAIN PRESENT <span className="req">*</span></label>
              <div className="radio-pair">
                {[{label:'No Pain',val:0},{label:'Pain Present',val:1}].map(o=>(
                  <label key={o.val} className={`radio-opt ${formData.pain===o.val?'sel':''}`}>
                    <span className="r-dot"/>
                    <input type="radio" name="pain" value={o.val} checked={formData.pain===o.val} onChange={e=>setFormData(p=>({...p,pain:parseInt(e.target.value)}))}/>
                    {o.label}
                    <span className="r-check"/>
                  </label>
                ))}
              </div>
              {formData.pain===1 && (
                <div style={{marginTop:'1rem'}}>
                  <label>NRS PAIN SCORE (0–10)</label>
                  <input type="number" name="nrs_pain" min={0} max={10} value={formData.nrs_pain??''} onChange={handleChange}/>
                </div>
              )}
            </div>
          </div>

          <button className="run-btn" onClick={handleSubmit} disabled={loading}>
            {loading?<><span className="btn-spin"/> Analysing...</>:<><Stethoscope size={17}/> Run Triage Assessment</>}
          </button>
        </div>

        {/* RIGHT: Results */}
        <div className="dash-col dash-col-right">
          {!result&&!error&&!loading&&(
            <div className="dash-card result-empty">
              <Globe size={52} className="empty-icon"/>
              <h3>Ready for Assessment</h3>
              <p>Fill in demographics, vitals, and clinical presentation, then run the AI assessment.</p>
            </div>
          )}

          {loading&&(
            <div className="dash-card result-empty">
              <span className="big-spin"/>
              <h3>Syncing Decision Engines…</h3>
            </div>
          )}

          {error&&(
            <div className="dash-card result-error">
              <AlertCircle size={22}/>
              <p>{error}</p>
            </div>
          )}

          {result&&(
            <>
              <div className="dash-card animate-pop">
                <div className="dc-header">
                  <div className="dc-icon blue"><Cpu size={14}/></div>
                  <span>AI Diagnostic Intelligence</span>
                </div>
                <div className="ai-row">
                  <div className="ai-box">
                    <span>XGBoost Urgency</span>
                    <strong className={ai.prediction==='Critical'?'stat-danger':'stat-ok'}>{ai.prediction}</strong>
                  </div>
                  <div className="ai-box">
                    <span>Confidence</span>
                    <strong>{(ai.confidence*100).toFixed(1)}%</strong>
                  </div>
                </div>
                <div className="risk-box">
                  <div className="risk-top"><span>Safety Risk Profile</span><span className={`risk-badge ${ai.risk_label.toLowerCase()}`}>{ai.risk_label} RISK</span></div>
                  <div className="risk-track"><div className="risk-fill" style={{width:`${ai.mistriage_risk*100}%`}}/></div>
                  <p className="risk-note">Random Forest mistake-detection model.</p>
                </div>
                <div className="prob-section">
                  <span className="prob-lbl">Class Probabilities</span>
                  {Object.entries(ai.probabilities).map(([k,v])=>(
                    <div className="p-row" key={k}>
                      <span className="p-key">{k}</span>
                      <div className="p-track"><div className={`p-fill ${k.toLowerCase()}`} style={{width:`${v*100}%`}}/></div>
                      <span className="p-pct">{(v*100).toFixed(0)}%</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className={`dash-card animate-pop`} style={{marginTop:'1rem'}}>
                <div className="dc-header">
                  <div className="dc-icon blue"><ClipboardCheck size={14}/></div>
                  <span>Clinical Safety Protocol</span>
                </div>
                <div className={`reco-box ${scenario.colorClass}`}>
                  <div>{scenario.icon}</div>
                  <div><h4>{scenario.title}</h4><p>{protocol.final_recommendation}</p></div>
                </div>
                {Object.keys(protocol.rule_breaches).length>0&&(
                  <div className="findings crit">
                    <div className="find-lbl"><AlertCircle size={12}/> SATS Level 1 Breaches</div>
                    {Object.entries(protocol.rule_breaches).map(([k,v])=><div className="find-item" key={k}><strong>{k}:</strong> {v}</div>)}
                  </div>
                )}
                {Object.keys(protocol.rule_warnings).length>0&&(
                  <div className="findings warn">
                    <div className="find-lbl"><AlertTriangle size={12}/> Clinical Warnings</div>
                    {Object.entries(protocol.rule_warnings).map(([k,v])=><div className="find-item" key={k}><strong>{k}:</strong> {v}</div>)}
                  </div>
                )}
                <div className="nurse-box">
                  <div className="nurse-lbl"><Info size={13}/> Nurse Action Plan</div>
                  <p>{protocol.alerts[0]}</p>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [user, setUser] = useState(null);
  if (!user) return <LoginPage onLogin={setUser}/>;
  return <TriageDashboard user={user} onLogout={()=>setUser(null)}/>;
}
