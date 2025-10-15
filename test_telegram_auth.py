"""
Test Telegram authentication
"""
import requests
import json

def test_telegram_auth():
    """Test Telegram authentication endpoint"""
    print("🧪 Testing Telegram Authentication")
    print("=" * 40)
    
    # Test data - replace with real Telegram user data
    test_user = {
        "id": 489146762,
        "first_name": "Вова",
        "username": "kutikv",
        "language_code": "en"
    }
    
    url = "https://snake-gcaeog0dh-volodymyr-s-projects-9f0184a4.vercel.app/api/auth/authenticate"
    
    try:
        response = requests.post(url, json={
            "telegramData": test_user,
            "initData": "test_init_data"
        }, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Authentication successful!")
            print(f"User: {data.get('user', {})}")
            return True
        else:
            print("❌ Authentication failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_app_access():
    """Test direct app access"""
    print("\n🌐 Testing App Access")
    print("=" * 40)
    
    url = "https://snake-gcaeog0dh-volodymyr-s-projects-9f0184a4.vercel.app"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ App accessible")
            return True
        else:
            print(f"❌ App not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_categories():
    """Test categories endpoint"""
    print("\n🏷️ Testing Categories")
    print("=" * 40)
    
    url = "https://snake-gcaeog0dh-volodymyr-s-projects-9f0184a4.vercel.app/api/categories"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Categories loaded")
            print(f"Categories: {len(data.get('categories', []))}")
            return True
        else:
            print(f"❌ Categories failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 Telegram Authentication Debug")
    print("=" * 50)
    
    tests = [
        test_app_access,
        test_categories,
        test_telegram_auth
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed")

if __name__ == "__main__":
    main()
