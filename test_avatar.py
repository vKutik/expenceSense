#!/usr/bin/env python3
"""
Test script to check avatar API functionality
"""

import requests
import json

BOT_TOKEN = "8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4"
USER_ID = 489146762

def test_telegram_api():
    """Test Telegram API directly"""
    print("🔍 Testing Telegram API directly...")
    
    # Get user profile photos
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUserProfilePhotos"
    params = {
        'user_id': USER_ID,
        'limit': 1
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    print(f"Response: {json.dumps(data, indent=2)}")
    
    if data.get('ok') and data.get('result', {}).get('total_count', 0) > 0:
        print("✅ User has profile photos")
        
        # Get the file_id of the profile photo
        photos = data['result']['photos'][0]
        file_id = photos[-1]['file_id']  # Get the largest size
        
        print(f"📷 File ID: {file_id}")
        
        # Get file path
        file_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile"
        file_params = {'file_id': file_id}
        file_response = requests.get(file_url, params=file_params)
        file_data = file_response.json()
        
        print(f"File response: {json.dumps(file_data, indent=2)}")
        
        if file_data.get('ok'):
            file_path = file_data['result']['file_path']
            avatar_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            
            print(f"🖼️ Avatar URL: {avatar_url}")
            
            # Test if URL is accessible
            img_response = requests.get(avatar_url)
            print(f"🖼️ Image response status: {img_response.status_code}")
            
            if img_response.status_code == 200:
                print("✅ Avatar URL is accessible!")
            else:
                print("❌ Avatar URL is not accessible")
        else:
            print("❌ Failed to get file path")
    else:
        print("❌ No profile photos found")

def test_our_api():
    """Test our API endpoint"""
    print("\n🔍 Testing our API endpoint...")
    
    url = f"https://snake-j86alylhc-volodymyr-s-projects-9f0184a4.vercel.app/api/user/avatar/{USER_ID}"
    response = requests.get(url)
    data = response.json()
    
    print(f"Our API response: {json.dumps(data, indent=2)}")
    
    if data.get('success'):
        print("✅ Our API works!")
        avatar_url = data.get('avatar_url')
        if avatar_url:
            print(f"🖼️ Avatar URL: {avatar_url}")
    else:
        print("❌ Our API failed")

if __name__ == "__main__":
    test_telegram_api()
    test_our_api()
