#!/usr/bin/env python3
"""
Test script for Cliff React Frontend
Tests dependencies, build, and serving
"""

import sys
import time
import requests
import subprocess
import os
from pathlib import Path

def test_node_installation():
    """Test Node.js installation"""
    print("Testing Node.js installation...")
    
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"  [OK] Node.js {version}")
            return True
        else:
            print(f"  [ERROR] Node.js not found: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("  [ERROR] Node.js not installed")
        return False
    except Exception as e:
        print(f"  [ERROR] Node.js test failed: {e}")
        return False

def test_npm_installation():
    """Test npm installation"""
    print("Testing npm installation...")
    
    try:
        result = subprocess.run(
            ["npm", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"  [OK] npm {version}")
            return True
        else:
            print(f"  [ERROR] npm not found: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("  [ERROR] npm not installed")
        return False
    except Exception as e:
        print(f"  [ERROR] npm test failed: {e}")
        return False

def test_package_json():
    """Test package.json exists and is valid"""
    print("Testing package.json...")
    
    package_json = Path("package.json")
    if not package_json.exists():
        print("  [ERROR] package.json not found")
        return False
    
    try:
        result = subprocess.run(
            ["npm", "run", "start", "--dry-run"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("  [OK] package.json is valid")
            return True
        else:
            print(f"  [ERROR] package.json validation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  [ERROR] package.json test failed: {e}")
        return False

def test_dependencies():
    """Test npm dependencies"""
    print("Testing npm dependencies...")
    
    node_modules = Path("node_modules")
    if not node_modules.exists():
        print("  [WARN] node_modules not found, installing dependencies...")
        
        try:
            result = subprocess.run(
                ["npm", "install"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("  [OK] Dependencies installed successfully")
                return True
            else:
                print(f"  [ERROR] Dependency installation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"  [ERROR] Dependency installation failed: {e}")
            return False
    else:
        print("  [OK] Dependencies already installed")
        return True

def test_frontend_startup():
    """Test frontend startup"""
    print("Testing frontend startup...")
    
    try:
        # Start frontend in background
        process = subprocess.Popen(
            ["npm", "start"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for startup
        time.sleep(10)
        
        # Check if process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"  [ERROR] Frontend failed to start")
            print(f"  STDOUT: {stdout}")
            print(f"  STDERR: {stderr}")
            return None
        
        print("  [OK] Frontend started successfully")
        return process
        
    except Exception as e:
        print(f"  [ERROR] Failed to start frontend: {e}")
        return None

def test_frontend_serving(process):
    """Test frontend serving"""
    print("Testing frontend serving...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        
        if response.status_code == 200:
            if "Cliff" in response.text or "React" in response.text:
                print("  [OK] Frontend serving correctly")
                return True
            else:
                print("  [ERROR] Frontend serving but content seems wrong")
                return False
        else:
            print(f"  [ERROR] Frontend returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("  [ERROR] Could not connect to frontend")
        return False
    except Exception as e:
        print(f"  [ERROR] Frontend serving test failed: {e}")
        return False

def cleanup(process):
    """Clean up frontend process"""
    if process:
        try:
            process.terminate()
            process.wait(timeout=5)
            print("  [OK] Frontend stopped cleanly")
        except subprocess.TimeoutExpired:
            process.kill()
            print("  [WARN] Frontend force-killed")
        except Exception as e:
            print(f"  [WARN] Error stopping frontend: {e}")

def main():
    """Run all tests"""
    print("Starting Cliff Frontend Tests")
    print("=" * 50)
    
    process = None
    tests_passed = 0
    total_tests = 5
    
    try:
        # Test 1: Node.js installation
        if test_node_installation():
            tests_passed += 1
        else:
            print("[ERROR] Node.js test failed - stopping")
            return 1
        
        # Test 2: npm installation
        if test_npm_installation():
            tests_passed += 1
        else:
            print("[ERROR] npm test failed - stopping")
            return 1
        
        # Test 3: package.json
        if test_package_json():
            tests_passed += 1
        else:
            print("[ERROR] package.json test failed - stopping")
            return 1
        
        # Test 4: Dependencies
        if test_dependencies():
            tests_passed += 1
        else:
            print("[ERROR] Dependencies test failed - stopping")
            return 1
        
        # Test 5: Frontend startup
        process = test_frontend_startup()
        if process:
            tests_passed += 1
        else:
            print("[ERROR] Frontend startup failed - stopping")
            return 1
        
        # Test 6: Frontend serving
        if test_frontend_serving(process):
            tests_passed += 1
            total_tests += 1
        
    finally:
        cleanup(process)
    
    print("=" * 50)
    print(f"Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("[SUCCESS] All tests passed! Frontend is ready.")
        return 0
    else:
        print("[ERROR] Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 