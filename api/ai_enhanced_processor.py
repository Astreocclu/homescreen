"""
AI-Enhanced Image Processor for Homescreen Visualization

This processor uses the service-agnostic AI framework to generate realistic
screen visualizations with intelligent window detection and quality assessment.
"""

import logging
import time
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image
from django.core.files.base import ContentFile
import io

from .ai_services import (
    AIServiceFactory,
    AIServiceType,
    AIServiceConfig,
    ai_service_registry,
    ai_config_manager
)
from .ai_services.providers.mock_provider import MockAIProvider
from .ai_services.providers.openai_provider import OpenAIProvider

logger = logging.getLogger(__name__)


class AIEnhancedImageProcessor:
    """
    Enhanced image processor that uses AI services for intelligent screen visualization.

    This processor provides a service-agnostic approach to generating realistic
    screen overlays using various AI providers for computer vision and image generation.
    """

    def __init__(self, preferred_providers: Dict[str, str] = None):
        """
        Initialize the AI-enhanced processor.

        Args:
            preferred_providers: Dictionary mapping service types to preferred provider names
        """
        self.preferred_providers = preferred_providers or {}
        self.output_formats = ['JPEG', 'PNG']
        self.quality = 85
        self.max_output_size = (1920, 1080)

        # Initialize AI services
        self._initialize_ai_services()

        logger.info("AI-Enhanced Image Processor initialized")

    def _initialize_ai_services(self):
        """Initialize AI service providers and registry."""
        try:
            # Register mock provider for development/testing
            mock_provider = MockAIProvider()
            ai_service_registry.register_provider('mock_ai', mock_provider)

            # Register OpenAI provider if API key is available
            self._register_openai_provider()

            # TODO: Register other providers when API keys are available
            # self._register_google_provider()
            # self._register_anthropic_provider()

            logger.info("AI services initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing AI services: {str(e)}")

    def _register_openai_provider(self):
        """Register OpenAI provider if API key is available."""
        try:
            openai_config = ai_config_manager.get_config('openai')
            if openai_config and openai_config.api_key:
                openai_provider = OpenAIProvider()
                ai_service_registry.register_provider('openai', openai_provider)
                logger.info("OpenAI provider registered successfully")
            else:
                logger.info("OpenAI API key not found, skipping OpenAI provider registration")
        except Exception as e:
            logger.error(f"Error registering OpenAI provider: {str(e)}")

    def process_image(self, visualization_request):
        """
        Process an image using AI-enhanced visualization generation.

        Args:
            visualization_request: VisualizationRequest instance

        Returns:
            list: List of generated image instances
        """
        try:
            # Mark request as processing
            visualization_request.mark_as_processing()

            # Load the original image
            visualization_request.update_progress(10, "Loading and analyzing image...")
            original_image = Image.open(visualization_request.original_image.path)
            screen_type = visualization_request.screen_type

            # Step 1: Detect windows and doors using AI vision (context-aware)
            visualization_request.update_progress(20, f"Detecting areas for {screen_type.name}...")
            detection_results = self._detect_windows_and_doors(original_image, screen_type.name)

            # Step 2: Analyze existing screens if any
            visualization_request.update_progress(30, "Analyzing image characteristics...")
            analysis_results = self._analyze_image_characteristics(original_image)

            # Step 3: Generate AI-enhanced visualizations
            visualization_request.update_progress(40, f"Generating {screen_type.name} visualizations...")
            generated_images = self._generate_ai_visualizations(
                original_image,
                screen_type,
                detection_results,
                analysis_results,
                visualization_request
            )

            # Step 4: Assess and enhance quality
            visualization_request.update_progress(80, "Assessing and enhancing quality...")
            enhanced_images = self._assess_and_enhance_quality(generated_images, original_image)

            # Step 5: Save results
            visualization_request.update_progress(90, "Saving results...")
            saved_images = self._save_generated_images(enhanced_images, visualization_request)

            # Mark request as complete
            visualization_request.mark_as_complete()

            logger.info(f"Successfully processed request {visualization_request.id} with AI enhancement, generated {len(saved_images)} images")
            return saved_images

        except Exception as e:
            error_msg = f"Error in AI-enhanced processing: {str(e)}"
            logger.error(error_msg)
            visualization_request.mark_as_failed(error_msg)
            return []

    def _detect_windows_and_doors(self, image: Image.Image, screen_type: str = None) -> Dict[str, Any]:
        """
        Detect windows and doors in the image using AI vision services.

        Args:
            image: Input image to analyze
            screen_type: Type of screen for context-aware detection

        Returns:
            Dictionary with detection results
        """
        try:
            # Get vision service
            vision_service = AIServiceFactory.create_vision_service(
                provider_name=self.preferred_providers.get('vision', 'mock_ai')
            )

            if not vision_service:
                logger.warning("No vision service available, using fallback detection")
                return self._fallback_window_detection(image)

            # Perform context-aware detection
            result = vision_service.detect_windows_and_doors(
                image,
                confidence_threshold=0.7,
                screen_type=screen_type
            )

            if result.success:
                logger.info(f"Detected {len(result.detected_windows)} windows/doors")
                return {
                    'success': True,
                    'detections': result.detected_windows,
                    'bounding_boxes': result.bounding_boxes,
                    'confidence_scores': result.confidence_scores,
                    'metadata': result.metadata
                }
            else:
                logger.warning(f"Window detection failed: {result.message}")
                return self._fallback_window_detection(image)

        except Exception as e:
            logger.error(f"Error in window detection: {str(e)}")
            return self._fallback_window_detection(image)

    def _analyze_image_characteristics(self, image: Image.Image) -> Dict[str, Any]:
        """
        Analyze image characteristics for better screen application.

        Args:
            image: Input image to analyze

        Returns:
            Dictionary with analysis results
        """
        try:
            # Get vision service for analysis
            vision_service = AIServiceFactory.create_vision_service(
                provider_name=self.preferred_providers.get('vision', 'mock_ai')
            )

            if not vision_service:
                return self._fallback_image_analysis(image)

            # Analyze screen patterns if any exist
            analysis_result = vision_service.analyze_screen_pattern(image)

            if analysis_result.success:
                return {
                    'success': True,
                    'lighting_conditions': self._analyze_lighting(image),
                    'color_profile': analysis_result.color_analysis,
                    'texture_info': analysis_result.texture_features,
                    'metadata': analysis_result.metadata
                }
            else:
                return self._fallback_image_analysis(image)

        except Exception as e:
            logger.error(f"Error in image analysis: {str(e)}")
            return self._fallback_image_analysis(image)

    def _generate_ai_visualizations(
        self,
        original_image: Image.Image,
        screen_type,
        detection_results: Dict[str, Any],
        analysis_results: Dict[str, Any],
        request
    ) -> List[Dict[str, Any]]:
        """
        Generate AI-enhanced screen visualizations.

        Args:
            original_image: Original house image
            screen_type: Type of screen to apply
            detection_results: Window/door detection results
            analysis_results: Image analysis results
            request: Visualization request for progress updates

        Returns:
            List of generated image data
        """
        generated_images = []

        try:
            # Get image generation service
            generation_service = AIServiceFactory.create_image_generation_service(
                provider_name=self.preferred_providers.get('generation', 'mock_ai')
            )

            if not generation_service:
                logger.warning("No generation service available, using fallback")
                return self._fallback_generation(original_image, screen_type, detection_results)

            # Prepare detection areas
            detection_areas = detection_results.get('bounding_boxes', [])

            # Generate multiple variations
            variations = self._get_screen_variations(screen_type)

            for i, variation in enumerate(variations):
                try:
                    request.update_progress(
                        50 + (i * 20 // len(variations)),
                        f"Generating {variation} variation..."
                    )

                    # Generate visualization
                    result = generation_service.generate_screen_visualization(
                        original_image,
                        variation,
                        detection_areas,
                        style_preferences=analysis_results
                    )

                    if result.success:
                        generated_images.append({
                            'image_data': result.metadata.get('generated_image_data'),
                            'variation': variation,
                            'quality_score': 0.8,  # Will be assessed later
                            'metadata': result.metadata
                        })
                        logger.info(f"Generated {variation} visualization successfully")
                    else:
                        logger.warning(f"Failed to generate {variation}: {result.message}")

                except Exception as e:
                    logger.error(f"Error generating {variation}: {str(e)}")
                    continue

            return generated_images

        except Exception as e:
            logger.error(f"Error in AI visualization generation: {str(e)}")
            return self._fallback_generation(original_image, screen_type, detection_results)

    def _assess_and_enhance_quality(
        self,
        generated_images: List[Dict[str, Any]],
        reference_image: Image.Image
    ) -> List[Dict[str, Any]]:
        """
        Assess and enhance the quality of generated images.

        Args:
            generated_images: List of generated image data
            reference_image: Original reference image

        Returns:
            List of enhanced image data
        """
        enhanced_images = []

        try:
            # Get vision service for quality assessment
            vision_service = AIServiceFactory.create_vision_service(
                provider_name=self.preferred_providers.get('vision', 'mock_ai')
            )

            # Get generation service for enhancement
            generation_service = AIServiceFactory.create_image_generation_service(
                provider_name=self.preferred_providers.get('generation', 'mock_ai')
            )

            for image_data in generated_images:
                try:
                    # Convert image data back to PIL Image for assessment
                    if image_data.get('image_data'):
                        image_bytes = image_data['image_data']
                        image = Image.open(io.BytesIO(image_bytes))
                    else:
                        continue

                    # Assess quality
                    quality_result = None
                    if vision_service:
                        quality_result = vision_service.assess_image_quality(image, reference_image)

                    # Enhance if needed
                    enhanced_image = image
                    if generation_service and quality_result and quality_result.overall_score < 0.7:
                        enhancement_result = generation_service.enhance_image_quality(image, "general")
                        if enhancement_result.success:
                            enhanced_data = enhancement_result.metadata.get('enhanced_image_data')
                            if enhanced_data:
                                enhanced_image = Image.open(io.BytesIO(enhanced_data))

                    # Convert back to bytes
                    output = io.BytesIO()
                    enhanced_image.save(output, format='JPEG', quality=self.quality)
                    enhanced_data = output.getvalue()

                    enhanced_images.append({
                        'image_data': enhanced_data,
                        'variation': image_data['variation'],
                        'quality_score': quality_result.overall_score if quality_result else 0.8,
                        'metadata': {
                            **image_data.get('metadata', {}),
                            'quality_assessment': quality_result.metadata if quality_result else {},
                            'enhanced': True
                        }
                    })

                except Exception as e:
                    logger.error(f"Error enhancing image: {str(e)}")
                    # Keep original if enhancement fails
                    enhanced_images.append(image_data)

            return enhanced_images

        except Exception as e:
            logger.error(f"Error in quality assessment and enhancement: {str(e)}")
            return generated_images

    def _save_generated_images(
        self,
        image_data_list: List[Dict[str, Any]],
        request
    ) -> List:
        """
        Save generated images and create GeneratedImage records.

        Args:
            image_data_list: List of image data dictionaries
            request: Visualization request

        Returns:
            List of GeneratedImage instances
        """
        from .models import GeneratedImage

        saved_images = []

        for i, image_data in enumerate(image_data_list):
            try:
                # Get image bytes
                image_bytes = image_data.get('image_data')
                if not image_bytes:
                    continue

                # Create filename
                variation = image_data.get('variation', f'variation_{i}')
                filename = f"ai_generated_{request.id}_{variation}.jpg"

                # Create GeneratedImage record
                generated_image = GeneratedImage(request=request)
                generated_image.generated_image.save(
                    filename,
                    ContentFile(image_bytes),
                    save=True
                )

                saved_images.append(generated_image)
                logger.info(f"Saved generated image: {filename}")

            except Exception as e:
                logger.error(f"Error saving generated image: {str(e)}")
                continue

        return saved_images

    def _get_screen_variations(self, screen_type) -> List[str]:
        """Get variations to generate for a screen type."""
        base_name = screen_type.name.lower()

        if 'security' in base_name:
            return ['security_mesh_fine', 'security_mesh_coarse', 'security_heavy_duty']
        elif 'lifestyle' in base_name:
            return ['lifestyle_phifer', 'lifestyle_twitchell', 'lifestyle_standard']
        elif 'solar' in base_name:
            return ['solar_light', 'solar_medium', 'solar_dark']
        else:
            return [f'{base_name}_standard', f'{base_name}_premium']

    def _fallback_window_detection(self, image: Image.Image) -> Dict[str, Any]:
        """Fallback window detection when AI services are unavailable."""
        width, height = image.size
        # Simple fallback: assume windows in common locations
        return {
            'success': True,
            'detections': [{'type': 'window', 'id': 'fallback_1'}],
            'bounding_boxes': [(width//4, height//4, 3*width//4, 3*height//4)],
            'confidence_scores': [0.5],
            'metadata': {'method': 'fallback'}
        }

    def _fallback_image_analysis(self, image: Image.Image) -> Dict[str, Any]:
        """Fallback image analysis when AI services are unavailable."""
        return {
            'success': True,
            'lighting_conditions': 'normal',
            'color_profile': {'brightness': 0.5, 'saturation': 0.5},
            'texture_info': {'roughness': 0.5},
            'metadata': {'method': 'fallback'}
        }

    def _fallback_generation(self, original_image, screen_type, detection_results) -> List[Dict[str, Any]]:
        """Fallback generation when AI services are unavailable."""
        # Use the original processor as fallback
        from .image_processor import HomescreenImageProcessor

        fallback_processor = HomescreenImageProcessor()
        # This would need to be adapted to return the expected format
        return []

    def _analyze_lighting(self, image: Image.Image) -> str:
        """Analyze lighting conditions in the image."""
        # Simple brightness analysis
        import numpy as np

        gray = image.convert('L')
        brightness = np.array(gray).mean()

        if brightness < 85:
            return 'dark'
        elif brightness > 170:
            return 'bright'
        else:
            return 'normal'

    def get_processor_status(self) -> Dict[str, Any]:
        """Get processor status and AI service information."""
        return {
            'processor_type': 'ai_enhanced',
            'ai_services_status': ai_service_registry.get_registry_status(),
            'preferred_providers': self.preferred_providers,
            'available_services': AIServiceFactory.get_factory_status()
        }
