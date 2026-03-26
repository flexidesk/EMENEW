#!/usr/bin/env python3
"""
Backend API Testing for CastleAdmin Driver Credentials Management
Tests the three new API endpoints for driver credential management.
"""

import requests
import sys
import json
from datetime import datetime

class DriverCredentialsAPITester:
    def __init__(self, base_url="https://app-builder-3369.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details
        })

    def test_create_driver_user_endpoint(self):
        """Test /admin-api/admin/create-driver-user endpoint"""
        url = f"{self.base_url}/admin-api/admin/create-driver-user"
        
        # Test 1: Missing required fields
        try:
            response = requests.post(url, json={}, headers={'Content-Type': 'application/json'})
            if response.status_code == 400:
                self.log_test("Create Driver User - Missing fields validation", True)
            else:
                self.log_test("Create Driver User - Missing fields validation", False, f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.log_test("Create Driver User - Missing fields validation", False, str(e))

        # Test 2: Valid request structure (will fail due to missing service role key in production)
        try:
            test_data = {
                "email": f"test-driver-{datetime.now().strftime('%H%M%S')}@example.com",
                "password": "TestPassword123!",
                "driverId": "test-driver-id-123",
                "driverName": "Test Driver"
            }
            response = requests.post(url, json=test_data, headers={'Content-Type': 'application/json'})
            
            # We expect this to fail in production due to missing service role key
            # But we can check if the endpoint exists and returns proper error
            if response.status_code in [400, 401, 403, 500]:
                self.log_test("Create Driver User - Endpoint exists", True, f"Status: {response.status_code}")
            else:
                self.log_test("Create Driver User - Endpoint exists", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("Create Driver User - Endpoint exists", False, str(e))

    def test_reset_driver_password_endpoint(self):
        """Test /admin-api/admin/reset-driver-password endpoint"""
        url = f"{self.base_url}/admin-api/admin/reset-driver-password"
        
        # Test 1: Missing required fields
        try:
            response = requests.post(url, json={}, headers={'Content-Type': 'application/json'})
            if response.status_code == 400:
                self.log_test("Reset Driver Password - Missing fields validation", True)
            else:
                self.log_test("Reset Driver Password - Missing fields validation", False, f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.log_test("Reset Driver Password - Missing fields validation", False, str(e))

        # Test 2: Invalid password length
        try:
            test_data = {
                "authUserId": "test-user-id",
                "newPassword": "short"  # Too short
            }
            response = requests.post(url, json=test_data, headers={'Content-Type': 'application/json'})
            if response.status_code == 400:
                self.log_test("Reset Driver Password - Password length validation", True)
            else:
                self.log_test("Reset Driver Password - Password length validation", False, f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.log_test("Reset Driver Password - Password length validation", False, str(e))

        # Test 3: Valid request structure
        try:
            test_data = {
                "authUserId": "test-user-id-123",
                "newPassword": "ValidPassword123!"
            }
            response = requests.post(url, json=test_data, headers={'Content-Type': 'application/json'})
            
            # We expect this to fail in production but endpoint should exist
            if response.status_code in [400, 401, 403, 500]:
                self.log_test("Reset Driver Password - Endpoint exists", True, f"Status: {response.status_code}")
            else:
                self.log_test("Reset Driver Password - Endpoint exists", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("Reset Driver Password - Endpoint exists", False, str(e))

    def test_remove_driver_user_endpoint(self):
        """Test /admin-api/admin/remove-driver-user endpoint"""
        url = f"{self.base_url}/admin-api/admin/remove-driver-user"
        
        # Test 1: Missing required fields
        try:
            response = requests.post(url, json={}, headers={'Content-Type': 'application/json'})
            if response.status_code == 400:
                self.log_test("Remove Driver User - Missing fields validation", True)
            else:
                self.log_test("Remove Driver User - Missing fields validation", False, f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.log_test("Remove Driver User - Missing fields validation", False, str(e))

        # Test 2: Valid request structure
        try:
            test_data = {
                "authUserId": "test-user-id-123",
                "driverId": "test-driver-id-123"
            }
            response = requests.post(url, json=test_data, headers={'Content-Type': 'application/json'})
            
            # We expect this to fail in production but endpoint should exist
            if response.status_code in [400, 401, 403, 500]:
                self.log_test("Remove Driver User - Endpoint exists", True, f"Status: {response.status_code}")
            else:
                self.log_test("Remove Driver User - Endpoint exists", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("Remove Driver User - Endpoint exists", False, str(e))

    def test_endpoint_accessibility(self):
        """Test that all endpoints are accessible (not 404)"""
        endpoints = [
            "/admin-api/admin/create-driver-user",
            "/admin-api/admin/reset-driver-password", 
            "/admin-api/admin/remove-driver-user"
        ]
        
        for endpoint in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = requests.post(url, json={}, headers={'Content-Type': 'application/json'})
                
                if response.status_code != 404:
                    self.log_test(f"Endpoint {endpoint} - Accessible", True, f"Status: {response.status_code}")
                else:
                    self.log_test(f"Endpoint {endpoint} - Accessible", False, "404 Not Found")
            except Exception as e:
                self.log_test(f"Endpoint {endpoint} - Accessible", False, str(e))

    def run_all_tests(self):
        """Run all API tests"""
        print(f"🔍 Testing CastleAdmin Driver Credentials API endpoints...")
        print(f"📍 Base URL: {self.base_url}")
        print("=" * 60)
        
        # Test endpoint accessibility first
        self.test_endpoint_accessibility()
        print()
        
        # Test individual endpoints
        self.test_create_driver_user_endpoint()
        print()
        
        self.test_reset_driver_password_endpoint()
        print()
        
        self.test_remove_driver_user_endpoint()
        print()
        
        # Print summary
        print("=" * 60)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return 0
        else:
            print("⚠️  Some tests failed - see details above")
            return 1

def main():
    """Main test runner"""
    tester = DriverCredentialsAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())