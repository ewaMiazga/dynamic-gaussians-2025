import cv2
import os
from pathlib import Path

videos_dir = "videos"  # folder with cam00.mp4, cam01.mp4, ...
output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)

# Open all video files and assign camera IDs
video_paths = sorted(Path(videos_dir).glob("*.mp4"))
video_caps = {}
for path in video_paths:
    cam_id = path.stem  # e.g., cam00
    video_caps[cam_id] = cv2.VideoCapture(str(path))

frame_counter = 0

while True:
    current_frames = {}
    end_of_any_video = False

    for cam_id, cap in video_caps.items():
        ret, frame = cap.read()
        if not ret:
            end_of_any_video = True
            break
        current_frames[cam_id] = frame

    if end_of_any_video:
        break

    # Save all camera frames into folder frame_XXXXXX
    frame_folder = os.path.join(output_dir, f"frame_{frame_counter:06d}")
    os.makedirs(frame_folder, exist_ok=True)
    for cam_id, frame in current_frames.items():
        out_path = os.path.join(frame_folder, f"{cam_id}.png")
        cv2.imwrite(out_path, frame)

    frame_counter += 1

# Release all video captures
for cap in video_caps.values():
    cap.release()

print(f"✅ Extracted {frame_counter} frame folders to {output_dir}")
