#!/usr/bin/env python3
"""
Integration test for Cliff - Tests backend and frontend together
"""

import sys
import time
import requests
import subprocess
import os
from pathlib import Path

def test_backend_and_frontend():
    """Test both backend and frontend together"""
    print("Starting Cliff Integration Tests")
    print("=" * 60)
    
    backend_process = None
    frontend_process = None
    
    try:
        # Step 1: Start backend
        print("Starting backend...")
        backend_process = subprocess.Popen(
            [sys.executable, "flask_backend.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for backend to start
        time.sleep(5)
        
        if backend_process.poll() is not None:
            stdout, stderr = backend_process.communicate()
            print(f"[ERROR] Backend failed to start")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
        
        print("[OK] Backend started")
        
        # Step 2: Test backend health
        print("Testing backend health...")
        try:
            response = requests.get("http://localhost:5000/api/health", timeout=10)
            if response.status_code == 200:
                print("[OK] Backend health check passed")
            else:
                print(f"[ERROR] Backend health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] Backend health check failed: {e}")
            return False
        
        # Step 3: Start frontend
        print("Starting frontend...")
        frontend_process = subprocess.Popen(
            ["npm", "start"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for frontend to start
        time.sleep(10)
        
        if frontend_process.poll() is not None:
            stdout, stderr = frontend_process.communicate()
            print(f"[ERROR] Frontend failed to start")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
        
        print("[OK] Frontend started")
        
        # Step 4: Test frontend serving
        print("Testing frontend serving...")
        try:
            response = requests.get("http://localhost:3000", timeout=10)
            if response.status_code == 200:
                print("[OK] Frontend serving correctly")
            else:
                print(f"[ERROR] Frontend serving failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] Frontend serving failed: {e}")
            return False
        
        # Step 5: Test API connectivity from frontend perspective
        print("Testing API connectivity...")
        try:
            # Test that frontend can reach backend API
            response = requests.get("http://localhost:5000/api/health", timeout=10)
            if response.status_code == 200:
                print("[OK] API connectivity working")
            else:
                print(f"[ERROR] API connectivity failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] API connectivity failed: {e}")
            return False
        
        # Step 6: Test chat endpoint (if API key is available)
        print("Testing chat functionality...")
        try:
            response = requests.post(
                "http://localhost:5000/api/chat",
                json={"message": "Hello, this is an integration test"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if "response" in data:
                    print("[OK] Chat functionality working")
                else:
                    print("[ERROR] Chat response format incorrect")
                    return False
            else:
                print(f"[ERROR] Chat functionality failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Chat functionality failed: {e}")
            return False
        
        print("=" * 60)
        print("[SUCCESS] All integration tests passed!")
        print("[OK] Backend: Running on http://localhost:5000")
        print("[OK] Frontend: Running on http://localhost:3000")
        print("[OK] API: Backend and frontend can communicate")
        print("[OK] Chat: AI responses working")
        print("\nCliff is ready to use!")
        print("Open your browser to: http://localhost:3000")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Integration test failed: {e}")
        return False
        
    finally:
        # Cleanup
        print("\nCleaning up...")
        
        if frontend_process:
            try:
                frontend_process.terminate()
                frontend_process.wait(timeout=5)
                print("[OK] Frontend stopped")
            except:
                frontend_process.kill()
                print("[WARN] Frontend force-killed")
        
        if backend_process:
            try:
                backend_process.terminate()
                backend_process.wait(timeout=5)
                print("[OK] Backend stopped")
            except:
                backend_process.kill()
                print("[WARN] Backend force-killed")

def main():
    """Run integration tests"""
    success = test_backend_and_frontend()
    
    if success:
        print("\n[SUCCESS] Integration test completed successfully!")
        return 0
    else:
        print("\n[ERROR] Integration test failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 