#!/usr/bin/env python3
"""
Generate all icon files from source image
"""
from PIL import Image
import os

# Source image path
source_path = "kemeow0815.webp"

# Target directory
target_dir = "frontend/public"
icons_dir = os.path.join(target_dir, "icons")

# Ensure directories exist
os.makedirs(icons_dir, exist_ok=True)

# Open source image
img = Image.open(source_path)

# Convert to RGBA if necessary
if img.mode != 'RGBA':
    img = img.convert('RGBA')

# Define icon sizes
icons = {
    # PWA icons
    "icons/pwa-192.png": (192, 192),
    "icons/pwa-512.png": (512, 512),

    # Apple touch icon
    "apple-icon.png": (180, 180),

    # Favicon PNG variants
    "favicon-dark-32x32.png": (32, 32),
    "favicon-light-32x32.png": (32, 32),

    # Favicon ICO (multi-size)
    "favicon.ico": [(16, 16), (32, 32), (48, 48)],
}

# Generate PNG icons
for filename, size in icons.items():
    if filename == "favicon.ico":
        continue  # Handle ICO separately

    # Resize image
    resized = img.copy()
    resized.thumbnail(size, Image.Resampling.LANCZOS)

    # Create a new image with the exact size (center the icon)
    new_img = Image.new('RGBA', size, (0, 0, 0, 0))

    # Calculate position to center the image
    x = (size[0] - resized.width) // 2
    y = (size[1] - resized.height) // 2

    # Paste the resized image
    new_img.paste(resized, (x, y), resized)

    # Save
    output_path = os.path.join(target_dir, filename)
    new_img.save(output_path, 'PNG')
    print(f"Generated: {output_path}")

# Generate ICO file with multiple sizes
ico_sizes = icons["favicon.ico"]
ico_images = []
for ico_size in ico_sizes:
    resized = img.copy()
    resized.thumbnail(ico_size, Image.Resampling.LANCZOS)

    # Create a new image with the exact size
    new_img = Image.new('RGBA', ico_size, (0, 0, 0, 0))

    # Calculate position to center the image
    x = (ico_size[0] - resized.width) // 2
    y = (ico_size[1] - resized.height) // 2

    # Paste the resized image
    new_img.paste(resized, (x, y), resized)

    # Convert to RGB for ICO (some sizes)
    if ico_size[0] <= 32:
        rgb_img = Image.new('RGB', ico_size, (255, 255, 255))
        rgb_img.paste(new_img, mask=new_img.split()[3])
        ico_images.append(rgb_img)
    else:
        ico_images.append(new_img)

# Save ICO file
ico_path = os.path.join(target_dir, "favicon.ico")
ico_images[0].save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in ico_images], append_images=ico_images[1:])
print(f"Generated: {ico_path}")

# Generate SVG favicon (using the original image as base64)
import base64

# Create a 512x512 version for SVG
svg_size = (512, 512)
resized = img.copy()
resized.thumbnail(svg_size, Image.Resampling.LANCZOS)

# Save to bytes
import io
buffer = io.BytesIO()
resized.save(buffer, format='PNG')
img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

# Create SVG with embedded image
svg_content = f'''<svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <image xlink:href="data:image/png;base64,{img_base64}" width="512" height="512"/>
</svg>'''

svg_path = os.path.join(target_dir, "favicon.svg")
with open(svg_path, 'w') as f:
    f.write(svg_content)
print(f"Generated: {svg_path}")

print("\nAll icons generated successfully!")
