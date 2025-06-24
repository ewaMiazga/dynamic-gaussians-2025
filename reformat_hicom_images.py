import os
import shutil
from pathlib import Path

# Adjust this path if needed
frames_root = Path("hicom-output")
gt_output = Path("hicom-output/gt")
rendered_output = Path("hicom-output/rendered")

gt_output.mkdir(exist_ok=True)
rendered_output.mkdir(exist_ok=True)

for frame_dir in sorted(frames_root.iterdir()):
    if not frame_dir.is_dir():
        continue
    for file in frame_dir.iterdir():
        if file.suffix != ".png":
            continue
        if "_0_gt.png" in file.name:
            shutil.copy(file, gt_output / f"{frame_dir.name}_{file.name}")
        elif "_0_step200.png" in file.name:
            shutil.copy(file, rendered_output / f"{frame_dir.name}_{file.name}")