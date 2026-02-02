import React, { useState, useEffect } from 'react';
import GuardianShield from './components/GuardianShield';
import { ArrowLeft, ArrowRight, RotateCw, Globe, Shield } from 'lucide-react';

// Use window.aegis exposed from preload
const aegis = window.aegis;

const App = () => {
    const [url, setUrl] = useState('https://www.google.com');
    const [inputUrl, setInputUrl] = useState('https://www.google.com');
    const [secureScore, setSecureScore] = useState(100);
    const [isSidebarOpen, setSidebarOpen] = useState(true);
    const [logs, setLogs] = useState([]);

    const log = (msg, type = 'info') => {
        setLogs(prev => [...prev, { time: new Date().toLocaleTimeString(), msg, type }].slice(-20));
    };

    const handleNavigate = (e) => {
        e.preventDefault();
        let target = inputUrl;
        if (!target.startsWith('http')) target = 'https://' + target;
        setUrl(target);
        log(`Navigating to ${target}`, 'nav');
        setSecureScore(null); // Reset score on nav
    };

    const handleWindowControl = (action) => {
        if (aegis && aegis[action]) aegis[action]();
    };

    const handleScan = async () => {
        setSecureScore('scanning');
        log("Initiating GADOS Guardian Connection...", 'warn');

        try {
            const report = await window.aegis.getSecurityReport(inputUrl);

            if (report.status === 'secure') {
                setSecureScore(report.score || 100);
                log(`GADOS Verification: PASS (Score: ${report.score})`, 'success');
            } else if (report.status === 'warning') {
                setSecureScore(report.score || 60);
                log(`GADOS Verification: WARNING - ${report.message || 'Issues found'}`, 'danger');
            } else {
                setSecureScore(report.score || 0);
                log(`GADOS Verification: BLOCKED - ${report.message || 'Critical Threat'}`, 'danger');
            }

            // Log detailed breakdown if available
            if (report.breakdown) {
                Object.entries(report.breakdown).forEach(([dim, score]) => {
                    if (dim !== 'overall' && score < 0.7) {
                        log(`Alert: ${dim} score is low (${(score * 100).toFixed(0)}%)`, 'danger');
                    }
                });
            }

        } catch (e) {
            setSecureScore(0);
            log("GADOS Connection Failed", 'danger');
        }
    };

    return (
        <div className="flex h-screen w-screen bg-black text-white overflow-hidden font-sans">
            {/* Titlebar / Drag Region */}
            <div className="absolute top-0 left-0 w-full h-10 app-drag-region z-50 pointer-events-none" style={{ WebkitAppRegion: 'drag' }} />
            <div className="aurora-bg"></div>

            <div className="flex-1 flex flex-col z-10">
                {/* Header */}
                <header className="glass-header h-14 bg-neutral-900 border-b border-white/5 flex items-center px-4 gap-4 z-50">
                    {/* Window Controls (Mac Style) */}
                    <div className="flex gap-2 z-50 opacity-60 hover:opacity-100 transition-opacity" style={{ WebkitAppRegion: 'no-drag' }}>
                        <button onClick={() => handleWindowControl('close')} className="w-3 h-3 rounded-full bg-red-500 hover:opacity-80"></button>
                        <button onClick={() => handleWindowControl('minimize')} className="w-3 h-3 rounded-full bg-yellow-500 hover:opacity-80"></button>
                        <button onClick={() => handleWindowControl('maximize')} className="w-3 h-3 rounded-full bg-green-500 hover:opacity-80"></button>
                    </div>

                    <div className="w-px h-6 bg-white/10 mx-2"></div>

                    {/* Navigation */}
                    <div className="flex gap-2 text-neutral-400 z-50" style={{ WebkitAppRegion: 'no-drag' }}>
                        <button className="p-1 hover:text-white hover:bg-white/10 rounded"><ArrowLeft size={16} /></button>
                        <button className="p-1 hover:text-white hover:bg-white/10 rounded"><ArrowRight size={16} /></button>
                        <button className="p-1 hover:text-white hover:bg-white/10 rounded"><RotateCw size={16} /></button>
                    </div>

                    {/* Omnibox */}
                    <form onSubmit={handleNavigate} className="flex-1 max-w-2xl mx-auto z-50" style={{ WebkitAppRegion: 'no-drag' }}>
                        <div className={`omnibox relative group flex items-center bg-black/40 border border-white/10 rounded-xl px-3 py-1.5 ${secureScore === 100 ? 'border-green-500/50' : secureScore === 60 ? 'border-yellow-500/50' : secureScore === 0 ? 'border-red-500/50' : ''}`}>
                            <div className="mr-2 text-gray-400">
                                <Globe size={14} className="text-neutral-500" />
                            </div>
                            <input
                                type="text"
                                value={inputUrl}
                                onChange={(e) => setInputUrl(e.target.value)}
                                className="bg-transparent border-none outline-none text-sm w-full text-neutral-200 placeholder-neutral-500 font-medium"
                            />
                            {secureScore === 'scanning' ? (
                                <div className="animate-spin text-blue-400"><RotateCw size={14} /></div>
                            ) : (
                                <button type="button" onClick={handleScan} className="text-xs bg-white/5 hover:bg-white/10 text-gray-300 px-2 py-0.5 rounded border border-white/10 transition-colors">
                                    VERIFY
                                </button>
                            )}
                        </div>
                    </form>

                    <button onClick={() => setSidebarOpen(!isSidebarOpen)} className={`p-2 rounded hover:bg-white/10 transition-colors ${isSidebarOpen ? 'text-blue-400' : 'text-gray-400'}`} style={{ WebkitAppRegion: 'no-drag' }}>
                        <Shield size={18} />
                    </button>
                </header>

                {/* Content Area */}
                <main className="flex-1 relative bg-white/5">
                    {/* Webview Tag */}
                    <webview src={url} className="w-full h-full" allowpopups="true"></webview>
                </main>
            </div>

            {/* Guardian Sidebar */}
            {isSidebarOpen && (
                <div className={`glass-panel w-80 flex flex-col border-l border-white/10 transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] z-50`}>
                    <div className="p-4 border-b border-white/5 flex items-center justify-between">
                        <h2 className="text-xs font-bold tracking-widest text-gray-400 uppercase">Aegis Intelligence</h2>
                        <div className="flex gap-2">
                            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                            <span className="text-[10px] text-green-500 font-mono">ONLINE</span>
                        </div>
                    </div>

                    <div className="p-4 space-y-4 flex-1 overflow-y-auto">
                        <div className="bg-black/40 rounded-lg p-3 border border-white/5">
                            <div className="flex items-center gap-2 mb-2">
                                <Shield size={14} className="text-blue-400" />
                                <span className="text-sm font-medium">GADOS Guardian v2</span>
                            </div>
                            <div className="flex justify-between items-end">
                                <div className="text-2xl font-bold font-mono text-white">
                                    {typeof secureScore === 'number' ? `${secureScore}%` : '--'}
                                </div>
                                <div className="text-[10px] text-gray-500">TRUST SCORE</div>
                            </div>
                            <div className="w-full h-1 bg-white/10 mt-2 rounded-full overflow-hidden">
                                <div className={`h-full transition-all duration-1000 ${secureScore === 100 ? 'bg-green-500 w-full' : secureScore >= 60 ? 'bg-yellow-500 w-[60%]' : 'bg-red-500 w-[20%]'}`}></div>
                            </div>
                        </div>

                        {/* Live Log */}
                        <div className="font-mono text-[10px] text-gray-400 space-y-1">
                            <div className="uppercase text-gray-600 mb-2 font-bold">System Stream</div>
                            {logs.map((l, i) => (
                                <div key={i} className={`flex gap-2 ${l.type === 'nav' ? 'text-blue-300' : l.type === 'success' ? 'text-green-400' : l.type === 'danger' ? 'text-red-400' : ''}`}>
                                    <span className="opacity-50">[{l.time}]</span>
                                    <span>{l.msg}</span>
                                </div>
                            ))}
                        </div>

                    </div>
                </div>
            )}
        </div>
    );
};

export default App;
