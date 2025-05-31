"""
Mock AI service provider for testing and development.

This provider simulates AI services without making actual API calls,
useful for development, testing, and demonstrations.
"""

import time
import random
import logging
from typing import Dict, Any, List, Tuple, Optional
from PIL import Image, ImageDraw, ImageEnhance
import numpy as np

from ..interfaces import (
    AIServiceType,
    AIServiceConfig,
    AIImageGenerationService,
    AIVisionService,
    AIServiceResult,
    WindowDetectionResult,
    ScreenAnalysisResult,
    QualityAssessmentResult,
    ProcessingStatus
)
from .base_provider import BaseAIProvider

logger = logging.getLogger(__name__)


class MockImageGenerationService(AIImageGenerationService):
    """Mock implementation of AI image generation service."""

    def _validate_config(self) -> None:
        """Validate the service configuration."""
        if not self.config.service_name:
            raise ValueError("Service name is required")

    def generate_screen_visualization(
        self,
        original_image: Image.Image,
        screen_type: str,
        detection_areas: List[Tuple[int, int, int, int]] = None,
        style_preferences: Dict[str, Any] = None
    ) -> AIServiceResult:
        """Generate a mock screen visualization."""
        start_time = time.time()

        try:
            # Simulate processing time
            time.sleep(random.uniform(1, 3))

            # Create a mock visualization by applying a simple overlay
            result_image = self._apply_mock_screen_overlay(original_image, screen_type, detection_areas)

            # Convert to bytes for storage
            import io
            output = io.BytesIO()
            result_image.save(output, format='JPEG', quality=85)
            image_data = output.getvalue()

            processing_time = time.time() - start_time

            return AIServiceResult(
                success=True,
                status=ProcessingStatus.COMPLETED,
                message=f"Successfully generated {screen_type} visualization",
                processing_time_seconds=processing_time,
                cost_estimate=random.uniform(0.01, 0.05),
                metadata={
                    'screen_type': screen_type,
                    'image_size': result_image.size,
                    'detection_areas_used': len(detection_areas) if detection_areas else 0,
                    'generated_image_data': image_data
                }
            )

        except Exception as e:
            processing_time = time.time() - start_time
            return AIServiceResult(
                success=False,
                status=ProcessingStatus.FAILED,
                message="Failed to generate visualization",
                error_details=str(e),
                processing_time_seconds=processing_time
            )

    def enhance_image_quality(
        self,
        image: Image.Image,
        enhancement_type: str = "general"
    ) -> AIServiceResult:
        """Enhance image quality using mock processing."""
        start_time = time.time()

        try:
            # Simulate processing time
            time.sleep(random.uniform(0.5, 1.5))

            # Apply mock enhancement
            enhanced_image = self._apply_mock_enhancement(image, enhancement_type)

            # Convert to bytes
            import io
            output = io.BytesIO()
            enhanced_image.save(output, format='JPEG', quality=95)
            image_data = output.getvalue()

            processing_time = time.time() - start_time

            return AIServiceResult(
                success=True,
                status=ProcessingStatus.COMPLETED,
                message=f"Successfully enhanced image with {enhancement_type} enhancement",
                processing_time_seconds=processing_time,
                cost_estimate=random.uniform(0.005, 0.02),
                metadata={
                    'enhancement_type': enhancement_type,
                    'original_size': image.size,
                    'enhanced_image_data': image_data
                }
            )

        except Exception as e:
            processing_time = time.time() - start_time
            return AIServiceResult(
                success=False,
                status=ProcessingStatus.FAILED,
                message="Failed to enhance image",
                error_details=str(e),
                processing_time_seconds=processing_time
            )

    def get_service_status(self) -> Dict[str, Any]:
        """Get mock service status."""
        return {
            'service_name': self.config.service_name,
            'status': 'operational',
            'uptime': '99.9%',
            'avg_response_time': '2.1s',
            'requests_today': random.randint(100, 1000)
        }

    def _apply_mock_screen_overlay(
        self,
        image: Image.Image,
        screen_type: str,
        detection_areas: List[Tuple[int, int, int, int]] = None
    ) -> Image.Image:
        """Apply a mock screen overlay to the image."""
        result = image.copy()
        width, height = result.size

        # If no detection areas provided, use the whole image
        if not detection_areas:
            detection_areas = [(0, 0, width, height)]

        # Apply overlay to each detected area
        for area in detection_areas:
            x1, y1, x2, y2 = area
            area_width = x2 - x1
            area_height = y2 - y1

            # Create overlay based on screen type
            overlay = Image.new('RGBA', (area_width, area_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)

            if 'security' in screen_type.lower():
                # Security mesh pattern
                mesh_color = (100, 100, 100, 150)
                mesh_size = 8
            elif 'lifestyle' in screen_type.lower():
                # Lifestyle screen pattern
                mesh_color = (150, 150, 150, 100)
                mesh_size = 6
            else:
                # Default pattern
                mesh_color = (120, 120, 120, 120)
                mesh_size = 7

            # Draw mesh pattern
            for y in range(0, area_height, mesh_size):
                draw.line([(0, y), (area_width, y)], fill=mesh_color, width=1)
            for x in range(0, area_width, mesh_size):
                draw.line([(x, 0), (x, area_height)], fill=mesh_color, width=1)

            # Apply overlay to the specific area
            area_image = result.crop((x1, y1, x2, y2))
            area_image = area_image.convert('RGBA')
            area_image = Image.alpha_composite(area_image, overlay)
            result.paste(area_image.convert('RGB'), (x1, y1))

        return result

    def _apply_mock_enhancement(self, image: Image.Image, enhancement_type: str) -> Image.Image:
        """Apply mock image enhancement."""
        enhanced = image.copy()

        if enhancement_type == "brightness":
            enhancer = ImageEnhance.Brightness(enhanced)
            enhanced = enhancer.enhance(1.1)
        elif enhancement_type == "contrast":
            enhancer = ImageEnhance.Contrast(enhanced)
            enhanced = enhancer.enhance(1.1)
        elif enhancement_type == "sharpness":
            enhancer = ImageEnhance.Sharpness(enhanced)
            enhanced = enhancer.enhance(1.2)
        else:  # general enhancement
            # Apply multiple enhancements
            enhancer = ImageEnhance.Brightness(enhanced)
            enhanced = enhancer.enhance(1.05)
            enhancer = ImageEnhance.Contrast(enhanced)
            enhanced = enhancer.enhance(1.05)
            enhancer = ImageEnhance.Sharpness(enhanced)
            enhanced = enhancer.enhance(1.1)

        return enhanced


class MockVisionService(AIVisionService):
    """Mock implementation of AI vision service."""

    def _validate_config(self) -> None:
        """Validate the service configuration."""
        if not self.config.service_name:
            raise ValueError("Service name is required")

    def detect_windows_and_doors(
        self,
        image: Image.Image,
        confidence_threshold: float = 0.7,
        screen_type: str = None
    ) -> WindowDetectionResult:
        """Mock window and door detection."""
        start_time = time.time()

        try:
            # Simulate processing time
            time.sleep(random.uniform(1, 2))

            # Generate mock detections
            width, height = image.size
            num_detections = random.randint(1, 4)

            detected_windows = []
            confidence_scores = []
            bounding_boxes = []

            for i in range(num_detections):
                # Generate random window/door detection
                x1 = random.randint(0, width // 2)
                y1 = random.randint(0, height // 2)
                x2 = random.randint(x1 + 50, min(x1 + 200, width))
                y2 = random.randint(y1 + 50, min(y1 + 200, height))

                confidence = random.uniform(confidence_threshold, 1.0)
                window_type = random.choice(['window', 'door', 'sliding_door'])

                detected_windows.append({
                    'type': window_type,
                    'id': f'detection_{i}',
                    'area': (x2 - x1) * (y2 - y1)
                })
                confidence_scores.append(confidence)
                bounding_boxes.append((x1, y1, x2, y2))

            processing_time = time.time() - start_time

            return WindowDetectionResult(
                success=True,
                status=ProcessingStatus.COMPLETED,
                message=f"Detected {num_detections} windows/doors",
                processing_time_seconds=processing_time,
                cost_estimate=random.uniform(0.01, 0.03),
                detected_windows=detected_windows,
                confidence_scores=confidence_scores,
                bounding_boxes=bounding_boxes,
                metadata={
                    'image_size': image.size,
                    'confidence_threshold': confidence_threshold,
                    'detection_method': 'mock_ai'
                }
            )

        except Exception as e:
            processing_time = time.time() - start_time
            return WindowDetectionResult(
                success=False,
                status=ProcessingStatus.FAILED,
                message="Failed to detect windows/doors",
                error_details=str(e),
                processing_time_seconds=processing_time
            )

    def analyze_screen_pattern(
        self,
        image: Image.Image,
        screen_area: Tuple[int, int, int, int] = None
    ) -> ScreenAnalysisResult:
        """Mock screen pattern analysis."""
        start_time = time.time()

        try:
            # Simulate processing time
            time.sleep(random.uniform(0.5, 1.5))

            # Generate mock analysis results
            screen_types = ['security_mesh', 'lifestyle_screen', 'solar_screen', 'pet_resistant']
            mesh_patterns = ['fine_weave', 'coarse_weave', 'diamond_pattern', 'square_mesh']

            processing_time = time.time() - start_time

            return ScreenAnalysisResult(
                success=True,
                status=ProcessingStatus.COMPLETED,
                message="Successfully analyzed screen pattern",
                processing_time_seconds=processing_time,
                cost_estimate=random.uniform(0.005, 0.015),
                screen_type=random.choice(screen_types),
                mesh_pattern=random.choice(mesh_patterns),
                opacity_level=random.uniform(0.1, 0.8),
                color_analysis={
                    'dominant_color': f'rgb({random.randint(50, 200)}, {random.randint(50, 200)}, {random.randint(50, 200)})',
                    'brightness': random.uniform(0.2, 0.8),
                    'saturation': random.uniform(0.1, 0.6)
                },
                texture_features={
                    'roughness': random.uniform(0.1, 0.9),
                    'uniformity': random.uniform(0.5, 1.0),
                    'pattern_regularity': random.uniform(0.6, 1.0)
                },
                metadata={
                    'analysis_area': screen_area,
                    'image_size': image.size
                }
            )

        except Exception as e:
            processing_time = time.time() - start_time
            return ScreenAnalysisResult(
                success=False,
                status=ProcessingStatus.FAILED,
                message="Failed to analyze screen pattern",
                error_details=str(e),
                processing_time_seconds=processing_time
            )

    def assess_image_quality(
        self,
        image: Image.Image,
        reference_image: Image.Image = None
    ) -> QualityAssessmentResult:
        """Mock image quality assessment."""
        start_time = time.time()

        try:
            # Simulate processing time
            time.sleep(random.uniform(0.3, 1.0))

            # Generate mock quality scores
            overall_score = random.uniform(0.6, 0.95)
            realism_score = random.uniform(0.5, 0.9)
            technical_quality = random.uniform(0.7, 0.95)
            aesthetic_score = random.uniform(0.6, 0.9)

            # Generate improvement suggestions based on scores
            suggestions = []
            if realism_score < 0.7:
                suggestions.append("Improve lighting consistency")
            if technical_quality < 0.8:
                suggestions.append("Enhance image sharpness")
            if aesthetic_score < 0.7:
                suggestions.append("Adjust color balance")

            processing_time = time.time() - start_time

            return QualityAssessmentResult(
                success=True,
                status=ProcessingStatus.COMPLETED,
                message="Successfully assessed image quality",
                processing_time_seconds=processing_time,
                cost_estimate=random.uniform(0.002, 0.01),
                overall_score=overall_score,
                realism_score=realism_score,
                technical_quality=technical_quality,
                aesthetic_score=aesthetic_score,
                improvement_suggestions=suggestions,
                metadata={
                    'image_size': image.size,
                    'has_reference': reference_image is not None,
                    'assessment_method': 'mock_ai'
                }
            )

        except Exception as e:
            processing_time = time.time() - start_time
            return QualityAssessmentResult(
                success=False,
                status=ProcessingStatus.FAILED,
                message="Failed to assess image quality",
                error_details=str(e),
                processing_time_seconds=processing_time
            )

    def get_service_status(self) -> Dict[str, Any]:
        """Get mock service status."""
        return {
            'service_name': self.config.service_name,
            'status': 'operational',
            'uptime': '99.8%',
            'avg_response_time': '1.3s',
            'requests_today': random.randint(50, 500)
        }


class MockAIProvider(BaseAIProvider):
    """Mock AI service provider for testing and development."""

    def __init__(self):
        super().__init__(
            provider_name='mock_ai',
            supported_services=[
                AIServiceType.IMAGE_GENERATION,
                AIServiceType.COMPUTER_VISION,
                AIServiceType.IMAGE_ENHANCEMENT
            ]
        )

    def create_service(self, service_type: AIServiceType, config: AIServiceConfig):
        """Create a mock service instance."""
        if not self._validate_service_type(service_type):
            return None

        if service_type == AIServiceType.IMAGE_GENERATION:
            return MockImageGenerationService(config)
        elif service_type == AIServiceType.COMPUTER_VISION:
            return MockVisionService(config)
        elif service_type == AIServiceType.IMAGE_ENHANCEMENT:
            # For mock provider, image enhancement is handled by the generation service
            return MockImageGenerationService(config)

        return None
