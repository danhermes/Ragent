# Cliff Startup Script (PowerShell version for Windows)
# Shuts down any running backend/frontend, checks environment, then starts both

Write-Host "Starting Cliff AI Speech Assistant..." -ForegroundColor Green

# Kill any process using port 3000 (React dev server)
Write-Host "[CLIFF] Checking for React dev server on port 3000..." -ForegroundColor Yellow
$process3000 = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($process3000) {
    Write-Host "[CLIFF] Killing React dev server (PID $process3000)" -ForegroundColor Yellow
    Stop-Process -Id $process3000 -Force
} else {
    Write-Host "[CLIFF] No React dev server running." -ForegroundColor Yellow
}

# Kill any process using port 5000 (Flask backend)
Write-Host "[CLIFF] Checking for Flask backend on port 5000..." -ForegroundColor Yellow
$process5000 = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($process5000) {
    Write-Host "[CLIFF] Killing Flask backend (PID $process5000)" -ForegroundColor Yellow
    Stop-Process -Id $process5000 -Force
} else {
    Write-Host "[CLIFF] No Flask backend running." -ForegroundColor Yellow
}

# Use current Python environment (conda or system)
Write-Host "Using current Python environment..." -ForegroundColor Cyan
$pythonPath = (Get-Command python).Source
Write-Host "Python being used: $pythonPath" -ForegroundColor Cyan
python --version

# Check if we're in the right directory
if (-not (Test-Path "package.json") -or -not (Test-Path "flask_backend.py")) {
    Write-Host "Error: Please run this script from the cliff directory" -ForegroundColor Red
    Write-Host "   cd cliff && .\cliff.ps1" -ForegroundColor Red
    exit 1
}

# Check for .env file
if (-not (Test-Path "..\.env")) {
    Write-Host "Error: .env file not found in project root" -ForegroundColor Red
    Write-Host "   Please create ..\.env file with OPENAI_API_KEY=your_key" -ForegroundColor Red
    exit 1
}

# Check for Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Node.js not found" -ForegroundColor Red
    Write-Host "   Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check for Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python not found" -ForegroundColor Red
    Write-Host "   Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if node_modules exists, install if not
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing React dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to install React dependencies" -ForegroundColor Red
        exit 1
    }
}

# Function to cleanup background processes
function Cleanup {
    Write-Host ""
    Write-Host "Stopping Cliff..." -ForegroundColor Yellow
    if ($backendJob) {
        Stop-Job $backendJob -ErrorAction SilentlyContinue
        Remove-Job $backendJob -ErrorAction SilentlyContinue
        Write-Host "   Backend stopped" -ForegroundColor Yellow
    }
    if ($frontendJob) {
        Stop-Job $frontendJob -ErrorAction SilentlyContinue
        Remove-Job $frontendJob -ErrorAction SilentlyContinue
        Write-Host "   Frontend stopped" -ForegroundColor Yellow
    }
    exit 0
}

# Set up signal handlers
Register-EngineEvent PowerShell.Exiting -Action { Cleanup }

Write-Host "Starting Flask backend..." -ForegroundColor Green
$backendJob = Start-Job -ScriptBlock { 
    Set-Location $using:PWD
    python flask_backend.py 
}

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Check if backend started successfully
if ($backendJob.State -eq "Failed") {
    Write-Host "Error: Backend failed to start" -ForegroundColor Red
    exit 1
}

Write-Host "Backend running on http://localhost:5000" -ForegroundColor Green

Write-Host "Starting React frontend..." -ForegroundColor Green
$frontendJob = Start-Job -ScriptBlock { 
    Set-Location $using:PWD
    npm start 
}

# Wait a moment for frontend to start
Start-Sleep -Seconds 5

# Check if frontend started successfully
if ($frontendJob.State -eq "Failed") {
    Write-Host "Error: Frontend failed to start" -ForegroundColor Red
    Stop-Job $backendJob -ErrorAction SilentlyContinue
    Remove-Job $backendJob -ErrorAction SilentlyContinue
    exit 1
}

Write-Host "Frontend running on http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Cliff is ready!" -ForegroundColor Green
Write-Host "   Open your browser to: http://localhost:3000" -ForegroundColor Cyan
Write-Host "   Press Ctrl+C to stop" -ForegroundColor Cyan
Write-Host ""

# Wait for user to stop
try {
    while ($true) {
        Start-Sleep -Seconds 1
        if ($backendJob.State -eq "Failed" -or $frontendJob.State -eq "Failed") {
            Write-Host "One of the services has failed" -ForegroundColor Red
            break
        }
    }
} catch {
    Cleanup
} 