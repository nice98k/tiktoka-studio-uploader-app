#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import threading
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import AudioClip
from moviepy.editor import concatenate_videoclips,concatenate_audioclips,TextClip,CompositeVideoClip
from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.colorx import colorx
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.freeze import freeze
from moviepy.video.fx.freeze_region import freeze_region
from moviepy.video.fx.gamma_corr import gamma_corr
from moviepy.video.fx.headblur import headblur
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.loop import loop
from moviepy.video.fx.lum_contrast import lum_contrast
from moviepy.video.fx.make_loopable import make_loopable
from moviepy.video.fx.margin import margin
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.painting import painting
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.scroll import scroll
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.time_mirror import time_mirror
from moviepy.video.fx.time_symmetrize import time_symmetrize

from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_left_right import audio_left_right
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.fx.volumex import volumex
import moviepy.audio.fx.all  as afx
import moviepy.video.fx.all as vfx
# here put the import lib
import json
import tkinter as tk
import webbrowser
from tkinter import OptionMenu, filedialog,ttk
import pandas as pd
import os
import base64
import subprocess
import sys
import random
import os
import time
# import multiprocessing.dummy as mp
import concurrent
from glob import glob
from src.dbmanipulation import *
from src.UploadSession import *
from PIL import Image,ImageTk
import multiprocessing as mp
from src.upload import *
from src.ai_detector import AiThumbnailGenerator
from datetime import datetime,date,timedelta
import asyncio
import requests
import re
import calendar
from tsup.utils.webdriver.setupPL import checkRequirments
import logging
from src.database import createEngine,pd2table,query2df,rmEngine
try:
    import tkinter.scrolledtext as ScrolledText
except ImportError:
    import Tkinter as tk # Python 2.x
    import ScrolledText
from easy_i18n.t import Ai18n
config = {
    "load_path": "./locales", # 指定在 /locales 下找对应的翻译 json文件
    "default_module": "global", # 指定默认的全局模块，你可以为比如用户模块，订单模块单独设置翻译，如果不指定 module 则会去全局模块查找。
}
a_i18n = Ai18n(locales=["en", "zh"], config=config)

i18labels= a_i18n.translate
window_size='1024x720'
height=720
width=1024
# Logging configuration
logging.basicConfig(filename='test.log',
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')        

# Add the handler to logger

logger = logging.getLogger()         
checkvideopaircounts=0
checkvideocounts=0
test_engine=createEngine('test')
prod_engine=createEngine('prod')
window=None
# after import or define a_i18n and t
# add translation dictionary manually.
# dbname = "reddit_popular"
# Open the database and make sure there is a table with appopriate indices
availableScheduleTimes = [
"0:00",
"0:15",
"0:30",
"0:45",
"1:00",
"1:15",
"1:30",
"1:45",
"2:00",
"2:15",
"2:30",
"2:45",
"3:00",
"3:15",
"3:30",
"3:45",
"4:00",
"4:15",
"4:30",
"4:45",
"5:00",
"5:15",
"5:30",
"5:45",
"6:00",
"6:15",
"6:30",
"6:45",
"7:00",
"7:15",
"7:30",
"7:45",
"8:00",
"8:15",
"8:30",
"8:45",
"9:00",
"9:15",
"9:30",
"9:45",
"10:00",
"10:15",
"10:30",
"10:45",
"11:00",
"11:15",
"11:30",
"11:45",
"12:00",
"12:15",
"12:30",
"12:45",
"13:00",
"13:15",
"13:30",
"13:45",
"14:00",
"14:15",
"14:30",
"14:45",
"15:00",
"15:15",
"15:30",
"15:45",
"16:00",
"16:15",
"16:30",
"16:45",
"17:00",
"17:15",
"17:30",
"17:45",
"18:00",
"18:15",
"18:30",
"18:45",
"19:00",
"19:15",
"19:30",
"19:45",
"20:00",
"20:15",
"20:30",
"20:45",
"21:00",
"21:15",
"21:30",
"21:45",
"22:00",
"22:15",
"22:30",
"22:45",
"23:00",
"23:15",
"23:30",
"23:45"] 
class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text
        self.max_length = 250


    def emit(self, record):
        msg = self.format(record)
        if len(msg) > self.max_length:
            lines = []
            while len(msg) > self.max_length:
                lines.append(msg[:self.max_length])
                msg = msg[self.max_length:]
            lines.append(msg)
            msg= '\n'.join(lines)

        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)

def url_ok(url,proxy_option=''):


    try:
        if not proxy_option=='':
            

            # proxies = {
            #    'http': 'http://proxy.example.com:8080',
            #    'https': 'http://secureproxy.example.com:8090',
            # }
            if 'http:' in proxy_option:

                proxies = {
                'http': proxy_option
                }                
            elif 'https:' in proxy_option:

                proxies = {
                'https': proxy_option,
                }                
            elif 'socks' in proxy_option:
                proxies = {
                'http': proxy_option,
                'https': proxy_option,
                }
            else:
                proxy_option='http://'
                proxies = {
                'http': proxy_option,
                'https': proxy_option,
                }            
            print('use proxy',proxy_option)
            response = requests.head(url,proxies=proxies)
            print('google access is ok use {proxy_option}')
        else:
            response = requests.head(url)
            print('we cant  access google without proxy')

    except Exception as e:
        # print(f"NOT OK: {str(e)}")
        print('we cant  access google')
        
        return False
    else:
        print('status code',response.status_code)
        if response.status_code == 200:
            print('we cant  access google')
            return True
        else:
            print(f"NOT OK: HTTP response code {response.status_code}")

            return False


def isfilenamevalid(filename):
    # print(imagename)
    invalid = '…,<>:."/\|?*!$\'\"#'

    for char in invalid:

        filename = filename.replace(char, '')
    if len(filename) > 260:
        filename = filename[:259]
    return filename


