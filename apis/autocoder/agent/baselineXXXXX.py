import os
import torch
import numpy as np
import random
import pickle
import logging
import argparse

# Set up logging to know exactly what’s happening (because the show must go on!)
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def set_deterministic(seed=42):
    """
    Sets seeds across different libraries for repeatable, deterministic behavior.
    """
    logging.info("Setting deterministic seeds...")
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

# Imagine this function is generated dynamically from your spec.
def generated_function(input_tensor):
    """
    Autocoder-generated function as per the spec.
    For demonstration, it doubles the input tensor.
    """
    return input_tensor * 2

def create_baseline_data(input_data, baseline_file='baseline.pkl'):
    """
    Runs the verified golden reference (your autocoder's spec output) on the input data
    and saves the resulting baseline output to a file.
    """
    logging.info("Creating baseline data from input...")
    golden_output = generated_function(input_data)
    with open(baseline_file, 'wb') as f:
        pickle.dump(golden_output, f)
    logging.info("Baseline data saved to %s", baseline_file)
    return golden_output

def load_baseline_data(baseline_file='baseline.pkl'):
    """
    Loads the baseline output (golden data) from a file.
    """
    if os.path.exists(baseline_file):
        with open(baseline_file, 'rb') as f:
            data = pickle.load(f)
        logging.info("Loaded baseline data from %s", baseline_file)
        return data
    else:
        logging.warning("Baseline file %s not found.", baseline_file)
        return None

def run_test(input_data, baseline_data, rtol=1e-4, atol=1e-5):
    """
    Runs the test by comparing current output from generated_function against the baseline data.
    Uses PyTorch's tolerance-based assertion to check the correctness.
    """
    logging.info("Running test on dynamic output...")
    current_output = generated_function(input_data)
    torch.testing.assert_allclose(current_output, baseline_data, rtol=rtol, atol=atol)
    logging.info("Test passed: current output matches baseline data!")

def main(update_baseline=False, baseline_file='baseline.pkl'):
    # Step 1: Prepare the deterministic runtime.
    set_deterministic(42)

    # Step 2: Generate your dynamic test input (from your spec).
    input_tensor = torch.tensor([1.0, 2.0, 3.0])
    logging.info("Input tensor: %s", input_tensor)

    # Step 3: Produce or load the golden baseline data.
    if update_baseline or not os.path.exists(baseline_file):
        baseline_data = create_baseline_data(input_tensor, baseline_file=baseline_file)
    else:
        baseline_data = load_baseline_data(baseline_file)
        if baseline_data is None:
            # Fallback: create baseline if file missing.
            baseline_data = create_baseline_data(input_tensor, baseline_file=baseline_file)

    # Step 4: Run your dynamically generated test.
    run_test(input_tensor, baseline_data)
    logging.info("All dynamic tests completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamic Autocoder Test Runner")
    parser.add_argument("--update-baseline", action="store_true", help="Force update of baseline data.")
    args = parser.parse_args()
    main(update_baseline=args.update_baseline)
    
    
    
    #Documentation : How baseline.py Works:
    # Determinism First: The set_deterministic() function seeds PyTorch, NumPy, and Python’s random library so your behavior is as predictable as a metronome.

    # Dynamic Input & Golden Run: The script creates a simple input tensor and runs your generated function (here, simply doubling the tensor) to produce a baseline ("golden") output.

    # Baseline Management: If the baseline file (baseline.pkl) doesn’t exist or you explicitly tell it to update, it creates and saves fresh baseline data.

    # Test Execution: Finally, the test compares the current output from generated_function to your saved baseline using a tolerance-based assertion.

    # This whole enchilada gives you a complete workflow—from preparing your dynamic environment to validating the correctness of your autocoder’s generated code. Run it with the --update-baseline flag when you want to lock in a new set of golden outputs, or simply run it to check against the current baseline. Enjoy taming your dynamic testing beast!

    # Updated spec, regenerate baseline data: python dynamic_test.py --update-baseline

    # Run test against current baseline: python dynamic_test.py

