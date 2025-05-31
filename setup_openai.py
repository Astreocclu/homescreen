#!/usr/bin/env python3
"""
Setup script to configure OpenAI API key for the homescreen application.
This script sets up the environment variable and tests the OpenAI integration.
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
django.setup()

def setup_openai_key():
    """Set up OpenAI API key in environment."""

    # Your OpenAI API key
    openai_api_key = "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"

    # Set environment variable
    os.environ['OPENAI_API_KEY'] = openai_api_key

    print("✅ OpenAI API key set in environment")

    # Test the AI services
    test_ai_services()

def test_ai_services():
    """Test the AI services integration."""
    try:
        from api.ai_services import ai_service_registry, AIServiceFactory, AIServiceType, ai_config_manager
        from api.ai_enhanced_processor import AIEnhancedImageProcessor

        print("\n🧪 Testing AI Services Integration...")

        # Force reload configuration to pick up environment variables
        ai_config_manager._load_from_environment()

        # Check if OpenAI config is loaded
        openai_config = ai_config_manager.get_config('openai')
        if openai_config:
            print(f"✅ OpenAI configuration loaded (key: {openai_config.api_key[:10]}...)")
        else:
            print(f"❌ OpenAI configuration not found")

        # Initialize the processor (this will register providers)
        processor = AIEnhancedImageProcessor()

        # Check registry status
        status = ai_service_registry.get_registry_status()
        print(f"📊 Registry Status:")
        print(f"   Total providers: {status['total_providers']}")
        print(f"   Providers by service: {status['providers_by_service']}")

        # Check available providers
        all_providers = ai_service_registry.get_all_providers()
        print(f"\n🔌 Available Providers:")
        for provider_name, provider in all_providers.items():
            capabilities = ai_service_registry.get_provider_capabilities(provider_name)
            print(f"   {provider_name}: {capabilities['available_services']}")

        # Test OpenAI provider specifically
        openai_providers = ai_service_registry.get_providers_for_service(AIServiceType.IMAGE_GENERATION)
        if 'openai' in openai_providers:
            print(f"\n🎉 OpenAI provider successfully registered!")

            # Test creating a service
            try:
                service = AIServiceFactory.create_image_generation_service(provider_name='openai')
                if service:
                    print(f"✅ OpenAI image generation service created successfully")

                    # Test service status
                    status = service.get_service_status()
                    print(f"📡 OpenAI Service Status: {status.get('status', 'unknown')}")
                else:
                    print(f"❌ Failed to create OpenAI service")
            except Exception as e:
                print(f"⚠️  Error testing OpenAI service: {str(e)}")
        else:
            print(f"❌ OpenAI provider not found in registry")

        # Test vision service
        vision_providers = ai_service_registry.get_providers_for_service(AIServiceType.COMPUTER_VISION)
        if 'openai' in vision_providers:
            print(f"✅ OpenAI vision service available")

            try:
                vision_service = AIServiceFactory.create_vision_service(provider_name='openai')
                if vision_service:
                    print(f"✅ OpenAI vision service created successfully")

                    # Test service status
                    status = vision_service.get_service_status()
                    print(f"📡 OpenAI Vision Status: {status.get('status', 'unknown')}")
                else:
                    print(f"❌ Failed to create OpenAI vision service")
            except Exception as e:
                print(f"⚠️  Error testing OpenAI vision service: {str(e)}")

        print(f"\n🚀 AI Services Setup Complete!")
        print(f"   Your homescreen application now has access to OpenAI's AI capabilities!")
        print(f"   You can now upload images and get AI-enhanced screen visualizations.")

    except Exception as e:
        print(f"❌ Error testing AI services: {str(e)}")
        import traceback
        traceback.print_exc()

def create_env_file():
    """Create a .env file with the OpenAI API key."""
    env_content = f"""# OpenAI Configuration
OPENAI_API_KEY=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
OPENAI_API_ENDPOINT=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_REQUESTS=60
OPENAI_TIMEOUT=30

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
"""

    env_file = project_root / '.env'
    with open(env_file, 'w') as f:
        f.write(env_content)

    print(f"✅ Created .env file at {env_file}")

if __name__ == "__main__":
    print("🏠 Homescreen AI Services Setup")
    print("=" * 40)

    # Create .env file
    create_env_file()

    # Set up OpenAI key
    setup_openai_key()

    print("\n" + "=" * 40)
    print("🎉 Setup Complete!")
    print("\nNext steps:")
    print("1. Restart your Django server: python manage.py runserver")
    print("2. Upload an image and select a screen type")
    print("3. Watch as AI analyzes your image and generates realistic screen visualizations!")
