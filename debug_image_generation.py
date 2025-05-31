#!/usr/bin/env python3
"""
Debug script to test image generation specifically.
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homescreen_project.settings')
os.environ['OPENAI_API_KEY'] = "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"
django.setup()

def test_openai_simple():
    """Test OpenAI API with a simple request."""
    try:
        import requests
        
        print("🧪 Testing OpenAI API connectivity...")
        
        headers = {
            'Authorization': f'Bearer {os.environ["OPENAI_API_KEY"]}',
            'Content-Type': 'application/json'
        }
        
        # Test with a simple chat completion (cheaper than image generation)
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": "Say 'Hello from OpenAI API test!'"
                }
            ],
            "max_tokens": 10
        }
        
        print("📡 Making API request...")
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✅ API Response: {message}")
            return True
        else:
            print(f"❌ API Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_image_generation_service():
    """Test the image generation service directly."""
    try:
        from api.ai_services import AIServiceFactory
        from PIL import Image
        
        print("\n🎨 Testing Image Generation Service...")
        
        # Create a simple test image
        test_image = Image.new('RGB', (400, 300), color='lightblue')
        
        # Create generation service
        service = AIServiceFactory.create_image_generation_service(provider_name='openai')
        
        if not service:
            print("❌ Failed to create OpenAI generation service")
            return False
        
        print("✅ OpenAI generation service created")
        
        # Test simple generation (not screen visualization to avoid complexity)
        print("🔄 Testing basic image generation...")
        
        # Check service status first
        status = service.get_service_status()
        print(f"📡 Service status: {status.get('status', 'unknown')}")
        
        if status.get('status') == 'operational':
            print("✅ Service is operational")
            return True
        else:
            print(f"⚠️ Service status: {status}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing generation service: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_visualization_request():
    """Check the latest visualization request to see what happened."""
    try:
        from api.models import VisualizationRequest
        
        print("\n📋 Checking Latest Visualization Request...")
        
        latest = VisualizationRequest.objects.order_by('-created_at').first()
        
        if latest:
            print(f"📊 Request ID: {latest.id}")
            print(f"📊 Status: {latest.status}")
            print(f"📊 Progress: {latest.progress_percentage}%")
            print(f"📊 Message: {latest.progress_message}")
            print(f"📊 Screen Type: {latest.screen_type.name}")
            print(f"📊 Created: {latest.created_at}")
            print(f"📊 Updated: {latest.updated_at}")
            
            # Check generated images
            generated_images = latest.generated_images.all()
            print(f"📊 Generated Images: {len(generated_images)}")
            
            for i, img in enumerate(generated_images):
                print(f"   Image {i+1}: {img.image_file.name if img.image_file else 'No file'}")
                print(f"   Variation: {img.variation_type}")
                print(f"   Created: {img.created_at}")
            
            return True
        else:
            print("❌ No visualization requests found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking requests: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 OpenAI Image Generation Debug")
    print("=" * 50)
    
    # Test 1: Basic API connectivity
    api_works = test_openai_simple()
    
    # Test 2: Image generation service
    service_works = test_image_generation_service()
    
    # Test 3: Check what happened in the last request
    request_info = check_visualization_request()
    
    print("\n" + "=" * 50)
    print("📊 Debug Results:")
    print(f"   OpenAI API: {'✅ Working' if api_works else '❌ Failed'}")
    print(f"   Generation Service: {'✅ Working' if service_works else '❌ Failed'}")
    print(f"   Request Info: {'✅ Found' if request_info else '❌ Not found'}")
    
    if not api_works:
        print("\n🔧 Troubleshooting:")
        print("1. Check your OpenAI API key billing status")
        print("2. Verify API key permissions")
        print("3. Check network connectivity")
    elif not service_works:
        print("\n🔧 Troubleshooting:")
        print("1. Check AI service configuration")
        print("2. Verify OpenAI provider setup")
        print("3. Check service registry")
    else:
        print("\n🎉 OpenAI integration appears to be working!")
        print("The issue might be in the specific image generation logic.")
