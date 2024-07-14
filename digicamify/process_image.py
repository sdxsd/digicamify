#!/usr/bin/env python3

# DIGICAMIFY IS LICENSED UNDER THE GNU GPLv3
# Copyright (C) 2024 Will Maguire

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

# The definition of Free Software is as follows:
# 	- The freedom to run the program, for any purpose.
# 	- The freedom to study how the program works, and adapt it to your needs.
# 	- The freedom to redistribute copies so you can help your neighbor.
# 	- The freedom to improve the program, and release your improvements
#   - to the public, so that the whole community benefits.

# A program is free software if users have all of these freedoms.

from PIL import (ImageFilter, ImageChops, Image, ImageOps)
from pillow_lut import load_cube_file
import math
import os

NOISE_DATA = "NOISE12.tif"

def apply_noise(noise, base):
    return (ImageChops.overlay(base, noise))

def resize(noise, base):
    bwidth, bheight = base.size
    nwidth, nheight = noise.size
    true_nwidth = int(nwidth * (1 / math.sqrt(2)))
    true_nheight = int(nheight * (1 / math.sqrt(2)))
    if (bwidth > true_nwidth):
        new_bheight = int(bheight * (true_nwidth / bwidth))
        resized = base.resize((true_nwidth, new_bheight), Image.Resampling.NEAREST)
        new_bheight = int(new_bheight * (nwidth / true_nwidth))
        resized = base.resize((nwidth, new_bheight), Image.Resampling.HAMMING)
        return (resized)
    return (base)

# Constantly being changed lol
def enhance_image(base, noise):
    # lut = load_cube_file("./LUT/kyocerasix.cube")
    # base = base.filter(lut)
    # noise = noise.filter(ImageFilter.GaussianBlur(0.2))
    # noise = noise.filter(ImageFilter.UnsharpMask(1))
    base = apply_noise(noise, base)
    base = base.filter(ImageFilter.UnsharpMask(0.5))
    # base = base.filter(ImageFilter.GaussianBlur(0.5))
    return (base)

def process_and_save_image(filename, upload_dir, save_dir):
    base = Image.open(os.path.join(upload_dir, filename))
    noise = Image.open(NOISE_DATA)
    base = resize(noise, base)
    base = enhance_image(base, noise)
    processed_path = os.path.join(save_dir, filename)
    base.save(processed_path)
