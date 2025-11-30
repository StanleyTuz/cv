# Project 01: 3D-to-2D Projection

The goal of this project is to understand how an object in 3D space is projected onto a 2D image plane.

For simplicity, we will assume that the object is already in the camera coordinate system, i.e., the world coordinate system coincides with the camera coordinate system. This means that our extrinsics are trivial here: $$ R = I \text{ and } t = 0. $$

The full 3D-to-2D projection model takes a point $X \in \mathbb{R}^3$ in the world coordinate system and maps it to pixel coordinates $x_{\text{pix}}$ in the resulting image. This is encoded in the formula $$ \tilde{x}_{\text{pix}} = K\left[R \middle| t\right] \tilde{X}_{\text{w}} $$ where the tildes indicate homogeneous coordinate representations:
$$ X = \left(X,Y,Z\right) \leftrightarrow \tilde{X} = \left(X,Y,Z,1\right). $$

This can be confusing, so here are the detailed steps:
- Start with a point $X = \left(X,Y,Z\right) \in \mathbb{R}^3$.
- Lift $X$ to homogeneous coordinates $\tilde{X} = \left(X,Y,Z,1\right) \in \mathbb{P}^3$.
- Apply $\left[ R\middle| t\right]$ to $\tilde{X}$: $$ \left[R\middle| t\right] \tilde{X} \in \mathbb{P}^2.$$
    - This step combines the rigid body transformation from world coordinates to camera coordinates and the perspective projection from 3D projective space $\mathbb{P}^3$ to 2D projective space $\mathbb{P}^2$.
- Apply the intrinsic camera matrix $K$ to get: $$\tilde{x} = K\left[R\middle|t\right]\tilde{X} \in \mathbb{P}^2.$$
- Lastly, normalize by dividing by the last homogeneous coordinate to obtain coordinates in the Euclidean space: $$ \left(u,v\right) \in \mathbb{R}^2. $$



