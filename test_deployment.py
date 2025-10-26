#!/usr/bin/env python3
"""
Fashion Guru Bot - Deployment Test Suite
Comprehensive tests for the deployed bot
"""

import requests
import json
import sys
import time
from typing import Dict, Any

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

class BotTester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.passed = 0
        self.failed = 0

    def print_header(self, text: str):
        print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"{Colors.BLUE}{text}{Colors.END}")
        print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

    def print_test(self, name: str):
        print(f"{Colors.YELLOW}Testing: {name}...{Colors.END}")

    def print_pass(self, message: str):
        print(f"{Colors.GREEN}✓ {message}{Colors.END}")
        self.passed += 1

    def print_fail(self, message: str):
        print(f"{Colors.RED}✗ {message}{Colors.END}")
        self.failed += 1

    def test_health(self):
        """Test health endpoint"""
        self.print_test("Health Endpoint")

        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)

            if response.status_code == 200:
                self.print_pass(f"Status code: {response.status_code}")

                data = response.json()
                if data.get('status') == 'healthy':
                    self.print_pass("Bot is healthy")

                    modules = data.get('modules', [])
                    if len(modules) == 6:
                        self.print_pass(f"All 6 modules loaded: {', '.join(modules)}")
                    else:
                        self.print_fail(f"Expected 6 modules, got {len(modules)}")
                else:
                    self.print_fail("Bot is not healthy")
            else:
                self.print_fail(f"Status code: {response.status_code}")

        except Exception as e:
            self.print_fail(f"Request failed: {str(e)}")

    def test_chat(self, message: str, expected_module: str = None):
        """Test chat endpoint"""
        self.print_test(f"Chat: '{message[:50]}...'")

        try:
            payload = {
                "user_id": f"test_user_{int(time.time())}",
                "message": message
            }

            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                self.print_pass(f"Status code: {response.status_code}")

                data = response.json()
                if data.get('success'):
                    self.print_pass("Response successful")

                    bot_response = data.get('response', {}).get('message', '')
                    if len(bot_response) > 50:
                        self.print_pass(f"Got response ({len(bot_response)} chars)")
                        print(f"   Preview: {bot_response[:100]}...")
                    else:
                        self.print_fail("Response too short")

                    if expected_module:
                        actual_module = data.get('response', {}).get('module')
                        if actual_module == expected_module:
                            self.print_pass(f"Correct module: {actual_module}")
                        else:
                            self.print_fail(f"Expected {expected_module}, got {actual_module}")
                else:
                    self.print_fail(f"Request failed: {data.get('error')}")
            else:
                self.print_fail(f"Status code: {response.status_code}")

        except Exception as e:
            self.print_fail(f"Request failed: {str(e)}")

    def test_modules(self):
        """Test modules endpoint"""
        self.print_test("Modules Endpoint")

        try:
            response = requests.get(f"{self.base_url}/modules", timeout=10)

            if response.status_code == 200:
                self.print_pass(f"Status code: {response.status_code}")

                data = response.json()
                modules = data.get('modules', [])

                expected_modules = [
                    'pattern_intelligence',
                    'fabric_oracle',
                    'troubleshooting',
                    'trend_synthesis',
                    'color_psychology',
                    'design_critique'
                ]

                if set(modules) == set(expected_modules):
                    self.print_pass(f"All expected modules present")
                else:
                    self.print_fail(f"Module mismatch")
                    print(f"   Expected: {expected_modules}")
                    print(f"   Got: {modules}")
            else:
                self.print_fail(f"Status code: {response.status_code}")

        except Exception as e:
            self.print_fail(f"Request failed: {str(e)}")

    def test_stats(self):
        """Test stats endpoint"""
        self.print_test("Stats Endpoint")

        try:
            response = requests.get(f"{self.base_url}/stats", timeout=10)

            if response.status_code == 200:
                self.print_pass(f"Status code: {response.status_code}")

                data = response.json()
                if 'active_conversations' in data and 'modules_loaded' in data:
                    self.print_pass(f"Stats: {data}")
                else:
                    self.print_fail("Missing expected fields")
            else:
                self.print_fail(f"Status code: {response.status_code}")

        except Exception as e:
            self.print_fail(f"Request failed: {str(e)}")

    def run_all_tests(self):
        """Run comprehensive test suite"""
        self.print_header("Fashion Guru Bot - Deployment Test Suite")
        print(f"Testing: {self.base_url}\n")

        # Basic endpoint tests
        self.print_header("Basic Endpoint Tests")
        self.test_health()
        self.test_modules()
        self.test_stats()

        # Module-specific tests
        self.print_header("Pillar 1: Technical Mastery Tests")

        self.test_chat(
            "What fabric should I use for a summer dress?",
            "fabric_oracle"
        )

        self.test_chat(
            "How do I draft a basic skirt pattern?",
            "pattern_intelligence"
        )

        self.test_chat(
            "My seams are puckering, what should I do?",
            "troubleshooting"
        )

        self.print_header("Pillar 2: Creative Evolution Tests")

        self.test_chat(
            "What are the current fashion trends?",
            "trend_synthesis"
        )

        self.test_chat(
            "What does the color red mean in fashion?",
            "color_psychology"
        )

        self.test_chat(
            "I would like feedback on my design",
            "design_critique"
        )

        # Results
        self.print_header("Test Results")
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0

        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.failed}{Colors.END}")
        print(f"Pass Rate: {pass_rate:.1f}%\n")

        if self.failed == 0:
            print(f"{Colors.GREEN}✓ All tests passed! Bot is working correctly.{Colors.END}\n")
            return 0
        else:
            print(f"{Colors.RED}✗ Some tests failed. Please check the logs.{Colors.END}\n")
            return 1

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_deployment.py <bot-url>")
        print("Example: python test_deployment.py https://fashion-guru-bot-xxxxx.run.app")
        sys.exit(1)

    bot_url = sys.argv[1]
    tester = BotTester(bot_url)

    try:
        exit_code = tester.run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
