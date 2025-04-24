# YAML Generator Tests

This directory contains test files for the YAML Generator module. The tests verify the functionality of generating YAML files for different tools (AutoCoder and LitLegos).

## Test Files

- `test_generator.py`: Main test file containing test cases
- `run_tests.py`: Script to run the test suite
- Test specification files:
  - `test_framework_spec.yaml`: Input spec for AutoCoder test framework
  - `test_framework_expected.yaml`: Expected output for AutoCoder test framework
  - `webapp_spec.yaml`: Input spec for AutoCoder webapp
  - `webapp_expected.yaml`: Expected output for AutoCoder webapp
  - `tech_writing_spec.yaml`: Input spec for LitLegos tech writing
  - `tech_writing_expected.yaml`: Expected output for LitLegos tech writing

## Running Tests

To run the tests, use one of the following commands:

```bash
# Using the test runner script
python run_tests.py

# Using unittest directly
python -m unittest discover -v tests
```

## Test Structure

The tests verify that:
1. YAML files are correctly generated from input specifications
2. The generated YAML matches the expected output format
3. Both AutoCoder and LitLegos formats are handled correctly

Each test case:
1. Loads an input specification file
2. Generates YAML using the YAMLGenerator
3. Compares the generated output with the expected output file 