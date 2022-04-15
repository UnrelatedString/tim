#!/usr/bin/env python3

import PIL.Image
import os
import sys
from subprocess import run

palette = [
    (255, 0, 0), # red
    (255, 69, 0), # orangered
    (255, 165, 0), # orange
    (255, 215, 0), # gold
    (255, 255, 0), # yellow
    (154, 205, 50), # yellowgreen
    (0, 255, 0), # lime
    (0, 128, 0), # green
    (64, 224, 208), # turquoise
    (30, 144, 255), # dodgerblue
    (0, 0, 255), # blue
    (75, 0, 130), # indigo
    (238, 130, 238), # violet
    (255, 192, 203), # pink
    (255, 255, 255), # white
    (0, 0, 0), # black
]

directory = 'timfrim'
frame_format = f'{directory}/%06d.png'

def ffmpegify_palette():
    palette_image = PIL.Image.new('RGB', (256, 1), (255, 255, 255))
    for i, color in enumerate(palette):
        palette_image.putpixel((i, 0), color)
    return palette_image

def main():
    destination = sys.argv[1] if len(sys.argv) > 1 else 'timelapse.gif'
    pixels_per_frame = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    run(['rm', '-r', directory])
    os.mkdir(directory)
    canvas = PIL.Image.new('RGB', (128, 128), (255, 255, 255))
    pixels = 0
    frame = 0

    for line in sys.stdin:
        x, y, color, _timestamp = map(int, line.rstrip().split(' '))
        canvas.putpixel((x, y), palette[color])
        pixels += 1
        if not pixels % pixels_per_frame:
            canvas.save(frame_format % frame)
            frame += 1

    if pixels % pixels_per_frame:
        canvas.save(frame_format % frame)

    palette_dir = directory+'/palette.png'
    ffmpegify_palette().save(palette_dir)
    run(['ffmpeg', '-i', frame_format, '-i', palette_dir, '-filter_complex', 'paletteuse,fps=50', destination])

if __name__ == '__main__':
    main()
