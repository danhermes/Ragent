# Build Docker image for autocoder
Write-Host "Building Docker image for autocoder..."

# Get the directory containing this script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Build the Docker image
docker build -t autocoder_agent_sandbox -f "$scriptDir\Dockerfile" $scriptDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "Docker image built successfully!"
} else {
    Write-Host "Failed to build Docker image."
    exit 1
} 