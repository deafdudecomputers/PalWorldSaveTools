import os, sys
external_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'external_libs'))
os.makedirs(external_libs_path, exist_ok=True)
sys.path.insert(0, external_libs_path)
import argparse, code, collections, copy, ctypes, datetime, functools, gc, importlib.metadata, json, shutil, glob, requests
import logging, multiprocessing, platform, pprint, re, subprocess, tarfile, threading, cProfile, pickle, zipfile
import time, traceback, uuid, io, pathlib, tkinter as tk, tkinter.font, pstats, hashlib, csv, urllib.request, tempfile
from tkinter import ttk, filedialog, messagebox
import pandas as pd, psutil, msgpack, palworld_coord
import matplotlib.pyplot as plt, matplotlib.patches as patches, matplotlib.font_manager as font_manager
import matplotlib.patheffects as path_effects
import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageOps, ImageFont
from PIL import Image as PILImage
from palworld_save_tools.archive import *
from palworld_save_tools.palsav import *
from palworld_save_tools.paltypes import *
import palworld_save_tools.rawdata.group as palworld_save_group
from internal_libs.palobject import *
from palworld_save_tools.gvas import *
from palworld_save_tools.rawdata import *
from palworld_save_tools.json_tools import *
from internal_libs.bases import *
from internal_libs.pal_names import *
from internal_libs.pal_passives import *