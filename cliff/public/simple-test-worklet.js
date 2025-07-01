class SimpleTestProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    console.log('SimpleTestProcessor initialized');
  }

  process(inputs, outputs, parameters) {
    return true;
  }
}

registerProcessor('simple-test-processor', SimpleTestProcessor); 