# 🛠️ Setup Guide

> **Note**: Step 1 is optional — only needed if not yet on the cluster.

---

### 1. Connect to Haas

```bash
ssh miazga@haas001.rcp.epfl.ch
```
### 1.b get to your directory
```bash 
cd /mnt/cvlab/scratch/cvlab/home/miazga/
```

### 2. Connect to RCP
```bash
runai login
```

### 3. Submit job 
```bash
source runai_new.sh <job-name> 1
runai describe job <job-name> -p cvlab-miazga
runai bash <job-name>
```

### ======> Now we are in the job <======

### 4. Go to my foldercd 3
```bash
cd /scratch/cvlab/home/miazga
```


### 5. Activate environments
```bash
su miazga
source act_conda.sh
conda activate dynamic_gaussians
```

- for 3dgstream training:
```bash
sudo ln -s /usr/lib/x86_64-linux-gnu/libcuda.so.1 /usr/lib/x86_64-linux-gnu/libcuda.so
```

### ======>  Ready to work with a cluster <======


### 6. Run training of dynamic gaussian splatting methods

#### 6.1 Dynamic 3D Gaussian Splatting

Panoptic: 
```bash
python train.py   --exp 1_experiment_panoptic   --seq basketball --dataset_path data  --duration 150  --test_camera_ids 0 5 10 15   --no_seg
```

Discussion:
```bash
python train.py   --exp discussion-training-day-3000   --seq ""   --dataset_path videos-named   --duration 300   --test_camera_ids 0   --no_seg
```

#### 6.2 HiCOM
```bash
python main.py --config=config/meetroom.yaml
```

#### 6.3 3DGStream
```bash
python train_frames.py \
--read_config --config_path test/discussion/cfg_args.json \
-o output/Monday/0.00007-old-code-100iter \
-m test/discussion/discussion_init/ \
-v discussion_scene \
--image images  \
--first_load_iteration 30000 \
--quiet
```


### 7. Random commands
#### Copy the new environment
```bash
(dynamic_gaussian) miacd zga@cuda-0-0:/scratch/cvlab/home/miazga/miniconda3/envs$ cp -r ../../../javed/anaconda3/envs/dynamic_gaussians .
```

#### Copy all the files from current location to new dir
```bash
mv . discussions/
``` 

#### Run colmap (in ../videos-300 I need to have mp4 files nad pose_bounds.npy): 
1. run pre_n3d.py
```bash
python script/pre_n3d.py --videopath ../videos-300 --startframe 0 --endframe 300 --downscale 1
```


2. run colmap_reformat_first.py 
```bash
python colmap_reformat_first.py --folder videos-300 --duration 300 --test_cameras 0
```

3. Place viedos-300 in Dynamic3dGaussians-main
```bash
mv ../videos-300 .
```


#### Comparizons on DynamicGaussians // original repo
1. Panoptic dataset:
```bash
python train.py   --exp panoptic-no-bg-loss   --seq basketball   --dataset_path data   --duration 150   --test_camera_ids 0 5 10 15  --no_seg
```

2. Discussion dataset: 
```bash
python train.py --exp try-discussion
```


#### Deleting one env
```bash
conda env remove --name <env_name>
```

#### Deleting multiple envs at once
```bash
for env in $(conda env list | awk '{print $1}' | grep '^<pattern>'); do   conda env remove -n "$env" -y; done
```


#### Copy files from cluster to my local machine
```bash
scp -r miazga@haas001.rcp.epfl.ch:/mnt/cvlab/scratch/cvlab/home/miazga/Dynamic3DGaussians-main/output/<test_output_dir> ../Desktop/studies/CVLAB/output
```


#### Generate vidoes out of photos
```bash
ffmpeg -framerate 30 -pattern_type glob -i 'exp__t_*_00002.png' -c:v libx264 -pix_fmt yuv420p output_renders_3.mp4
```


#### Whenever reinstalling numpy to lower version do it with pip
```bash
pip install "numpy=<2" - sth like this
```

### 9. Notes
**PSNR (Peak Signal-to-Noise Ratio)** is a metric used to measure the quality of a reconstructed image (e.g., from a neural renderer) compared to a reference (ground-truth) image.

Higher PSNR = better quality (lower error)
Values typically range:
•	30 dB = good
•	40 dB = excellent
•	<20 dB = poor