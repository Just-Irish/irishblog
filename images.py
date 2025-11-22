import os
import re
import shutil
from urllib.parse import quote

# Paths
posts_dir = "/home/irish/irishblog/content/posts/"
attachments_dir = "/home/irish/Github Projects/Website Posts/"
static_images_dir = "/home/irish/irishblog/static/images/"

# Ensure static images directory exists
os.makedirs(static_images_dir, exist_ok=True)

# Step 1: Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        original_content = content

        # Step 2: Find all image links in VSCodium format: ![alt text](image.png)
        # This pattern captures both the alt text and the image filename
        image_pattern = r'!\[([^\]]*)\]\(([^)]+\.(?:png|jpg|jpeg|gif|webp|svg))\)'
        images = re.findall(image_pattern, content, re.IGNORECASE)

        # Step 3: Replace relative image paths with Hugo /images/ paths and copy images
        for alt_text, image_path in images:
            # Extract just the filename from the path (in case it has subdirectories)
            image_filename = os.path.basename(image_path)
            
            # Create the Hugo-compatible path
            hugo_path = f"/images/{quote(image_filename)}"
            
            # Replace the old path with the new Hugo path
            old_link = f"![{alt_text}]({image_path})"
            new_link = f"![{alt_text}]({hugo_path})"
            content = content.replace(old_link, new_link)

            # Step 4: Copy the image to the Hugo static/images directory if it exists
            # Try the image path as-is first, then try in attachments_dir
            image_source = None
            
            # Check if image_path is relative to posts_dir
            potential_source = os.path.join(os.path.dirname(filepath), image_path)
            if os.path.exists(potential_source):
                image_source = potential_source
            # Check if it's in the attachments directory
            elif os.path.exists(os.path.join(attachments_dir, image_filename)):
                image_source = os.path.join(attachments_dir, image_filename)
            # Check if it's directly the filename in attachments
            elif os.path.exists(os.path.join(attachments_dir, image_path)):
                image_source = os.path.join(attachments_dir, image_path)
            
            if image_source and os.path.exists(image_source):
                shutil.copy(image_source, static_images_dir)
                print(f"  ✓ Copied: {image_filename}")
            else:
                print(f"  ✗ Missing: {image_filename}")

        # Step 5: Write the updated content back to the markdown file only if changed
        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"Updated: {filename}")

print("\nMarkdown files processed and images copied successfully.")
