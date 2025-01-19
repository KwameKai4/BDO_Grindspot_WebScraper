const { contextBridge, ipcRenderer } = require('electron');

// Expose secure Electron APIs to the renderer process
contextBridge.exposeInMainWorld('electronAPI', {
    runPython: () => ipcRenderer.send('run-python'),
    onPythonOutput: (callback) => ipcRenderer.on('python-output', (event, output) => callback(output))
});