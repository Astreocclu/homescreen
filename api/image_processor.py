"""
Image processing service for generating homescreen visualizations.
Visualizes how physical window/door screens would look on homes.
"""

import os
import io
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
from django.core.files.base import ContentFile
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class HomescreenImageProcessor:
    """Service for processing images and generating physical screen visualizations."""

    def __init__(self):
        self.output_formats = ['JPEG', 'PNG']
        self.quality = 85
        self.max_output_size = (1920, 1080)

    def process_image(self, visualization_request):
        """
        Process an image and generate homescreen visualizations.

        Args:
            visualization_request: VisualizationRequest instance

        Returns:
            list: List of generated image file paths
        """
        try:
            # Mark request as processing
            visualization_request.mark_as_processing()

            # Load the original image
            visualization_request.update_progress(10, "Loading and validating image...")
            time.sleep(1)  # Simulate processing time
            original_image = Image.open(visualization_request.original_image.path)
            screen_type = visualization_request.screen_type

            # Generate different variations based on screen type
            visualization_request.update_progress(20, f"Preparing {screen_type.name} visualizations...")
            time.sleep(1)  # Simulate processing time
            generated_images = []

            if 'security' in screen_type.name.lower():
                generated_images.extend(self._generate_security_screen_overlays(original_image, visualization_request))
            elif 'entertainment' in screen_type.name.lower() or 'lifestyle' in screen_type.name.lower():
                generated_images.extend(self._generate_lifestyle_screen_overlays(original_image, visualization_request))
            elif 'smart home' in screen_type.name.lower():
                generated_images.extend(self._generate_smart_home_screen_overlays(original_image, visualization_request))
            else:
                # Default processing - show multiple screen types
                generated_images.extend(self._generate_multiple_screen_overlays(original_image, visualization_request))

            # Mark request as complete
            visualization_request.mark_as_complete()

            logger.info(f"Successfully processed request {visualization_request.id}, generated {len(generated_images)} images")
            return generated_images

        except Exception as e:
            error_msg = f"Error processing image: {str(e)}"
            logger.error(error_msg)
            visualization_request.mark_as_failed(error_msg)
            return []

    def _generate_security_screen_overlays(self, original_image, request):
        """Generate security screen overlays on the house image."""
        generated_images = []

        # Stainless Steel Mesh Screen
        request.update_progress(30, "Applying stainless steel mesh pattern...")
        time.sleep(1)
        steel_mesh = self._apply_security_mesh_overlay(original_image, mesh_type="stainless_steel")
        generated_images.append(self._save_generated_image(steel_mesh, request, "stainless_steel_mesh"))

        # Heavy Duty Security Screen
        request.update_progress(60, "Applying heavy duty security mesh...")
        time.sleep(1)
        heavy_duty = self._apply_security_mesh_overlay(original_image, mesh_type="heavy_duty")
        generated_images.append(self._save_generated_image(heavy_duty, request, "heavy_duty_security"))

        # Fine Mesh Security Screen
        request.update_progress(90, "Applying fine mesh security screen...")
        time.sleep(1)
        fine_mesh = self._apply_security_mesh_overlay(original_image, mesh_type="fine_mesh")
        generated_images.append(self._save_generated_image(fine_mesh, request, "fine_mesh_security"))

        return generated_images

    def _generate_lifestyle_screen_overlays(self, original_image, request):
        """Generate lifestyle screen overlays (Phifer, Twitchell, etc.)."""
        generated_images = []

        # Phifer Style Screen
        request.update_progress(40, "Applying Phifer-style screen pattern...")
        time.sleep(1)
        phifer_style = self._apply_lifestyle_screen_overlay(original_image, screen_type="phifer")
        generated_images.append(self._save_generated_image(phifer_style, request, "phifer_style"))

        # Twitchell Style Screen
        request.update_progress(70, "Applying Twitchell-style screen pattern...")
        time.sleep(1)
        twitchell_style = self._apply_lifestyle_screen_overlay(original_image, screen_type="twitchell")
        generated_images.append(self._save_generated_image(twitchell_style, request, "twitchell_style"))

        # Standard Fiberglass Screen
        request.update_progress(90, "Applying standard fiberglass screen...")
        time.sleep(1)
        fiberglass = self._apply_lifestyle_screen_overlay(original_image, screen_type="fiberglass")
        generated_images.append(self._save_generated_image(fiberglass, request, "fiberglass_standard"))

        return generated_images

    def _generate_smart_home_screen_overlays(self, original_image, request):
        """Generate smart home screen overlays."""
        generated_images = []

        # Solar Screen
        request.update_progress(50, "Applying solar screen pattern...")
        time.sleep(1)
        solar_screen = self._apply_lifestyle_screen_overlay(original_image, screen_type="solar")
        generated_images.append(self._save_generated_image(solar_screen, request, "solar_screen"))

        # Pet-Resistant Screen
        request.update_progress(75, "Applying pet-resistant screen...")
        time.sleep(1)
        pet_resistant = self._apply_lifestyle_screen_overlay(original_image, screen_type="pet_resistant")
        generated_images.append(self._save_generated_image(pet_resistant, request, "pet_resistant"))

        return generated_images

    def _generate_multiple_screen_overlays(self, original_image, request):
        """Generate multiple screen type overlays for comparison."""
        generated_images = []

        # Security mesh
        request.update_progress(40, "Applying security mesh...")
        time.sleep(1)
        security = self._apply_security_mesh_overlay(original_image, mesh_type="stainless_steel")
        generated_images.append(self._save_generated_image(security, request, "security_comparison"))

        # Lifestyle screen
        request.update_progress(70, "Applying lifestyle screen...")
        time.sleep(1)
        lifestyle = self._apply_lifestyle_screen_overlay(original_image, screen_type="phifer")
        generated_images.append(self._save_generated_image(lifestyle, request, "lifestyle_comparison"))

        return generated_images

    def _apply_security_mesh_overlay(self, original_image, mesh_type="stainless_steel"):
        """Apply security mesh overlay to simulate physical security screens."""
        result = original_image.copy()
        width, height = result.size

        # Create mesh pattern based on type (made more visible for testing)
        if mesh_type == "stainless_steel":
            mesh_color = (120, 120, 120, 200)  # Darker gray, more visible
            mesh_size = 12  # Larger mesh for visibility
        elif mesh_type == "heavy_duty":
            mesh_color = (80, 80, 80, 220)  # Much darker gray, very visible
            mesh_size = 16  # Even coarser mesh
        else:  # fine_mesh
            mesh_color = (150, 150, 150, 180)  # Medium gray, visible
            mesh_size = 8  # Fine but visible mesh

        # Create mesh overlay
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Draw horizontal lines
        for y in range(0, height, mesh_size):
            draw.line([(0, y), (width, y)], fill=mesh_color, width=1)

        # Draw vertical lines
        for x in range(0, width, mesh_size):
            draw.line([(x, 0), (x, height)], fill=mesh_color, width=1)

        # Apply overlay to original image
        result = result.convert('RGBA')
        result = Image.alpha_composite(result, overlay)
        result = result.convert('RGB')

        # Add subtle darkening to simulate screen effect
        enhancer = ImageEnhance.Brightness(result)
        result = enhancer.enhance(0.95)

        # Add a colored border to clearly show this is a processed image
        draw_final = ImageDraw.Draw(result)
        border_color = (255, 0, 0) if mesh_type == "stainless_steel" else (0, 255, 0) if mesh_type == "heavy_duty" else (0, 0, 255)
        border_width = 5
        draw_final.rectangle([0, 0, width-1, height-1], outline=border_color, width=border_width)

        # Add text label
        draw_final.text((10, 10), f"SECURITY MESH: {mesh_type.upper()}", fill=border_color)

        return result

    def _apply_lifestyle_screen_overlay(self, original_image, screen_type="phifer"):
        """Apply lifestyle screen overlay to simulate decorative/functional screens."""
        result = original_image.copy()
        width, height = result.size

        # Create screen pattern based on type (made more visible for testing)
        if screen_type == "phifer":
            # Phifer-style fine weave
            mesh_color = (180, 180, 180, 150)  # More visible gray
            mesh_size = 8  # Larger for visibility
            weave_pattern = True
        elif screen_type == "twitchell":
            # Twitchell-style decorative pattern
            mesh_color = (160, 160, 160, 160)  # More visible gray
            mesh_size = 10  # Larger weave
            weave_pattern = True
        elif screen_type == "solar":
            # Solar screen - darker to block sun
            mesh_color = (60, 60, 60, 200)  # Much darker, very visible
            mesh_size = 8  # Visible mesh
            weave_pattern = False
        elif screen_type == "pet_resistant":
            # Pet-resistant - thicker strands
            mesh_color = (120, 120, 120, 180)  # More visible gray
            mesh_size = 14  # Much thicker weave
            weave_pattern = False
        else:  # fiberglass
            # Standard fiberglass
            mesh_color = (140, 140, 140, 140)  # More visible gray
            mesh_size = 9  # Larger standard weave
            weave_pattern = True

        # Create screen overlay
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        if weave_pattern:
            # Create woven pattern (alternating over/under effect)
            for y in range(0, height, mesh_size):
                for x in range(0, width, mesh_size * 2):
                    # Horizontal strand
                    draw.line([(x, y), (x + mesh_size, y)], fill=mesh_color, width=1)

            for x in range(0, width, mesh_size):
                for y in range(mesh_size//2, height, mesh_size * 2):
                    # Vertical strand (offset to create weave)
                    draw.line([(x, y), (x, y + mesh_size)], fill=mesh_color, width=1)
        else:
            # Simple grid pattern
            for y in range(0, height, mesh_size):
                draw.line([(0, y), (width, y)], fill=mesh_color, width=1)
            for x in range(0, width, mesh_size):
                draw.line([(x, 0), (x, height)], fill=mesh_color, width=1)

        # Apply overlay to original image
        result = result.convert('RGBA')
        result = Image.alpha_composite(result, overlay)
        result = result.convert('RGB')

        # Apply screen-specific effects
        if screen_type == "solar":
            # Solar screens reduce brightness and add slight tint
            enhancer = ImageEnhance.Brightness(result)
            result = enhancer.enhance(0.85)
        else:
            # Other screens have minimal brightness impact
            enhancer = ImageEnhance.Brightness(result)
            result = enhancer.enhance(0.98)

        # Add a colored border to clearly show this is a processed image
        draw_final = ImageDraw.Draw(result)
        border_colors = {
            "phifer": (255, 165, 0),      # Orange
            "twitchell": (128, 0, 128),   # Purple
            "solar": (255, 255, 0),       # Yellow
            "pet_resistant": (0, 255, 255), # Cyan
            "fiberglass": (255, 192, 203)   # Pink
        }
        border_color = border_colors.get(screen_type, (128, 128, 128))
        border_width = 5
        draw_final.rectangle([0, 0, width-1, height-1], outline=border_color, width=border_width)

        # Add text label
        draw_final.text((10, 10), f"LIFESTYLE SCREEN: {screen_type.upper()}", fill=border_color)

        return result

    def _save_generated_image(self, image, request, suffix):
        """Save a generated image and create a GeneratedImage record."""
        from .models import GeneratedImage

        # Resize if too large
        if image.size[0] > self.max_output_size[0] or image.size[1] > self.max_output_size[1]:
            image.thumbnail(self.max_output_size, Image.Resampling.LANCZOS)

        # Save to BytesIO
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=self.quality)
        output.seek(0)

        # Create filename
        filename = f"generated_{request.id}_{suffix}.jpg"

        # Create GeneratedImage record
        generated_image = GeneratedImage(request=request)
        generated_image.generated_image.save(
            filename,
            ContentFile(output.getvalue()),
            save=True
        )

        return generated_image
