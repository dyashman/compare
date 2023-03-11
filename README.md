# compare.py
Compare multiple Stable Diffusion models quickly with a contact sheet of multiple images from multiple models with the same prompt

Written and tested on Windows, but should work on Linux with minimal modifications (mostly just the os.system calls)

# Requirements

ImageMagik - https://imagemagick.org/script/download.php
- Required for all the post-generation image processing and labeling.

AUTOMATIC1111 stable_diffusion_webui - https://github.com/AUTOMATIC1111/stable-diffusion-webui
- All the image generation uses API calls to AUTOMATIC1111.
- You need to add --api to COMMANDLINE_ARGS in webui-user.bat to enable API access.

# Parameters

Run with no arguments or empty arguments, the script will read from 'prompt.txt' and 'prompt_neg.txt' files in the same directory.

Currently supports the following commandline arguments:
```
options:
  -h, --help            show this help message and exit
  -p PROMPT, --prompt PROMPT
                        Text prompt to run. Leave blank to load ./prompt.txt file
  -n NEGATIVE_PROMPT, --negative-prompt NEGATIVE_PROMPT
                        Negative prompt. Leave blank to load ./prompt_neg.txt file
  -b BATCH_SIZE, --batch-size BATCH_SIZE
                        Number of images to generate per model
  -s STEPS, --steps STEPS
  -d SEED, --seed SEED  Seed to start at, consecutive batch images increment by 1
  -H HIRES, --hires HIRES
                        Enable hi-res fix
  -D DENOISE, --denoise DENOISE
                        De-noising strength
  -c CFG, --cfg CFG     Config Scale
```

# Example
```
D:\stable-diffusion-webui\outputs>python compare.py -p"female superhero with a cape flying in the sky" -n"ugly, deformed, missing limbs, naked, nude"
[2023-03-11 12:42:44] [1/6] anything-v4.5-pruned.ckpt
[2023-03-11 12:42:44]   🡒 Generating [5] images with [25] steps.
[2023-03-11 12:43:19]   🡒 Saving generated images to disk.
[2023-03-11 12:43:21] [2/6] deliberate_v2.safetensors
[2023-03-11 12:43:28]   🡒 Generating [5] images with [25] steps.
[2023-03-11 12:44:04]   🡒 Saving generated images to disk.
[2023-03-11 12:44:06] [3/6] dreamlike-photoreal-2.0.safetensors
[2023-03-11 12:44:13]   🡒 Generating [5] images with [25] steps.
[2023-03-11 12:44:48]   🡒 Saving generated images to disk.
[2023-03-11 12:44:50] [4/6] DreamShaper_331BakedVae.safetensors
[2023-03-11 12:44:57]   🡒 Generating [5] images with [25] steps.
[2023-03-11 12:45:33]   🡒 Saving generated images to disk.
[2023-03-11 12:45:35] [5/6] NeverendingDreamNED_bakedVae.safetensors
[2023-03-11 12:45:37]   🡒 Generating [5] images with [25] steps.
[2023-03-11 12:46:12]   🡒 Saving generated images to disk.
[2023-03-11 12:46:15] [6/6] moDi-v1-pruned.ckpt
[2023-03-11 12:46:21]   🡒 Generating [5] images with [25] steps.
[2023-03-11 12:46:54]   🡒 Saving generated images to disk.
[2023-03-11 12:46:57]   🡒 Combining all models together and saving generation metadata to text file.
[2023-03-11 12:47:04]   🡒 Completed in 4:20
```
![Example contact sheet](/examples/230311_124244.png)
