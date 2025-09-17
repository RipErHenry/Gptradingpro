#!/usr/bin/env python3
"""
GPTading Pro Backend API Tests
Tests all backend endpoints for the trading bot platform
"""

import requests
import json
import time
import os
from datetime import datetime
from typing import Dict, Any

# Get backend URL from frontend .env
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except:
        pass
    return "https://realtime-profit-bot.preview.emergentagent.com"

BASE_URL = get_backend_url()
API_URL = f"{BASE_URL}/api"

class GPTadingAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.test_results = []
        self.created_bot_id = None
        
    def log_test(self, test_name: str, success: bool, message: str, response_data: Any = None):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'response_data': response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if response_data and not success:
            print(f"   Response: {response_data}")
    
    def test_health_check(self):
        """Test API health check endpoint"""
        try:
            response = self.session.get(f"{API_URL}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log_test("Health Check", True, f"API is healthy - {data}")
                else:
                    self.log_test("Health Check", False, f"Unexpected health status: {data}")
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
    
    def test_zaffex_connection(self):
        """Test Zaffex broker connection simulation"""
        try:
            # Test connection with valid credentials format (>=20 chars)
            connection_data = {
                "api_key": "test_api_key_12345678901234567890",
                "api_secret": "test_api_secret_12345678901234567890",
                "test_mode": True
            }
            
            response = self.session.post(f"{API_URL}/zaffex/connect", 
                                       json=connection_data, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if "balance_info" in data:
                    self.log_test("Zaffex Connection", True, 
                                f"Connected successfully - Balance: ${data['balance_info']['total_balance']}")
                else:
                    self.log_test("Zaffex Connection", False, f"Missing balance info: {data}")
            else:
                self.log_test("Zaffex Connection", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Zaffex Connection", False, f"Connection error: {str(e)}")
    
    def test_zaffex_status(self):
        """Test Zaffex connection status"""
        try:
            response = self.session.get(f"{API_URL}/zaffex/status", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                is_connected = data.get('is_connected', False)
                self.log_test("Zaffex Status", True, 
                            f"Status retrieved - Connected: {is_connected}")
            else:
                self.log_test("Zaffex Status", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Zaffex Status", False, f"Error: {str(e)}")
    
    def test_zaffex_balance(self):
        """Test getting Zaffex account balance"""
        try:
            response = self.session.get(f"{API_URL}/zaffex/balance", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "total_balance" in data:
                    self.log_test("Zaffex Balance", True, 
                                f"Balance retrieved - Total: ${data['total_balance']}")
                else:
                    self.log_test("Zaffex Balance", False, f"Missing balance data: {data}")
            elif response.status_code == 400:
                # Expected if not connected
                self.log_test("Zaffex Balance", True, 
                            "Expected error - No active connection (need to connect first)")
            else:
                self.log_test("Zaffex Balance", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Zaffex Balance", False, f"Error: {str(e)}")
    
    def test_market_data(self):
        """Test getting market data"""
        try:
            response = self.session.get(f"{API_URL}/zaffex/market-data", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    market_info = data["data"][0]
                    self.log_test("Market Data", True, 
                                f"Market data retrieved - {market_info['symbol']}: ${market_info['price']}")
                else:
                    self.log_test("Market Data", False, f"No market data returned: {data}")
            else:
                self.log_test("Market Data", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Market Data", False, f"Error: {str(e)}")
    
    def test_create_bot(self):
        """Test creating a trading bot"""
        try:
            bot_data = {
                "name": "Test Trading Bot",
                "strategy": "Grid Trading",
                "risk_level": "Medio",
                "initial_investment": 5000.0,
                "max_investment_per_trade": 250.0,
                "stop_loss_percentage": 3.0,
                "take_profit_percentage": 8.0
            }
            
            response = self.session.post(f"{API_URL}/bots/", json=bot_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "id" in data:
                    self.created_bot_id = data["id"]
                    self.log_test("Create Bot", True, 
                                f"Bot created successfully - ID: {data['id']}, Name: {data['name']}")
                else:
                    self.log_test("Create Bot", False, f"Missing bot ID: {data}")
            else:
                self.log_test("Create Bot", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Create Bot", False, f"Error: {str(e)}")
    
    def test_list_bots(self):
        """Test listing user bots"""
        try:
            response = self.session.get(f"{API_URL}/bots/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("List Bots", True, 
                                f"Retrieved {len(data)} bots")
                    if len(data) > 0:
                        print(f"   First bot: {data[0]['name']} - Status: {data[0]['status']}")
                else:
                    self.log_test("List Bots", False, f"Expected list, got: {type(data)}")
            else:
                self.log_test("List Bots", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("List Bots", False, f"Error: {str(e)}")
    
    def test_activate_bot(self):
        """Test activating a trading bot"""
        if not self.created_bot_id:
            self.log_test("Activate Bot", False, "No bot ID available (create bot first)")
            return
            
        try:
            response = self.session.post(f"{API_URL}/bots/{self.created_bot_id}/activate", 
                                       timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    self.log_test("Activate Bot", True, 
                                f"Bot activated - {data['message']}")
                else:
                    self.log_test("Activate Bot", False, f"Unexpected response: {data}")
            elif response.status_code == 400:
                # Expected if Zaffex not connected
                self.log_test("Activate Bot", True, 
                            "Expected error - Need Zaffex connection first")
            else:
                self.log_test("Activate Bot", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Activate Bot", False, f"Error: {str(e)}")
    
    def test_bot_performance(self):
        """Test getting bot performance metrics"""
        if not self.created_bot_id:
            self.log_test("Bot Performance", False, "No bot ID available")
            return
            
        try:
            response = self.session.get(f"{API_URL}/bots/{self.created_bot_id}/performance", 
                                      timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "total_trades" in data:
                    self.log_test("Bot Performance", True, 
                                f"Performance data - Trades: {data['total_trades']}, ROI: {data['roi']:.2f}%")
                else:
                    self.log_test("Bot Performance", False, f"Missing performance data: {data}")
            else:
                self.log_test("Bot Performance", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Bot Performance", False, f"Error: {str(e)}")
    
    def test_portfolio(self):
        """Test getting user portfolio"""
        try:
            response = self.session.get(f"{API_URL}/portfolio/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "total_balance" in data:
                    self.log_test("Portfolio", True, 
                                f"Portfolio retrieved - Balance: ${data['total_balance']}, P/L: ${data.get('total_profit_loss', 0)}")
                else:
                    self.log_test("Portfolio", False, f"Missing portfolio data: {data}")
            else:
                self.log_test("Portfolio", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Portfolio", False, f"Error: {str(e)}")
    
    def test_portfolio_holdings(self):
        """Test getting portfolio asset holdings"""
        try:
            response = self.session.get(f"{API_URL}/portfolio/holdings", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Portfolio Holdings", True, 
                                f"Holdings retrieved - {len(data)} assets")
                else:
                    self.log_test("Portfolio Holdings", False, f"Expected list: {data}")
            else:
                self.log_test("Portfolio Holdings", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Portfolio Holdings", False, f"Error: {str(e)}")
    
    def test_portfolio_performance(self):
        """Test getting portfolio performance metrics"""
        try:
            response = self.session.get(f"{API_URL}/portfolio/performance", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "summary" in data:
                    summary = data["summary"]
                    self.log_test("Portfolio Performance", True, 
                                f"Performance data - Trades: {summary['total_trades']}, Win Rate: {summary['win_rate']:.1f}%")
                else:
                    self.log_test("Portfolio Performance", False, f"Missing summary: {data}")
            else:
                self.log_test("Portfolio Performance", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Portfolio Performance", False, f"Error: {str(e)}")
    
    def test_automated_trading_flow(self):
        """Test the complete automated trading flow"""
        print("\n🔄 Testing Complete Automated Trading Flow...")
        
        # Step 1: Connect to Zaffex
        self.test_zaffex_connection()
        time.sleep(1)
        
        # Step 2: Create a bot
        self.test_create_bot()
        time.sleep(1)
        
        # Step 3: Try to activate bot (should work now that Zaffex is connected)
        if self.created_bot_id:
            try:
                response = self.session.post(f"{API_URL}/bots/{self.created_bot_id}/activate", 
                                           timeout=10)
                
                if response.status_code == 200:
                    self.log_test("Automated Trading Flow", True, 
                                "Bot activated successfully - Trading automation started")
                    
                    # Wait a bit to see if trading loop starts
                    print("   Waiting 10 seconds to check for automated trading...")
                    time.sleep(10)
                    
                    # Check bot performance for any trades
                    self.test_bot_performance()
                    
                else:
                    self.log_test("Automated Trading Flow", False, 
                                f"Failed to activate bot: {response.text}")
                    
            except Exception as e:
                self.log_test("Automated Trading Flow", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all backend tests"""
        print(f"🚀 Starting GPTading Pro Backend Tests")
        print(f"📡 Testing API at: {API_URL}")
        print("=" * 60)
        
        # Basic API tests
        self.test_health_check()
        time.sleep(0.5)
        
        # Zaffex integration tests
        self.test_zaffex_status()
        time.sleep(0.5)
        
        self.test_market_data()
        time.sleep(0.5)
        
        # Bot management tests
        self.test_create_bot()
        time.sleep(0.5)
        
        self.test_list_bots()
        time.sleep(0.5)
        
        # Portfolio tests
        self.test_portfolio()
        time.sleep(0.5)
        
        self.test_portfolio_holdings()
        time.sleep(0.5)
        
        self.test_portfolio_performance()
        time.sleep(0.5)
        
        # Test activation without Zaffex connection first
        self.test_activate_bot()
        time.sleep(0.5)
        
        # Test balance without connection
        self.test_zaffex_balance()
        time.sleep(0.5)
        
        # Test complete automated trading flow
        self.test_automated_trading_flow()
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        if total - passed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  • {result['test']}: {result['message']}")
        
        print("\n✅ CRITICAL ENDPOINTS STATUS:")
        critical_tests = [
            "Health Check",
            "Zaffex Connection", 
            "Create Bot",
            "Portfolio",
            "Market Data"
        ]
        
        for test_name in critical_tests:
            result = next((r for r in self.test_results if r['test'] == test_name), None)
            if result:
                status = "✅" if result['success'] else "❌"
                print(f"  {status} {test_name}")

if __name__ == "__main__":
    tester = GPTadingAPITester()
    tester.run_all_tests()