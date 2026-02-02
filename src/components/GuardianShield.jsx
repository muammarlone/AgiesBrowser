import React, { useState, useEffect } from 'react';
import { Shield, ShieldAlert, Lock, Globe } from 'lucide-react';

const GuardianShield = ({ secureScore }) => {
    const [status, setStatus] = useState('secure');

    useEffect(() => {
        if (secureScore === 100) setStatus('secure');
        else if (secureScore < 50) setStatus('danger');
        else setStatus('warning');
    }, [secureScore]);

    return (
        <div className={`flex items-center gap-2 px-3 py-1 bg-white/5 border border-white/10 rounded-full transition-colors ${status === 'secure' ? 'border-green-500/30' : 'border-red-500/30'}`}>
            {status === 'secure' ? (
                <Shield size={14} className="text-green-400" />
            ) : (
                <ShieldAlert size={14} className="text-red-500 animate-pulse" />
            )}
            <span className={`text-xs font-mono ${status === 'secure' ? 'text-green-400' : 'text-red-400'}`}>
                GUARDIAN {status === 'secure' ? 'ACTIVE' : 'ALERT'}
            </span>
        </div>
    );
};

export default GuardianShield;
