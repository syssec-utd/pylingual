import shutil
import os
from canvas import Canvas
from canvas import irio
from artists.map_art import Artist as MapArtArtist
import argparse
parse = argparse.ArgumentParser()
parse.add_argument('file', type=str, help='input file')
parse.add_argument('-x', default=1, type=int, help='x_maps')
parse.add_argument('-z', default=1, type=int, help='z_maps')
parse.add_argument('-y', default=0, type=int, help='use y to create 3d img')
parse.add_argument('-o', default=None, help='output dir')
args = parse.parse_args()
if __name__ == '__main__':
    output_dir = args.o
    if output_dir is None:
        output_dir = '.'.join(args.file.split('.')[:-1])
    os.makedirs(output_dir, exist_ok=True)
    if args.y != 0:
        if args.y < 10 or args.y > 255:
            raise ValueError(f'y can only be 0 or 10~255')
    canvas = Canvas()
    p = canvas
    artist = MapArtArtist(canvas=canvas, y=0)
    artist.add_img(img_path=args.file, level_x=args.x, level_y=args.z, d3=args.y != 0, save_resized_file_to=os.path.join(output_dir, 'resized.png'), save_preview_to=os.path.join(output_dir, 'preview.png'), y_max=args.y)
    artist.to_canvas()
    final_ir = canvas.done()
    irio.dump_ir_to_bdx(final_ir, os.path.join(output_dir, 'map.bdx'), need_sign=True, author='2401PT')
    print(f'output to {output_dir}')
    shutil.copy(args.file, os.path.join(output_dir, os.path.split(args.file)[1]))