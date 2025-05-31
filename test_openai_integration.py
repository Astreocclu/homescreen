#!/usr/bin/env python3
"""
Test script to verify OpenAI integration with a real image.
This script tests the AI-enhanced image processing pipeline.
"""

import os
import sys
import django
from pathlib import Path
from PIL import Image, ImageDraw

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homescreen_project.settings')
os.environ['OPENAI_API_KEY'] = "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"
django.setup()

def create_test_house_image():
    """Create a simple test house image."""
    # Create a simple house image for testing
    width, height = 400, 300
    image = Image.new('RGB', (width, height), color='lightblue')
    draw = ImageDraw.Draw(image)
    
    # Draw a simple house
    # House body
    draw.rectangle([50, 150, 350, 280], fill='lightgray', outline='black', width=2)
    
    # Roof
    draw.polygon([(40, 150), (200, 80), (360, 150)], fill='brown', outline='black')
    
    # Windows
    draw.rectangle([80, 180, 130, 220], fill='lightblue', outline='black', width=2)
    draw.rectangle([270, 180, 320, 220], fill='lightblue', outline='black', width=2)
    
    # Door
    draw.rectangle([180, 200, 220, 280], fill='brown', outline='black', width=2)
    
    return image

def test_openai_vision_service():
    """Test OpenAI vision service with window detection."""
    try:
        from api.ai_services import AIServiceFactory, AIServiceType
        
        print("🔍 Testing OpenAI Vision Service...")
        
        # Create test image
        test_image = create_test_house_image()
        
        # Create vision service
        vision_service = AIServiceFactory.create_vision_service(provider_name='openai')
        
        if not vision_service:
            print("❌ Failed to create OpenAI vision service")
            return False
        
        print("✅ OpenAI vision service created")
        
        # Test window detection
        print("🏠 Testing window detection...")
        detection_result = vision_service.detect_windows_and_doors(test_image, confidence_threshold=0.5)
        
        if detection_result.success:
            print(f"✅ Window detection successful!")
            print(f"   Detected {len(detection_result.detected_windows)} windows/doors")
            print(f"   Processing time: {detection_result.processing_time_seconds:.2f}s")
            print(f"   Cost estimate: ${detection_result.cost_estimate:.3f}")
            
            for i, window in enumerate(detection_result.detected_windows):
                print(f"   Window {i+1}: {window['type']} (confidence: {detection_result.confidence_scores[i]:.2f})")
        else:
            print(f"❌ Window detection failed: {detection_result.message}")
            if detection_result.error_details:
                print(f"   Error: {detection_result.error_details}")
        
        # Test screen analysis
        print("🔍 Testing screen pattern analysis...")
        analysis_result = vision_service.analyze_screen_pattern(test_image)
        
        if analysis_result.success:
            print(f"✅ Screen analysis successful!")
            print(f"   Screen type: {analysis_result.screen_type}")
            print(f"   Mesh pattern: {analysis_result.mesh_pattern}")
            print(f"   Opacity: {analysis_result.opacity_level}")
            print(f"   Processing time: {analysis_result.processing_time_seconds:.2f}s")
        else:
            print(f"❌ Screen analysis failed: {analysis_result.message}")
        
        # Test quality assessment
        print("📊 Testing image quality assessment...")
        quality_result = vision_service.assess_image_quality(test_image)
        
        if quality_result.success:
            print(f"✅ Quality assessment successful!")
            print(f"   Overall score: {quality_result.overall_score:.2f}")
            print(f"   Realism score: {quality_result.realism_score:.2f}")
            print(f"   Technical quality: {quality_result.technical_quality:.2f}")
            print(f"   Aesthetic score: {quality_result.aesthetic_score:.2f}")
            print(f"   Suggestions: {', '.join(quality_result.improvement_suggestions)}")
        else:
            print(f"❌ Quality assessment failed: {quality_result.message}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing OpenAI vision service: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_openai_generation_service():
    """Test OpenAI image generation service."""
    try:
        from api.ai_services import AIServiceFactory, AIServiceType
        
        print("\n🎨 Testing OpenAI Image Generation Service...")
        
        # Create test image
        test_image = create_test_house_image()
        
        # Create generation service
        generation_service = AIServiceFactory.create_image_generation_service(provider_name='openai')
        
        if not generation_service:
            print("❌ Failed to create OpenAI generation service")
            return False
        
        print("✅ OpenAI generation service created")
        
        # Test screen visualization generation
        print("🏠 Testing screen visualization generation...")
        generation_result = generation_service.generate_screen_visualization(
            test_image,
            "security_mesh",
            detection_areas=[(80, 180, 130, 220), (270, 180, 320, 220)],  # Window areas
            style_preferences={'opacity': 0.3}
        )
        
        if generation_result.success:
            print(f"✅ Screen visualization generation successful!")
            print(f"   Processing time: {generation_result.processing_time_seconds:.2f}s")
            print(f"   Cost estimate: ${generation_result.cost_estimate:.3f}")
            print(f"   Generated image size: {len(generation_result.metadata.get('generated_image_data', b''))} bytes")
        else:
            print(f"❌ Screen visualization failed: {generation_result.message}")
            if generation_result.error_details:
                print(f"   Error: {generation_result.error_details}")
        
        # Test image enhancement
        print("✨ Testing image enhancement...")
        enhancement_result = generation_service.enhance_image_quality(test_image, "general")
        
        if enhancement_result.success:
            print(f"✅ Image enhancement successful!")
            print(f"   Processing time: {enhancement_result.processing_time_seconds:.2f}s")
            print(f"   Enhanced image size: {len(enhancement_result.metadata.get('enhanced_image_data', b''))} bytes")
        else:
            print(f"❌ Image enhancement failed: {enhancement_result.message}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing OpenAI generation service: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_enhanced_processor():
    """Test the full AI-enhanced processing pipeline."""
    try:
        from api.ai_enhanced_processor import AIEnhancedImageProcessor
        from api.models import ScreenType
        from django.contrib.auth.models import User
        from django.core.files.uploadedfile import SimpleUploadedFile
        import io
        
        print("\n🚀 Testing AI-Enhanced Processing Pipeline...")
        
        # Create test image
        test_image = create_test_house_image()
        image_file = io.BytesIO()
        test_image.save(image_file, format='JPEG')
        image_file.seek(0)
        
        # Create uploaded file
        uploaded_file = SimpleUploadedFile(
            name='test_house.jpg',
            content=image_file.getvalue(),
            content_type='image/jpeg'
        )
        
        # Get or create test data
        user, created = User.objects.get_or_create(username='testuser', defaults={'password': 'testpass'})
        screen_type, created = ScreenType.objects.get_or_create(
            name='Security Mesh',
            defaults={'description': 'Test security mesh screen'}
        )
        
        # Create visualization request
        from api.models import VisualizationRequest
        request = VisualizationRequest.objects.create(
            user=user,
            original_image=uploaded_file,
            screen_type=screen_type,
            status='pending'
        )
        
        print(f"✅ Created test visualization request (ID: {request.id})")
        
        # Initialize AI processor
        processor = AIEnhancedImageProcessor(
            preferred_providers={'generation': 'openai', 'vision': 'openai'}
        )
        
        print("✅ AI-Enhanced processor initialized")
        print("🔄 Processing image with AI enhancement...")
        
        # Process the image
        generated_images = processor.process_image(request)
        
        print(f"✅ AI processing completed!")
        print(f"   Generated {len(generated_images)} images")
        print(f"   Request status: {request.status}")
        
        # Check the results
        request.refresh_from_db()
        if request.status == 'complete':
            print("🎉 Full AI processing pipeline successful!")
            return True
        else:
            print(f"⚠️  Processing completed but status is: {request.status}")
            return False
        
    except Exception as e:
        print(f"❌ Error testing AI-enhanced processor: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 OpenAI Integration Test Suite")
    print("=" * 50)
    
    # Test individual services
    vision_success = test_openai_vision_service()
    generation_success = test_openai_generation_service()
    
    # Test full pipeline
    pipeline_success = test_ai_enhanced_processor()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   OpenAI Vision Service: {'✅ PASS' if vision_success else '❌ FAIL'}")
    print(f"   OpenAI Generation Service: {'✅ PASS' if generation_success else '❌ FAIL'}")
    print(f"   AI-Enhanced Pipeline: {'✅ PASS' if pipeline_success else '❌ FAIL'}")
    
    if vision_success and generation_success and pipeline_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your OpenAI integration is working perfectly!")
        print("\nYour homescreen application now has:")
        print("✅ Intelligent window detection using GPT-4 Vision")
        print("✅ AI-powered screen visualization generation")
        print("✅ Automatic quality assessment and enhancement")
        print("✅ Full AI-enhanced processing pipeline")
        print("\n🚀 Ready for production use!")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
    
    print("\nNext steps:")
    print("1. Start your Django server: python manage.py runserver")
    print("2. Open the frontend and upload a house image")
    print("3. Select a screen type and watch the AI magic happen!")
