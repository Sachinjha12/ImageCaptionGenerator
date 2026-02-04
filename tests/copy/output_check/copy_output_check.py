from dunetuf.utility.systemtestpath import get_system_test_binaries_path
import dunetuf.common.commonActions as CommonActions
import hashlib, math, time, os
from PIL import Image, ImageFile, PpmImagePlugin



################################################################################
# default_ppm_save
#
# Used to reset the image saver to the default.
#
# Copied directly from:
#   https://pillow.readthedocs.io/en/stable/_modules/PIL/PpmImagePlugin.html
#
################################################################################
def default_ppm_save(im, fp, filename):
    if im.mode == "1":
        rawmode, head = "1;I", b"P4"
    elif im.mode == "L":
        rawmode, head = "L", b"P5"
    elif im.mode == "I":
        rawmode, head = "I;16B", b"P5"
    elif im.mode in ("RGB", "RGBA"):
        rawmode, head = "RGB", b"P6"
    else:
        msg = f"cannot write mode {im.mode} as PPM"
        raise OSError(msg)
    fp.write(head + b"\n%d %d\n" % im.size)
    if head == b"P6":
        fp.write(b"255\n")
    elif head == b"P5":
        if rawmode == "L":
            fp.write(b"255\n")
        else:
            fp.write(b"65535\n")
    ImageFile._save(im, fp, [("raw", (0, 0) + im.size, 0, (rawmode, 0, 1))])



################################################################################
# dune_ppm_save
#
# Saves out a ppm, but with the custom header required by the dune ppm reader
#   based on the outline given in SimulationPpmHandler.cpp
#
# A modified version of
#   https://pillow.readthedocs.io/en/stable/_modules/PIL/PpmImagePlugin.html
#
# TODO add support for multiple DPI options;
#   possibly multiple versions of this method
#   could be decided by an enum + switch in check_copy_output_checksum
################################################################################
def dune_ppm_save(im, fp, filename):
    if im.mode == "1":
        rawmode, head = "1;I", b"P4"
    elif im.mode == "L":
        rawmode, head = "L", b"P5"
    elif im.mode == "I":
        rawmode, head = "I;16B", b"P5"
    elif im.mode in ("RGB", "RGBA"):
        rawmode, head = "RGB", b"P6"
    else:
        msg = f"cannot write mode {im.mode} as PPM"
        raise OSError(msg)
    fp.write(head + b"\n%d %d\n# planes 1\n# resx 300\n# resy 300\n" % im.size)
    if head == b"P6":
        fp.write(b"255\n")
    elif head == b"P5":
        if rawmode == "L":
            fp.write(b"255\n")
        else:
            fp.write(b"65535\n")
    ImageFile._save(im, fp, [("raw", (0, 0) + im.size, 0, (rawmode, 0, 1))])