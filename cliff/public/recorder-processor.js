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
      
      // Chunk sending configuration
      this._chunkSize = Math.floor(this._sampleRate * 0.5); // Send chunks every 0.5 seconds
      this._chunkCounter = 0;
      this._totalSamples = 0;
      
      console.log('[RecorderProcessor] Initialized with sampleRate:', this._sampleRate);
    } catch (e) {
      console.error('[RecorderProcessor] Init error:', e);
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
            this.port.postMessage({ type: 'speech' });
            console.log('[RecorderProcessor] Speech detected');
          }
        } else {
          this._silenceCount++;
          if (this._silenceCount > this._maxSilenceFrames) {
            if (this._speaking) {
              this._speaking = false;
              this.port.postMessage({ type: 'silence-and-stop' });
              console.log('[RecorderProcessor] Silence detected, stopping');
            }
          }
        }

        // Always buffer audio
        this._buffer.push(...channel);
        this._totalSamples += channel.length;
        
        // Send chunks periodically
        if (this._buffer.length >= this._chunkSize) {
          const chunk = this._buffer.splice(0, this._chunkSize);
          this.port.postMessage({
            type: 'chunk',
            data: chunk,
            chunkIndex: this._chunkCounter++,
            totalSamples: this._totalSamples
          });
          console.log('[RecorderProcessor] Sent chunk', this._chunkCounter - 1, 'with', chunk.length, 'samples');
        }
      }
      return true;
    } catch (e) {
      console.error('[RecorderProcessor] Process error:', e);
      return false;
    }
  }
}

registerProcessor('record-processor', RecorderProcessor);
