import argparse, code, collections, copy, ctypes, datetime, functools, gc, importlib.metadata, json, shutil
import logging, multiprocessing, os, platform, pprint, re, subprocess, sys, tarfile, threading, cProfile
import time, traceback, uuid, io, pathlib, tkinter as tk, tkinter.font, pstats, hashlib, csv, urllib.request
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
def ensure_package_installed(package_name):
    #print(f'Attempting to find {package_name}...')
    try:
        importlib.import_module(package_name)
        #print(f"{package_name} is already installed.")
    except ImportError:
        #print(f"{package_name} not found. Installing...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package_name, "--target=" + external_libs_path, "--no-cache-dir"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            #print(f"{package_name} installed successfully.")
        except subprocess.CalledProcessError as e:
            #print(f"Failed to install {package_name}. Error: {e}")
            pass
def download_from_dropbox(dropbox_link, dest_path):
    urllib.request.urlretrieve(dropbox_link, dest_path)
def extract_zip(zip_path, extract_to_folder):
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_folder)
def ensure_internal_libs_exists():
    internal_libs_path = 'internal_libs'
    zip_path = 'PST_Assets.zip'
    required_files = [
        'worldmap.png',
        'marker.png',
        'NotoSans-Regular.ttf'
    ]
    if not os.path.exists(internal_libs_path):
        os.makedirs(internal_libs_path)
    files_missing = any(not os.path.exists(os.path.join(internal_libs_path, file)) for file in required_files)
    if files_missing:
        print(f"Downloading and extracting assets...")
        dropbox_link = 'https://www.dropbox.com/scl/fi/9fdibnhxl2dhn79856klj/PST_Assets.zip?rlkey=ulp17jmz9630dr97pavop4b4h&st=mtrbvswh&dl=1'        
        try:
            download_from_dropbox(dropbox_link, zip_path)
            extract_zip(zip_path, internal_libs_path)
            os.remove(zip_path)
        except Exception as e:
            print(f"Network/Permission error, unable to download the assets. Error details: {str(e)}")
lock_file_path = 'import_lock.txt'
def delete_lock_file_after_delay(file_path, delay):
    time.sleep(delay)
    if os.path.exists(file_path):
        os.remove(file_path)
if not os.path.exists(lock_file_path):
    #print(f"Attempting to ensure pip is installed...")
    try:
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print(f"Pip installed successfully.")
    except subprocess.CalledProcessError as e:
        #print(f"Failed to ensure pip is installed. Error: {e}")
        pass
    for package in ['msgpack', 'palworld_coord', 'psutil', 'palworld_save_tools', 'matplotlib', 'pandas', 'cityhash']:
        ensure_package_installed(package)
    ensure_internal_libs_exists()    
    with open(lock_file_path, 'w') as lock_file:
        lock_file.write('initialized')
    delete_thread = threading.Thread(target=delete_lock_file_after_delay, args=(lock_file_path, 10))
    delete_thread.start()
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
import palworld_save_tools.rawdata.group as palworld_save_group
from palworld_save_tools.rawdata import *
def set_high_priority():
    try:
        p = psutil.Process(os.getpid())
        if os.name == 'nt':
            p.nice(psutil.HIGH_PRIORITY_CLASS)
        else:
            p.nice(-20)
    except Exception as e:
        print(f"Failed to set high priority: {e}")
set_high_priority()