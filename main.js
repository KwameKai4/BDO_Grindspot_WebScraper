const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { exec, spawn } = require('child_process');

// Store reference to the Flask server process
let flaskProcess;

// Create the main Electron window
let win;
function createWindow() {
    win = new BrowserWindow({
        width: 500,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true, // Enables security
            nodeIntegration: false,
        },
    });

    win.loadFile('index.html'); // Load the frontend (index.html)
}

// Start the Flask server
function startFlaskServer() {
    const flaskScriptPath = path.join(__dirname, 'server.py'); // Path to server.py
    flaskProcess = spawn('python', [flaskScriptPath]);

    flaskProcess.stdout.on('data', (data) => {
        console.log(`Flask server: ${data}`);
    });

    flaskProcess.stderr.on('data', (data) => {
        console.error(`Flask error: ${data}`);
    });

    flaskProcess.on('close', (code) => {
        console.log(`Flask server exited with code ${code}`);
    });
}

// Stop Flask server when application closes
app.on('quit', () => {
    if (flaskProcess) {
        flaskProcess.kill();
    }
});

// Event: When the app is ready
app.on('ready', () => {
    startFlaskServer(); // Start Flask server
    createWindow(); // Create Electron window
});

// Event: Quit the app when all windows are closed
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

// IPC event: Run the Python script
ipcMain.on('run-python', (event) => {
    const botPath = path.join(__dirname, 'bot.py'); // Full path to bot.py
    exec(`python "${botPath}"`, (error, stdout, stderr) => { // Wrap botPath in quotes
        if (error) {
            event.sender.send('python-output', `Error: ${error.message}`);
            return;
        }
        if (stderr) {
            event.sender.send('python-output', `Error: ${stderr}`);
            return;
        }
        event.sender.send('python-output', stdout);
    });
});