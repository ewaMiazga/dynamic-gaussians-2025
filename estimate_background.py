import cv2
import numpy as np
import glob
import os

import argparse
# Load all image paths (adjust extension if needed)

def estimate_background(folder):
    image_paths = sorted(glob.glob(f'{folder}/*.png'))
    # now I want to pass global folder which includes folders like cam_0 to cam_12 



    frames = []

    for path in image_paths:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # Use cv2.IMREAD_COLOR if images are RGB
        frames.append(img)

    # Stack all frames into a 3D NumPy array: shape (num_images, height, width)
    stack = np.stack(frames, axis=0)

    # Compute pixel-wise median across the stack
    background = np.median(stack, axis=0).astype(np.uint8)

    # Save the estimated background image
    cv2.imwrite("background_median.png", background)

    print("Background saved as background_median.png")
    return background


import cv2
import numpy as np
import os

def create_segmentation_mask(background_path, image_path, output_mask_path, threshold_value=30, morph_kernel_size=3,
    morph_iterations=2, dilate_iterations=2):
    """
    Generates a binary segmentation mask by subtracting a static background
    from a target image and saves the result.
    Parameters:
        background_path (str): Path to background image (grayscale).
        image_path (str): Path to image to segment.
        output_mask_path (str): Path to save the binary mask (PNG).
        threshold_value (int): Threshold for foreground detection.
        morph_kernel_size (int): Size of morphological kernel.
        morph_iterations (int): Iterations for morphological open.
        dilate_iterations (int): Iterations for dilation to fill gaps.

    Returns:
        mask (np.ndarray): The binary segmentation mask.
    """

    # Load grayscale images
    background = cv2.imread(background_path, cv2.IMREAD_GRAYSCALE)
    target = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if background is None or target is None:
        raise FileNotFoundError("Check if both background and image paths are valid.")

    if background.shape != target.shape:
        raise ValueError("Background and target image must be the same size.")

    # Background subtraction
    diff = cv2.absdiff(target, background)

    # Threshold the difference
    _, mask = cv2.threshold(diff, threshold_value, 255, cv2.THRESH_BINARY)

    # Morphological operations to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_kernel_size, morph_kernel_size))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=morph_iterations)
    mask = cv2.dilate(mask, kernel, iterations=dilate_iterations)

    # Save the mask
    os.makedirs(os.path.dirname(output_mask_path), exist_ok=True)
    cv2.imwrite(output_mask_path, mask)

    print(f"Segmentation mask saved to {output_mask_path}")
    return mask

if __name__ == "__main__":
    # pass path to the images folder by args in terminal
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=str, help="Path to the folder containing images")


    args = parser.parse_args()
    
    background = estimate_background(args.folder)

    for image_path in sorted(glob.glob(os.path.join(args.folder, "*.png"))):
        print(f"Processing {image_path}")
        
        seg_dir = os.path.join(args.folder, "seg")
        os.makedirs(seg_dir, exist_ok=True)
        # split image_path before name of the file
        image_path = os.path.basename(image_path)
        # image_path = os.path.join(args.folder, image_path)  # Full path to the image file
        # Create a segmentation mask for each image using the estimated background

        create_segmentation_mask(
            background_path="background_median.png",
            image_path=os.path.join(args.folder, image_path),  # Change to the first image in your folder
            output_mask_path=os.path.join(args.folder, "seg", image_path),
            threshold_value=30,
            morph_kernel_size=3,
            morph_iterations=2,
            dilate_iterations=2
        )
    