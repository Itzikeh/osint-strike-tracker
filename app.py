import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import { 
  ShieldAlert, Ship, Plane, Radio, Crosshair, Landmark, 
  Globe, Activity, AlertCircle, ChevronRight, RefreshCw,
  Search, Database, Zap, Share2, Users, AlertTriangle, Clock,
  FileText, Volume2, BrainCircuit, Play, Pause, X, Info,
  ChevronDown, MessageSquare, Terminal
} from 'lucide-react';
import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from 'firebase/auth';
import { getFirestore, doc, setDoc, onSnapshot, updateDoc } from 'firebase/firestore';

// --- Configuration & Services ---
// Use environment provided variables
const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : null;
const appId = typeof __app_id !== 'undefined' ? __app_id : 'strategic-tracker-v1';
const apiKey = ""; // Runtime provides the key

let db, auth;
if (firebaseConfig) {
  const app = initializeApp(firebaseConfig);
  auth = getAuth(app);
  db = getFirestore(app);
}

const MODEL_NAME = "gemini-2.5-flash-preview-09-2025";
const TTS_MODEL = "gemini-2.5-flash-preview-tts";

const INITIAL_STATE = {
  maritime: { warRisk: 40, oilAnomaly: 20, polymarket: 35, rialCollapse: 50, khargEvac: 10 },
  aviation: { israeliFleet: 15, saudiEscat: 5, iranCancels: 30, vipFlights: 25 },
  military: { ussGeorgia: 60, tankerBridge: 45, bomberDeploy: 30, bunkerSealing: 10, irgcUnderground: 20 },
  cyber: { gpsJamming: 70, internetBlackout: 15, proxyChatter: 55, sigintSpikes: 40, cyberWaves: 30 },
  diplomacy: { envoyWatch: 10, embassyEvac: 5, hospitalAlert: 20, summitDeception: 40 }
};

