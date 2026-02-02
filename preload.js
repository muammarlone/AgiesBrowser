const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('aegis', {
    // Platform control
    minimize: () => ipcRenderer.send('window-minimize'),
    maximize: () => ipcRenderer.send('window-maximize'),
    close: () => ipcRenderer.send('window-close'),

    // Browser functionality
    createTab: (url) => ipcRenderer.send('create-tab', url),

    // Guardian Security
    getSecurityReport: () => ipcRenderer.invoke('guardian-get-report'),
    onSecurityAlert: (callback) => ipcRenderer.on('security-alert', callback)
});
