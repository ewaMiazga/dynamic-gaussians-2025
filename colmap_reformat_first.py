import os
from tqdm import tqdm
import numpy as np
import argparse
import json
from PIL import Image as PImage
from scipy import ndimage
from matplotlib import pyplot as plt

from colmap_loader import *

from os import makedirs

def main(args):
    scene_folder = args.folder
    
    duration = args.duration
    test_cameras = args.test_cameras


    train_meta = {}
    test_meta = {}



    train_meta["k"] = []
    train_meta["w2c"] = []
    train_meta["fn"] = []
    train_meta["cam_id"] = []

    test_meta["k"] = []
    test_meta["w2c"] = []
    test_meta["fn"] = []
    test_meta["cam_id"] = []

    colmap_path = os.path.join(scene_folder, f"colmap_0")
    intrinsics = read_intrinsics_binary(os.path.join(colmap_path, "sparse", "0","cameras.bin"))
    extrinsics = read_extrinsics_binary(os.path.join(colmap_path, "sparse", "0","images.bin"))
    xyz, rgb, _ = read_points3D_binary(os.path.join(colmap_path, "sparse", "0","points3D.bin"))
        

    # Calculate the intrinsics matrices
    intrinsics_matrices = {}
    for cam_id, camera in intrinsics.items():
        mat = np.eye(3)
        mat[0,0] = camera.params[0]
        mat[1,1] = camera.params[1]
        mat[0,2] = camera.params[2]
        mat[1,2] = camera.params[3]

        intrinsics_matrices[cam_id] = mat

    # Calculate the extrinsics matrices
    w2c_matrices = {}
    camera_names = {}
    for cam_id, image in extrinsics.items():
        qvec = image.qvec
        tvec = image.tvec
        rot = qvec2rotmat(qvec)
        w2c = np.eye(4)
        w2c[:3, :3] = rot
        w2c[:3, 3] = tvec
        w2c_matrices[cam_id] = w2c
        camera_names[cam_id] = int(image.name[3:-4])
        #camera_names[cam_id] = int(image.name[3:-4].lstrip('_'))



    for t in tqdm(range(duration)):
        train_ks = []
        train_w2cs = []
        train_fns = []
        train_cam_ids = []

        test_ks = []
        test_w2cs = []
        test_fns = []
        test_cam_ids = []

        #cameras = intrinsics_matrices.keys()
        cameras = sorted(intrinsics_matrices.keys(), key=lambda x: camera_names[x])

        for cam_id in cameras:
            camera_name = camera_names[cam_id]

            if camera_name in test_cameras:
                test_ks.append(intrinsics_matrices[cam_id].tolist())
                test_w2cs.append(w2c_matrices[cam_id].tolist())
                test_fns.append(os.path.join(f"cam{camera_name:02d}", f"{t}.png"))
                test_cam_ids.append(camera_name)
                test_meta["w"] = intrinsics[cam_id].width
                test_meta["h"] = intrinsics[cam_id].height
            else:
                train_ks.append(intrinsics_matrices[cam_id].tolist())
                train_w2cs.append(w2c_matrices[cam_id].tolist())
                train_fns.append(os.path.join(f"cam{camera_name:02d}", f"{t}.png"))
                train_cam_ids.append(camera_name)
                train_meta["w"] = intrinsics[cam_id].width
                train_meta["h"] = intrinsics[cam_id].height
        
        train_meta["k"].append(train_ks)
        train_meta["w2c"].append(train_w2cs)
        train_meta["fn"].append(train_fns)
        train_meta["cam_id"].append(train_cam_ids)

        

        test_meta["k"].append(test_ks)
        test_meta["w2c"].append(test_w2cs)
        test_meta["fn"].append(test_fns)
        test_meta["cam_id"].append(test_cam_ids)

            
    with open(os.path.join(scene_folder, "train_meta.json"), 'w') as f:
        json.dump(train_meta, f)

    with open(os.path.join(scene_folder, "test_meta.json"), 'w') as f:
        json.dump(test_meta, f)



    # Point cloud of just the first frame
    rgb = rgb / 255.

    point_cloud = np.concatenate([xyz, rgb, np.ones((xyz.shape[0], 1))], axis=-1)


    # if point_cloud.shape[0] > points_to_keep:
    #     idxs = np.random.choice(point_cloud.shape[0], points_to_keep, replace=False)
    #     point_cloud = point_cloud[idxs]

    print("Final point cloud shape: ", point_cloud.shape)

    assert point_cloud.shape[-1] == 7

    save_file = {"data": point_cloud}

    np.savez(os.path.join(scene_folder, "init_pt_cld"), **save_file)





if __name__ == '__main__':
    test_cameras = [0, 5, 10]

    parser = argparse.ArgumentParser(description='Colmap reformatting')
    parser.add_argument('--folder', type=str, required=True, help='Input folder containing the colmap files of the sequence')
    parser.add_argument('--duration', type=int, required=True, help='Number of frames')
    parser.add_argument('--test_cameras',type=int, nargs='+', default=[0, 5, 15, 30],help='Camera IDs of cameras for test')

    args = parser.parse_args()
    main(args)