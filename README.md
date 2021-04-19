# PointPainting
This repository aims to build an open-source PointPainting package which is easy to understand, deploy and run! We refer to the idea in the [original paper](https://arxiv.org/abs/1911.10150) to implement this open-source framework to conduct the sequential 3D object detection. We utilize the Pytorch and mmsegmentation as the image-based segmnentation approach, and the OpenPCDet as the LiDAR detector.

## Update
We propose to support Kitti dataset first and utilize OpenPCDet as the LiDAR detection framework. We are expected to release the code to support Kitti and at least two semantic segmentation methods to do painting by the end of April 2021.
Update on April 20, 2021: Code released! We currently support Kitti dataset, with DeepLab V3/V3+ and HMA!

## Table of Contents
- [PointPainting](#pointpainting)
  - [Update](#update)
  - [Table of Contents](#table-of-contents)
  - [Background](#background)
    - [Framework Overview](#framework-overview)
  - [Install](#install)
    - [OpenPCDet](#openpcdet)
    - [mmsegmentation](#mmsegmentation)
  - [How to Use](#how-to-use)
    - [Dataset Preparation](#dataset-preparation)
    - [Painting](#painting)
    - [LiDAR Detector Training](#lidar-detector-training)
  - [Results](#results)
  - [Authors](#authors)

## Background
The PointPainting means to fuse the semantic segmentation results based on RGB images and add class scores to the raw LiDAR pointcloud to achieve higher accuracy than LiDAR-only approach.

### Framework Overview
The PointPainting architecture consists of three main stages: (1) image based semantics network, (2) fusion (painting), and (3) lidar based detector. In the first step, the images are passed through a semantic segmentation network obtaining pixelwise segmentation scores. In the second stage, the lidar points are projected into the segmentation mask and decorated with the scores obtained in the earlier step. Finally, a lidar based object detector can be used on this decorated (painted) point cloud to obtain 3D detections.
![](framework_overview.png)

## Install
To use this repo, first install these dependencies. For the Pytorch, please follow the official instructions to install and it is preferred that you have a conda and install Pytorch in your conda environment.
- [Pytorch](https://pytorch.org/), tested on Pytorch 1.6/1.7 with CUDA toolkit
- [OpenPCDet](#openpcdet)
- [mmsegmentation](#mmsegmentation)

### OpenPCDet
OpenPCDet is an open-source LiDAR detection framework. It supports many popular datasets like Kitti, Nuscenes etc. We utilize the OpenPCDet as the LiDAR detector. To install the OpenPCDet please first install its [requirements](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/INSTALL.md). And as we modify some parts of the OpenPCDet (including dataset loader and training configuration) to support the painted Kitti dataset, you can directly use the modified version in `./detector`. To install it, run the following commands.

```
$ cd PointPainting/detector
$ python setup.py develop
```

### mmsegmentation
For the image-based semantic segmentation, we use the [mmsegmentation](https://github.com/open-mmlab/mmsegmentation) (OpenLab V3+). To install this package, run the following commands (you may need to change the CUDA and Pytorch version accordingly).
```
$ pip install terminaltables
$ pip install mmcv-full -f https://download.openmmlab.com/mmcv/dist/cu101/torch1.7.0/index.html
```
You may notice there is a folder in the `./detector/mmseg`, so you do not have to manually clone its repository.

## How to Use
As this is a sequential detection framework, so the first thing is to prepare your kitti dataset and then paint your raw LiDAR. With the painted LiDAR, you could then train a neural network and see the enhanced result.
### Dataset Preparation
Currently we only support the Kitti dataset, and we expect to update support for Nuscenes dataset in the future. For the Kitti dataset, you may need to manage your dataset as shown below.
```
detector
├── data
│   ├── kitti
│   │   │── ImageSets
│   │   │── training
│   │   │   ├── calib
│   │   │   ├── image_2
│   │   │   ├── image_3
│   │   │   ├── label_2
│   │   │   ├── velodyne
│   │   │   ├── painted_lidar (keep it empty)
│   │   │── kitti_infos_train.pkl
│   │   │── kitti_info_val.pkl
```
Notice we have already generated the train and val info for you. So you may only put the Kitti raw data into corresponding folder.
### Painting
When you have managed your data as shown below, doing the painting should be very easy. Firstly check the `painting.py` script and choose the segmentation network index that you want to use! We suggest the DeepLab V3+ and it is by default.
To use DeepLab V3+ you may go to download the [weight](https://download.openmmlab.com/mmsegmentation/v0.5/deeplabv3plus/deeplabv3plus_r101-d8_512x1024_80k_cityscapes/deeplabv3plus_r101-d8_512x1024_80k_cityscapes_20200606_114143-068fcfe9.pth) and save it in `./mmseg/checkpoints/`. Then you could run the following command.
```
$ cd painting
$ python painting.py
```
The painting process might take hours depending on your computing device performance. When you have done the painting, you can procees to the LiDAR Detector training!
### LiDAR Detector Training
For the training part, you should run the following commands to start training based on the painted pointclouds.
```
$ cd detector
$ python -m pcdet.datasets.kitti.painted_kitti_dataset create_kitti_infos tools/cfgs/dataset_configs/painted_kitti_dataset.yaml
$ cd tools
$ python train.py --cfg_file cfgs/kitti_models/pointpillar_painted.yaml
```

## Results

## Authors