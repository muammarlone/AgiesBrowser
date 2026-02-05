
import React from 'react';
import { Cpu, Terminal, Eye, Brain } from 'lucide-react';

const AgentHub = ({ status }) => {
    const agents = [
        { id: 'genius', name: 'Genius (L4)', icon: <Brain size={16} />, status: 'Online', color: 'text-purple-400' },
        { id: 'uat', name: 'UAT Helper', icon: <Eye size={16} />, status: 'Active', color: 'text-green-400' },
        { id: 'devops', name: 'DevOps Worker', icon: <Terminal size={16} />, status: 'Idle', color: 'text-blue-400' }
    ];

    return (
        <div className="space-y-4 p-4 bg-black/20 rounded-xl border border-white/5 backdrop-blur-md">
            <h3 className="text-[10px] font-bold tracking-[0.2em] text-neutral-500 uppercase">Agent Hub</h3>
            <div className="space-y-2">
                {agents.map(agent => (
                    <div key={agent.id} className="flex items-center justify-between p-2 rounded-lg bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
                        <div className="flex items-center gap-3">
                            <div className={`${agent.color} opacity-80`}>{agent.icon}</div>
                            <span className="text-xs font-medium text-neutral-200">{agent.name}</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className={`w-1.5 h-1.5 rounded-full ${agent.status === 'Online' || agent.status === 'Active' ? 'bg-green-500' : 'bg-neutral-500'} animate-pulse`}></div>
                            <span className={`text-[9px] font-mono ${agent.color}`}>{agent.status}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AgentHub;
