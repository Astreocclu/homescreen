#!/usr/bin/env python3
"""
Script to help add and manage screen reference images.
This script provides utilities for organizing and validating reference images.
"""

import os
import shutil
from pathlib import Path
from PIL import Image
import argparse

def setup_reference_directories():
    """Create the comprehensive reference image directory structure."""
    base_dir = Path("media/screen_references")

    # Main screen type categories
    screen_types = ["security", "lifestyle", "solar", "pet_resistant"]

    # Sub-categories for organization
    subcategories = [
        "real_installs",      # Actual customer installations
        "fabric_samples",     # Close-up fabric/mesh samples
        "top_tier_renders",   # Best AI-generated examples
        "brand_samples",      # Manufacturer product photos
        "lighting_examples",  # Different lighting conditions
        "angle_variations",   # Different viewing angles
        "before_after",       # Before/after comparisons
        "problem_cases",      # Challenging installations
        "seasonal_examples"   # Different seasons/weather
    ]

    # Create main directories
    for screen_type in screen_types:
        for subcategory in subcategories:
            dir_path = base_dir / screen_type / subcategory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {dir_path}")

    # Create additional specialized directories
    specialized_dirs = [
        "reference_comparisons",  # Side-by-side comparisons
        "customer_feedback",      # Customer-submitted photos
        "quality_benchmarks",     # High-quality reference standards
        "troubleshooting",        # Common issues and solutions
        "competitive_analysis"    # Competitor examples for reference
    ]

    for spec_dir in specialized_dirs:
        dir_path = base_dir / spec_dir
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created specialized: {dir_path}")

    print(f"\n📁 Comprehensive reference system ready at: {base_dir}")
    print(f"📊 Created {len(screen_types) * len(subcategories) + len(specialized_dirs)} directories")

def add_reference_image(image_path, screen_type, subcategory=None, description=None):
    """Add a reference image to the appropriate directory."""
    try:
        source_path = Path(image_path)
        if not source_path.exists():
            print(f"❌ Source image not found: {image_path}")
            return False

        # Validate it's an image
        try:
            with Image.open(source_path) as img:
                width, height = img.size
                print(f"📸 Image info: {width}x{height}, format: {img.format}")
        except Exception as e:
            print(f"❌ Invalid image file: {str(e)}")
            return False

        # Determine target directory
        screen_type_lower = screen_type.lower()
        if 'security' in screen_type_lower:
            target_dir = "security"
        elif 'lifestyle' in screen_type_lower or 'decorative' in screen_type_lower:
            target_dir = "lifestyle"
        elif 'solar' in screen_type_lower or 'uv' in screen_type_lower:
            target_dir = "solar"
        elif 'pet' in screen_type_lower:
            target_dir = "pet_resistant"
        else:
            target_dir = "lifestyle"  # Default

        # Determine subcategory
        if not subcategory:
            subcategory = "fabric_samples"  # Default subcategory

        # Create target path
        base_dir = Path("media/screen_references")
        target_directory = base_dir / target_dir / subcategory
        target_directory.mkdir(parents=True, exist_ok=True)

        # Generate filename
        if description:
            # Use description for filename
            filename = f"{screen_type}_{description}".replace(" ", "_").lower()
        else:
            # Use original filename
            filename = source_path.stem

        # Add extension
        filename += source_path.suffix
        target_path = target_directory / filename

        # Copy the file
        shutil.copy2(source_path, target_path)
        print(f"✅ Added reference image: {target_path}")

        return True

    except Exception as e:
        print(f"❌ Error adding reference image: {str(e)}")
        return False

def list_reference_images():
    """List all reference images by organized category structure."""
    base_dir = Path("media/screen_references")

    if not base_dir.exists():
        print("❌ Reference directory not found. Run setup first.")
        return

    total_images = 0
    screen_types = ["security", "lifestyle", "solar", "pet_resistant"]

    # List organized screen type directories
    for screen_type in screen_types:
        screen_dir = base_dir / screen_type
        if screen_dir.exists():
            screen_total = 0
            print(f"\n📁 {screen_type.upper()}")

            # List subcategories
            for subcategory_dir in sorted(screen_dir.iterdir()):
                if subcategory_dir.is_dir():
                    images = list(subcategory_dir.glob("*.jpg")) + list(subcategory_dir.glob("*.jpeg")) + list(subcategory_dir.glob("*.png"))

                    if images:
                        print(f"   📂 {subcategory_dir.name} ({len(images)} images)")
                        for image in sorted(images):
                            try:
                                with Image.open(image) as img:
                                    size_info = f"{img.size[0]}x{img.size[1]}"
                            except:
                                size_info = "unknown"

                            print(f"      📸 {image.name} ({size_info})")
                            screen_total += 1
                            total_images += 1
                    else:
                        print(f"   📂 {subcategory_dir.name} (empty)")

            if screen_total == 0:
                print("   (no images in any subcategory)")

    # List specialized directories
    specialized_dirs = ["reference_comparisons", "customer_feedback", "quality_benchmarks", "troubleshooting", "competitive_analysis"]

    print(f"\n📁 SPECIALIZED DIRECTORIES")
    for spec_dir_name in specialized_dirs:
        spec_dir = base_dir / spec_dir_name
        if spec_dir.exists():
            images = list(spec_dir.glob("*.jpg")) + list(spec_dir.glob("*.jpeg")) + list(spec_dir.glob("*.png"))

            if images:
                print(f"   📂 {spec_dir_name} ({len(images)} images)")
                for image in sorted(images):
                    try:
                        with Image.open(image) as img:
                            size_info = f"{img.size[0]}x{img.size[1]}"
                    except:
                        size_info = "unknown"

                    print(f"      📸 {image.name} ({size_info})")
                    total_images += 1
            else:
                print(f"   📂 {spec_dir_name} (empty)")

    print(f"\n📊 Total reference images: {total_images}")

    # Show organization summary
    if total_images > 0:
        print(f"\n📈 Organization Summary:")
        for screen_type in screen_types:
            screen_dir = base_dir / screen_type
            if screen_dir.exists():
                screen_count = sum(len(list(subdir.glob("*.jpg")) + list(subdir.glob("*.jpeg")) + list(subdir.glob("*.png")))
                                 for subdir in screen_dir.iterdir() if subdir.is_dir())
                if screen_count > 0:
                    print(f"   {screen_type}: {screen_count} images")
    else:
        print(f"\n💡 Tip: Add reference images using:")
        print(f"   python add_screen_references.py add --image photo.jpg --type security --subcategory real_installs")

