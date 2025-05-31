#!/usr/bin/env python3
"""
Demo script for AI Services Framework

This script demonstrates the AI services framework capabilities
including service registration, image processing, and monitoring.
"""

import os
import sys
import django
from PIL import Image
import io

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homescreen_project.settings')
django.setup()

from api.ai_services import (
    ai_service_registry,
    AIServiceFactory,
    AIServiceType,
    AIServiceConfig
)
from api.ai_services.providers.mock_provider import MockAIProvider
from api.ai_enhanced_processor import AIEnhancedImageProcessor


def demo_service_registry():
    """Demonstrate the AI service registry functionality."""
    print("🔧 AI Service Registry Demo")
    print("=" * 50)
    
    # Register mock provider
    provider = MockAIProvider()
    success = ai_service_registry.register_provider('demo_mock', provider)
    print(f"✅ Provider registration: {'Success' if success else 'Failed'}")
    
    # Get registry status
    status = ai_service_registry.get_registry_status()
    print(f"📊 Total providers: {status['total_providers']}")
    print(f"📊 Services by type: {status['providers_by_service']}")
    
    # Get providers for specific service types
    image_providers = ai_service_registry.get_providers_for_service(AIServiceType.IMAGE_GENERATION)
    vision_providers = ai_service_registry.get_providers_for_service(AIServiceType.COMPUTER_VISION)
    
    print(f"🖼️  Image generation providers: {image_providers}")
    print(f"👁️  Computer vision providers: {vision_providers}")
    print()


def demo_service_factory():
    """Demonstrate the AI service factory functionality."""
    print("🏭 AI Service Factory Demo")
    print("=" * 50)
    
    # Create image generation service
    image_service = AIServiceFactory.create_image_generation_service(provider_name='demo_mock')
    print(f"✅ Image generation service: {'Created' if image_service else 'Failed'}")
    
    # Create vision service
    vision_service = AIServiceFactory.create_vision_service(provider_name='demo_mock')
    print(f"✅ Vision service: {'Created' if vision_service else 'Failed'}")
    
    # Get factory status
    factory_status = AIServiceFactory.get_factory_status()
    print(f"📊 Factory version: {factory_status['factory_version']}")
    print(f"📊 Supported service types: {factory_status['supported_service_types']}")
    print()


def demo_image_processing():
    """Demonstrate AI-enhanced image processing."""
    print("🖼️ AI Image Processing Demo")
    print("=" * 50)
    
    # Create a test image
    test_image = Image.new('RGB', (400, 300), color='lightblue')
    print("✅ Created test image (400x300)")
    
    # Create services
    image_service = AIServiceFactory.create_image_generation_service(provider_name='demo_mock')
    vision_service = AIServiceFactory.create_vision_service(provider_name='demo_mock')
    
    if image_service and vision_service:
        # Test window detection
        print("🔍 Testing window detection...")
        detection_result = vision_service.detect_windows_and_doors(test_image)
        print(f"   - Success: {detection_result.success}")
        print(f"   - Windows detected: {len(detection_result.detected_windows)}")
        print(f"   - Processing time: {detection_result.processing_time_seconds:.2f}s")
        
        # Test screen visualization generation
        print("🎨 Testing screen visualization generation...")
        generation_result = image_service.generate_screen_visualization(
            test_image,
            'security_mesh',
            detection_areas=detection_result.bounding_boxes
        )
        print(f"   - Success: {generation_result.success}")
        print(f"   - Processing time: {generation_result.processing_time_seconds:.2f}s")
        print(f"   - Cost estimate: ${generation_result.cost_estimate:.3f}")
        
        # Test quality assessment
        print("📊 Testing quality assessment...")
        quality_result = vision_service.assess_image_quality(test_image)
        print(f"   - Success: {quality_result.success}")
        print(f"   - Overall score: {quality_result.overall_score:.2f}")
        print(f"   - Realism score: {quality_result.realism_score:.2f}")
        print(f"   - Technical quality: {quality_result.technical_quality:.2f}")
        
        # Test image enhancement
        print("✨ Testing image enhancement...")
        enhancement_result = image_service.enhance_image_quality(test_image, 'general')
        print(f"   - Success: {enhancement_result.success}")
        print(f"   - Processing time: {enhancement_result.processing_time_seconds:.2f}s")
    
    print()


def demo_ai_enhanced_processor():
    """Demonstrate the AI-enhanced processor."""
    print("🤖 AI-Enhanced Processor Demo")
    print("=" * 50)
    
    # Create processor
    processor = AIEnhancedImageProcessor()
    print("✅ AI-Enhanced processor created")
    
    # Get processor status
    status = processor.get_processor_status()
    print(f"📊 Processor type: {status['processor_type']}")
    print(f"📊 AI services available: {len(status['ai_services_status']['provider_status'])}")
    
    # Test individual components
    test_image = Image.new('RGB', (500, 400), color='lightgreen')
    
    # Test window detection
    detection_results = processor._detect_windows_and_doors(test_image)
    print(f"🔍 Window detection: {'Success' if detection_results['success'] else 'Failed'}")
    
    # Test image analysis
    analysis_results = processor._analyze_image_characteristics(test_image)
    print(f"📊 Image analysis: {'Success' if analysis_results['success'] else 'Failed'}")
    
    print()


def demo_service_health():
    """Demonstrate service health monitoring."""
    print("🏥 Service Health Monitoring Demo")
    print("=" * 50)
    
    # Get all providers
    providers = ai_service_registry.get_all_providers()
    
    for provider_name, provider in providers.items():
        print(f"🔧 Provider: {provider_name}")
        
        # Get provider capabilities
        capabilities = ai_service_registry.get_provider_capabilities(provider_name)
        print(f"   - Available: {capabilities.get('is_available', False)}")
        print(f"   - Services: {capabilities.get('available_services', [])}")
        
        # Get health status
        if hasattr(provider, 'get_service_health'):
            health = provider.get_service_health()
            print(f"   - Health: {health.get('status', 'unknown')}")
            print(f"   - Active instances: {health.get('active_instances', 0)}")
    
    print()


def main():
    """Run all demos."""
    print("🚀 AI Services Framework Demo")
    print("=" * 60)
    print("This demo showcases the service-agnostic AI framework")
    print("for the Homescreen Visualization application.")
    print("=" * 60)
    print()
    
    try:
        # Run all demo functions
        demo_service_registry()
        demo_service_factory()
        demo_image_processing()
        demo_ai_enhanced_processor()
        demo_service_health()
        
        print("🎉 Demo completed successfully!")
        print("=" * 60)
        print("Key Features Demonstrated:")
        print("✅ Service-agnostic architecture")
        print("✅ Multiple AI provider support")
        print("✅ Intelligent image processing")
        print("✅ Real-time health monitoring")
        print("✅ Comprehensive error handling")
        print("✅ Fallback mechanisms")
        print()
        print("Next Steps:")
        print("1. Add API keys for real AI providers (OpenAI, Google, etc.)")
        print("2. Test with actual house images")
        print("3. Deploy to production environment")
        print("4. Monitor performance and costs")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        ai_service_registry.clear_registry()
        print("\n🧹 Cleanup completed")


if __name__ == '__main__':
    main()
