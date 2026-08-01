import os
import sys
import tkinter as tk
import platform
from PIL import ImageTk, ImageDraw
import PIL.Image as PilImage    #we need another name, as it collides with tkinter.Image otherwise


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def _global_variables():
        return None


PROGNAME = 'FadeMaid';


#RESOURCE_DIR = './resources'   #use this only for pyinstaller --one-file
RESOURCE_DIR = '../resources'    #use this for normal execution
RES_VERSION = resource_path(RESOURCE_DIR+'/version.txt')
RES_GFX_AC = resource_path(RESOURCE_DIR+'/ac.png')
RES_GFX_FONT = resource_path(RESOURCE_DIR+'/font.png')
RES_DOC_HELP = resource_path(RESOURCE_DIR+'/help.txt')
RES_DOC_ABOUT = resource_path(RESOURCE_DIR+'/about.txt')
RES_GFX_ICON = resource_path(RESOURCE_DIR+'/icon.png')
RES_GFX_ABOUT = resource_path(RESOURCE_DIR+'/about.png')





print('my path: "'+getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))+'"')
print('looking for "'+RES_VERSION+'"')
VERSION = open(RES_VERSION, encoding="utf_8").read().rstrip()

SCREEN_WIDTH = 40
SCREEN_HEIGHT = 25

BGCOLOR='#cccccc'
BGCOLOR_LIGHT='#dddddd'
BGCOLOR2='#ccccff'

_padx = 2
_pady = 2
_bd = 4

FONT_ABC = 'ABCDEFHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!/()=?+.,-:*1234567890 $'

PREVIEW_DELAY   = 40
CURSOR_HAND = 'hand2'
        
root = tk.Tk()

cursor_image_normal = 'tcross'
cursor_image = cursor_image_normal
cursor_image_none = 'X_cursor'

textvariable_coords = tk.StringVar()   #position on screen (320x200)
textvariable_pos   = tk.StringVar()    #position on char-screen (40x25)
textvariable_value   = tk.StringVar()  #value
textvariable_filename_data   = tk.StringVar()
textvariable_filename_image   = tk.StringVar()
textvariable_max   = tk.StringVar()

my_image = PilImage.new("RGB", (640, 400), "black")
image_Tk = ImageTk.PhotoImage(my_image)
label_image = tk.Label()
label_preview_image = tk.Label()

grid_image = PilImage.new("RGBA", (640, 400), "black")
numbers_image = PilImage.new("RGBA", (640, 400), "black")
font_image = PilImage.new("RGBA", (10, 10), "black")
logo_image = PilImage.new("RGBA", (609, 79), "black")

fadedata = SCREEN_HEIGHT*SCREEN_WIDTH*[0]
copybuffer_data = SCREEN_HEIGHT*SCREEN_WIDTH*[0]
copybuffer_width = 0
copybuffer_height = 0

args = None

screenx = 0
screeny = 0
last_screenx = 0
last_screeny = 0
screen_value = 1
value_max = 0
keymode_last_screenx = int(SCREEN_WIDTH/2)
keymode_last_screeny = int(SCREEN_HEIGHT/2)

mouse_posx = 0
mouse_posy = 0
#mouse_button_right = False
#mouse_button_left = False
filename_data = ''
filename_image = ''
preview_in_action = False
show_values = True
show_grid   = True
auto_mode   = False

button_toggle_automode = tk.Button()
button_toggle_grid = tk.Button()
button_toggle_values = tk.Button()
button_toggle_keymode = tk.Button()
button_fade_in = tk.Button()
button_fade_out = tk.Button()

mouse_release_Button1 = True
mouse_release_Button3 = True

CURSOR_BOX_SIZE = 16
keymode = False
keymode_first_number = True

selectmode    = False
select_box_startx    = 0
select_box_starty    = 0
select_box_x1    = 0
select_box_y1    = 0
select_box_x2    = 0
select_box_y2    = 0
