#!/usr/bin/env python3
"""
Script to organize existing reference images into the new structure.
This will move your existing solar screen photos into the proper organized folders.
"""

import os
import shutil
from pathlib import Path

def organize_solar_images():
    """Organize existing solar screen images into proper structure."""
    base_dir = Path("media/screen_references/solar")
    
    # Source directories with existing images
    source_dirs = [
        base_dir / "Real Installs",
        base_dir / "Solar Screens"
    ]
    
    # Target directory for real installations
    target_dir = base_dir / "real_installs"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    moved_count = 0
    
    for source_dir in source_dirs:
        if source_dir.exists():
            print(f"📁 Processing {source_dir.name}...")
            
            # Find all image files
            image_files = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
                image_files.extend(source_dir.glob(ext))
            
            print(f"   Found {len(image_files)} images")
            
            # Move each image to the organized structure
            for image_file in image_files:
                try:
                    # Create new filename to avoid conflicts
                    new_filename = f"solar_install_{moved_count:03d}_{image_file.name}"
                    target_path = target_dir / new_filename
                    
                    # Move the file
                    shutil.move(str(image_file), str(target_path))
                    print(f"   ✅ Moved: {image_file.name} → {new_filename}")
                    moved_count += 1
                    
                except Exception as e:
                    print(f"   ❌ Error moving {image_file.name}: {str(e)}")
            
            # Remove empty source directory
            try:
                if source_dir.exists() and not any(source_dir.iterdir()):
                    source_dir.rmdir()
                    print(f"   🗑️ Removed empty directory: {source_dir.name}")
            except:
                pass
    
    print(f"\n🎉 Organization complete!")
    print(f"   Moved {moved_count} solar screen images to real_installs/")
    return moved_count

def categorize_images_by_content():
    """Categorize images based on their content and filenames."""
    base_dir = Path("media/screen_references/solar/real_installs")
    
    if not base_dir.exists():
        print("❌ No real_installs directory found")
        return
    
    # Create subcategory directories
    subcategories = {
        'hardware_examples': base_dir.parent / 'brand_samples',
        'lighting_variations': base_dir.parent / 'lighting_examples',
        'angle_shots': base_dir.parent / 'angle_variations',
        'close_ups': base_dir.parent / 'fabric_samples'
    }
    
    for subcat_dir in subcategories.values():
        subcat_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all images
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        image_files.extend(base_dir.glob(ext))
    
    categorized = 0
    
    print(f"📊 Analyzing {len(image_files)} images for categorization...")
    
    for image_file in image_files:
        filename_lower = image_file.name.lower()
        moved = False
        
        # Categorize based on filename
        if 'hardware' in filename_lower or 'bronze' in filename_lower or 'ivory' in filename_lower:
            # Hardware/brand examples
            target_dir = subcategories['hardware_examples']
            new_name = f"hardware_{image_file.name}"
            try:
                shutil.move(str(image_file), str(target_dir / new_name))
                print(f"   🏷️ Hardware: {image_file.name} → brand_samples/")
                categorized += 1
                moved = True
            except:
                pass
        
        elif 'no see um' in filename_lower or 'noseeum' in filename_lower:
            # Close-up fabric samples
            target_dir = subcategories['close_ups']
            new_name = f"fabric_{image_file.name}"
            try:
                shutil.move(str(image_file), str(target_dir / new_name))
                print(f"   🧵 Fabric: {image_file.name} → fabric_samples/")
                categorized += 1
                moved = True
            except:
                pass
        
        # If not moved, keep in real_installs (which is perfect!)
        if not moved:
            print(f"   🏠 Install: {image_file.name} → staying in real_installs/")
    
    print(f"\n📈 Categorization complete!")
    print(f"   Categorized {categorized} images into specialized folders")
    print(f"   Remaining images stay in real_installs/ (perfect!)")

def show_organization_summary():
    """Show summary of organized images."""
    base_dir = Path("media/screen_references/solar")
    
    print(f"\n📊 SOLAR SCREEN ORGANIZATION SUMMARY")
    print(f"=" * 50)
    
    subcategories = [
        'real_installs',
        'fabric_samples', 
        'brand_samples',
        'lighting_examples',
        'angle_variations'
    ]
    
    total_images = 0
    
    for subcat in subcategories:
        subcat_dir = base_dir / subcat
        if subcat_dir.exists():
            images = list(subcat_dir.glob("*.jpg")) + list(subcat_dir.glob("*.jpeg")) + list(subcat_dir.glob("*.png"))
            count = len(images)
            total_images += count
            
            if count > 0:
                print(f"📂 {subcat}: {count} images")
                # Show a few example filenames
                for i, img in enumerate(sorted(images)[:3]):
                    print(f"   📸 {img.name}")
                if count > 3:
                    print(f"   ... and {count - 3} more")
            else:
                print(f"📂 {subcat}: empty")
    
    print(f"\n🎯 Total Solar Images: {total_images}")
    
    if total_images > 0:
        print(f"\n🚀 AI Impact:")
        print(f"   ✅ Real customer installations will provide authentic reference")
        print(f"   ✅ Hardware examples will show proper frame integration")
        print(f"   ✅ Fabric samples will ensure accurate mesh patterns")
        print(f"   ✅ Your AI will generate incredibly realistic solar screen visualizations!")

if __name__ == "__main__":
    print("🏠 Organizing Existing Solar Screen References")
    print("=" * 50)
    
    # Step 1: Move images to organized structure
    moved_count = organize_solar_images()
    
    if moved_count > 0:
        # Step 2: Categorize by content
        categorize_images_by_content()
        
        # Step 3: Show summary
        show_organization_summary()
        
        print(f"\n🎉 SUCCESS!")
        print(f"Your {moved_count} solar screen photos are now perfectly organized!")
        print(f"The AI will use these real installation photos to generate incredibly accurate visualizations!")
        
        print(f"\n🚀 Next Steps:")
        print(f"1. Test the AI with a house image and solar screen type")
        print(f"2. Add security/lifestyle photos to their respective folders")
        print(f"3. Watch your AI generate professional-quality results!")
    else:
        print(f"ℹ️ No images found to organize")
