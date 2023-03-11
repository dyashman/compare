#!/usr/bin/env python

"""
Python script to generate a contact sheet for model comparisons.
Generates multiple different images in a row for each model, one row per model.
Labels rows with the model name and saves full generation data to a text file.

MIT License

Copyright (c) 2023 David Ashman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import requests
import io
import base64
import os
import sys
import random
import argparse
from datetime import datetime
from PIL import Image

__author__ = 'David Ashman'
__copyright__ = 'Copyright 2023, Contact Sheet Generator for AUTOMATIC1111'
__license__ = 'MIT License'
__version__ = '0.1.0'
__maintainer__ = 'David Ashman'
__email__ = 'kadaan@gmail.com'
__status__ = 'dev'

##################################################
# Config settings
##################################################
url = "http://127.0.0.1:7860"
savePath = "comparisons/"
imgWidth = 512
imgHeight = 512
restoreFaces = "true"

# If modelList is empty, the script will pull a list of models and run ALL of them
#   If you want to run comparisons for only a few models, list them out here
#   Format is { "model" : "<filename>", "keywords" : "any keywords to append for only this model" }
#
modelList = []
#
# modelList = [
#     { "model" : "_Model\\anything-v4.5-pruned.ckpt", "keywords" : "" },
#     { "model" : "_Style\\moDi-v1-pruned.ckpt", "keywords" : "(modern disney style)" },
# ]

##################################################
# CLI arguments / defaults
##################################################
parser = argparse.ArgumentParser(
        prog = 'Comparison.py',
        description = 'Generate batches of stable diffusion outputs for multiple models to easily compare the same prompt')
parser.add_argument('-p', '--prompt', default='', help='Text prompt to run. Leave blank to load ./prompt.txt file')
parser.add_argument('-n', '--negative-prompt', default='', help='Negative prompt. Leave blank to load ./prompt_neg.txt file')
parser.add_argument('-b', '--batch-size', default='5', help='Number of images to generate per model')
parser.add_argument('-s', '--steps', default='25')
parser.add_argument('-d', '--seed', default='-1', help='Seed to start at, consecutive batch images increment by 1')
parser.add_argument('-H', '--hires', default='false', help='Enable hi-res fix')
parser.add_argument('-D', '--denoise', default='0.7', help='De-noising strength')
parser.add_argument('-c', '--cfg', default='7', help='Config Scale')
args = parser.parse_args()

# --prompt
if args.prompt == '':
    fileHandle = open(r"prompt.txt", "r")
    prompt = fileHandle.read()
    fileHandle.close()
else:
    prompt = args.prompt

# --negative-prompt
if args.negative_prompt == '':
    fileHandle = open(r"prompt_neg.txt", "r")
    prompt_neg = fileHandle.read()
    fileHandle.close()
else:
    prompt_neg = args.negative_prompt

# --seed
if int(args.seed) == -1:
    seedNum = random.randrange(sys.maxsize)
else:
    seedNum = int(args.seed)

# Populate model list dynamically if list not explicitly set in config
if len(modelList) == 0:
    response = requests.get(url=f'{url}/sdapi/v1/sd-models')
    for _model in response.json():
        modelList.append({"model" : _model['title'], "keywords" : ""})

##################################################
# Generate images via API calls
##################################################
def pr(msg):
    _time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{_time}] {msg}")

saveFile = datetime.now().strftime("%y%m%d_%H%M%S")
startTime = datetime.now()
y = 1000
for _model in modelList:
    modelName = _model['model']
    modelKeywords = _model['keywords']

    option_payload = {
        "sd_model_checkpoint": modelName,
        "CLIP_stop_at_last_layers": 2
    }
    pr(f"[{y-999}/{len(modelList)}] {modelName}")
    response = requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)

    payload = {
        "prompt": prompt+", "+modelKeywords,
        "negative_prompt": prompt_neg,
        "batch_size": args.batch_size,
        "steps" : args.steps,
        "seed" : seedNum,
        "enable_hr": args.hires,
        "denoising_strength": args.denoise,
        "cfg_scale" : args.cfg,
        "width": imgWidth,
        "height": imgHeight,
        "restore_faces": "true",
    }
    pr(f"  🡒 Generating [{payload['batch_size']}] images with [{payload['steps']}] steps.")
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    try:
        r = response.json()
    except ValueError as e:
        print("NOT JSON RESPONSE")
        exit()

    x = 100
    pr("  🡒 Saving generated images to disk.")
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
        image.save(f'output{x}.png')
        x = x + 1

    # If models are nested in subfolders, retrieve just the model name
    _modelName = modelName.split("\\")
    if len(_modelName) > 1:
        _modelName = _modelName[len(_modelName)-1]

    # Do some imageMagik rotation/text magic to add the model name label to the first image in a row
    os.system(f'convert output100.png -rotate 90 -background black -fill white -pointsize 24 label:"{_modelName}" +swap  -gravity Center -append -rotate 270 output100r.png')
    os.system(f'del output100.png')
    os.system(f'convert +append output*.png combined{y}.png')
    os.system(f'del output*.png')
    y = y + 1

pr("  🡒 Combining all models together and saving generation metadata to text file.")
os.system(f'convert -append combined*.png {savePath}{saveFile}.png')
os.system(f'del combined*.png')
saveFile = open(f'{savePath}{saveFile}.txt','w')
saveFile.write(json.dumps(payload, indent=4))
saveFile.close()

runtime = datetime.now() - startTime
pr("  🡒 Completed in {}:{}".format(int(runtime.total_seconds() / 60), int(runtime.total_seconds()) % 60))