const App = () => {
  const [user, setUser] = useState(null);
  const [data, setData] = useState(INITIAL_STATE);
  const [isFetching, setIsFetching] = useState(false);
  const [activeCategory, setActiveCategory] = useState('military');
  const [analysisLog, setAnalysisLog] = useState([]);
  const [isSystemReady, setIsSystemReady] = useState(false);
  
  // AI States
  const [sitrep, setSitrep] = useState("");
  const [isGeneratingSitrep, setIsGeneratingSitrep] = useState(false);
  const [isAudioLoading, setIsAudioLoading] = useState(false);
  const audioRef = useRef(null);

  // Auto-scan Timer
  const [isAutoUpdating, setIsAutoUpdating] = useState(true);
  const [nextScanIn, setNextScanIn] = useState(1200);

  // --- Auth & Sync Loop ---
  useEffect(() => {
    const init = async () => {
      if (!auth) return;
      try {
        if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
          await signInWithCustomToken(auth, __initial_auth_token);
        } else {
          await signInAnonymously(auth);
        }
      } catch (err) { console.error("Auth init failed", err); }
      
      setIsSystemReady(true);
    };
    init();
    const unsubscribe = auth ? onAuthStateChanged(auth, setUser) : () => {};
    return () => unsubscribe();
  }, []);

  useEffect(() => {
    if (!user || !db) return;
    const docRef = doc(db, 'artifacts', appId, 'public', 'data', 'states', 'global_state');
    const unsubscribe = onSnapshot(docRef, (snapshot) => {
      if (snapshot.exists()) {
        const remoteData = snapshot.data().indicators;
        if (remoteData) setData(remoteData);
      } else {
        setDoc(docRef, { indicators: INITIAL_STATE, lastUpdated: Date.now() });
      }
    }, (err) => console.error("Sync error", err));
    return () => unsubscribe();
  }, [user]);

  const updateCloudData = async (newData) => {
    if (!user || !db) return;
    const docRef = doc(db, 'artifacts', appId, 'public', 'data', 'states', 'global_state');
    try {
      await updateDoc(docRef, { indicators: newData, timestamp: Date.now() });
    } catch (e) { console.error("Cloud update failed", e); }
  };

  // --- AI Engines ---
  const runGlobalAnalysis = useCallback(async () => {
    if (isFetching) return;
    setIsFetching(true);
    const systemPrompt = `Strategic Intelligence Engine. Analyze Iran-Israel tensions. Return JSON matching structure: ${JSON.stringify(INITIAL_STATE)}. 0-100 scale.`;
    
    try {
      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${MODEL_NAME}:generateContent?key=${apiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: "Perform a live OSINT sweep based on today's strategic events." }] }],
          systemInstruction: { parts: [{ text: systemPrompt }] },
          tools: [{ "google_search": {} }],
          generationConfig: { responseMimeType: "application/json" }
        })
      });
      const result = await response.json();
      const text = result.candidates?.[0]?.content?.parts?.[0]?.text;
      if (text) {
        const parsed = JSON.parse(text);
        setData(parsed);
        await updateCloudData(parsed);
        setAnalysisLog(p => [`[${new Date().toLocaleTimeString()}] OSINT Matrix Updated`, ...p].slice(0, 5));
        setNextScanIn(1200);
      }
    } catch (e) {
      setAnalysisLog(p => [`[${new Date().toLocaleTimeString()}] Analysis Error: Connection timeout`, ...p]);
    } finally { setIsFetching(false); }
  }, [isFetching, user]);

  const generateSitrep = async () => {
    setIsGeneratingSitrep(true);
    try {
      const prompt = `Based on these indicators: ${JSON.stringify(data)}, write a professional strategic SITREP in Hebrew. 
      Focus on escalation probability for the next 24h. Be concise and use military-grade tone.`;
      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${MODEL_NAME}:generateContent?key=${apiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
      });
      const result = await response.json();
      setSitrep(result.candidates?.[0]?.content?.parts?.[0]?.text || "Unable to generate report.");
    } catch (e) { setSitrep("Communication failure with SITREP engine."); } finally { setIsGeneratingSitrep(false); }
  };

  const playAudioBriefing = async () => {
    if (!sitrep || isAudioLoading) return;
    setIsAudioLoading(true);
    try {
      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${TTS_MODEL}:generateContent?key=${apiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: `Read this sitrep professionally: ${sitrep}` }] }],
          generationConfig: { 
            responseModalities: ["AUDIO"],
            speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: "Puck" } } }
          }
        })
      });
      const result = await response.json();
      const pcmData = result.candidates[0].content.parts[0].inlineData.data;
      const wavBlob = pcmToWav(pcmData, 24000);
      const url = URL.createObjectURL(wavBlob);
      if (audioRef.current) {
        audioRef.current.src = url;
        audioRef.current.play();
      }
    } catch (e) { console.error("Audio error", e); } finally { setIsAudioLoading(false); }
  };

  const pcmToWav = (base64, rate) => {
    const buffer = Uint8Array.from(atob(base64), c => c.charCodeAt(0)).buffer;
    const header = new ArrayBuffer(44);
    const view = new DataView(header);
    view.setUint32(0, 0x46464952, true); view.setUint32(4, 36 + buffer.byteLength, true); view.setUint32(8, 0x45564157, true);
    view.setUint32(12, 0x20746d66, true); view.setUint32(16, 16, true); view.setUint16(20, 1, true); view.setUint16(22, 1, true);
    view.setUint32(24, rate, true); view.setUint32(28, rate * 2, true); view.setUint16(32, 2, true); view.setUint16(34, 16, true);
    view.setUint32(36, 0x61746164, true); view.setUint32(40, buffer.byteLength, true);
    return new Blob([header, buffer], { type: 'audio/wav' });
  };

  useEffect(() => {
    if (isAutoUpdating) {
      const timer = setInterval(() => {
        setNextScanIn(p => { if (p <= 1) { runGlobalAnalysis(); return 1200; } return p - 1; });
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [isAutoUpdating, runGlobalAnalysis]);

  // --- Logic & UI Helpers ---
  const calculateTotalScore = useMemo(() => {
    const weights = { military: 0.35, maritime: 0.20, aviation: 0.15, cyber: 0.15, diplomacy: 0.15 };
    const getAvg = (obj) => {
      const v = Object.values(obj || {});
      return v.length ? v.reduce((a, b) => a + Number(b), 0) / v.length : 0;
    };
    const s = Object.keys(weights).reduce((a, c) => a + (getAvg(data[c]) * weights[c]), 0);
    return Math.min(100, Math.round(s * 1.3));
  }, [data]);

  const getLabel = (k) => {
    const labels = {
      warRisk: "ביטוח ימי", oilAnomaly: "מחירי נפט", polymarket: "הימורי 'כסף חכם'", rialCollapse: "הריאל האיראני", khargEvac: "ריקון ח'ארג",
      israeliFleet: "פינוי אל-על", saudiEscat: "נוהל ESCAT", iranCancels: "ביטולי טיסות", vipFlights: "מטוסי VIP",
      ussGeorgia: "USS Georgia", tankerBridge: "מטוסי תדלוק", bomberDeploy: "מפציצי B-52", bunkerSealing: "איטום בונקרים", irgcUnderground: "בכירי IRGC",
      gpsJamming: "שיבושי GPS", internetBlackout: "ניתוקי אינטרנט", proxyChatter: "שיח פרוקסי", sigintSpikes: "פטפטת קשר", cyberWaves: "גלי סייבר",
      envoyWatch: "מטוס השליח", embassyEvac: "פינוי שגרירויות", hospitalAlert: "כוננות בתי חולים", summitDeception: "הונאה אסטרטגית"
    };
    return labels[k] || k;
  };

  if (!isSystemReady) {
    return (
      <div className="min-h-screen bg-black flex flex-col items-center justify-center gap-6 p-8">
        <Activity className="text-red-500 animate-pulse" size={64} />
        <div className="text-center space-y-2">
          <h1 className="text-white font-black text-2xl tracking-widest">INITIALIZING DEFCON-OSINT</h1>
          <p className="text-slate-600 font-mono text-xs uppercase animate-bounce italic">Establishing cloud synchronization nodes...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#020305] text-slate-100 font-sans selection:bg-red-500/30">
      <audio ref={audioRef} hidden />
      
      {/* HUD Header */}
      <nav className="sticky top-0 z-50 bg-black/80 backdrop-blur-xl border-b border-white/5 px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <ShieldAlert className="text-red-600 drop-shadow-[0_0_10px_rgba(220,38,38,0.5)]" size={32} />
          <div>
            <h1 className="font-black tracking-tighter text-2xl uppercase italic leading-none">DEFCON TRACKER</h1>
            <span className="text-[9px] text-slate-500 font-mono tracking-[0.2em]">NODE: OSINT-TAU-01</span>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
           <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-emerald-500/5 border border-emerald-500/20 rounded-xl text-[9px] font-mono text-emerald-400">
             <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
             LIVE_DATA_SYNC
           </div>
           <div className="bg-red-600/10 border border-red-600/30 text-red-500 px-4 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-widest">
             Level: {calculateTotalScore > 75 ? 'Critical' : 'Elevated'}
           </div>
        </div>
      </nav>

      {/* Main Interface */}
      <main className="max-w-7xl mx-auto p-4 md:p-10 grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Probability Dashboard */}
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-[#080b12] border border-white/10 rounded-[3rem] p-12 text-center relative overflow-hidden shadow-2xl">
             <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-red-500 to-transparent opacity-40" />
             <span className="text-[10px] font-black text-slate-600 uppercase tracking-[0.5em] block mb-6">Escalation Probability</span>
             <div className={`text-[130px] font-black leading-none tracking-tighter ${calculateTotalScore > 75 ? 'text-red-600' : 'text-white'}`}>
               {calculateTotalScore}<span className="text-3xl text-slate-800">%</span>
             </div>
             <div className="mt-8 space-y-4">
                <div className={`px-5 py-2 rounded-full text-[11px] font-black inline-block border ${calculateTotalScore > 75 ? 'bg-red-600/10 border-red-600 text-red-500' : 'bg-emerald-600/10 border-emerald-600 text-emerald-500'}`}>
                  {calculateTotalScore > 75 ? 'WAR WINDOW DETECTED' : 'SURVEILLANCE BASELINE'}
                </div>
                <div className="text-[10px] font-mono text-slate-500 flex justify-center items-center gap-2">
                  <Clock size={12} className="text-blue-500" /> 
                  NEXT SCAN: <span className="text-blue-400 font-bold">{Math.floor(nextScanIn/60)}:{(nextScanIn%60).toString().padStart(2,'0')}</span>
                </div>
             </div>
          </div>

          {/* AI Strategic Intelligence */}
          <div className="bg-white/5 border border-white/10 rounded-[2.5rem] p-8 backdrop-blur-3xl space-y-6 shadow-2xl">
             <div className="flex items-center justify-between">
                <h3 className="text-xs font-black text-white flex items-center gap-2 uppercase tracking-widest">
                   <BrainCircuit size={18} className="text-indigo-400" /> Strategic AI Sitrep
                </h3>
                <Terminal size={14} className="text-slate-600" />
             </div>
             
             {sitrep ? (
               <div className="space-y-4 animate-in slide-in-from-bottom-4 duration-500">
                  <div className="bg-black/50 p-6 rounded-3xl border border-white/5 text-sm leading-relaxed text-slate-300 rtl text-right max-h-60 overflow-y-auto font-medium">
                    {sitrep}
                  </div>
                  <div className="flex gap-2">
                    <button onClick={playAudioBriefing} disabled={isAudioLoading} className="flex-1 bg-white/10 hover:bg-white/20 border border-white/10 py-3 rounded-2xl text-[10px] font-black flex items-center justify-center gap-2 transition-all">
                      {isAudioLoading ? <RefreshCw className="animate-spin" size={14} /> : <Volume2 size={14} />}
                      VOICE BRIEFING
                    </button>
                    <button onClick={() => setSitrep("")} className="px-4 bg-white/5 border border-white/10 rounded-2xl text-slate-500 hover:text-white transition-all">
                      <X size={16} />
                    </button>
                  </div>
               </div>
             ) : (
               <button onClick={generateSitrep} disabled={isGeneratingSitrep} className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-white py-5 rounded-2xl font-black text-xs shadow-xl shadow-indigo-900/30 flex items-center justify-center gap-3 transition-all">
                 {isGeneratingSitrep ? <RefreshCw className="animate-spin" size={18} /> : <Zap size={18} />}
                 GENERATE STRATEGIC REPORT
               </button>
             )}
          </div>
        </div>

        {/* Matrix Controls */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          <div className="flex gap-2 overflow-x-auto pb-4 no-scrollbar">
            {[
              { id: 'military', Icon: Crosshair, label: 'צבא' },
              { id: 'maritime', Icon: Ship, label: 'כלכלה' },
              { id: 'aviation', Icon: Plane, label: 'תעופה' },
              { id: 'cyber', Icon: Radio, label: 'סייבר' },
              { id: 'diplomacy', Icon: Landmark, label: 'ממשל' }
            ].map(({ id, Icon, label }) => (
              <button
                key={id}
                onClick={() => setActiveCategory(id)}
                className={`flex items-center gap-4 px-10 py-6 rounded-[2rem] font-black text-sm transition-all border shrink-0 ${
                  activeCategory === id ? 'bg-white text-black border-white shadow-2xl scale-105' : 'bg-white/5 border-white/5 text-slate-500 hover:bg-white/10'
                }`}
              >
                <Icon size={18} /> {label}
              </button>
            ))}
          </div>

          <div className="bg-[#080b12]/50 border border-white/10 rounded-[3.5rem] p-10 md:p-14 min-h-[600px] backdrop-blur-xl">
             <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-12">
               {data[activeCategory] && Object.entries(data[activeCategory]).map(([key, value]) => (
                 <div key={key} className="space-y-4">
                    <div className="flex justify-between items-end">
                      <div>
                        <span className="text-[10px] font-bold text-slate-600 uppercase tracking-widest">{key}</span>
                        <h4 className="text-base font-black text-white mt-1">{getLabel(key)}</h4>
                      </div>
                      <span className={`font-mono text-2xl font-black ${Number(value) > 70 ? 'text-red-500' : 'text-blue-500'}`}>
                        {Number(value)}%
                      </span>
                    </div>
                    <div className="relative h-2.5 w-full bg-white/5 rounded-full overflow-hidden shadow-inner">
                      <div className={`h-full transition-all duration-1000 rounded-full ${Number(value) > 70 ? 'bg-red-600 shadow-[0_0_15px_rgba(239,68,68,0.5)]' : 'bg-blue-600 shadow-[0_0_15px_rgba(37,99,235,0.3)]'}`} style={{ width: `${Number(value)}%` }} />
                      <input type="range" min="0" max="100" value={Number(value)} onChange={(e) => {
                        const val = parseInt(e.target.value);
                        const newData = { ...data, [activeCategory]: { ...data[activeCategory], [key]: val } };
                        setData(newData);
                        updateCloudData(newData);
                      }} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-20" />
                    </div>
                 </div>
               ))}
             </div>

             <div className="mt-20 p-8 border border-white/5 bg-white/5 rounded-[2.5rem] flex items-start gap-6">
                <div className="p-4 bg-blue-500/10 rounded-2xl text-blue-400">
                   <Info size={28} />
                </div>
                <div>
                   <h5 className="text-sm font-black text-white mb-2 uppercase">Sync Protocol Active</h5>
                   <p className="text-xs text-slate-500 leading-relaxed italic">
                     This interface is a live satellite terminal. Any modifications to the matrix will be mirrored across all active Defcon nodes. AI sweep engines update the baseline every 20 minutes using global OSINT signals.
                   </p>
                </div>
             </div>
          </div>
        </div>
      </main>

      <footer className="max-w-7xl mx-auto p-12 opacity-20 text-[9px] font-mono flex flex-col md:flex-row justify-between items-center gap-4 uppercase tracking-[0.3em]">
         <div className="flex gap-6">
            <span>Asset: {appId}</span>
            <span>Cipher: AES-512</span>
         </div>
         <div className="flex gap-6">
            <span>Model: {MODEL_NAME}</span>
            <span>Sync: ONLINE</span>
         </div>
      </footer>
    </div>
  );
};

export default App;
