#  Run ONCE ONLY to build the Docker image for the agent sandbox
#  cd...../Ragents/autocoder
#  execute $ ./build_image_ONCE_ONLY.sh

echo "Building Docker image: autocoder_agent_sandbox"
docker build -t autocoder_agent_sandbox -f Dockerfile .

if [ $? -eq 0 ]; then
    echo "✅ autocoder_agent_sandbox image built successfully."
else
    echo "❌ Docker build failed."
fi