def validate_reference_images():
    """Validate all reference images."""
    base_dir = Path("media/screen_references")

    if not base_dir.exists():
        print("❌ Reference directory not found.")
        return

    valid_images = 0
    invalid_images = 0

    for category_dir in base_dir.iterdir():
        if category_dir.is_dir():
            print(f"\n🔍 Validating {category_dir.name}...")

            for image_file in category_dir.glob("*"):
                if image_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    try:
                        with Image.open(image_file) as img:
                            width, height = img.size

                            # Check minimum size
                            if width < 400 or height < 300:
                                print(f"   ⚠️  {image_file.name}: Small size ({width}x{height})")
                            else:
                                print(f"   ✅ {image_file.name}: {width}x{height}")

                            valid_images += 1

                    except Exception as e:
                        print(f"   ❌ {image_file.name}: Invalid image ({str(e)})")
                        invalid_images += 1

    print(f"\n📊 Validation Results:")
    print(f"   ✅ Valid images: {valid_images}")
    print(f"   ❌ Invalid images: {invalid_images}")

def create_sample_images():
    """Create sample reference images for testing."""
    print("🎨 Creating sample reference images...")

    base_dir = Path("media/screen_references")

    # Sample image configurations
    samples = [
        ("security", "fine_mesh", (128, 128, 128), 4),
        ("security", "coarse_mesh", (100, 100, 100), 8),
        ("lifestyle", "decorative_pattern", (150, 150, 150), 6),
        ("solar", "dark_blocking", (60, 60, 60), 5),
        ("pet_resistant", "heavy_duty", (120, 120, 120), 7)
    ]

    for category, name, color, mesh_size in samples:
        # Create a simple mesh pattern image
        width, height = 400, 300
        image = Image.new('RGB', (width, height), color='white')

        # Draw mesh pattern
        from PIL import ImageDraw
        draw = ImageDraw.Draw(image)

        # Horizontal lines
        for y in range(0, height, mesh_size):
            draw.line([(0, y), (width, y)], fill=color, width=1)

        # Vertical lines
        for x in range(0, width, mesh_size):
            draw.line([(x, 0), (x, height)], fill=color, width=1)

        # Save the image
        target_dir = base_dir / category
        target_dir.mkdir(parents=True, exist_ok=True)

        filename = f"sample_{name}.jpg"
        target_path = target_dir / filename

        image.save(target_path, 'JPEG', quality=85)
        print(f"✅ Created sample: {target_path}")

    print("🎉 Sample reference images created!")

def main():
    parser = argparse.ArgumentParser(description="Manage screen reference images")
    parser.add_argument('command', choices=['setup', 'add', 'list', 'validate', 'samples'],
                       help='Command to execute')
    parser.add_argument('--image', help='Path to image file (for add command)')
    parser.add_argument('--type', help='Screen type: security, lifestyle, solar, pet_resistant')
    parser.add_argument('--subcategory', help='Subcategory: real_installs, fabric_samples, top_tier_renders, etc.')
    parser.add_argument('--description', help='Description for filename (for add command)')

    args = parser.parse_args()

    if args.command == 'setup':
        setup_reference_directories()

    elif args.command == 'add':
        if not args.image or not args.type:
            print("❌ --image and --type are required for add command")
            return
        add_reference_image(args.image, args.type, args.subcategory, args.description)

    elif args.command == 'list':
        list_reference_images()

    elif args.command == 'validate':
        validate_reference_images()

    elif args.command == 'samples':
        create_sample_images()

if __name__ == "__main__":
    print("🏠 Screen Reference Image Manager")
    print("=" * 40)

    if len(os.sys.argv) == 1:
        # No arguments, show help
        print("\nUsage examples:")
        print("  python add_screen_references.py setup")
        print("  python add_screen_references.py samples")
        print("  python add_screen_references.py add --image photo.jpg --type security --subcategory real_installs --description fine_mesh")
        print("  python add_screen_references.py add --image fabric.jpg --type lifestyle --subcategory fabric_samples")
        print("  python add_screen_references.py list")
        print("  python add_screen_references.py validate")

        print("\nCommands:")
        print("  setup     - Create comprehensive reference directory structure")
        print("  add       - Add a reference image to organized folders")
        print("  list      - List all reference images by category")
        print("  validate  - Validate reference images quality")
        print("  samples   - Create sample images for testing")

        print("\nScreen Types:")
        print("  security, lifestyle, solar, pet_resistant")

        print("\nSubcategories:")
        print("  real_installs      - Actual customer installations")
        print("  fabric_samples     - Close-up fabric/mesh samples")
        print("  top_tier_renders   - Best AI-generated examples")
        print("  brand_samples      - Manufacturer product photos")
        print("  lighting_examples  - Different lighting conditions")
        print("  angle_variations   - Different viewing angles")
        print("  before_after       - Before/after comparisons")
        print("  problem_cases      - Challenging installations")
        print("  seasonal_examples  - Different seasons/weather")
    else:
        main()
