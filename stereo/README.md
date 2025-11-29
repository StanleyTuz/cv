# Stereo

## Capturing Stereo Image Pairs

I can interactively capture stereo image pairs by running 
```shell
python capture_images.py --dirname "<NAME>"
```
or just
```shell
python capture_images.py
```
This opens both webcams and displays them to the screen. When SPACE is pressed, a frame will be captured from both cameras and saved to `stereo/data/<NAME>`. Press `q` to exit.