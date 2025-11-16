#!/usr/bin/env python3
"""
Environment Testing Script for OpenSpace Django Application
Tests both development and production Docker environments
"""

import subprocess
import time
import requests
import sys
from urllib.parse import urljoin

class EnvironmentTester:
    def __init__(self):
        self.dev_url = "http://localhost:8000"
        self.prod_url = "http://localhost:8001"  # Different port for local prod testing
        
    def run_command(self, command, cwd=None):
        """Run shell command and return result"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                cwd=cwd
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def wait_for_service(self, url, timeout=60):
        """Wait for service to be available"""
        print(f"⏳ Waiting for service at {url}...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code < 500:
                    print(f"✅ Service available at {url}")
                    return True
            except requests.exceptions.RequestException:
                pass
            time.sleep(2)
        
        print(f"❌ Service not available at {url} after {timeout}s")
        return False
    
    def test_endpoints(self, base_url):
        """Test common endpoints"""
        endpoints = [
            "/",
            "/admin/",
            "/api/",
            "/graphql/",
        ]
        
        results = {}
        for endpoint in endpoints:
            url = urljoin(base_url, endpoint)
            try:
                response = requests.get(url, timeout=10, allow_redirects=True)
                results[endpoint] = {
                    "status": response.status_code,
                    "accessible": response.status_code < 500
                }
                status_icon = "✅" if response.status_code < 500 else "❌"
                print(f"  {status_icon} {endpoint}: {response.status_code}")
            except requests.exceptions.RequestException as e:
                results[endpoint] = {"status": "ERROR", "accessible": False}
                print(f"  ❌ {endpoint}: ERROR - {str(e)}")
        
        return results
    
    def test_development(self):
        """Test development environment"""
        print("\n🔧 Testing Development Environment")
        print("=" * 50)
        
        # Stop any running containers
        print("🛑 Stopping existing containers...")
        self.run_command("docker-compose -f docker-compose.dev.yml down")
        
        # Build and start development
        print("🏗️ Building development environment...")
        success, stdout, stderr = self.run_command("docker-compose -f docker-compose.dev.yml build")
        if not success:
            print(f"❌ Build failed: {stderr}")
            return False
        
        print("🚀 Starting development environment...")
        success, stdout, stderr = self.run_command("docker-compose -f docker-compose.dev.yml up -d")
        if not success:
            print(f"❌ Start failed: {stderr}")
            return False
        
        # Wait for services
        if not self.wait_for_service(self.dev_url):
            return False
        
        # Test endpoints
        print("🧪 Testing development endpoints...")
        results = self.test_endpoints(self.dev_url)
        
        # Check container status
        print("📊 Container status:")
        success, stdout, stderr = self.run_command("docker-compose -f docker-compose.dev.yml ps")
        print(stdout)
        
        return all(result["accessible"] for result in results.values())
    
    def test_production(self):
        """Test production environment"""
        print("\n🏭 Testing Production Environment")
        print("=" * 50)
        
        # Stop any running containers
        print("🛑 Stopping existing containers...")
        self.run_command("docker-compose -f docker-compose.prod.yml down")
        
        # Build and start production
        print("🏗️ Building production environment...")
        success, stdout, stderr = self.run_command("docker-compose -f docker-compose.prod.yml build")
        if not success:
            print(f"❌ Build failed: {stderr}")
            return False
        
        # Modify docker-compose for local testing (different port)
        print("🚀 Starting production environment...")
        # Note: You might need to modify docker-compose.prod.yml to use port 8001 for local testing
        success, stdout, stderr = self.run_command("docker-compose -f docker-compose.prod.yml up -d")
        if not success:
            print(f"❌ Start failed: {stderr}")
            return False
        
        # Wait for services (using port 80 since nginx handles it)
        if not self.wait_for_service("http://localhost"):
            return False
        
        # Test endpoints
        print("🧪 Testing production endpoints...")
        results = self.test_endpoints("http://localhost")
        
        # Check container status
        print("📊 Container status:")
        success, stdout, stderr = self.run_command("docker-compose -f docker-compose.prod.yml ps")
        print(stdout)
        
        # Security checks
        print("🔒 Security checks:")
        self.check_production_security()
        
        return all(result["accessible"] for result in results.values())
    
    def check_production_security(self):
        """Check production security settings"""
        try:
            response = requests.get("http://localhost", timeout=10)
            headers = response.headers
            
            security_headers = {
                "X-Frame-Options": "SAMEORIGIN",
                "X-Content-Type-Options": "nosniff",
                "X-XSS-Protection": "1; mode=block"
            }
            
            for header, expected in security_headers.items():
                if header in headers:
                    print(f"  ✅ {header}: {headers[header]}")
                else:
                    print(f"  ⚠️ {header}: Missing")
                    
        except Exception as e:
            print(f"  ❌ Security check failed: {e}")
    
    def cleanup(self):
        """Clean up test environments"""
        print("\n🧹 Cleaning up...")
        self.run_command("docker-compose -f docker-compose.dev.yml down")
        self.run_command("docker-compose -f docker-compose.prod.yml down")
        print("✅ Cleanup complete")
    
    def run_tests(self):
        """Run all tests"""
        print("🧪 OpenSpace Environment Testing")
        print("=" * 50)
        
        try:
            # Test development
            dev_success = self.test_development()
            
            # Test production
            prod_success = self.test_production()
            
            # Results
            print("\n📋 Test Results")
            print("=" * 50)
            print(f"Development: {'✅ PASS' if dev_success else '❌ FAIL'}")
            print(f"Production:  {'✅ PASS' if prod_success else '❌ FAIL'}")
            
            if dev_success and prod_success:
                print("\n🎉 All tests passed! Ready for deployment.")
                return True
            else:
                print("\n⚠️ Some tests failed. Check logs above.")
                return False
                
        except KeyboardInterrupt:
            print("\n⏹️ Tests interrupted by user")
            return False
        finally:
            self.cleanup()

if __name__ == "__main__":
    tester = EnvironmentTester()
    success = tester.run_tests()
    sys.exit(0 if success else 1)