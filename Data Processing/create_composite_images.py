
import os
import random
from PIL import Image
import albumentations as A
import numpy as np

def augment_image(image):
    aug = A.Compose([
        A.HorizontalFlip(p=0.5),
        A.Rotate(limit=20),
        A.RandomBrightnessContrast(p=0.2),
        A.RandomScale(scale_limit=0.2, p=1.0)
    ])

    image_np = np.array(image)

    # Apply the augmentation
    augmented_image_np = aug(image=image_np)['image']

    augmented_image = Image.fromarray(augmented_image_np)

    return augmented_image

def create_composite_image(images, save_path):
    composite_image = Image.new('RGB', (512, 512), (255, 255, 255))

    resized_images = [img.resize((256, 256)) for img in images]

    composite_image.paste(resized_images[0], (0, 0))
    composite_image.paste(resized_images[1], (255, 0))
    composite_image.paste(resized_images[2], (0, 255))
    composite_image.paste(resized_images[3], (255, 255))

    composite_image.save(save_path)
    print(f"Saved composite image to {save_path}")

def choose_images(image_files, total_images):
    if total_images >= 4:
        selected_images = random.sample(image_files, 4)
    else:
        selected_images = image_files + [image_files[-1]] * (4 - total_images)
    return selected_images

def process_directory(directory):
    image_files = [f for f in os.listdir(directory) if f.lower().startswith('image') and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print(f"No images found in {directory}. Skipping.")
        return

    total_images = len(image_files)
    image_files.sort()

    # First Composite: Random selection from original images
    selected_images = choose_images(image_files, total_images)
    images_to_use = [Image.open(os.path.join(directory, img)) for img in selected_images]
    save_path = os.path.join(directory, 'composite_0.jpg')
    create_composite_image(images_to_use, save_path)

    # Second Composite: Random selection with augmentation
    selected_images = choose_images(image_files, total_images)
    images_to_use = [augment_image(Image.open(os.path.join(directory, img))) for img in selected_images]
    save_path = os.path.join(directory, 'composite_1.jpg')
    create_composite_image(images_to_use, save_path)

    # Third Composite: Another random selection with augmentation
    selected_images = choose_images(image_files, total_images)
    images_to_use = [augment_image(Image.open(os.path.join(directory, img))) for img in selected_images]
    save_path = os.path.join(directory, 'composite_2.jpg')
    create_composite_image(images_to_use, save_path)

def process_image_folders(base_directory):
    for root, dirs, files in os.walk(base_directory):
        for dir_name in dirs:
            directory = os.path.join(root, dir_name)
            process_directory(directory)

# Usage
base_directory = 'images'
process_image_folders(base_directory)
