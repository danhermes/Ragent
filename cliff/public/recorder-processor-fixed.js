// recorder-processor.js

class RecorderProcessor extends AudioWorkletProcessor {
  constructor(options) {
    super();
    try {
      this._buffer = [];
      this._threshold = 0.02; // Audio gate threshold (adjust as needed)
      this._sampleRate = options?.processorOptions?.sampleRate || sampleRate || 16000;
      this._frameSize = 128;
      this._silenceCount = 0;
      this._maxSilenceFrames = Math.floor(this._sampleRate / this._frameSize * 1.5); // 1.5 seconds
      this._speaking = false;
      this._chunkCounter = 0;
      this._chunkSize = 10; // Send chunks every 10 frames
      this._totalSamples = 0;
      
      console.log("[RecorderProcessor] Initialized with sampleRate:", this._sampleRate);
    } catch (e) {
      console.error("[RecorderProcessor] Init error:", e);
    }
  }

  process(inputs) {
    try {
      const input = inputs[0];
      if (input.length > 0) {
        const channel = input[0];
        let rms = 0;

        for (let i = 0; i < channel.length; i++) {
          const sample = channel[i];
          rms += sample * sample;
        }
        rms = Math.sqrt(rms / channel.length);

        const aboveThreshold = rms > this._threshold;

        if (aboveThreshold) {
          this._silenceCount = 0;
          if (!this._speaking) {
            this._speaking = true;
            this.port.postMessage({ type: "speech" });
            console.log("[RecorderProcessor] Speech detected, RMS:", rms);
          }
        } else {
          this._silenceCount++;
          if (this._silenceCount > this._maxSilenceFrames) {
            if (this._speaking) {
              this._speaking = false;
              this.port.postMessage({ type: "silence-and-stop" });
              console.log("[RecorderProcessor] Silence detected, stopping");
            }
          }
        }

        // Always buffer audio
        this._buffer.push(...channel);
        this._chunkCounter++;
        this._totalSamples += channel.length;

        // Send chunks periodically
        if (this._chunkCounter >= this._chunkSize) {
          const chunkSize = this._buffer.length;
          this.port.postMessage({ 
            type: "chunk", 
            payload: [...this._buffer] 
          });
          console.log("[RecorderProcessor] Sent chunk with", chunkSize, "samples, total samples:", this._totalSamples);
          this._buffer = []; // Clear buffer after sending
          this._chunkCounter = 0;
        }
      }
      return true;
    } catch (e) {
      console.error("[RecorderProcessor] Process error:", e);
      return false;
    }
  }
}

registerProcessor("record-processor", RecorderProcessor);
