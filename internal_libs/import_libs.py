import argparse, code, collections, copy, ctypes, datetime, functools, gc, importlib.metadata, json, shutil
import logging, multiprocessing, os, platform, pprint, re, subprocess, sys, tarfile, threading, cProfile
import time, traceback, uuid, io, pathlib, tkinter as tk, tkinter.font, pstats, hashlib, csv, urllib.request
import PySimpleGUI as sg
from zipfile import ZipFile
from tkinter import ttk, messagebox, filedialog, simpledialog
from multiprocessing import shared_memory, Pool
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from functools import reduce
from io import BytesIO
external_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'external_libs'))
os.makedirs(external_libs_path, exist_ok=True)
sys.path.insert(0, external_libs_path)
from cityhash import CityHash64
from uuid import UUID
import pandas as pd
import psutil, msgpack, palworld_coord
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as font_manager
import matplotlib.patheffects as path_effects
from PIL import Image, ImageDraw, ImageOps, ImageFont
from PIL import Image as PILImage
from internal_libs.bases import *
from internal_libs.pal_names import *
from internal_libs.pal_passives import *
from internal_libs.palobject import *
from palworld_save_tools.gvas import *
from palworld_save_tools.palsav import *
from palworld_save_tools.paltypes import *
from palworld_save_tools.archive import *
from palworld_save_tools.rawdata import *