def fix_size(old_image_path, new_image_path, canvas_width=1080, canvas_height=720):
    """Edited from https://stackoverflow.com/questions/44231209/resize-rectangular-image-to-square-keeping-ratio-and-fill-background-with-black"""
    im = Image.open(old_image_path)
    x, y = im.size

    ratio = x / y
    desired_ratio = canvas_width / canvas_height

    w = max(canvas_width, x)
    h = int(w / desired_ratio)
    if h < y:
        h = y
        w = int(h * desired_ratio)

    mode = im.mode
    print(mode)
    if len(mode) == 1:  # L, 1
        new_background = (0)
    if len(mode) == 3:  # RGB
        new_background = (0, 0, 0)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (0, 0, 0, 0)
    new_im = Image.new(mode, (w, h), new_background)
    new_im.paste(im, ((w - x) // 2, (h - y) // 2))
    img = new_im.resize((canvas_width, canvas_height))
    if mode == 'RGBA':
        img = img.convert('RGB')
    img.save(new_image_path)


def load_setting():

    global setting

    if os.path.exists('latest-used-setting.txt') :
        try:
            fp = open('latest-used-setting.txt', 'r', encoding='utf-8')
            settingfile=fp.readlines()[0]

            fp = open(settingfile, 'r', encoding='utf-8')
            setting_json = fp.read()
            fp.close()
        except:
            print(i18labels("loading-default-setting", locale='en', module="g"))
            fp = open("./assets/config/demo.json", 'r', encoding='utf-8')
            setting_json = fp.read()
            fp.close()
    else:
        print(i18labels("loading-default-setting", locale='en', module="g"))
        fp = open("./assets/config/demo.json", 'r', encoding='utf-8')
        setting_json = fp.read()
        fp.close()        
    setting = json.loads(setting_json)
    return setting

def reset_gui():

    load_setting()

    # 清空表格
    # 写入数据

    prefertags.set(setting['prefertags'])
    preferdessuffix.set(setting['preferdessuffix'])
    preferdesprefix.set(setting['preferdesprefix'])

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj
# 加载剧本

settingid=0
# 保存配置

def save_setting(dbm):
    global settingid

    try:
        proxy_option_value = proxy_option.get()
        # print(' proxy_option setting',proxy_option.get())
    except NameError:
        print('no  proxy_option,using existing setting',
              setting['proxy_option'])
        proxy_option_value = setting['proxy_option']
    try:
        firefox_profile_folder_path = firefox_profile_folder.get()
        print('firefox_profile_folder is ',firefox_profile_folder_path)
        setting['firefox_profile_folder'] = firefox_profile_folder_path

    except NameError:
        print('no new  firefox_profile_folder,using existing setting',
              setting['firefox_profile_folder'])
        setting['firefox_profile_folder'] = ''

    try:
        video_folder_path=video_folder.get()
    except NameError:
        print('no new  video_folder_path,using existing setting',
              setting['video_folder'])
        video_folder_path = setting['video_folder']
        print(video_folder_path)
    else:
        if video_folder_path:
            if os.path.exists(video_folder_path):
                setting['video_folder'] = video_folder_path
            else:
                print('we can not find this video foler',video_folder_path)
    try:
        channel_cookie_path=channel_cookie.get()
    except NameError:
        print('no new  channel_cookie_path,using existing setting',
              setting['channelcookiepath'])
        channel_cookie_path = setting['channelcookiepath']
        print(channel_cookie_path)
    else:
        if channel_cookie_path:
            if os.path.exists(channel_cookie_path):
                setting['channelcookiepath'] = channel_cookie_path
            else:
                print('we cannot find cookie file',channel_cookie_path)
    try:
        music_folder_path=music_folder.get()
    except NameError:
        # print('no new  music_folder,using existing setting',
            #   setting['music_folder'])
        music_folder = setting['music_folder']
        # print(music_folder)
    else:
        if music_folder_path:
            setting['music_folder'] = music_folder_path

    setting['is_record_video'] = is_record_video.get()
    setting['is_open_browser'] = is_open_browser.get()    
    setting['ratio'] = ratio.get()
    setting['debug'] = is_debug.get()

    setting['dailycount'] = dailycount.get()
    setting['channelname'] = channelname.get()
    setting['start_publish_date'] = start_publish_date.get()

    setting['preferdesprefix'] = preferdesprefix.get()
    setting['preferdessuffix'] = preferdessuffix.get()
    setting['proxy_option']=proxy_option_value
    setting['prefertags'] = prefertags.get()
    setting['publishpolicy']=publishpolicy.get()    
    if setting['publishpolicy']=='': 
        setting['publishpolicy']=1
    if setting['start_publish_date']=='': 
        setting['start_publish_date']='1'
    if setting['channelname'] is None or setting['channelname']=='' :
        print('before save setting,you need input channelname')
    else:
        if setting['video_folder'] is None or setting['video_folder']=='' :
            print('before save setting,you need input video_folder')
        else:
            if os.path.exists(channel_cookie_path):

                
                newsetting=json.dumps(setting, indent=4, separators=(',', ': '))
                if os.path.exists('./assets/config/'+setting['channelname']+".json"):
                    with open('./assets/config/'+setting['channelname']+".json", 'r') as fr:
                        exitingsetting=json.loads(fr.read())

                        if ordered(setting)==ordered(exitingsetting):
                            print('no change at all')
                        else:
                            print('new change will be saved')
                        with open('./assets/config/'+setting['channelname']+".json", 'w') as f:
                            f.write(json.dumps(setting, indent=4, separators=(',', ': ')))
                        settingid=dbm.Add_New_UploadSetting_In_Db(setting)
                        print("配置保存成功",settingid)
                        with open('latest-used-setting.txt','w+') as fw:
                            fw.write('./assets/config/'+setting['channelname']+".json")                        
                else:
                    with open('./assets/config/'+setting['channelname']+".json", 'w') as f:
 
                        f.write(json.dumps(setting, indent=4, separators=(',', ': ')))                                     
                # print('当前使用的配置为：', setting)
                
                    settingid=dbm.Add_New_UploadSetting_In_Db(setting)
                    print("配置保存成功",settingid)
                    with open('latest-used-setting.txt','w+') as fw:
                        fw.write('./assets/config/'+setting['channelname']+".json")
            else:
                print('请检查cookie文件是否存在 是否损坏',channel_cookie_path)

def select_profile_folder():
    global firefox_profile_folder_path
    try:
        firefox_profile_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')

        if os.path.exists(firefox_profile_folder_path):
            firefox_profile_folder_path = str(firefox_profile_folder_path)
            print("You chose %s" % firefox_profile_folder_path)
            firefox_profile_folder.set(firefox_profile_folder_path)
        else:
            print('please choose a valid profile folder')

            # setting['firefox_profile_folder'] = firefox_profile_folder
    except:
        print('please choose a valid profile folder')

def select_thumbView_video_folder():
    global thumbView_video_folder_path
    try:
        thumbView_video_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')
        if os.path.exists(thumbView_video_folder_path):
            print("You chose %s" % thumbView_video_folder_path)
            thumbView_video_folder.set(thumbView_video_folder_path)
            print("You chose %s" % thumbView_video_folder.get())

        else:
            print('please choose a valid video folder')

    except:
        print('please choose a valid video folder')



def select_videosView_video_folder():
    global videosView_video_folder_path
    try:
        videosView_video_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')
        if os.path.exists(videosView_video_folder_path):
            print("You chose %s" % videosView_video_folder_path)
            videosView_video_folder.set(videosView_video_folder_path)
            print("You chose %s" % videosView_video_folder.get())

        else:
            print('please choose a valid video folder')

    except:
        print('please choose a valid video folder')

def select_videos_folder():
    global video_folder_path
    try:
        video_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')
        if os.path.exists(video_folder_path):
            print("You chose %s" % video_folder_path)
            video_folder.set(video_folder_path)
            setting['video_folder'] = video_folder_path
        else:
            print('please choose a valid video folder')

    except:
        print('please choose a valid video folder')
def select_musics_folder():
    global music_folder_path
    try:
        music_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')


        if os.path.exists(music_folder_path):
            print("You chose %s" % music_folder_path)
            music_folder.set(music_folder_path)
            setting['music_folder'] = music_folder_path
        else:
            print('please choose a valid music folder')
    except:
        print('please choose a valid music folder')

docsopen=False
def docs(frame,lang):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    print('open docmentations')
    label_helptext_setting = tk.Label(newWindow, text = i18labels("docs_str", locale='en', module="g").replace('\\n','\n'),justify='left', wraplength=450)
    label_helptext_setting.pack()
    
def version(frame,lang):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    # print(type(i18labels("version_str", locale='en', module="g")))
    # print(str(i18labels("version_str", locale='en', module="g")))
    # if '\\n' in i18labels("version_str", locale='en', module="g"):
    print('111111111111')
    # print(type("First line\n and this is the second"))
    # print("First line\n and this is the second")
    # if '\n' in "First line\n and this is the second":
    #     print('22222222222')    
    label_helptext_setting = tk.Label(newWindow, 
                                      text = i18labels("version_str", locale='en', module="g").replace('\\n','\n'),
                                    #   text = "First line\n and this is the second",
                                      justify='left')
    label_helptext_setting.pack()


def contact(frame,lang):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    # due to \n in json string should in \\n, so read it from json  need to convert to original 
    label_helptext_setting = tk.Label(newWindow, text = i18labels("contact_str", locale=lang, module="g").replace('\\n','\n'),anchor='e',justify='left', wraplength=450)
    label_helptext_setting.pack()

    group = tk.Label(newWindow, text =i18labels("contact_str_group", locale=lang, module="g"),anchor='e',justify='left')
    group.pack()
    path_group = './assets/feishu-chatgroup.jpg'
    img_group = Image.open(path_group)
    photo_group = ImageTk.PhotoImage(img_group)
    
    label_group = tk.Label(newWindow,image=photo_group,height=400, width=256)
    label_group.pack()

    personal = tk.Label(newWindow, text = i18labels("contact_str_personal", locale=lang, module="g").replace('\\n','\n'),anchor='e',justify='left')
    personal.pack()
    path_personal = './assets/wechat.jpg'
    img_personal = Image.open(path_personal)
    photo_personal = ImageTk.PhotoImage(img_personal)#在root实例化创建，否则会报错
    
    label_personal = tk.Label(newWindow,image=photo_personal,height=400, width=256)
    label_personal.pack()

    newWindow.mainloop()

def get_record_video():
    is_record_video=record_video.get()
def get_is_open_browser():
    is_open_browser=open_browser.get()

def install():
    # subprocess.check_call([sys.executable, "-m", "playwright ", "install"])
    subprocess.check_call(["playwright ", "install"])

def testInstallRequirements():
    print('check install requirments')
    checkRequirments()
def testNetwork():
    print('start to test network and proxy setting')
    if proxy_option.get() is None:
        url_ok('www.youtube.com')
        print('you can access google without proxy setting')
    else:
        # print('please check your proxy setting\nsocks5://127.0.0.1:1080\nhttp://proxy.example.com:8080\n222.165.235.2:80\n')
    
        print('your proxy setting is ',proxy_option.get())
        if  proxy_option.get()=='':

            print('you should provide valid your proxy setting,format as follows \nsocks5://127.0.0.1:1080\nhttp://proxy.example.com:8080\n222.165.235.2:80\n')
        else:
            if url_ok('www.youtube.com',proxy_option=proxy_option.get()):        
                print('your  proxy is running ok')
            else:
                print('you should provide valid your proxy setting,format as follows \nsocks5://127.0.0.1:1080\nhttp://proxy.example.com:8080\n222.165.235.2:80\n')
    print('netwrork and proxy test is done')
def ValidateSetting():
    print('start to validate your upload settings')
    time.sleep(4)
    print('end to validate your upload settings')



def create_setting_file():
    ROOT_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    print('使用默认模版新建配置文件')
    default_setting_path ="./assets/config/template.json"

    global setting_file
    if os.path.exists(ROOT_DIR+os.path.sep+default_setting_path):
        print('default template exists')
        fp = open(ROOT_DIR+os.path.sep+default_setting_path, 'r', encoding='utf-8')
        setting_json = fp.read()
        fp.close()        
        setting = json.loads(setting_json)
    else:
        setting={}
    firefox_profile_folder_path = setting['firefox_profile_folder']
    firefox_profile_folder.set(firefox_profile_folder_path)

    proxy_option.set(setting['proxy_option'])
    # firefox_profile_folder.set(setting['firefox_profile_folder'])
    channel_cookie.set(setting['channelcookiepath'])
    video_folder.set(setting['video_folder'])

    prefertags.set(setting['prefertags'])
    preferdessuffix.set(setting['preferdessuffix'])
    preferdesprefix.set(setting['preferdesprefix'])
    
    dailycount.set(setting['dailycount'])
    channelname.set('hints-we use this as setting file name,you should change it')
    music_folder_path= setting['music_folder']
    publishpolicy.set(setting['publishpolicy'])
    music_folder.set(music_folder_path)
    ratio.set(setting['ratio'])    
    with open(ROOT_DIR+os.path.sep+'./assets/config/'+channelname.get()+".json", 'w') as f:

        f.write(json.dumps(setting, indent=4, separators=(',', ': ')))      

    if os.path.exists(ROOT_DIR+os.path.sep+'./assets/config/'+channelname.get()+".json"):
        print('setting file create done')

def videosMenuMangement():
    # global frame
    # frame=tk.Frame(root,width=str(width),  height=str(height),  )
    # frame.pack()
    window = tk.Tk()
    
    window.title("Airline Management System")

    window.geometry('550x450')    
    tab_control = ttk.Notebook(window)
    
    right = ttk.Frame(tab_control)
    
    left = ttk.Frame(tab_control)

    three = ttk.Frame(tab_control)

    four = ttk.Frame(tab_control)

    right1 = tk.Frame(three, width = 500, height = 500)
    right1.pack(side = tk.RIGHT)

    left1 = tk.Frame(three, width = 500, height = 500)
    left1.pack(side = tk.LEFT)

    tab_control.add(right, text='Passenger Info')
    
    tab_control.add(left, text='Airline Info')

    tab_control.add(three, text='Book Ticket')

    tab_control.add(four, text='Boarding Pass')
    tab_control.pack(expand=1, fill='both')
    window.mainloop()
def load_setting_file():
    ROOT_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )
    default_setting_path=''
    if os.path.exists('latest-used-setting.txt') :
        try:
            fp = open('latest-used-setting.txt', 'r', encoding='utf-8')
            default_setting_path=fp.readlines()[0]
            print('读取最近保存的配置文件',default_setting_path)


        except:
            print('读取配置文件失败 加载默认模版')
            default_setting_path ="./assets/config/demo.json"

    else:
        print('读取配置文件失败 加载默认模版')
        default_setting_path ="./assets/config/demo.json"



    print('======',ROOT_DIR+os.path.sep+default_setting_path)

    global setting_file
    setting_file = filedialog.askopenfilenames(initialdir=ROOT_DIR,initialfile=ROOT_DIR+os.path.sep+default_setting_path,title="请选择该频道配置文件", filetypes=[
        ("Json", "*.json"), ("All Files", "*")])[0]
    load_setting()
    firefox_profile_folder_path = setting['firefox_profile_folder']
    firefox_profile_folder.set(firefox_profile_folder_path)

    proxy_option.set(setting['proxy_option'])
    # firefox_profile_folder.set(setting['firefox_profile_folder'])
    channel_cookie.set(setting['channelcookiepath'])
    video_folder.set(setting['video_folder'])

    prefertags.set(setting['prefertags'])
    preferdessuffix.set(setting['preferdessuffix'])
    preferdesprefix.set(setting['preferdesprefix'])
    
    dailycount.set(setting['dailycount'])
    channelname.set(setting['channelname'])
    music_folder_path= setting['music_folder']
    publishpolicy.set(setting['publishpolicy'])
    music_folder.set(music_folder_path)
    ratio.set(setting['ratio'])



def auto_gen_cookie_file():
    
    print('call tsup gen cookie api')

def genThumbnailFromTemplate(video_folder,thumb_template,mode):
    print('find missing files')
    print('render thumbnails for videos')
def select_thumb_template_file():
    global thumbnail_template_file_path
    try:
        thumbnail_template_file_path = filedialog.askopenfilenames(title="请选择 template文件", filetypes=[
            ("Json", "*.json"), ("All Files", "*")])[0]

        thumbnail_template_file.set(thumbnail_template_file_path)
    except:
        print('please select a valid template json file')

def select_cookie_file():

    global channel_cookie_path
    try:
        channel_cookie_path = filedialog.askopenfilenames(title="请选择该频道对应cookie文件", filetypes=[
            ("Json", "*.json"), ("All Files", "*")])[0]

        channel_cookie.set(channel_cookie_path)
        setting['channelcookiepath'] = channel_cookie_path
    except:
        print('please select a valid cookie json file')


# 清理残留文件

def threadusing_free_musichelper(numbers):

    using_free_music(numbers[0],numbers[1])

def using_free_music(setting,inputmp4):

    if os.path.exists(inputmp4):

        print('video exists', inputmp4)
    else:
        print('video not found')
    try:
        music_folder =setting['music_folder']
    except:
        music_folder='assets/freemusic'

    else:

        music_folder = setting['music_folder']
    if os.path.exists(music_folder):
        print('there are free music folder',music_folder)
    else:
        print('choose valid free music folder',music_folder)

    freemusic = []

    for ext in ('*.mp3', '*.wav','*.wma','*.ogg','*.aac'):
        freemusic.extend(glob(os.path.join(music_folder, ext)))
        
    if len(freemusic) > 0:    
        soundeffect = random.choice(freemusic)
        print('randomly choose a background music',soundeffect)
        ext = os.path.splitext(soundeffect)[1]
        videoext= os.path.splitext(inputmp4)[1]
        videofilename= os.path.splitext(inputmp4)[0]

        print('videoext',videoext)
        print('videofilename',videofilename)
        oldvideofiles=[]

        audioclip = AudioFileClip(soundeffect)
        if not os.path.exists(videofilename+'-old'+videoext):
            os.rename(inputmp4, videofilename+'-old'+videoext)
        videoclip = VideoFileClip(videofilename+'-old'+videoext)
        if audioclip.duration>videoclip.duration:
            audioclip =audioclip.subclip(0,videoclip.duration)
        else:
            audioclip = vfx.loop( audioclip, duration=videoclip.duration)
        if setting['ratio']:
            pass
        else:
            setting['ratio']=1
        # audioclip = audioclip.fx( afx.volumex, float(setting['ratio']))
        # audioclip.write_audiofile(videofilename+'.mp3')

        # audioclip = volumex(audioclip,setting['ratio'])          
        videoclip = videoclip.set_audio(audioclip)

        videoclip.write_videofile(videofilename+'.mp4', threads=0, audio=True)
        if not videoclip == None:
            print('force close clip')
            audioclip.close()

            videoclip.close()

            del audioclip 
            del videoclip 
 
            import gc 
            gc.collect()

           
        # time.sleep(2) 
        print('start cleaning old video file')
        if os.path.exists(videofilename+'-old'+videoext):
            os.remove(videofilename+'-old'+videoext)
def init_worker(mps, fps, cut):
    global memorizedPaths, filepaths, cutoff
    global DG

    print("process initializing", mp.current_process())
    memorizedPaths, filepaths, cutoff = mps, fps, cut
    DG = 1##nx.read_gml("KeggComplete.gml", relabel = True)
def changeLoglevel(level,window,log_frame):
    values = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    if level=='DEBUG':
        logging.basicConfig(filename='test.log',
            level=logging.DEBUG, 
            format='%(asctime)s - %(levelname)s - %(message)s')   
    elif level=='INFO':
        logging.basicConfig(filename='test.log',
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s') 
    elif level=='WARNING':
        logging.basicConfig(filename='test.log',
            level=logging.WARNING, 
            format='%(asctime)s - %(levelname)s - %(message)s') 
    elif level=='ERROR':
        logging.basicConfig(filename='test.log',
            level=logging.ERROR, 
            format='%(asctime)s - %(levelname)s - %(message)s') 
    elif level=='CRITICAL':
        logging.basicConfig(filename='test.log',
            level=logging.CRITICAL, 
            format='%(asctime)s - %(levelname)s - %(message)s') 


def changeDisplayLang(lang,window,log_frame):

    window.destroy()
    log_frame.destroy()
    root.title(i18labels("title", locale=lang, module="g"))        
    window=tk.Frame(root,width=str(width),  height=str(height+200),  )
    
    log_frame = tk.Frame(window, width = width, height = 5)
    log_frame.pack(side = tk.BOTTOM)
    st = ScrolledText.ScrolledText(log_frame,                                      
                                width = width, 
                                    height = 5, 
                                     wrap=tk.WORD,
                                    state='disabled')
    st.configure(font='TkFixedFont')
    st.grid(column=0, 
            row=0, 
            # sticky='n',
            # columnspan=4
            )
    # st.pack(padx=10, pady=10,side= tk.LEFT, fill=tk.X, expand=True)
    # Create textLogger
    text_handler = TextHandler(st)

    logger.addHandler(text_handler)    
    # print('debug message')
    # print('info message')
    # logger.warning('warn message')
    # logger.error('error message')
    # logger.critical('critical message')
    window.pack()
    render(root,window,log_frame,lang)
    logger.info(f'switch lang to locale:{lang}')

def hiddenwatermark():
    print('add hiddenwatermark to each video for  copyright theft')
def batchchangebgmusic():

    # use all available CPUs
    # p = mp.Pool(initializer=init_worker, initargs=(memorizedPaths,
    #                                                filepaths,
    #                                                cutoff))
    folder =setting['video_folder']    
    oldvideofiles=[]
    videofiles = []

    if os.path.isdir(folder):
        print('this is a directory',folder)

        for ext in ('*.flv', '*.mp4', '*.avi'):
            videofiles.extend(glob(os.path.join(folder, ext)))
        print('detecting videos in folder',folder,videofiles)
        if len(videofiles) > 0:
            arguments=[]
            for i,f in enumerate(videofiles):
                videofilename= os.path.splitext(f)[0]
                videoext= os.path.splitext(f)[1]
                if not videofilename.endswith('-old'):
                    using_free_music(setting,f)
                    # arguments.append((setting,f)) 

            print('awaiting convert files',videofiles)                                                   
            # degreelist = range(100000) ##
    #         for _ in p.imap_unordered(threadusing_free_musichelper, arguments, chunksize=500):
    #             pass
    # p.close()
    # p.join()


    # print('start cleaning old video files')
    # oldvideofiles=[]

    # if os.path.isdir(folder):

    #     for ext in ('*.flv', '*.mp4', '*.avi'):
    #         oldvideofiles.extend(glob(os.path.join(folder, ext)))
    #     # print('this is a directory',folder)
  
    # for f in oldvideofiles:   
    #     videofilename= os.path.splitext(f)[0]

    #     if  videofilename.endswith('-old'):
    #         print('start cleaning old video file',f)
    #         if os.path.exists(f.replace('-old','')):
    #             os.remove( f)
    print('finish cleaning old video files')
def changebgmusic():
    folder =setting['video_folder']    
    if os.path.isdir(folder):
        print('this is a directory',folder)

        videofiles = []
        for ext in ('*.flv', '*.mp4', '*.avi'):
            videofiles.extend(glob(os.path.join(folder, ext)))
        print('detecting videos in folder',folder,videofiles)
        if len(videofiles) > 0:
            # for i,f in enumerate(videofiles):

            #     videofiles.append(f)    
            print('awaiting convert files',videofiles)
            start = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                # while True:
                tasks = [using_free_music(x) for x in videofiles]
                for task, future in [(i, executor.submit(i)) for i in tasks]:
                    try:
                        # print(future.result(timeout=1))
                        print('ok')
                    except concurrent.futures.TimeoutError:
                        print("this took too long...")
            #             # task.interrupt()
            end = time.time()
            print("批量替换took {} seconds\n".format(end-start))



def b64e(s):
    return base64.b64encode(s.encode()).decode()


def autothumb():

    save_setting()
# 文件夹下是否有视频文件

# 视频文件是否有同名的图片

    try:
        video_folder_path = setting['video_folder']

    except NameError:
        print('not found fastlane folder  file')
    else:
        if video_folder_path:
            print("sure, it was defined dir.",video_folder_path)

            check_video_thumb_pair(video_folder_path,False)
        else:
            print("pls choose file or folder")
def editVideoMetas():
    print('go to web json editor to edit prepared video metas in json format')


def SelectVideoMetasfile():
    logger.debug('start to import prepared video metas in json format')
    try:
        video_meta_json_path = filedialog.askopenfilenames(title="choose video meta json file", filetypes=[
        ("Json", "*.json"), ("All Files", "*")])[0]
        imported_video_metas_file.set(video_meta_json_path)

    except:
        logger.error('you should choose a valid path')
    # setting['channelcookiepath'] = channel_cookie_path
    logger.debug('finished to import prepared video metas in json format')

def downVideoMetas():
    template_url='https://raw.githubusercontent.com/wanghaisheng/tiktoka-studio-uploader-app/main/assets/youtube-videos-meta-comments.json'
    logger.info(f'start to down video metas json template from:{template_url}')
    time.sleep(3)
    logger.info('finish to down video metas json template')

    
def genVideoMetas():
    dbm=DBM('prod')
    save_setting(dbm)
# 文件夹下是否有视频文件

# 视频文件是否有同名的图片

    try:
        video_folder_path = setting['video_folder']

    except NameError:
        print('not found fastlane folder  file')
    else:
        if video_folder_path:
            if os.path.exists(video_folder_path):
                check_video_thumb_pair(dbm,video_folder_path,False)
            else:
                print("there is no defined video dir.")
        else:
            print("pls choose file or folder")
    print('save metas to json /csv excel format for later processing')

def validateMetafile(engine,ttkframe,metafile):
    logger.info('load video metas to database .create upload task for each video')


    if metafile !='' and metafile is not None:
        
        logger.info(f'you select metafile is {metafile}')
        if  os.path.exists(metafile):
            # check_video_thumb_pair(dbm,video_folder_path,True)
            logger.info('start to load  and parse meta json')

            
            settingidsdict={}
            try:
                data = json.load(open(metafile))
            # df = pd.read_json(metafile)     
            except:
                logger.error(f'{metafile} cannot be read') 
            else:
                try:
                    settings=data["uploadSetting"]

                    for setting in settings:
                        logger.info(f'setting json is {setting}')

                        for key in ['proxy_option','channel_cookie_path']:
                            if setting.get(key)==None:
                                logger.error(f" this field {key} is required in given setting json data")
                                raise ValueError(f"this field {key} is required  in given data")
                                
                        for key in ['timeout','timeout','debug','wait_policy','is_record_video','username','password']:
                            if setting.get(key)==None:
                                logger.info(f"no {key} filed provide in given setting json data,we can use default value")

                        if setting.get('browser_type')==None:
                            setting['browser_type']='firefox'        
                            logger.info('we use browser_type =firefox')
                        else:
                            if type(setting.get('browser_type'))!=str:
                                logger.error('browser_type should be one of "chromium", "firefox", "webkit"')
                            else:
                                if not setting.get('browser_type') in ["chromium", "firefox", "webkit"]:
                                    logger.error('browser_type should be one of"chromium", "firefox", "webkit"')

                        if setting.get('platform')==None:
                            setting['platform']='youtube'        
                            logger.info('you dont specify platform field,we use default youtube')
                        else:
                            if type(setting.get('platform'))!=str:
                                logger.error('platform should be one of "youtube", "tiktok", "douyin"')
                            else:
                                if not setting.get('platform') in ["youtube", "tiktok", "douyin"]:
                                    logger.error('platform should be one of "youtube", "tiktok", "douyin"')


                        if setting.get('timeout')==None:
                            setting['timeout']=200000
                            logger.info("you dont specify timeout field,we use default 200*1000")
                        else:
                            if type(setting.get('timeout'))!=int:
                                logger.error('timeout should be integer,such as 20*1000=20000, 20 seconds')
                        if setting.get('is_open_browser')==None:
                            setting['is_open_browser']=True
                            logger.info("you dont specify is_open_browser field,we use default True")
                            
                        else:
                            
                            if type(setting.get('is_open_browser'))==bool:
                                pass
                            elif type(setting.get('is_open_browser'))==str and setting.get('is_open_browser').lower() not in ['true','false']:

                                logger.error(f'is_open_browser is {setting.get("is_open_browser")} of {type(setting.get("is_open_browser"))},it should be bool, true or false')

                        if setting.get('debug')==None:
                            setting['debug']=True
                            logger.info("you dont specify debug field,we use default True")
                            
                        else:
                            
                            if type(setting.get('debug'))==bool:
                                pass
                            elif type(setting.get('debug'))==str and setting.get('debug').lower() not in ['true','false']:

                                logger.error(f'debug is {setting.get("debug")} of {type(setting.get("debug"))},it should be bool, true or false')

               
                        if setting.get('wait_policy')==None:
                            setting['wait_policy']=2        
                            logger.info("you dont specify wait_policy field,we use default 2")
                        else:
                            if type(setting.get('wait_policy'))!=int:
                                logger.error('wait_policy should be one of 0,1,2')
                            else:
                                if not setting.get('wait_policy') in [0,1,2]:
                                    logger.error('wait_policy should be one of 0,1,2')

                        if setting.get('is_record_video')==None:
                            setting['is_record_video']=True        
                            logger.info("you dont specify is_record_video field,we use default True")
                            
                        else:
                            
                            if type(setting.get('is_record_video'))==bool:
                                pass
                            elif type(setting.get('is_record_video'))==str and setting.get('is_record_video').lower() not in ['true','false']:

                                logger.error(f'is_record_video is {setting.get("is_record_video")} of {type(setting.get("is_record_video"))},it should be bool, true or false')


                        df_setting=    pd.json_normalize(setting)

                        newid=pd.Timestamp.now().value  
                        if setting.get('id')==None:
                            df_setting['id']=newid  
                            logger.info(f"you dont specify id field,we generate a new {newid} for this setting")
                            
                            settingidsdict[newid]=newid   
                            logger.info(f"setting old id and new ids mapping dicts is {settingidsdict}")

                        else:
                            if type(setting['id'])==str:
                                try:
                                    setting['id']=int(setting['id'])
                                    
                                except Exception as e:
                                    logger.error(f'setting["id"] should be a int value')
                            settingidsdict[setting['id']]=newid                               
                            logger.info(f"you  specify id field,we add a mapping to {setting['id']}  of {type({setting['id']} )}a new {newid} for this setting")
                            df_setting['id']=newid  

                            logger.info(f"setting old id and new ids mapping dicts is {settingidsdict}")

                        df_setting['inserted_at']=datetime.now()           

                        logger.info('start to check whether setting duplicate or save as new')

                        table_name = "uploadsetting"
                        
                        is_setting_ok=pd2table(engine,table_name,df_setting,logger,if_exists='replace')

                    query = 'SELECT * FROM uploadsetting'
                    # Display the results
                    df=query2df(engine,query,logger)
                    print(df.columns)
                    print(df.head(3))

            # prepareuploadsession( dbm,videopath,thumbpath,filename,start_index,setting['channelname'],settingid)

                except Exception as e:
                    logger.error(f'there is no uploadSetting key in  your metajson:{e}')
                try:
                    videos=data["videos"]
                    logger.info(f'we found {len(videos)} videos to be load in db')
                    
                    for idx,video in enumerate(videos):
                        logger.info(f'start to process {str(idx)}th\n:{video} ')
                    
                        for key in ['video_local_path','video_title','video_description','thumbnail_local_path','publish_policy','tags']:
                            if video.get(key)==None:
                                logger.error(f"these {key} field is required,No target{key} in given video json data")
                                raise ValueError(f"these {key} field is required,No target{key} in given video json data")
                            if key in['video_local_path','thumbnail_local_path']:
                                if os.path.exists(video.get(key))==False:
                                    logger.error(f"these {key} field is required,and check whether local file exists")
                                    raise ValueError(f"these {key} field is required,and check whether local file exists")
                        for key in ['video_film_date','video_film_location','first_comment','subtitles']:
                            video[key]=None 
                            logger.info(f'now we have no rules about {key} validation ')

                        for key in ['is_allow_embedding','is_publish_to_subscriptions_feed_notify',
                                    'is_automatic_chapters','is_featured_place', 'is_not_for_kid',
                                    'is_show_howmany_likes',
                                    'is_monetization_allowed']:

                            if video.get(key)==None:
                                video[key]=True 
                                logger.info(f"This field {key} is optional in given video json data,we can use default true")
                            else:
                                if video.get(key) not in ['true','false']:
                                    logger.error(f'{key} should be bool, true or false') 


                        for key in ['is_age_restriction','is_paid_promotion']:
                            if video.get(key)==None:
                                video[key]=False 

                                logger.info(f"This field {key} is optional in given video json data,we can use default false")
                            else:
                                if video.get(key) not in ['true','false']:
                                    logger.error(f'{key} should be bool, true or false') 

                        if video.get('categories')==None:
                            video['categories']=None      
                            logger.info('we use categories =none')
                        else:
                            if type(video.get('categories'))!=int:
                                logger.error('categories should be one of 0,1,....,14')
                            else:
                                if not video.get('categories') in range(0,15):
                                    logger.error('categories should be one of 0,1,2,3..........,14')

                        if video.get('license_type')==None:
                            video['license_type']=0       
                            logger.info('we use license_type =0')
                        else:
                            if type(video.get('license_type'))!=int:
                                logger.error('license_type should be one of 0,1')
                            else:
                                if not video.get('license_type') in range(0,2):
                                    logger.error('license_type should be one of 0,1')
                        if video.get('shorts_remixing_type')==None:
                            video['shorts_remixing_type']=0       
                            logger.info('we use shorts_remixing_type =0')
                        else:
                            if type(video.get('shorts_remixing_type'))!=int:
                                logger.error('shorts_remixing_type should be one of 0,1,2')
                            else:
                                if not video.get('shorts_remixing_type') in range(0,3):
                                    logger.error('shorts_remixing_type should be one of 0,1,2')
                        if video.get('comments_ratings_policy')==None:
                            video['comments_ratings_policy']=1       
                            logger.info('we use comments_ratings_policy =1')
                        else:
                            if type(video.get('comments_ratings_policy'))!=int:
                                logger.error('comments_ratings_policy should be one of 0,1,2,3,4,5')
                            else:
                                if not video.get('comments_ratings_policy') in range(0,6):
                                    logger.error('comments_ratings_policy should be one of 0,1,2,3,4,5')



                        if video.get('captions_certification')==None:
                            video['captions_certification']=0       
                            logger.info('we use captions_certification =0')
                        else:
                            if type(video.get('captions_certification'))!=int:
                                logger.error('captions_certification should be one of 0,1,2,3,4,5')
                            else:
                                if not video.get('captions_certification') in range(0,6):
                                    logger.error('captions_certification should be one of 0,1,2,3,4,5')
                        if video.get('video_language')==None:
                            video['video_language']=None       
                            logger.info('we use video_language =none')
                        else:
                            if type(video.get('video_language'))!=int:
                                logger.error('video_language should be one of 0,1,2,3,4...23')
                            else:
                                if not video.get('video_language') in range(0,24):
                                    logger.error('video_language should be one of 0,1,2,3,4...23')

                        if video.get('publish_policy')==None:
                            video['publish_policy']=0       
                            logger.info('we use publish_policy =0')
                        else:
                            if type(video.get('publish_policy'))!=int:
                                logger.error('publish_policy should be one of 0,1,2,3,4')
                            else:
                                if not video.get('publish_policy') in [0,1,2,3,4]:
                                    logger.error('publish_policy should be one of 0,1,2,3,4')
                                else:
                                    # check release date and datehour exists
                                    if video.get('publish_policy')==2:
                                        if video.get('release_date')==None:
                                            video['release_date']=None      
                                            logger.info('we use release_date ==none')  
                                        else:
                                            if video.get('release_date_hour')==None:     
                                                logger.info('we use default release_date_hour 10:15')    
                                            elif video.get('release_date_hour') not in availableScheduleTimes:
                                                logger.error(f'we use choose one from {availableScheduleTimes}') 
                        if video.get('release_date')==None:
                            nowdate=datetime.now() 
                            video['release_date']=nowdate      
                            logger.info(f'we use release_date =={nowdate }')  
                        else:
                            if video.get('release_date_hour')==None:    
                                video['release_date_hour']="10:15"   
                                logger.info('we use default release_date_hour 10:15')    
                            elif video.get('release_date_hour') not in availableScheduleTimes:
                                logger.error(f'we use choose one from {availableScheduleTimes}')    
                        if video.get('release_date_hour')==None:     
                            video['release_date_hour']="10:15"   
                            logger.info('we use default release_date_hour 10:15')    
                        elif video.get('release_date_hour') not in availableScheduleTimes:
                            logger.error(f'we use choose one from {availableScheduleTimes}')  
                        if video.get('tags')==None:
                            video['tags']=None      
                            logger.info('we use tags =[]')
                        else:
                            if type(video.get('tags'))==str and "," in video.get('tags'):
                                logger.info(f'tags is ok:{video.get("tags")}')                                

                            else:
                                logger.error('tags should be a list of keywords such as "one,two" ')

                        logger.info(f'length of settingidsdict is {len(settingidsdict)}')
                        df_video=pd.json_normalize(video)                        
                        if len(settingidsdict)>1:       
                            if video.get('uploadSettingid')==None:
    
                                logger.error('we need explicitly specify  uploadSettingid in each video ')
                            else:

                                if  settingidsdict[video.get('uploadSettingid')]:
                                    df_video['upload_setting_id']=settingidsdict[video.get('uploadSettingid')]
                                else:       
                                    logger.error(f'please check {video.get("uploadSettingid")} is saved sucess in db')
                        elif len(settingidsdict)==1:       
                            logger.info(f'there is only one setting:{list(settingidsdict.items())}')
                            # there is two case, 
                            # 1.user input a setting id,we gen a new as value in the dict,key is the old
                            # 2. user give no id, we gen a new as key and value in the dict
                            df_video['upload_setting_id']= list(settingidsdict.keys())[0]
                           
                        else:

                            logger.error('we need at least 1 uploadsetting saved sucess in db')

                        newid=pd.Timestamp.now().value  
                        df_video['id']=newid
                        df_video['youtube_video_id']=None
                        df_video['inserted_at']=datetime.now()           
                        df_video['updated_at']=None           
                        df_video['uploaded_at']=None    
       
                        df_video['status']=False         
                        # print('videos',videos)   
                        logger.info(f'start to check {str(idx)}th video whether  duplicate or save as new')

                        table_name = "uploadtasks"
                        

                        is_video_ok=pd2table(engine,table_name,df_video,logger,if_exists='append')
                        if is_video_ok:
                            logger.info(f'save {str(idx)}th video ok:{df_video["video_title"]}')
                            
                    query = 'SELECT * FROM uploadtasks'
                    # Display the results
                    df=query2df(engine,query,logger)

                    logger.info(f'there is {len(df.index)} records in table {table_name}')      
                    lab = tk.Label(ttkframe,text="validation pass,try to create upload task next",bg="green",width=40)
                    lab.place(x=10, y=220)       
                    lab.after(5*1000,lab.destroy)                                        
                                                 
                except Exception as e:
                    logger.error(f'there is no videos in  your metajson.check metajson docs for reference:{e}')                
                


        else:
            logger.error("you choosed video meta json file is missing or broken.")
            lab = tk.Label(ttkframe,text="please choose a valid json file",bg="lightyellow",width=40)
            lab.place(x=10, y=220)       
            lab.after(10*1000,lab.destroy)
    else:
        logger.error('please provide a video meta json file')
        lab = tk.Label(ttkframe,text="please choose a  json file",bg="lightyellow",width=40)
        lab.place(x=10, y=220)       
        lab.after(10*1000,lab.destroy)       


def createuploadsession(dbm,ttkframe,metafile):
    save_setting(dbm)
    logger.info('load video metas to database .create upload task for each video')
# 文件夹下是否有视频文件

# 视频文件是否有同名的图片

    try:
        metafile

    except NameError:
        logger.error('please provide a video meta json file')
        is_createuploadsession.set(False)
       
    else:
        if metafile:
            if os.path.exists(metafile):
                # check_video_thumb_pair(dbm,video_folder_path,True)
                logger.info('start to load  and parse meta json')
                # prepareuploadsession( dbm,videopath,thumbpath,filename,start_index,setting['channelname'],settingid)
                logger.info('start to create uploading task for each video')
            else:
                is_createuploadsession.set(False)                
                print("there is no defined video dir.",is_createuploadsession.get())
                print('===',is_createuploadsession.get())


        else:
            print("pls choose file or folder")
            is_createuploadsession.set(False)

        if is_createuploadsession.get()==False:
            logger.info('show import meta to database error hints in 10 seconds')
            lab = tk.Label(ttkframe,text="创建失败，请参考日志修改文件后重新提交",bg="lightyellow",width=40)
            lab.place(x=10, y=220)       
            lab.after(10*1000,lab.destroy)

def analyse_video_thumb_pair(folder,frame):
    print(f'detecting----------{folder}')
    checkvideopaircountsvalue=0
    checkvideocountsvalue=0
    for r, d, f in os.walk(folder):
        with os.scandir(r) as i:

            for entry in i:
                if entry.is_file():
                    filename = os.path.splitext(entry.name)[0]
                    ext = os.path.splitext(entry.name)[1]

                    start_index=1
                    if ext in ('.flv', '.mp4', '.avi'):
                        videopath = os.path.join(r, entry.name)
                        print(videopath,'==',ext) 
                        checkvideocountsvalue+=1

                        isPaired=0
                        for image_ext in ['.jpeg', '.png', '.jpg','webp']:
                            thumbpath = os.path.join(r, filename+image_ext)

                            if  os.path.exists(thumbpath):     
                                isPaired=1
                        if isPaired==1:
                            checkvideopaircountsvalue+=1
                        start_index=start_index+1
    if checkvideocountsvalue==0:
        print('we could not find any video,prefer format mp4,mkv,flv,mov')
    print('dingding',checkvideopaircountsvalue,checkvideocountsvalue)
    checkvideocounts.set(checkvideocountsvalue)
    video_thumb_pairs_counts.set(checkvideopaircountsvalue)
    render_video_folder_check_results(frame)

def check_video_thumb_pair(dbm,folder,session):
    # print(f'detecting----------{folder}')

    for r, d, f in os.walk(folder):
        with os.scandir(r) as i:
            print('detecting----------',r)
            videopair=0

            for entry in i:
                if entry.is_file():
                    filename = os.path.splitext(entry.name)[0]
                    ext = os.path.splitext(entry.name)[1]
                    # print(filename,'==',ext) 

                    start_index=1
                    if ext in ('.flv', '.mp4', '.avi'):
                        videopath = os.path.join(r, entry.name)
                        count=0
                        exist_image_ext=''
                        for image_ext in ['.jpeg', '.png', '.jpg','webp']:
                            thumbpath = os.path.join(r, filename+image_ext)

                            if not os.path.exists(thumbpath):     
                                count+=1
                            else:
                                exist_image_ext=image_ext  
                        if count==len(['.jpeg', '.png', '.jpg']):
                            no=random.choice(['001','002','003'])
                            if not os.path.exists(os.path.join(r, filename+'-'+no+'.jpg')):   
                                generator = AiThumbnailGenerator(videopath)

                                thumbpath=os.path.join(r, filename+'-'+no+'.jpg')                                
                                print('generated thumbnail is',thumbpath)
                        else:
                            thubmpath=os.path.join(r,filename+exist_image_ext)
                            print('thumbnail is there.if you need create,pls delete the old one')
                        if session:
                            print( videopath,thumbpath,filename,start_index,setting['channelname'],settingid)

                            prepareuploadsession( dbm,videopath,thumbpath,filename,start_index,setting['channelname'],settingid)
                            print('all video added to task list,you should start uploading next ')
                        else:
                            print('save video meta json to local disk')
                        start_index=start_index+1
                        videopair+=1

                if videopair==0:
                    print('we could not find any video,prefer format mp4,mkv,flv,mov')



def prepareuploadsession(dbm,videopath,thumbpath,filename,start_index,channelname,settingid):
    global uploadsessionid
    isadded,isuploaded=dbm.Query_video_status_in_channel(videopath,channelname,settingid)
              
    # filename = os.path.splitext(f)[0]
    if isadded:

        if isuploaded:
            print('task completed', isuploaded, videopath)
        else:

            print('task added but not uploaded')

    else:
        print('task not added before')
        
        tags = setting['prefertags']
        
        
        preferdesprefix = setting['preferdesprefix']
        preferdessuffix = setting['preferdessuffix']
        filename=filename.split(os.sep)[-1]
        des =filename
        if preferdesprefix:

            des=preferdesprefix+'========\n'+des
        if preferdessuffix:
            des=des+'=========\n'+preferdessuffix
        des=des[:4900]
        title = isfilenamevalid(filename)
        if len(filename) > 100:
            title = filename[:90]
        nowtime = time.time()
        videoid = b64e(filename)

        olddata = UploadSession()
        olddata.uploadSettingid=settingid
        olddata.videoid = videoid
        olddata.channelname=setting['channelname']
        publishpolicy=setting['publishpolicy']
        start_publish_date=setting['start_publish_date']
        olddata.publishpolicy=publishpolicy
        today = date.today()
        publish_date =datetime(today.year, today.month, today.day, 20, 15)

        if publishpolicy == 0:
            olddata.publish_date = publish_date
        elif publishpolicy == 1:
            olddata.publish_date = publish_date
        else:
            # Oct 19, 2021
            start_index = int(start_publish_date)+start_index
            maxdays=calendar._monthlen(today.year, today.month)

            monthoffset=int(int(start_index)/maxdays)
            startingday=today.day
            dayoffset=int(int(start_index)/int(setting['dailycount']))
            if today.day+1>maxdays:
                monthoffset=1
                startingday=today.day+1-maxdays
            publish_date =datetime(today.year, today.month+monthoffset, startingday+1+dayoffset, 20, 15)



            olddata.publish_date = publish_date
        olddata.thumbpath = thumbpath
        olddata.title= title
        olddata.des= des
        olddata.videopath = videopath
        olddata.tags= tags
        olddata.status = False
        uploadsessionid=dbm.Add_New_UploadSession_In_Db(olddata)
        print('add 1 new videos ',filename,'for upload session',uploadsessionid)



def exportcsv(dbm):
    videos=dbm.Query_undone_videos_in_channel()


def importundonefromcsv(dbm):
    videos=dbm.Query_undone_videos_in_channel()



def testupload(dbm,ttkframe):
    print('we got setting proxy ,',setting['proxy_option'])
    try:
        uploadsessionid
        if uploadsessionid is None:
            print('weir error',uploadsessionid)
            createuploadsession(dbm,ttkframe)
    except:

        print('before upload,you need create upload session first')
        createuploadsession(dbm,ttkframe)

    videos=dbm.Query_undone_videos_in_channel()
    print('there is ',len(videos),' video need to uploading for task ')

    if len(videos)>0:
        publicvideos=[]
        privatevideos=[]
        othervideos=[]
        if url_ok('http://www.google.com'):
            print('network is fine,there is no need for proxy ')
            setting['proxy_option']=""
            print('start browser in headless mode',is_open_browser)

        else:
            print('google can not be access ')

            print('we need for proxy ',setting['proxy_option'])   
            print('start browser in headless mode',is_open_browser,setting['proxy_option'])
        upload =  YoutubeUpload(
                root_profile_directory=setting['firefox_profile_folder'],
                proxy_option=setting['proxy_option'],
                is_open_browser=is_open_browser,
                debug=True,
                use_stealth_js=False,
                # if you want to silent background running, set watcheveryuploadstep false
                channel_cookie_path=setting['channelcookiepath'],
                username=setting['username'],
                browser_type='firefox',
                wait_policy="go next after copyright check success",
                password=setting['password'],
                is_record_video=setting['is_record_video']

                # for test purpose we need to check the video step by step ,
            )

        for video in videos:
            
            if int(video.publishpolicy)==1:
                print('add public uploading task video',video.videopath)
                
                publicvideos.append(video)
            elif int(video.publishpolicy)==0:
                print('add private uploading task video',video.videopath)

                privatevideos.append(video)
            else:
                print('add schedule uploading task video',video.videopath)

                othervideos.append(video)
        if len(publicvideos)>0:
            print('start public uploading task')
            asyncio.run(bulk_instantpublish(videos=publicvideos,upload=upload))
        if len(privatevideos)>0:
            print('start private uploading task')

            asyncio.run(bulk_privatedraft(videos=privatevideos,upload=upload))
        if len(othervideos)>0:
            print('start schedule uploading task')

            asyncio.run(bulk_scheduletopublish_specific_date(videos=othervideos,upload=upload))


def upload(mode='prod'):
    print('we got setting proxy ,',setting['proxy_option'])
    dbm=DBM('prod')
    
    try:
        uploadsessionid
        if uploadsessionid is None:
            print('weir error',uploadsessionid)
            # createuploadsession()
    except:

        print('before upload,you need create upload session first')
        # createuploadsession()

    videos=dbm.Query_undone_videos_in_channel()
    print('there is ',len(videos),' video need to uploading for task ')

    if len(videos)>0:
        publicvideos=[]
        privatevideos=[]
        othervideos=[]
        if url_ok('http://www.google.com'):
            print('network is fine,there is no need for proxy ')
            setting['proxy_option']=""
            print('start browser in headless mode',is_open_browser)

        else:
            print('google can not be access ')

            print('we need for proxy ',setting['proxy_option'])   
            print('start browser in headless mode',is_open_browser,setting['proxy_option'])
        upload =  YoutubeUpload(
                root_profile_directory=setting['firefox_profile_folder'],
                proxy_option=setting['proxy_option'],
                is_open_browser=is_open_browser,
                debug=True,
                use_stealth_js=False,
                # if you want to silent background running, set watcheveryuploadstep false
                channel_cookie_path=setting['channelcookiepath'],
                username=setting['username'],
                browser_type='firefox',
                wait_policy="go next after copyright check success",
                password=setting['password'],
                is_record_video=setting['is_record_video']

                # for test purpose we need to check the video step by step ,
            )

        for video in videos:
            
            if int(video.publishpolicy)==1:
                print('add public uploading task video',video.videopath)
                
                publicvideos.append(video)
            elif int(video.publishpolicy)==0:
                print('add private uploading task video',video.videopath)

                privatevideos.append(video)
            else:
                print('add schedule uploading task video',video.videopath)

                othervideos.append(video)
        if len(publicvideos)>0:
            print('start public uploading task')
            asyncio.run(bulk_instantpublish(videos=publicvideos,upload=upload))
        if len(privatevideos)>0:
            print('start private uploading task')

            asyncio.run(bulk_privatedraft(videos=privatevideos,upload=upload))
        if len(othervideos)>0:
            print('start schedule uploading task')

            asyncio.run(bulk_scheduletopublish_specific_date(videos=othervideos,upload=upload))

def docView(frame,ttkframe,lang):
    b_view_readme=tk.Button(frame,text=i18labels("docs", locale=lang, module="g"),command=lambda: threading.Thread(target=docs(frame,lang)).start() )
    b_view_readme.place(x=50, y=100)    

    b_view_contact=tk.Button(frame,text=i18labels("contact", locale=lang, module="g"),command=lambda: threading.Thread(target=contact(frame,lang)).start() )
    b_view_contact.place(x=50, y=200)    
    

    b_view_version=tk.Button(frame,text=i18labels("version", locale=lang, module="g"),command=lambda: threading.Thread(target=version(frame,lang)).start() )
    b_view_version.place(x=50, y=300)   

def installView(frame,ttkframe,lang):
    b_view_readme=tk.Button(frame,text=i18labels("testinstall", locale=lang, module="g"),command=lambda: threading.Thread(target=testInstallRequirements).start() )
    b_view_readme.place(x=50, y=100)    

    b_view_contact=tk.Button(frame,text=i18labels("testnetwork", locale=lang, module="g"),command=lambda: threading.Thread(target=testNetwork).start() )
    b_view_contact.place(x=50, y=200)    
    

    b_view_version=tk.Button(frame,text=i18labels("testsettingok", locale=lang, module="g"),command=lambda: threading.Thread(target=ValidateSetting).start() )
    b_view_version.place(x=50, y=300)    
def videosView(frame,ttkframe,lang):
    global videosView_video_folder
    videosView_video_folder = tk.StringVar()

    videosView_video_folder.set(setting['video_folder'])

    l_video_folder = tk.Label(frame, text=i18labels("videoFolder", locale=lang, module="g"))
    l_video_folder.place(x=10, y=20)
    e_video_folder = tk.Entry(frame, width=45, textvariable=videosView_video_folder)
    e_video_folder.place(x=150, y=20)
    b_video_folder=tk.Button(frame,text="Select",command=lambda: threading.Thread(target=select_videosView_video_folder).start() )
    b_video_folder.place(x=580, y=20)    

    l_mode_1 = tk.Label(frame, text=i18labels("toolkits", locale=lang, module="g"))
    l_mode_1.place(x=10, y=int(height-250))
    
    
    b_autothumb = tk.Button(frame, text=i18labels("autothumb", locale=lang, module="g"), command=lambda: threading.Thread(target=autothumb).start())
    b_autothumb.place(x=150, y=int(height-250))
    b_batchchangebgmusic = tk.Button(frame, text=i18labels("batchchangebgmusic", locale=lang, module="g"), command=lambda: threading.Thread(target=batchchangebgmusic).start())
    b_batchchangebgmusic.place(x=350,y=int(height-250))
    
    
    b_hiddenwatermark = tk.Button(frame, text=i18labels("hiddenwatermark", locale=lang, module="g"), command=lambda: threading.Thread(target=hiddenwatermark))
    b_hiddenwatermark.place(x=500,y=int(height-250))

def thumbView(frame,ttkframe,lang):
    global thumbView_video_folder
    thumbView_video_folder = tk.StringVar()


    global checkvideocounts
    checkvideocounts = tk.IntVar()

    global video_thumb_pairs_counts
    video_thumb_pairs_counts = tk.IntVar()

    # videosView_video_folder.set(setting['video_folder'])

    l_video_folder = tk.Label(frame, text=i18labels("videoFolder", locale=lang, module="g"))
    l_video_folder.place(x=10, y=20)
    e_video_folder = tk.Entry(frame, width=45, textvariable=thumbView_video_folder)
    e_video_folder.place(x=150, y=20)
    
    b_video_folder=tk.Button(frame,text="Select",command=lambda: threading.Thread(target=select_thumbView_video_folder).start() )
    b_video_folder.place(x=580, y=20)    
    b_video_folder_check=tk.Button(frame,text="Step1:check video assets",command=lambda: threading.Thread(target=analyse_video_thumb_pair(thumbView_video_folder.get(),frame)).start() )
    b_video_folder_check.place(x=10, y=50)    
    print(b_video_folder_check)
    # print(checkvideocounts)
    # print('===============')
    # print(checkvideopaircounts)


def render_video_folder_check_results(frame):
    lb_video_counts = tk.Label(frame, text='video total counts', font=(' ', 9))
    lb_video_counts.place(x=140, y=110, anchor=tk.NE)
    print(checkvideocounts.get())

    lb_video_counts_value = tk.Label(frame, text=str(checkvideocounts.get()), font=(' ', 9))
    lb_video_counts_value.place(x=200, y=110, width = 50, anchor=tk.NE)


    lb_video_thumb_pairs_counts = tk.Label(frame, text='video-thum paired', font=(' ', 9))
    lb_video_thumb_pairs_counts.place(x=140, y=140, anchor=tk.NE)



    print(video_thumb_pairs_counts.get())
    lb_video_thumb_pairs_counts_value = tk.Label(frame, text=str(video_thumb_pairs_counts.get()), font=(' ', 9))
    lb_video_thumb_pairs_counts_value.place(x=200, y=140, width = 50, anchor=tk.NE)


    lb_video_thumb_pairs_counts = tk.Label(frame, text='missing paired', font=(' ', 9))
    lb_video_thumb_pairs_counts.place(x=140, y=160, anchor=tk.NE)

    missing_video_thumb_pairs_counts=checkvideocounts.get()-video_thumb_pairs_counts.get()

    lb_video_thumb_pairs_counts_value = tk.Label(frame, text=str(missing_video_thumb_pairs_counts), font=(' ', 9))
    lb_video_thumb_pairs_counts_value.place(x=200, y=160, width = 50, anchor=tk.NE)

    if missing_video_thumb_pairs_counts==0:
        lb_thumb_wizard = tk.Label(frame, text='please try another video folder', font=(' ', 18))
        lb_thumb_wizard.place(x=50, y=180,anchor=tk.NW)   
    else:
        lb_thumb_wizard = tk.Label(frame, text='you need create thumbnails for '+str(missing_video_thumb_pairs_counts)+'  videos', font=(' ', 18))
        lb_thumb_wizard.place(x=50, y=180,anchor=tk.NW)        
        b_edit_thumb=tk.Button(frame,text="Step2:make a new thumbnails template use editor",command=lambda: webbrowser.open_new('file:///{base_dir}/template.html'.format(base_dir=ROOT_DIR)))


        b_edit_thumb.place(x=10, y=220)    

        global thumbnail_template_file
        thumbnail_template_file = tk.StringVar()        
        l_thumb_template = tk.Label(frame, text='thumbnail template file')

        l_thumb_template.place(x=10, y=260)
        e_video_folder = tk.Entry(frame, width=45, textvariable=thumbnail_template_file)
        e_video_folder.place(x=150, y=260)
        
        b_video_folder=tk.Button(frame,text="Select",command=lambda: threading.Thread(target=select_thumb_template_file).start() )
        b_video_folder.place(x=580, y=260)    




        b_edit_thumb_metas=tk.Button(frame,text="Step3:make new video thumbnails metas use editor",command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"))
        b_edit_thumb_metas.place(x=10, y=300)    

        global thumbnail_metas_file
        thumbnail_metas_file = tk.StringVar()        
        l_thumb_metas = tk.Label(frame, text='thumbnail metas file')

        l_thumb_metas.place(x=10, y=340)
        e_thumb_metas = tk.Entry(frame, width=45, textvariable=thumbnail_metas_file)
        e_thumb_metas.place(x=150, y=340)

        b_video_folder=tk.Button(frame,text="Select",command=lambda: threading.Thread(target=select_thumb_template_file).start() )
        b_video_folder.place(x=580, y=340)    


        mode = tk.StringVar()
        mode.set("4")

        lab = tk.Label(frame,text="请选择你的缩略图背景图片从何而来",bg="lightyellow",width=30)
        lab.place(x=10, y=380)    
        mode1=tk.Radiobutton(frame,text="视频第一帧作为背景图",variable=mode,value="1",command='')
        mode1.place(x=10, y=420)    
        mode2=tk.Radiobutton(frame,text="视频任意关键帧作为背景图",variable=mode,value="2",command='')
        mode2.place(x=10, y=450)    
        mode3=tk.Radiobutton(frame,text="文件夹中任意图片作为背景图",variable=mode,value="3",command='')
        mode3.place(x=10, y=480)    
        mode4=tk.Radiobutton(frame,text="元数据中已指定背景图地址",variable=mode,value="4",command='')
        mode4.place(x=10, y=510)    
        b_import_thumb_metas_=tk.Button(frame,text="Step4:gen thumbnails use thumb metas and thumb template file",command=lambda: genThumbnailFromTemplate(videosView_video_folder.get(),thumbnail_template_file.get(),mode.get()))
        b_import_thumb_metas_.place(x=10, y=560)    

def  queryAccounts(tree,engine,logger,uid):



    query = "SELECT * FROM accounts ORDER by inserted_at DESC"
    print('uid',uid,type(uid))
    if uid is not None and uid !='' and not "input" in uid:
        query=f"SELECT * FROM accounts  where id={uid}"
    try:
        db_rows = query2df(engine,query,logger)
        records = tree.get_children()
        for element in records:
            tree.delete(element) 
        for row in db_rows.itertuples():
            tree.insert(
                "", 0, text=row.id, values=(row.video_title,row.video_description,row.status,row.release_date, row.release_date_hour, row.publish_policy, row.uploaded_at, row.video_local_path)
            )
    except:
        print('keep the same')    


def printValues(choices):
    for name, var in choices.items():
        print("%s: %s" % (name, var.get()))


def chooseProxies(ttkframe,username):
    newWindow = tk.Toplevel(ttkframe)
    newWindow.geometry(window_size)
    
    
    newWindow.title('proxy selection')

    if username=='':
        username='this user account'

    label = tk.Label(newWindow,
                text = f"Select the proxies for {username} below : ",
                font = ("Times New Roman", 10),
                padx = 10, pady = 10)
    # label.pack()
    label.grid(row=0,column=0, sticky=tk.W)
    
 
    
        
    global vid
    vid = tk.StringVar()
    lbl15 = tk.Label(newWindow, text='Filter by location.')
    # lbl15.place(x=430, y=30, anchor=tk.NE)
    # lbl15.pack(side='left')

    lbl15.grid(row=1,column=0, sticky=tk.W)

    txt15 = tk.Entry(newWindow, width=11,textvariable=vid)
    txt15.insert(0,'input location')
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt15.grid(row=2,column=0, sticky=tk.W)
    
    
    btn5= tk.Button(newWindow, text="Get proxy list", padx = 10, pady = 10,command = lambda: threading.Thread(target=filterProxiesLocations(prod_engine,logger,vid.get())).start())
    # btn5.place(x=800, y=30, anchor=tk.NE)    
    # btn5.pack(side='left')       
    btn5.grid(row=3,column=0, sticky=tk.W)


    
    btn6= tk.Button(newWindow, text="add selected", padx = 10, pady = 10,command = lambda: threading.Thread(target=filterProxiesLocations(prod_engine,logger,vid.get())).start())
    # btn5.place(x=800, y=30, anchor=tk.NE)    
    # btn6.pack(side='left')          
    btn6.grid(row=5,column=0, sticky=tk.W)
     
     

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(newWindow)
    frame_canvas.grid(row=4, column=0, pady=(5, 0), sticky='nw')
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    frame_canvas.grid_propagate(False)     

    # for scrolling vertically
    # for scrolling vertically
    yscrollbar = tk.Scrollbar(frame_canvas)
    yscrollbar.pack(side = tk.RIGHT, fill = tk.Y)
     
    langlist = tk.Listbox(frame_canvas, selectmode = "multiple",
                yscrollcommand = yscrollbar.set)
    langlist.pack(padx = 10, pady = 10,
            expand = tk.YES, fill = "both")

    proxylist =["C", "C++", "C#", "Java", "Python",
        "R", "Go", "Ruby", "JavaScript", "Swift",
        "SQL", "Perl", "XML"]

    def CurSelet(event):
        listbox = event.widget
        # values = [listbox.get(idx) for idx in listbox.curselection()]
        selection=listbox.curselection()
        # picked = listbox.get(selection[1])
        print(type(selection),list(selection))
        
        if len(list(selection))==3:
            lbl15 = tk.Label(newWindow, text='you have reached 3 proxy limit for one account.dont select anymore')
            lbl15.grid(row=6,column=0, sticky=tk.W)
            lbl15.after(5*1000,lbl15.destroy)        
        
        elif len(list(selection))>3:
            print('you should choose no more than 3 proxy for one account')
            lbl15 = tk.Label(newWindow, text='you should choose no more than 3 proxy for one account.please remove')
            lbl15.grid(row=6,column=0, sticky=tk.W)
            lbl15.after(3*1000,lbl15.destroy)
        else:
            lbl15 = tk.Label(newWindow, text='you can add at least 1 and max 3 proxy for one account.')
            lbl15.grid(row=6,column=0, sticky=tk.W)
            lbl15.after(500,lbl15.destroy)
            
    langlist.bind('<<ListboxSelect>>',CurSelet)

    for each_item in range(len(proxylist)):
        
        langlist.insert(tk.END, proxylist[each_item])
        langlist.itemconfig(each_item, bg = "lime")

def bulkImportUsers(ttkframe):
    newWindow = tk.Toplevel(ttkframe)
    newWindow.geometry(window_size)
    
    
    newWindow.title('user bulk import')
    
    input_canvas = tk.Frame(newWindow)
    input_canvas.grid(row=0, column=0, pady=(5, 0), sticky='nw')    
    

    lbl15 = tk.Label(input_canvas, text='input account info with \\n separator')
    lbl15.grid(row=0,column=0, sticky=tk.W)
    

        
    
    
    
    from tkinter.scrolledtext import ScrolledText
    textfield = ScrolledText(input_canvas, wrap=tk.WORD)
    textfield.grid(row = 1, column = 0, columnspan = 6, padx=14, pady=15)

    
    b_choose_proxy=tk.Button(input_canvas,text="load  from file",command=lambda: threading.Thread(target=select_cookie_file).start() )
    b_choose_proxy.grid(row=2,column=0, sticky=tk.W)

    
    res_canvas = tk.Frame(newWindow)
    res_canvas.grid(row=0, column=1, pady=(5, 0), sticky='ne')    
    
        
    global vid
    vid = tk.StringVar()
    lbl15 = tk.Label(res_canvas, text='Filter by location.')
    # lbl15.place(x=430, y=30, anchor=tk.NE)
    # lbl15.pack(side='left')

    lbl15.grid(row=0,column=0, sticky=tk.W)

    txt15 = tk.Entry(res_canvas, width=11,textvariable=vid)
    txt15.insert(0,'input location')
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt15.grid(row=0,column=1, sticky=tk.W)
    
    
    btn5= tk.Button(res_canvas, text="Get proxy list", padx = 10, pady = 10,command = lambda: threading.Thread(target=filterProxiesLocations(prod_engine,logger,vid.get())).start())
    # btn5.place(x=800, y=30, anchor=tk.NE)    
    # btn5.pack(side='left')       
    btn5.grid(row=0,column=2, sticky=tk.W)    
    
    
    
    # treeview_flight
    tree = ttk.Treeview(res_canvas, height = 20, column = 9)
    tree["column"]=('#0','#1','#2','#3','#4','#5','#6','#7')
    tree.grid(row = 1, column = 0, columnspan = 10, padx=14, pady=15)

    tree.heading('#0', text = 'Account No.')
    tree.column('#0', anchor = 'center', width = 70)
    tree.heading('#1', text = 'username')
    tree.column('#1', anchor = 'center', width = 60)
    tree.heading('#2', text = 'password')
    tree.column('#2', anchor = 'center', width = 60)
    tree.heading('#3', text = 'platform')
    tree.column('#3', anchor = 'center', width = 80)
    tree.heading('#4', text = 'proxies')
    tree.column('#4', anchor = 'center', width = 80)
    tree.heading('#5', text = 'Cookiefile')
    tree.column('#5', anchor = 'center', width = 80)
    tree.heading('#6', text = 'create. Time')
    tree.column('#6', anchor = 'center', width = 80)
    tree.heading('#7', text = 'updated. Time')
    tree.column('#7', anchor = 'center', width = 80)
def saveUser():
    pass
    
    
def accountView(frame,ttkframe,lang):



    channel_cookie= tk.StringVar()
    username = tk.StringVar()
    proxy_option = tk.StringVar()
    platform = tk.StringVar()

    password = tk.StringVar()


    l_platform = tk.Label(ttkframe, text=i18labels("platform", locale=lang, module="g"))
    l_platform.place(x=10, y=90)


    keepplatform = platform.get()    
    box = ttk.Combobox(ttkframe, width=int(width*0.01), textvariable=keepplatform, state='readonly')
    box.place(x=10, y=120)
    def selectedplatform(event):
        box = event.widget
        
        print('selected platform is :',box.get())
    box['values'] = ('youtube', 'tiktok', 'douyin')
    box.current(0)
    box.bind("<<ComboboxSelected>>", selectedplatform)



    l_username = tk.Label(ttkframe, text=i18labels("username", locale=lang, module="g"))
    l_username.place(x=10, y=150)
    e_username = tk.Entry(ttkframe, width=int(width*0.01), textvariable=username)
    e_username.place(x=10, y=180)

    l_password = tk.Label(ttkframe, text=i18labels("password", locale=lang, module="g"))
    l_password.place(x=10, y=210)
    e_password = tk.Entry(ttkframe, width=int(width*0.01), textvariable=password)
    e_password.place(x=10, y=240)



    l_proxy_option = tk.Label(ttkframe, text=i18labels("proxySetting", locale=lang, module="g"))
    l_proxy_option.place(x=10, y=270)
    
    
    e_proxy_option = tk.Entry(ttkframe, width=int(width*0.01), textvariable=proxy_option)
    e_proxy_option.place(x=10, y=300)

    b_choose_proxy=tk.Button(ttkframe,text="choose",command=lambda: threading.Thread(target=chooseProxies(ttkframe,username.get())).start() )
    
    b_choose_proxy.place(x=50, y=270)    




    l_channel_cookie = tk.Label(ttkframe, text=i18labels("cookiejson", locale=lang, module="g"))
    l_channel_cookie.place(x=10, y=330)
    e_channel_cookie = tk.Entry(ttkframe, width=int(width*0.01), textvariable=channel_cookie)
    e_channel_cookie.place(x=10, y=360)

    b_channel_cookie=tk.Button(ttkframe,text="Select",command=lambda: threading.Thread(target=select_cookie_file).start() )
    b_channel_cookie.place(x=10, y=390)    
    
    
    b_channel_cookie_gen=tk.Button(ttkframe,text="gen",command=auto_gen_cookie_file)
    b_channel_cookie_gen.place(x=100, y=390)    


    
    b_save_user=tk.Button(ttkframe,text="save user",command=saveUser())
    b_save_user.place(x=10, y=420)        
    
    b_bulk_import_users=tk.Button(ttkframe,text="bulk import",command=lambda: threading.Thread(target=bulkImportUsers(ttkframe)).start() )
    b_bulk_import_users.place(x=10, y=450)    

    global uid
    uid = tk.StringVar()
    lbl15 = tk.Label(ttkframe, text='Enter uid.')
    lbl15.place(x=430, y=15, anchor=tk.NE)
    txt15 = tk.Entry(ttkframe, width=11,textvariable=uid)
    txt15.insert(0,'input uid id')
    txt15.place(x=580, y=15, anchor=tk.NE)

    btn5= tk.Button(ttkframe, text="Get Info", command = lambda: threading.Thread(target=queryAccounts(tree,prod_engine,logger,vid.get())).start())
    btn5.place(x=800, y=15, anchor=tk.NE)    





    # treeview_flight
    tree = ttk.Treeview(frame, height = 20, column = 8)
    tree["column"]=('#0','#1','#2','#3','#4','#5','#6','#7')
    tree.grid(row = 0, column = 0, columnspan = 5, padx=14, pady=15)

    tree.heading('#0', text = 'Account No.')
    tree.column('#0', anchor = 'center', width = 70)
    tree.heading('#1', text = 'username')
    tree.column('#1', anchor = 'center', width = 60)
    tree.heading('#2', text = 'password')
    tree.column('#2', anchor = 'center', width = 60)
    tree.heading('#3', text = 'platform')
    tree.column('#3', anchor = 'center', width = 80)
    tree.heading('#4', text = 'proxies')
    tree.column('#4', anchor = 'center', width = 80)
    tree.heading('#5', text = 'Cookiefile')
    tree.column('#5', anchor = 'center', width = 80)
    tree.heading('#6', text = 'create. Time')
    tree.column('#6', anchor = 'center', width = 80)
    tree.heading('#7', text = 'updated. Time')
    tree.column('#7', anchor = 'center', width = 80)


    
    
def  queryTasks(tree,engine,logger,vid):



    query = "SELECT * FROM uploadtasks ORDER by inserted_at DESC"
    print('vid',vid,type(vid))
    if vid is not None and vid !='' and  not "input" in vid:
        query=f"SELECT * FROM uploadtasks  where id={vid}"
    try:
        db_rows = query2df(engine,query,logger)
        records = tree.get_children()
        for element in records:
            tree.delete(element) 
        for row in db_rows.itertuples():
            tree.insert(
                "", 0, text=row.id, values=(row.video_title,row.video_description,row.status,row.release_date, row.release_date_hour, row.publish_policy, row.uploaded_at, row.video_local_path)
            )
    except:
        print('keep the same')    


def uploadView(frame,ttkframe,lang):

    # treeview_flight
    tree = ttk.Treeview(frame, height = 20, column = 9)
    tree["column"]=('#0','#1','#2','#3','#4','#5','#6','#7')
    tree.grid(row = 0, column = 0, columnspan = 10, padx=14, pady=15)

    tree.heading('#0', text = 'Task No.')
    tree.column('#0', anchor = 'center', width = 70)
    tree.heading('#1', text = 'Video title')
    tree.column('#1', anchor = 'center', width = 60)
    tree.heading('#2', text = 'Description')
    tree.column('#2', anchor = 'center', width = 60)
    tree.heading('#3', text = 'Status')
    tree.column('#3', anchor = 'center', width = 80)
    tree.heading('#4', text = 'release. Date')
    tree.column('#4', anchor = 'center', width = 80)
    tree.heading('#5', text = 'release. Time')
    tree.column('#5', anchor = 'center', width = 80)
    
    tree.heading('#6', text = 'publish type')
    tree.column('#6', anchor = 'center', width = 80)
    tree.heading('#7', text = 'upload. Time')
    tree.column('#7', anchor = 'center', width = 80)
    tree.heading('#8', text = 'local path')
    tree.column('#8', anchor = 'center', width = 80)

    btn5= tk.Button(ttkframe, text="Get Info", command = lambda: threading.Thread(target=queryTasks(tree,prod_engine,logger,vid.get())).start())
    btn5.place(x=800, y=15, anchor=tk.NE)    
    
    
        
    global vid
    vid = tk.StringVar()
    lbl15 = tk.Label(ttkframe, text='Enter vid.')
    lbl15.place(x=430, y=15, anchor=tk.NE)
    txt15 = tk.Entry(ttkframe, width=11,textvariable=vid)
    txt15.insert(0,'input task id')
    txt15.place(x=580, y=15, anchor=tk.NE)




    lb_youtube_counts = tk.Label(ttkframe, text='youtube', font=(' ', 15))
    lb_youtube_counts.place(x=350, y=530, anchor=tk.NE)    

    lb_tiktok_counts = tk.Label(ttkframe, text='tiktok', font=(' ', 15))
    lb_tiktok_counts.place(x=330, y=560, anchor=tk.NE)    
    
    lb_video_counts = tk.Label(ttkframe, text='success', font=(' ', 15))
    lb_video_counts.place(x=450, y=510, anchor=tk.NE)

    lb_video_counts_value = tk.Label(ttkframe, text=str(checkvideocounts.get()), font=(' ', 18))
    lb_video_counts_value.place(x=550, y=510, width = 20, anchor=tk.NE)


    lb_video_thumb_pairs_counts = tk.Label(ttkframe, text='queued', font=(' ', 15))
    lb_video_thumb_pairs_counts.place(x=650, y=510, anchor=tk.NE)



    lb_video_thumb_pairs_counts_value = tk.Label(ttkframe, text=str(video_thumb_pairs_counts.get()), font=(' ', 18))
    lb_video_thumb_pairs_counts_value.place(x=750, y=510, width = 20, anchor=tk.NE)


    lb_video_thumb_pairs_counts = tk.Label(ttkframe, text='failure', font=(' ', 15))
    lb_video_thumb_pairs_counts.place(x=850, y=510, anchor=tk.NE)

    missing_video_thumb_pairs_counts=checkvideocounts.get()-video_thumb_pairs_counts.get()

    lb_video_thumb_pairs_counts_value = tk.Label(ttkframe, text=str(missing_video_thumb_pairs_counts), font=(' ', 18))
    lb_video_thumb_pairs_counts_value.place(x=950, y=510, width = 20, anchor=tk.NE)

        
    
    b_down_video_metas_temp = tk.Button(ttkframe, text=i18labels("downVideoMetas", locale=lang, module="g"), command=lambda: threading.Thread(target=downVideoMetas).start())
    b_down_video_metas_temp.place(x=10, y=int(50))    
    

    b_editVideoMetas = tk.Button(ttkframe, text=i18labels("editVideoMetas", locale=lang, module="g"), command=
                                #  lambda: webbrowser.open_new("https://jsoncrack.com/editor")
                                 lambda: threading.Thread(target=webbrowser.open_new("https://jsoncrack.com/editor")).start())
    b_editVideoMetas.place(x=10, y=int(100))
    


    l_import_video_metas = tk.Label(ttkframe, text=i18labels("importVideoMetas", locale=lang, module="g"), font=(' ', 14))
    l_import_video_metas.place(x=10, y=150, anchor=tk.NW)
    global video_meta_json_path
    b_imported_video_metas_file=tk.Button(ttkframe,text="Select",command=SelectVideoMetasfile)
    b_imported_video_metas_file.place(x=200, y=150)   


    global imported_video_metas_file   
    imported_video_metas_file = tk.StringVar()        
    # l_imported_video_metas_file = tk.Label(ttkframe, text='thumbnail template file')

    # l_imported_video_metas_file.place(x=10, y=200)
    e_imported_video_metas_file = tk.Entry(ttkframe, width=int(width*0.02), textvariable=imported_video_metas_file)
    e_imported_video_metas_file.place(x=10, y=200)

  
    b_validate_video_metas = tk.Button(ttkframe, text=i18labels("validateVideoMetas", locale=lang, module="g"), command=lambda: threading.Thread(target=validateMetafile(test_engine,ttkframe,imported_video_metas_file.get())).start())
    b_validate_video_metas.place(x=10, y=int(250))
    b_createuploadsession = tk.Button(ttkframe, text=i18labels("createuploadsession", locale=lang, module="g"), command=lambda: threading.Thread(target=validateMetafile(prod_engine,ttkframe,imported_video_metas_file.get())).start())
    b_createuploadsession.place(x=10, y=int(300))

    # test upload  跳转到一个单独页面，录入一个视频的上传信息，点击上传进行测试。
    b_upload = tk.Button(ttkframe, text=i18labels("testupload", locale=lang, module="g"), command=lambda: threading.Thread(target=testupload(DBM('test'),ttkframe)).start())
    b_upload.place(x=10, y=int(350))

    b_upload = tk.Button(ttkframe, text=i18labels("upload", locale=lang, module="g"), command=lambda: threading.Thread(target=upload).start())
    b_upload.place(x=10, y=int(400))


    queryTasks(tree,prod_engine,logger,vid.get())
    
def  filterProxiesLocations(engine,logger,pid):



    query = "SELECT * FROM proxies ORDER by inserted_at DESC"
    print('pid',pid,type(pid))
    if pid is not None and pid !='' and pid !="please input task id":
        query=f"SELECT * FROM proxies  where id={pid}"
    try:
        db_rows = query2df(engine,query,logger)
        # records = tree.get_children()
        # for element in records:
        #     tree.delete(element) 
        for row in db_rows.itertuples():
            print()
            # tree.insert(
            #     "", 0, text=row.id, values=(row.video_title,row.video_description,row.status,row.release_date, row.release_date_hour, row.publish_policy, row.uploaded_at, row.video_local_path)
            # )
    except:
        print('keep the same')    

def  queryProxies(tree,engine,logger,city,country):

    logger.info(f'you proxy filter conditions:{city},{country}')

    query = "SELECT * FROM proxies ORDER by inserted_at DESC"
    if city is not None and city !='' and  not "Filter by" in city:
        if country is not None and country !='' and  not "Filter by" in country:
            query=f"SELECT * FROM proxies  where city={city} and country={country}"
        else:
            query=f"SELECT * FROM proxies  where city={city}"
    try:
        db_rows = query2df(engine,query,logger)
        records = tree.get_children()
        for element in records:
            tree.delete(element) 
        for row in db_rows.itertuples():
            tree.insert(
                "", 0, text=row.id, values=(row.url,row.status,row.city,row.country, row.inserted_at,row.updated_at)
            )
    except:
        logger.info('you proxy filter conditions without any change,keep the same')
def updateproxies(engine,proxies_list_raw,logger):
    
    print('check proxy whether valid and its city country')
def saveproxies(engine,proxies_list_raw,logger):
    proxies_list=[]
    if proxies_list_raw and not 'proxy list should be one proxy oneline,and each proxy in such format' in proxies_list_raw:
        proxies_list=proxies_list_raw.split('\n')
        proxies_list=list(set(proxies_list))
        proxies_list=list(filter(None, proxies_list))
        
        for idx,url in enumerate(proxies_list):
            if url:
                print('check url format ',url)
        ids=[]
        status=[]
        cities=[]
        countries=[]
        inserted_ats=[]
        print('==0',proxies_list)
        for i in range(0,len(proxies_list)):
            newid=pd.Timestamp.now().value  
            ids.append(newid)
            status.append(0)
            cities.append(None)
            countries.append(None)
            inserted_ats.append(datetime.now() )     
            
        proxies_df= pd.DataFrame({'url':proxies_list,'id':ids,'status':status,'city':cities,"country":countries,'inserted_at':inserted_ats})
     
        proxies_df['updated_at']=None           
        print('===',proxies_df)
        is_proxy_ok=pd2table(engine,'proxies',proxies_df,logger)
        print('pass')
    else:
        logger.info('you should input valid proxy list and try again')
def returnProxy_textfield(event):
    proxy_textfield_str.set(event.widget.get("1.0", "end-1c"))
    print(proxy_textfield_str.get())
    return proxy_textfield_str.get()
def proxyView(frame,ttkframe,lang):

    
    input_canvas = tk.Frame(frame)
    input_canvas.grid(row=0, column=0, pady=(5, 0), sticky='nw')    
    input_canvas.grid_rowconfigure(100, weight=1)
    input_canvas.grid_columnconfigure(2, weight=1)

    lbl15 = tk.Label(input_canvas, text='copy proxy info here')
    lbl15.grid(row=0,column=0, sticky=tk.W)
    

        
    global proxy_textfield_str
    proxy_textfield_str = tk.StringVar()


    
    from tkinter.scrolledtext import ScrolledText
    proxy_textfield = ScrolledText(input_canvas, wrap=tk.WORD)
    proxy_textfield.grid(row = 2, column = 0, columnspan =2, padx=0, pady=15)
    proxy_textfield.insert(tk.END,'proxy list should be one proxy oneline,and each proxy in such format:\nsocks5://127.0.0.1:1080\nsocks5://127.0.0.1:1088')
    proxy_textfield.bind("<Return>", returnProxy_textfield)

    b_save_proxy=tk.Button(input_canvas,text="save proxy",command=lambda: threading.Thread(target=saveproxies(prod_engine,proxy_textfield.get("1.0", tk.END),logger)).start() )
    b_save_proxy.grid(row=4,column=0, sticky=tk.W)
    
    b_check_proxy=tk.Button(input_canvas,text="check proxy",command=lambda: threading.Thread(target=updateproxies(prod_engine,proxy_textfield.get("1.0", tk.END),logger)).start() )
    b_check_proxy.grid(row=4,column=1, sticky=tk.W)    
    

    b_clear_texts=tk.Button(input_canvas,text="clear all texts",command=lambda: threading.Thread(target=proxy_textfield.delete(1.0,tk.END)).start() )
    b_clear_texts.grid(row=3,column=1, sticky=tk.W)
    
    b_choose_proxy=tk.Button(input_canvas,text="load  from file",command=lambda: threading.Thread(target=select_cookie_file).start() )
    b_choose_proxy.grid(row=3,column=0, sticky=tk.W)




    res_canvas = tk.Frame(frame,width=int(0.7*width))
    res_canvas.grid(row=0, column=1, pady=(5, 0),columnspan=20, sticky=tk.W)    
    res_canvas.grid_rowconfigure(100, weight=1)
    res_canvas.grid_columnconfigure(2, weight=1)
        
    global city,country
    city = tk.StringVar()
    country = tk.StringVar()

    # lbl15 = tk.Label(res_canvas, text='Filter by location.')
    # # lbl15.place(x=430, y=30, anchor=tk.NE)
    # # lbl15.pack(side='left')

    # lbl15.grid(row=0,column=0, sticky=tk.W)

    txt15 = tk.Entry(res_canvas,textvariable=city,width=int(0.01*width))
    txt15.insert(0,'Filter by city')
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt15.grid(row=0,column=0, sticky=tk.NW)

    txt16 = tk.Entry(res_canvas,textvariable=country,width=int(0.01*width))
    txt16.insert(0,'Filter by country')
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt16.grid(row=0,column=1, sticky=tk.NW)
    
    btn5= tk.Button(res_canvas, text="Get proxy list", padx = 0, pady = 0,command = lambda: threading.Thread(target=queryProxies(tree,prod_engine,logger,city.get(),country.get())).start())
    # btn5.place(x=800, y=30, anchor=tk.NE)    
    # btn5.pack(side='left')       
    btn5.grid(row=0,column=2, sticky=tk.W)    
    
    
    
    # treeview_flight
    tree = ttk.Treeview(res_canvas, height = 20, column = 9)
    tree["column"]=('#0','#1','#2','#3','#4','#5','#6','#7')
    tree.grid(row = 2, column = 0, columnspan = 10, padx=14, pady=15)

    tree.heading('#0', text = 'proxy No.')
    tree.column('#0', anchor = 'center', width = 70)
    tree.heading('#1', text = 'URL')
    tree.column('#1', anchor = 'center', width = 60)
    tree.heading('#2', text = 'Status')
    tree.column('#2', anchor = 'center', width = 60)
    tree.heading('#3', text = 'City')
    tree.column('#3', anchor = 'center', width = 80)
    tree.heading('#4', text = 'Country')
    tree.column('#4', anchor = 'center', width = 80)
    tree.heading('#5', text = 'create. Time')
    tree.column('#5', anchor = 'center', width = 80)
    tree.heading('#6', text = 'updated. Time')
    tree.column('#6', anchor = 'center', width = 80)
    # tree.heading('#7', text = 'upload. Time')
    # tree.column('#7', anchor = 'center', width = 80)
    # tree.heading('#8', text = 'local path')
    # tree.column('#8', anchor = 'center', width = 80)    
    
    # viewing_records()

def metaView(frame,ttkframe,lang):

    # 
    global is_debug,is_open_browser,is_record_video,start_publish_date,channelname,ratio,publishpolicy,prefertags,preferdesprefix,preferdessuffix,channel_cookie,proxy_option,firefox_profile_folder,video_folder,dailycount,music_folder
    is_debug = tk.BooleanVar()
    is_debug.set(setting['is_debug']) 

    is_open_browser = tk.BooleanVar()
    is_open_browser.set(setting['is_open_browser']) 
    is_record_video = tk.BooleanVar()
    is_record_video.set(setting['is_record_video'])

    prefertags = tk.StringVar()
    prefertags.set(setting['prefertags'])
    preferdesprefix = tk.StringVar()
    preferdesprefix.set(setting['preferdesprefix'])
    preferdessuffix = tk.StringVar()
    preferdessuffix.set(setting['preferdessuffix'])
    dailycount = tk.StringVar()
    dailycount.set(setting['dailycount'])
    music_folder = tk.StringVar()
    music_folder.set(setting['music_folder'])

    ratio = tk.StringVar()
    ratio.set(setting['ratio'])        
    video_folder = tk.StringVar()
    video_folder.set(setting['video_folder'])
    firefox_profile_folder = tk.StringVar()
    firefox_profile_folder.set(setting['firefox_profile_folder'])
    proxy_option = tk.StringVar()
    proxy_option.set(setting['proxy_option'])
    channelname = tk.StringVar()
    channelname.set(setting['channelname'])
    channel_cookie = tk.StringVar()
    channel_cookie.set(setting['channelcookiepath'])
    publishpolicy = tk.StringVar()
    publishpolicy.set(setting['publishpolicy'])
    start_publish_date = tk.StringVar()
    start_publish_date.set(setting['start_publish_date'])
    username = tk.StringVar()
    username.set(setting['username'])

    password = tk.StringVar()
    password.set(setting['password'])    
    

    
    
    

    l_prefertags = tk.Label(frame, text=i18labels("preferTags", locale=lang, module="g"))
    l_prefertags.place(x=10, y=50)
    el_prefertags = tk.Entry(frame, width=55, textvariable=prefertags)
    el_prefertags.place(x=150, y=50)

    l_preferdesprefix = tk.Label(frame, text=i18labels("descriptionPrefix", locale=lang, module="g"))
    l_preferdesprefix.place(x=10, y=70)
    e_preferdesprefix = tk.Entry(frame, width=55, textvariable=preferdesprefix)
    e_preferdesprefix.place(x=150, y=70)


    l_preferdessuffix = tk.Label(frame, text=i18labels("descriptionSuffix", locale=lang, module="g"))
    l_preferdessuffix.place(x=10, y=100)
    e_preferdessuffix = tk.Entry(frame, width=55, textvariable=preferdessuffix)
    e_preferdessuffix.place(x=150, y=100)


    l_music_folder = tk.Label(frame, text=i18labels("bgVideoFolder", locale=lang, module="g"))
    l_music_folder.place(in_=frame, x=10, y=130)
    
    el_music_folder = tk.Entry(frame, width=45, textvariable=music_folder)
    el_music_folder.place(x=150, y=130)
    
    b_music_folder=tk.Button(frame,text="Select",command=select_musics_folder)
    b_music_folder.place(x=580, y=130)        
    
    

    l_bgMucisVolume = tk.Label(frame, text=i18labels("bgMucisVolume", locale=lang, module="g"))
    l_bgMucisVolume.place(x=10, y=160)
    e_bgMucisVolume = tk.Entry(frame, width=55, textvariable=ratio)
    e_bgMucisVolume.place(x=150, y=160)
    
    l_publishpolicy = tk.Label(frame, text=i18labels("publishPolicy", locale=lang, module="g"))
    l_publishpolicy.place(x=10, y=180)
    e_publishpolicy = tk.Entry(frame, width=55, textvariable=publishpolicy)
    e_publishpolicy.place(x=150, y=180)


    l_dailycount = tk.Label(frame, text=i18labels("dailyVideoLimit", locale=lang, module="g"))
    l_dailycount.place(x=10, y=200)



    e_dailycount = tk.Entry(frame, width=55, textvariable=dailycount)
    e_dailycount.place(x=150, y=200)

    l_start_publish_date=tk.Label(frame, text=i18labels("offsetDays", locale=lang, module="g"))
    l_start_publish_date.place(x=10, y=220)
    e_start_publish_date = tk.Entry(frame, width=55, textvariable=start_publish_date)
    e_start_publish_date.place(x=150, y=220)

    


    l_channelname = tk.Label(frame, text=i18labels("channelName", locale=lang, module="g"))
    l_channelname.place(x=10, y=240)
    e_channelname = tk.Entry(frame, width=55, textvariable=channelname)
    e_channelname.place(x=150, y=240)

    l_video_folder = tk.Label(frame, text=i18labels("videoFolder", locale=lang, module="g"))
    l_video_folder.place(x=10, y=270)
    e_video_folder = tk.Entry(frame, width=45, textvariable=video_folder)
    e_video_folder.place(x=150, y=270)
    
    b_video_folder=tk.Button(frame,text="Select",command=lambda: threading.Thread(target=select_videos_folder).start() )
    b_video_folder.place(x=580, y=270)    
    

    l_firefox_profile_folder = tk.Label(frame, text=i18labels("profileFolder", locale=lang, module="g"))
    l_firefox_profile_folder.place(x=10, y=300)
    e_firefox_profile_folder = tk.Entry(frame, width=45, textvariable=firefox_profile_folder)
    e_firefox_profile_folder.place(x=150, y=300)


    b_firefox_profile_folder=tk.Button(frame,text="Select",command=lambda: threading.Thread(target=select_profile_folder).start() )
    b_firefox_profile_folder.place(x=580, y=300)


    l_proxy_option = tk.Label(frame, text=i18labels("proxySetting", locale=lang, module="g"))
    l_proxy_option.place(x=10, y=330)
    e_proxy_option = tk.Entry(frame, width=55, textvariable=proxy_option)
    e_proxy_option.place(x=150, y=330)

    l_channel_cookie = tk.Label(frame, text=i18labels("cookiejson", locale=lang, module="g"))
    l_channel_cookie.place(x=10, y=360)
    e_channel_cookie = tk.Entry(frame, width=35, textvariable=channel_cookie)
    e_channel_cookie.place(x=150, y=360)

    b_channel_cookie=tk.Button(frame,text="Select",command=lambda: threading.Thread(target=select_cookie_file).start() )
    b_channel_cookie.place(x=480, y=360)    
    
    
    b_channel_cookie_gen=tk.Button(frame,text="gen",command=auto_gen_cookie_file)
    b_channel_cookie_gen.place(x=550, y=360)    

    l_username = tk.Label(frame, text=i18labels("username", locale=lang, module="g"))
    l_username.place(x=10, y=390)
    e_username = tk.Entry(frame, width=55, textvariable=username)
    e_username.place(x=150, y=390)

    l_password = tk.Label(frame, text=i18labels("password", locale=lang, module="g"))
    l_password.place(x=10, y=420)
    e_password = tk.Entry(frame, width=55, textvariable=password)
    e_password.place(x=150, y=420)



    
    # b_readfist = tk.Button(frame, text="Read First", command=docs)
    # b_readfist.place(x=10, y=10)




    

    b_is_open_browser = tk.Checkbutton(frame, text=i18labels("is_open_browser", locale=lang, module="g"), variable=is_open_browser)
    b_is_open_browser.place(x=280, y=10)


    b_recordvideo = tk.Checkbutton(frame, text=i18labels("is_record_video", locale=lang, module="g"), variable=is_record_video)
    b_recordvideo.place(x=200, y=10)


    b_debug = tk.Checkbutton(frame, text=i18labels("debug", locale=lang, module="g"), variable=is_debug)
    b_debug.place(x=120, y=10)

    
    

    
    # l_mode_1 = tk.Label(frame, text=i18labels("mode1", locale=lang, module="g"))
    # l_mode_1.place(x=10, y=int(height-200))

    # b_editVideoMetas = tk.Button(frame, text=i18labels("editVideoMetas", locale=lang, module="g"), command=lambda: threading.Thread(target=editVideoMetas).start())
    # b_editVideoMetas.place(x=150, y=int(height-200))
    
    
    
        
    l_mode_2 = tk.Label(frame, text=i18labels("mode2", locale=lang, module="g"))
    l_mode_2.place(x=10, y=int(height-150))
    
    
    
    b_gen_video_metas = tk.Button(frame, text=i18labels("genVideoMetas", locale=lang, module="g"), command=lambda: threading.Thread(target=genVideoMetas).start())
    b_gen_video_metas.place(x=150, y=int(height-150))





        
    # l_mode_3 = tk.Label(frame, text=i18labels("mode3", locale=lang, module="g"))
    # l_mode_3.place(x=10, y=int(height-100))
    

    # b_import_video_metas = tk.Button(frame, text=i18labels("importVideoMetas", locale=lang, module="g"), command=lambda: threading.Thread(target=importVideoMetas).start())
    # b_import_video_metas.place(x=150, y=int(height-100))
    
    # b_down_video_metas_temp = tk.Button(frame, text=i18labels("downVideoMetas", locale=lang, module="g"), command=lambda: threading.Thread(target=downVideoMetas).start())
    # b_down_video_metas_temp.place(x=350, y=int(height-100))    
    

    # b_createuploadsession = tk.Button(frame, text=i18labels("createuploadsession", locale=lang, module="g"), command=lambda: threading.Thread(target=createuploadsession).start())
    # b_createuploadsession.place(x=150, y=int(height-50))



    # b_upload = tk.Button(frame, text=i18labels("testupload", locale=lang, module="g"), command=lambda: threading.Thread(target=testupload).start())
    # b_upload.place(x=350, y=int(height-50))

    # b_upload = tk.Button(frame, text=i18labels("upload", locale=lang, module="g"), command=lambda: threading.Thread(target=upload).start())
    # b_upload.place(x=550, y=int(height-50))


    
    b_autothumb = tk.Button(frame, text=i18labels("load_setting_file", locale=lang, module="g"), command=lambda: threading.Thread(target=load_setting_file).start())
    b_autothumb.place(x=150, y=int(height-250))
    b_batchchangebgmusic = tk.Button(frame, text=i18labels("save_setting", locale=lang, module="g"), command=lambda: threading.Thread(target=save_setting).start())
    b_batchchangebgmusic.place(x=350,y=int(height-250))
    
    
    b_hiddenwatermark = tk.Button(frame, text=i18labels("create_setting_file", locale=lang, module="g"), command=lambda: threading.Thread(target=create_setting_file))
    b_hiddenwatermark.place(x=500,y=int(height-250))

def render(root,window,log_frame,lang):
    global doc_frame,install_frame,thumb_frame,video_frame,proxy_frame,account_frame,upload_frame,meta_frame

    tab_control = ttk.Notebook(window)
    doc_frame = ttk.Frame(tab_control)
    doc_frame_left1 = tk.Frame(doc_frame, width = width, height = height)
    doc_frame_left1.pack(side = tk.TOP)



    install_frame = ttk.Frame(tab_control)
    install_frame_left1 = tk.Frame(install_frame, width = width, height = height)
    install_frame_left1.pack(side = tk.LEFT)

    thumb_frame = ttk.Frame(tab_control)
    thumb_frame_left1 = tk.Frame(thumb_frame, width = width, height = height)
    thumb_frame_left1.pack(side = tk.LEFT)


    video_frame = ttk.Frame(tab_control)

    video_frame_left1 = tk.Frame(video_frame, width = width, height = height)
    video_frame_left1.pack(side = tk.LEFT)

    proxy_frame = ttk.Frame(tab_control)

    proxy_frame_left1 = tk.Frame(proxy_frame, width = width, height = height)
    proxy_frame_left1.pack(side = tk.RIGHT)


    account_frame = ttk.Frame(tab_control)

    account_frame_left1 = tk.Frame(account_frame, width = int(width*0.5), height = height)
    account_frame_left1.pack(side = tk.RIGHT)

    upload_frame = ttk.Frame(tab_control)

    upload_frame_left1 = tk.Frame(upload_frame, width = width, height = height)
    upload_frame_left1.pack(side = tk.RIGHT)


    meta_frame = ttk.Frame(tab_control)
    meta_frame_left1 = tk.Frame(meta_frame, width = width, height = height)
    meta_frame_left1.pack(side = tk.RIGHT)



    tab_control.add(doc_frame, text=i18labels("docView", locale=lang, module="g"))
    docView(doc_frame_left1,doc_frame,lang)

    tab_control.add(install_frame, text=i18labels("installView", locale=lang, module="g"))
    installView(install_frame_left1,install_frame,lang)


    tab_control.add(account_frame, text=i18labels("accountView", locale=lang, module="g"))
    accountView(account_frame_left1,account_frame,lang)

    tab_control.add(proxy_frame, text=i18labels("proxyView", locale=lang, module="g"))
    proxyView(proxy_frame_left1,proxy_frame,lang)

    tab_control.add(thumb_frame, text=i18labels("thumbView", locale=lang, module="g"))
    thumbView(thumb_frame_left1,thumb_frame,lang)


    tab_control.add(video_frame, text=i18labels("videosView", locale=lang, module="g"))
    videosView(video_frame_left1,video_frame,lang)


    tab_control.add(meta_frame, text=i18labels("metaView", locale=lang, module="g"))
    metaView(meta_frame_left1,meta_frame,lang)


    tab_control.add(upload_frame, text=i18labels("uploadView", locale=lang, module="g"))
    uploadView(upload_frame_left1,upload_frame,lang)

    tab_control.pack(expand=1, fill='both')









    Cascade_button = tk.Menubutton(window)
    # Cascade_button.pack(side=tk.LEFT, padx="2m")
 
     # the primary pulldown
    Cascade_button.menu = tk.Menu(Cascade_button)
 
     # this is the menu that cascades from the primary pulldown....
    Cascade_button.menu.choices = tk.Menu(Cascade_button.menu)
 
 
     # definition of the menu one level up...
    Cascade_button.menu.choices.add_command(label='zh',command=lambda:changeDisplayLang('zh',window,log_frame))
    Cascade_button.menu.choices.add_command(label='en',command=lambda:changeDisplayLang('en',window,log_frame))
    Cascade_button.menu.add_cascade(label= i18labels("chooseLang", locale=lang, module="g"),
                                    
                                     menu=Cascade_button.menu.choices)    
    
    Cascade_button.menu.loglevel = tk.Menu(Cascade_button.menu)
 
 
     # definition of the menu one level up...
    Cascade_button.menu.loglevel.add_command(label='DEBUG',command=lambda:changeLoglevel('DEBUG',window,log_frame))
    Cascade_button.menu.loglevel.add_command(label='INFO',command=lambda:changeLoglevel('INFO',window,log_frame))
    Cascade_button.menu.loglevel.add_command(label='WARNING',command=lambda:changeLoglevel('WARNING',window,log_frame))
    Cascade_button.menu.loglevel.add_command(label='ERROR',command=lambda:changeLoglevel('ERROR',window,log_frame))
    Cascade_button.menu.loglevel.add_command(label='CRITICAL',command=lambda:changeLoglevel('CRITICAL',window,log_frame))

    
    Cascade_button.menu.add_cascade(label= i18labels("loglevel", locale=lang, module="g"),
                                    
                                     menu=Cascade_button.menu.loglevel)    

    menubar = tk.Menu(window)

    menubar.add_cascade(label=i18labels("settings", locale=lang, module="g"), menu=Cascade_button.menu)    



    root.config(menu=menubar)
    # return langchoosen.get()


if __name__ == '__main__':

    gui_flag = 1

    # log_file = "log.txt"


    load_setting()
    global ROOT_DIR
    ROOT_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )



    if gui_flag:
        global root
        root = tk.Tk()
        # root.geometry('1280x720')
        root.geometry(window_size)

        window=tk.Frame(root,width=str(width),  height=str(height+200),  )
        # from src.collapsiblepane import CollapsiblePane as cp
        log_frame =tk.Frame(window, width = width, height = 5)
        # = cp(root, 'Expanded', 'Collapsed')
        # log_frame.resizable(width=True, height=True)
        log_frame.pack(side = tk.BOTTOM)
        st = ScrolledText.ScrolledText(log_frame,                                      
                                    width = width, 
                                        height = 5, 
                                        state='disabled')
        st.configure(font='TkFixedFont')
        st.grid(column=0, 
                row=0, 
                # sticky='n',
                # columnspan=4
                )
        # st.pack(padx=10, pady=10,side= tk.LEFT, fill=tk.X, expand=True)
        # Create textLogger
        text_handler = TextHandler(st)

        logger.addHandler(text_handler)    
        # print('debug message')
        # print('info message')
        # logger.warning('warn message')
        # logger.error('error message')
        # logger.critical('critical message')
        window.pack()

        logger.debug(f'ROOT_DIR is{ROOT_DIR}')
        root.resizable(width=True, height=True)
        root.iconbitmap("assets/icon.ico")

        render(root,window,log_frame,'en')
        root.title(i18labels("title", locale='en', module="g"))        
        logger.info('GUI started')

        root.mainloop()
