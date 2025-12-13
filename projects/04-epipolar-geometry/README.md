# Project 04: Epipolar Geometry

In this project, I start exploring epipolar geometry, which encodes the relationship between two images of the same scene as taken by different cameras. There are two main workflows that I work through here.

## Uncalibrated Workflow

**(Fundamental matrix-based; a single arbitrary stereo pair)**

File: `recover-pose-from-image-pair.ipynb`

In this case, we assume:
* We have two images of a general (nonplanar) scene;
* We know the intrinsics of the cameras;
* We *do not* know the extrinsics.

Steps:
1. Detect and match features between the two images.
2. Estimate the Fundamental matrix $F$ between the images.
    - This encodes all of the epipolar geometry, *up to scale*.
3. Compute the Essential matrix $$ E = K_2^T F K_1. $$
4. Recover the relative pose $\left(R,t\right)$ of the cameras via `cv2.recoverPose(E, ...)`.

Why?
* We can recover the relative camera pose from a single, arbitrary stereo pair.
* No planar object is required. This works for general 3D structure.

What's missing?
* We can't determine the absolute scale of the translation between the cameras.
* Since this is based on a single image pair, it is less robust than the flow below, which uses multiple pairs.

## Calibrated Workflow: 

**(Chessboard-based stereo camera calibration)**

File: `recover-pose-from-calibration.ipynb`

In this case, we assume:
* We have multiple stereo image pairs of a scene;
* All pairs contain a known planar calibration pattern (a chessboard);
* We want full metric calibration: $K_1, K_2, R, t$ with real-world scale;
* We *do not* know the camera intrinsics or extrinsics.

Steps:
1. For each stereo image pair $i$:
    1. Detect and match chessboard corners in both images;
    2. Compute the homographies $H_1^{\left(i\right)}, H_2^{\left(i\right)}$ which map the world plane to image plane 1 and 2, respectively.
2. From all homographies $\left\{H_1^{\left(i\right)}, H_2^{\left(i\right)} \right\}_{i=1}^n$, solve for
    1. Each camera's intrinsics $K_1$, $K_2$; and
    2. Each camera's extrinsics with respect to the chessboard plane.
3. Combine the extrinsics to recover the relative pose $\left(R,t\right)$ between the two cameras.

Why?
* Each stereo chessboard observation gives (linear) constraints on the cameras' intrinsics and on the chessboard's pose relative to the camera.
* Multiple such images constrain the solution and the metric.
