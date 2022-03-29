# Purpose

You will have a real time object detection, using your webcam.

# Installing yolor

0. Activate you virtual environment (not mandatory, but preferred option)
1. Fork submodule Yolor
   1. Run
   ```bash
   git submodule init
   ```
   2. Then
   ```bash
   git submodule update --init
   ```
2. Install dependencies of the yolor fork

```bash
pip install -r requirements.txt
```

3. Download the pre-trained weights (for example the [YOLOR-CSP](https://github.com/MathisFederico/yolor/tree/main#yolor) one, about 200Mo).
4. Put this `.pt` file in `..\yolor\models`

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
