# Purpose

You will have a real time object detection, using your webcam.

# Installing yolor

Activate you virtual environment (not mandatory, but preferred option)

## Fork submodule Yolor

```bash
git submodule init
```

```bash
git submodule update --init
```

## Install dependencies of the yolor fork

```bash
cd ../idnc/detection/yolor
pip install -r requirements.txt
```

## Download pre-trained weights

Download the pre-trained weights (for example the [YOLOR-CSP](https://drive.google.com/file/d/1ZEqGy4kmZyD-Cj3tEFJcLSZenZBDGiyg/view?usp=sharing) one, about 200Mo).

## Add it in the appropriated folder

Put this `.pt` file in `..\yolor\models`

# Runing the experiment

In the `yolor` folder,

## If you have CUDA

```bash
python detect.py --source 0 --cfg cfg/yolor_csp.cfg --weights models/yolor_csp.pt --conf 0.25 --img-size 640 --device 0 --view-img
```

## Without CUDA

Performances might be degraded.

```bash
python detect.py --source 0 --cfg cfg/yolor_csp.cfg --weights models/yolor_csp.pt --conf 0.25 --img-size 640 --device cpu --view-img
```

Remove the `--view-img` argument if you don't want to display live detection.
