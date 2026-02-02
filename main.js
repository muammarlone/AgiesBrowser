const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        frame: false, // Frameless for custom UI
        titleBarStyle: 'hidden',
        backgroundColor: '#000000',
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false, // For MVP Prototype speed
            webviewTag: true // Critical for browser functionality
        }
    });

    // Load the React App
    // In dev, usually localhost:5173. In prod, index.html.
    // For this prototype, we'll assume we can load the build or a simple file.
    // We will load the file directly for simplicity in this constrained env.
    win.loadFile('index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
