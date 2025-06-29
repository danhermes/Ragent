#!/usr/bin/env python3
"""
Master test script for Cliff - Runs all tests and provides comprehensive report
"""

import sys
import subprocess
import time
from pathlib import Path

def run_test(test_name, test_script):
    """Run a test script and return results"""
    print(f"\n{'='*60}")
    print(f"Running {test_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, test_script],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0, result.stdout
        
    except subprocess.TimeoutExpired:
        print(f"[ERROR] {test_name} timed out")
        return False, "Timeout"
    except Exception as e:
        print(f"[ERROR] {test_name} failed: {e}")
        return False, str(e)

def main():
    """Run all tests"""
    print("Cliff Complete Test Suite")
    print("=" * 60)
    print("This will test all components of Cliff:")
    print("1. Backend (Flask API)")
    print("2. Frontend (React)")
    print("3. Integration (Backend + Frontend)")
    print("=" * 60)
    
    # Get the tests directory
    tests_dir = Path(__file__).parent
    tests = [
        ("Backend Tests", tests_dir / "test_backend.py"),
        ("Frontend Tests", tests_dir / "test_frontend.py"),
        ("Integration Tests", tests_dir / "test_integration.py")
    ]
    
    results = []
    total_tests = len(tests)
    passed_tests = 0
    
    for test_name, test_script in tests:
        if not test_script.exists():
            print(f"[ERROR] Test script {test_script} not found")
            results.append((test_name, False, "Test script not found"))
            continue
        
        success, output = run_test(test_name, str(test_script))
        results.append((test_name, success, output))
        
        if success:
            passed_tests += 1
            print(f"[SUCCESS] {test_name} PASSED")
        else:
            print(f"[ERROR] {test_name} FAILED")
        
        # Brief pause between tests
        time.sleep(2)
    
    # Final report
    print(f"\n{'='*60}")
    print("FINAL TEST REPORT")
    print(f"{'='*60}")
    
    for test_name, success, output in results:
        status = "[SUCCESS] PASS" if success else "[ERROR] FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} test suites passed")
    
    if passed_tests == total_tests:
        print("\n[SUCCESS] ALL TESTS PASSED!")
        print("Cliff is fully functional and ready to use.")
        print("\nTo start Cliff:")
        print("1. Backend: python flask_backend.py")
        print("2. Frontend: npm start")
        print("3. Browser: http://localhost:3000")
        return 0
    else:
        print(f"\n[ERROR] {total_tests - passed_tests} test suite(s) failed.")
        print("Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 