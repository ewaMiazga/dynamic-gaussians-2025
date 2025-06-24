import os
import shutil
from pathlib import Path

source_root = Path("3dgstream-output/final-training")
rendered_output = Path("3dgstream-output/rendered")
rendered_output.mkdir(exist_ok=True)

for frame_dir in sorted(source_root.iterdir()):
    if not frame_dir.is_dir():
        continue

    rendered_path = frame_dir / "0_rendering2.png"
    if rendered_path.exists():
        dest_name = f"{frame_dir.name}_rendering2.png"
        shutil.copy(rendered_path, rendered_output / dest_name)

print("All rendered images copied to 'rendered/'")