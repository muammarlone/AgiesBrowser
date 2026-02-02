const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        frame: false,
        titleBarStyle: 'hidden',
        backgroundColor: '#000000',
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            sandbox: true,
            preload: path.join(__dirname, 'preload.js'),
            webviewTag: true // Required for browser functionality
        }
    });

    // Load the local Vite dev server in development, or build in production
    // For this prototype setup with 'concurrently', we default to localhost:5173
    // But fall back to index.html if file exists and we are not in dev mode
    // We'll use a simple environment check or try-catch strategy

    const isDev = !app.isPackaged;

    if (isDev) {
        win.loadURL('http://localhost:5173');
        // win.webContents.openDevTools();
    } else {
        win.loadFile('dist/index.html'); // Vite standard build output
    }

    // Window Control Handlers
    ipcMain.on('window-minimize', () => win.minimize());
    ipcMain.on('window-maximize', () => {
        if (win.isMaximized()) win.unmaximize();
        else win.maximize();
    });
    ipcMain.on('window-close', () => win.close());

    // Guardian Security Integration (Real GADOS Bridge)
    ipcMain.handle('guardian-get-report', async (event, url = 'current') => {
        return new Promise((resolve) => {
            const { spawn } = require('child_process');
            // We pass a dummy content for now, or fetch it via the event sender if possible
            // In a real app, we would grab the webContents 'executeJavaScript' to get HTML

            const pythonProcess = spawn('python', [
                path.join(__dirname, 'guardian_bridge.py'),
                url,
                "<html><body>Checking Content...</body></html>" // Placeholder content
            ]);

            let dataString = '';

            pythonProcess.stdout.on('data', (data) => {
                dataString += data.toString();
            });

            pythonProcess.stderr.on('data', (data) => {
                console.error(`Guardian Bridge Error: ${data}`);
            });

            pythonProcess.on('close', (code) => {
                try {
                    const result = JSON.parse(dataString);
                    resolve(result);
                } catch (e) {
                    console.error("Failed to parse Guardian response", e);
                    resolve({ status: 'error', threatLevel: 'unknown', score: 0 });
                }
            });
        });
    });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
