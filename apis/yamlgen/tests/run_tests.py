import sys
from pathlib import Path
import unittest

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from tests.test_generator import TestYAMLGenerator

def main():
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestYAMLGenerator)
    
    # Run the tests with verbosity level 2
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    # Exit with appropriate code
    sys.exit(not result.wasSuccessful())

if __name__ == '__main__':
    main() 