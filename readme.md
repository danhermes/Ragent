## Start:
## streamlit run "n:/2025/AI Development/Cursor Projects/Ragents/main.py"


## "n:/2025/AI Development/Cursor Projects/Ragents/llama.cpp/build/bin/Release/llama-cli.exe" -m "n:/2025/AI Development/Cursor Projects/Ragents/llama.cpp/tinyllama-1.1b-chat.gguf" -n 512 -c 512 -sys "Speak in single sentence responses of only a few words." -prompt "Hey Neville, what's up?" -no-mmap -ngl 0

powershell_cmd = f'& "{self.llama_cli_path}" "-m" "{self.model_path}" "--temp" "{self.temperature}" "-n" "512" "-c" "512" "--prompt" "{text}"'