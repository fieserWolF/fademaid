#!/usr/bin/env python3

"""
FadeMaid v2.0 [build 211113-164348] *** by WolF
usage: fademaid.py [-h] [-i IMAGE_FILE] [-d DATA_FILE]

You can edit char-wise values with this.

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE_FILE, --image_file IMAGE_FILE
                        background image filename
  -d DATA_FILE, --data_file DATA_FILE
                        fademaid data filename

Example: ./fademaid.py -i image.png -d data.bin
"""

import os
import sys
from PIL import ImageTk, ImageDraw
import PIL.Image as PilImage    #we need another name, as it collides with tkinter.Image otherwise
import tkinter as tk
import tkinter.filedialog as filedialog
import argparse
import struct



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

RES_VERSION = resource_path('resources/version.txt')
RES_GFX_AC = resource_path('resources/ac.png')
RES_GFX_FONT = resource_path('resources/font.png')
RES_DOC_HELP = resource_path('resources/help.txt')
RES_DOC_ABOUT = resource_path('resources/about.txt')
RES_GFX_ICON = resource_path('resources/icon.png')

#global variables
def _global_variables():
        return None



PROGNAME = 'FadeMaid';
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

raster_image = PilImage.new("RGBA", (640, 400), "black")
numbers_image = PilImage.new("RGBA", (640, 400), "black")
overlay_image = PilImage.new("RGBA", (640, 400), "black")
font_image = PilImage.new("RGBA", (10, 10), "black")
logo_image = PilImage.new("RGBA", (609, 79), "black")

fadedata = SCREEN_HEIGHT*SCREEN_WIDTH*[0]

args = None

screenx = 0
screeny = 0
last_screenx = 0
last_screeny = 0
screen_value = 1
value_max = 0

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
button_fade_in = tk.Button()
button_fade_out = tk.Button()


def save_data(
    filename,
    data
):
    print ('Opening file "%s" for writing data (%d ($%04x) bytes)...' % (filename, len(data), len(data)))
    try:
        file_out = open(filename , "wb")
    except IOError as err:
        print("I/O error: {0}".format(err))
        return None
    file_out.write(bytearray(data))
    file_out.close()




def load_data (
    filename
) :
    global fadedata
    
	#open input file
    print ('Opening data-file "%s" for reading...' % filename)
    try:
        file_in = open(filename , "rb")
    except IOError as err:
        print("I/O error: {0}".format(err))
        return None

    buffer=[]
    while True:
        data = file_in.read(1)  #read 1 byte
        if not data: break
        temp = struct.unpack('B',data)
        buffer.append(temp[0])

    fadedata = buffer



def action_Reload_Data (
) :
    if (filename_data == '') : return None
    load_data(filename_data)
    action_refresh_view()



def load_image(
    filename
):
    global label_image
    global my_image
    global image_Tk
    
    print('Opening image-file "%s"...' % filename)

    try:
        my_image = PilImage.open(filename)
    except IOError as err:
        print("I/O error: {0}".format(err))
        return None
        
    my_image = my_image.resize((640,400))
    my_image = my_image.convert("RGB")
        
    action_refresh_view()
    action_show_initial_preview_window()


def make_letter(
    letter_string
):
    letter = FONT_ABC.find(letter_string)+1
    
    LETTER_WIDTH = 7
    LETTER_HEIGHT = 8
    posx, posy = letter*LETTER_WIDTH,0
    
    box = (
        int(posx),
        int(posy),
        int(posx)+LETTER_WIDTH,
        int(posy)+LETTER_HEIGHT
    )

    return font_image.crop(box)


def action_refresh_numbers():
    global numbers_image

    HEXPRE = '0123456789abcdef'

    numbers_image = PilImage.new("RGBA", (640,400), "#00000000")   #clear all numbers
    blank_image = PilImage.new("RGBA", (15,15), "#000000aa")    #dark background for number

    for y in range(0,SCREEN_HEIGHT) :
        for x in range(0,SCREEN_WIDTH) :
            value = fadedata[y*SCREEN_WIDTH+x]
            if (value > 0) :
                high = HEXPRE[ (value >> 4 ) ]      # $0x high-nibble
                low = HEXPRE[ (value & 0b1111 ) ]   # $x0 low-nibble

                numbers_image.paste(blank_image, (16*x+1,16*y+1))   # dark background for number
                
                if (high != '0') :
                    letter_image = make_letter(high)   #high-nibble
                    numbers_image.paste(letter_image, (16*x+3+0,16*y+4), letter_image.convert('1'))
                    letter_image = make_letter(low)   #low-nibble
                    numbers_image.paste(letter_image, (16*x+1+8,16*y+4), letter_image.convert('1'))
                else :
                    letter_image = make_letter(low)   #only low-nibble
                    numbers_image.paste(letter_image, (16*x-3+8,16*y+4), letter_image.convert('1'))



def action_draw_raster():
    global raster_image

    raster_image = PilImage.new("RGBA", (640,400), "#00000000")

    draw = ImageDraw.Draw(raster_image, 'RGBA')
    for i in range(0,raster_image.height,8*2) :
        draw.line((0,i,raster_image.width,i), fill="#88888888")
    for i in range(0,raster_image.width,8*2) :
        draw.line((i,0,i,raster_image.height), fill="#88888888")

    

def action_refresh_view():
    global image_Tk

    action_refresh_numbers()
    
    if (show_grid) :
        overlay_image = raster_image.copy()
    else :
        overlay_image = PilImage.new("RGBA", (640,400), "#00000000")

    if (show_values) :
        overlay_image.paste(numbers_image, numbers_image.convert('RGBA'))
    
    final_image = my_image.copy()    
    final_image.paste(overlay_image, overlay_image.convert('RGBA'))
    image_Tk = ImageTk.PhotoImage(final_image)
    label_image.configure(image=image_Tk)
    label_image.image = final_image # keep a reference!


#    update_info()

    

def action_show_initial_preview_window():
#    global image_Tk

    #prepare preview image
    preview_image = my_image.copy().resize((640,400)).convert("RGB")

    #copy to label_preview_image
    image2_koalaTk = ImageTk.PhotoImage(preview_image)
    label_preview_image.configure(image=image2_koalaTk)
    label_preview_image.image = image2_koalaTk # keep a reference!


#    update_info()






def action_Value_Increase():
    global screen_value
    if (screen_value < 255) :
        screen_value += 1
        update_info()

def action_Value_Decrease():
    global screen_value
    if (screen_value > 0) :
        screen_value -= 1
        update_info()

def action_Value_Increase_Big():
    global screen_value
    screen_value += 16
    if (screen_value > 255) : screen_value = 255
    update_info()

def action_Value_Decrease_Big():
    global screen_value
    screen_value -= 16
    if (screen_value < 0) : screen_value = 0
    update_info()






def create_gui_drop_down_menu (
	root
) :
    menu = tk.Menu(root)
    root.config(menu=menu)

    filemenu = tk.Menu(menu)
    datamenu = tk.Menu(menu)
    infomenu = tk.Menu(menu)

    filemenu.add_command(label="open background-image", command=action_Open_Image, underline=5, accelerator="Alt+B")
    filemenu.add_command(label="open data", command=action_Open_Data, underline=0, accelerator="Alt+O")
    filemenu.add_command(label="save data", command=action_Save_Data, underline=0, accelerator="Alt+S")
    filemenu.add_command(label="save data as", command=action_Save_Data_As, underline=0, accelerator="Alt+Shift+S")
    filemenu.add_separator()
    filemenu.add_command(label="quit", command=root.quit, underline=0, accelerator="Alt+Q")

    datamenu.add_command(label="reload data", command=action_Reload_Data, underline=0, accelerator="Alt-R")
    datamenu.add_separator()
    datamenu.add_command(label="clear all data", command=action_Clear_Data, underline=0, accelerator="Alt+C")

    infomenu.add_command(label="help", command=action_Show_Help, accelerator="f1")
    infomenu.add_command(label="about", command=action_Show_About, accelerator="f2")

    #add all menus
    menu.add_cascade(label="menu", menu=filemenu)
    menu.add_cascade(label="data", menu=datamenu)
    menu.add_cascade(label="info", menu=infomenu)



def waithere():
    var = tk.IntVar()
    root.after(PREVIEW_DELAY, var.set, 1)
    root.wait_variable(var)



def action_Preview_FadeOut(
):
    global preview_in_action
    
    if (preview_in_action == True) : return None
    preview_in_action = True

    button_fade_out.configure(relief=tk.SUNKEN) #button looks activated
    
    original_image = my_image.copy().resize((640,400)).convert("RGB")

    preview_image = original_image.copy()

    blank_image = PilImage.new("RGBA", (16,16), "#00000044")    #dark background for number
    
    #print('Starting preview...')
    
    for i in range(0,value_max+1+16) :
        for y in range(0,SCREEN_HEIGHT) :
            for x in range(0,SCREEN_WIDTH) :
                if (fadedata[y*SCREEN_WIDTH+x] <= i) :
                    preview_image.paste(blank_image, ( (x*16), y*16 ), blank_image.convert('RGBA') )

        #copy to label_preview_image
        image2_koalaTk = ImageTk.PhotoImage(preview_image)
        label_preview_image.configure(image=image2_koalaTk)
        label_preview_image.image = image2_koalaTk # keep a reference!
        root.update()
        #print('$%02x / $%02x'%(i,value_max))
        waithere()

    #print('done preview.')

    #action_show_initial_preview_window()
    
    preview_in_action = False
    button_fade_out.configure(relief=tk.RAISED) #button looks normally

    return None


def action_Preview_FadeIn(
):
    global preview_in_action
    
    if (preview_in_action == True) : return None
    preview_in_action = True

    button_fade_in.configure(relief=tk.SUNKEN) #button looks activated
    
    original_image = my_image.copy().resize((640,400)).convert("RGB")

    preview_image = PilImage.new("RGB", (640,400), "#000000")
    alpha_image = PilImage.new("RGBA", (16,16), "#00000044")

    #print('Starting preview...')
    
    for i in range(0,value_max+1+16) :
        for y in range(0,SCREEN_HEIGHT) :
            for x in range(0,SCREEN_WIDTH) :
                if (fadedata[y*SCREEN_WIDTH+x] <= i) :
                    tmp_image = original_image.crop((
                        x*16,
                        y*16,
                        (x+1)*16,
                        (y+1)*16
                    ))
                    #preview_image.paste(tmp_image, ( (x*16), y*16 ), tmp_image.convert('RGBA') )
                    preview_image.paste(tmp_image, ( x*16, y*16 ), alpha_image )

        #copy to label_preview_image
        image2_koalaTk = ImageTk.PhotoImage(preview_image)
        label_preview_image.configure(image=image2_koalaTk)
        label_preview_image.image = image2_koalaTk # keep a reference!
        root.update()
        #print('$%02x / $%02x'%(i,value_max))
        waithere()

    #print('done preview.')

    #action_show_initial_preview_window()
    
    preview_in_action = False

    button_fade_in.configure(relief=tk.RAISED) #button looks normally

    return None



def action_Open_Data():
    global fadedata, filename_data
    
    ftypes = [('Fademaid Files', '*.bin *.fade')]
    user_filename_open = filedialog.askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    filename_data = user_filename_open
    textvariable_filename_data.set("\"..."+user_filename_open[-30:]+"\"")
    load_data(user_filename_open)
    action_refresh_view()
    return None

    
def action_Save_Data():
    save_data(filename_data, fadedata)
    return None

    
def action_Save_Data_As():
    global filename_data
    
    ftypes = [('Data Files', '*.bin *.fade')]
    user_filename_save = filedialog.asksaveasfilename(filetypes = ftypes)
    if not user_filename_save : return None
    filename_data = user_filename_save
    textvariable_filename_data.set("\"..."+user_filename_save[-30:]+"\"")
    save_data(user_filename_save, fadedata)
    
def action_Open_Image():
    global filename_image
    
    ftypes = [('Image Files', '*.tif *.jpg *.png *.bmp *.gif')]
    user_filename_open = filedialog.askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    filename_image = user_filename_open
    textvariable_filename_image.set("\"..."+user_filename_open[-30:]+"\"")
    load_image(user_filename_open)



def action_Toggle_AutoMode():
    global auto_mode

    if (auto_mode == True) :
        auto_mode = False
        button_toggle_automode.configure(relief=tk.RAISED) #button looks normally
    else :
        auto_mode = True
        button_toggle_automode.configure(relief=tk.SUNKEN) #button looks activated
    

def action_Toggle_Grid():
    global show_grid

    if (show_grid == True) :
        show_grid = False
        button_toggle_grid.configure(relief=tk.RAISED) #button looks normally
    else :
        show_grid = True
        button_toggle_grid.configure(relief=tk.SUNKEN) #button looks activated
    
    action_refresh_view()
    

def action_Toggle_Values():
    global show_values
    
    if (show_values == True) :
        show_values = False
        button_toggle_values.configure(relief=tk.RAISED) #button looks normally
    else :
        show_values = True
        button_toggle_values.configure(relief=tk.SUNKEN) #button looks activated
    
    action_refresh_view()

        



def action_Clear_Data():
    global fadedata
    for i in range(0,SCREEN_HEIGHT*SCREEN_WIDTH) :
        fadedata[i] = 0
    update_info()
    action_refresh_view()

def mouseButton1(event):
    #left mouse button
    global fadedata, mouse_posx, mouse_posy, last_screenx, last_screeny

    mouse_posx = event.x
    mouse_posy = event.y
    update_info()
    
    if (
        (last_screenx == screenx) &
        (last_screeny == screeny)
    ) :
        return None
        
    last_screenx = screenx
    last_screeny = screeny

    fadedata[screeny*SCREEN_WIDTH+screenx] = screen_value
    if (auto_mode) : action_Value_Increase()
    action_refresh_view()



def mouseButton3(event):
    #right mouse button
    global fadedata, mouse_posx, mouse_posy, last_screenx, last_screeny
        
    mouse_posx = event.x
    mouse_posy = event.y
    update_info()

    if (
        (last_screenx == screenx) &
        (last_screeny == screeny)
    ) :
        return None
        
    last_screenx = screenx
    last_screeny = screeny

    if (auto_mode) :
        fadedata[screeny*SCREEN_WIDTH+screenx] = screen_value
        action_Value_Decrease()
    else :
        fadedata[screeny*SCREEN_WIDTH+screenx] = 0

    action_refresh_view()



def update_info():
    global screenx, screeny, value_max
    
    tmp_posx = int(mouse_posx/2)
    if (tmp_posx > 319) : tmp_posx = 319
    tmp_posy = int(mouse_posy/2)
    if (tmp_posy > 199) : tmp_posy = 199
    
    screenx = int(tmp_posx/8)
    screeny = int(tmp_posy/8)
    
    value_max = max(fadedata)

    textvariable_coords.set('x=%03d y=%03d | x=$%04x y=$%02x' % (
        tmp_posx, tmp_posy,
        tmp_posx, tmp_posy
    ))

    textvariable_pos.set('col=%02d row=%02d | col=$%02x row=$%02x' % (
        screenx, screeny,
        screenx, screeny
    ))

    textvariable_value.set('%03d | $%02x' % (
        screen_value, screen_value
    ))

    textvariable_max.set('%03d | $%02x' % (
        value_max, value_max
    ))



def mouseMotion(event):
    global mouse_posx, mouse_posy
    mouse_posx = event.x
    mouse_posy = event.y
    update_info()



def create_gui_image (
	root,
    _row,
    _column
) :
    global label_image
    
    frame_border = tk.Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    
    label_image = tk.Label(
        frame_border,
        bg=BGCOLOR,
        cursor=cursor_image
    )
    label_image.grid(
        row=0,
        column=0,
        sticky= tk.W+ tk.E
    )
    
    label_image.bind('<Motion>', mouseMotion)
    label_image.bind('<Button-1>', mouseButton1)
    label_image.bind('<Button-3>', mouseButton3)
    label_image.bind('<B1-Motion>', mouseButton1)
    label_image.bind('<B3-Motion>', mouseButton3)



def create_gui_logo (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bd=_bd,
        bg=BGCOLOR
    )
    frame_border.grid(
        row=_row,
        column=_column
    )

    photo = tk.PhotoImage(file=RES_GFX_AC)
    label_logo = tk.Label(frame_border, image = photo)
    label_logo.image = photo # keep a reference!
    label_logo.grid( row=0, column=0)
    label_logo.configure(background=BGCOLOR)





def create_gui_infobox (
    root,
    my_row,
    my_column,
    my_text,
    my_textvariable,
    my_width
) :
    frame_border = tk.Frame(
        root,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady
        )

    frame_inner = tk.Frame(
        frame_border,
        bg=BGCOLOR_LIGHT,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief= tk.RAISED
        )

    label_info = tk.Label(
		frame_inner,
        bg=BGCOLOR2,
		text = my_text,
        bd=1
	)

    label_content = tk.Label(
		frame_inner,
        bg=BGCOLOR_LIGHT,
		textvariable = my_textvariable,
        bd=1,
        width=my_width,
	)


    # layout
    frame_border.grid(
        row=my_row,
        column=my_column,
        sticky= tk.W,
    )

    frame_inner.grid(
        row=0,
        column=0,
        sticky= tk.W,
    )

    label_info.grid(
        row=0,
        column=0,
        sticky= tk.W,
    )

    label_content.grid(
        row=0,
        column=1,
        sticky= tk.W,
    )



def create_gui_info (
	root,
    _row,
    _column
) :    
    frame_border = tk.Frame(
        root,
        bd=1,
        bg=BGCOLOR,
    )
    frame_border.grid(
        row=_row,
        column=_column,
        sticky= tk.W+ tk.E
    )
    frame_border.grid_columnconfigure(0, weight=1)
    frame_border.grid_rowconfigure(0, weight=1)

    frame_left = tk.Frame(
        frame_border,
        bd=1,
        bg=BGCOLOR,
    )
    frame_left.grid(
        row=0,
        column=0,
        sticky= tk.W
    )
    frame_left.grid_columnconfigure(0, weight=1)
    frame_left.grid_rowconfigure(0, weight=1)


    frame_right = tk.Frame(
        frame_border,
        bd=1,
        bg=BGCOLOR,
    )
    frame_right.grid(
        row=0,
        column=1,
        sticky= tk.W
    )
    frame_right.grid_columnconfigure(0, weight=1)
    frame_right.grid_rowconfigure(0, weight=1)

    create_gui_infobox (
        frame_left,   #root frame
        0,  #row
        0,  #column
        'value:',    #text
        textvariable_value,   #textvariable
        10   #text width
    )


    create_gui_infobox (
        frame_right,   #root frame
        0,  #row
        0,  #column
        'coords:',    #text
        textvariable_coords,   #textvariable
        30   #text width
    )

    create_gui_infobox (
        frame_left,   #root frame
        1,  #row
        0,  #column
        'max:',    #text
        textvariable_max,   #textvariable
        10   #text width
    )

    create_gui_infobox (
        frame_right,   #root frame
        1,  #row
        0,  #column
        'char:',    #text
        textvariable_pos,   #textvariable
        30   #text width
    )


    create_gui_infobox (
        frame_left,   #root frame
        2,  #row
        0,  #column
        'data:',    #text
        textvariable_filename_data,   #textvariable
        30   #text width
    )

    create_gui_infobox (
        frame_right,   #root frame
        2,  #row
        0,  #column
        'image:',    #text
        textvariable_filename_image,   #textvariable
        30   #text width
    )






def create_gui_control (
	root,
    _row,
    _column
) :
    global button_toggle_automode, button_toggle_grid, button_toggle_values, button_fade_in, button_fade_out
    
    frame_border = tk.Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column,
        sticky= tk.W
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=BGCOLOR_LIGHT,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief= tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
 
    button_fade_in = tk.Button(
        frame_inner,
        bg=BGCOLOR,
        text = "fade in",
        command=action_Preview_FadeIn,
        cursor=CURSOR_HAND,
    )
    button_fade_in.grid(
        row=0,
        column=0,
        sticky="w"
    )
 
    button_fade_out = tk.Button(
        frame_inner,
        bg=BGCOLOR,
        text = "fade out",
        command=action_Preview_FadeOut,
        cursor=CURSOR_HAND,
    )
    button_fade_out.grid(
        row=0,
        column=1,
        sticky="w"
    )

 
    button_toggle_automode = tk.Button(
        frame_inner,
        bg=BGCOLOR,
        text = "auto-mode",
        command=action_Toggle_AutoMode,
        cursor=CURSOR_HAND,
    )
    button_toggle_automode.grid(
        row=0,
        column=2,
        sticky="w"
    )

 
    button_toggle_grid = tk.Button(
        frame_inner,
        bg=BGCOLOR,
        text = "show grid",
        command=action_Toggle_Grid,
        cursor=CURSOR_HAND,
        relief=tk.SUNKEN,
    )
    button_toggle_grid.grid(
        row=0,
        column=3,
        sticky="w"
    )
 
 
    button_toggle_values = tk.Button(
        frame_inner,
        bg=BGCOLOR,
        text = "show values",
        command=action_Toggle_Values,
        cursor=CURSOR_HAND,
        relief=tk.SUNKEN,
    )
    button_toggle_values.grid(
        row=0,
        column=4,
        sticky="w"
    )
 

def action_reset_settings():
    global scale_settings_list
    for a in range(0,len(scale_settings_list)):
        scale_settings_list[a].set( scale_settings_list_default[a])






   
def action_Show_Help (
) :
    TEXT_HEIGHT=20
    TEXT_WIDTH=40

    def keyboard_up():
        msg.yview_scroll(-1,"units")

    def keyboard_down():
        msg.yview_scroll(1,"units")

    def keyboard_pageup():
        msg.yview_scroll(TEXT_HEIGHT,"units")

    def keyboard_pagedown():
        msg.yview_scroll(TEXT_HEIGHT*-1,"units")


    _padx = 10
    _pady = 10
    
	#http://effbot.org/tkinterbook/toplevel.htm
    info_window = tk.Toplevel(
        bd=10
    )
    info_window.title("Help")
    info_window.iconphoto(False, tk.PhotoImage(file=RES_GFX_ICON))
    info_window.configure(background=BGCOLOR)

    frame_left = tk.Frame( info_window)
    frame_right = tk.Frame( info_window)

    #http://effbot.org/tkinterbook/message.htm
    #text
    msg = tk.Text(
        frame_right,
#        bd=10,
        relief=tk.FLAT,
        width=TEXT_WIDTH,
        height=TEXT_HEIGHT
    )

    #scrollbar
    msg_scrollBar = tk.Scrollbar(
        frame_right,
        bg=BGCOLOR
    )
    msg_scrollBar.config(command=msg.yview)
    msg.insert(tk.END, open(RES_DOC_HELP, encoding="utf_8").read())
    msg.config(yscrollcommand=msg_scrollBar.set)
    msg.config(state=tk.DISABLED)


    #button
    button = tk.Button(
        frame_left,
        bg=BGCOLOR,
        text="OK",
        command=info_window.destroy,
        padx=_padx,
        pady=_pady
    )

    #placement in grid
    frame_left.grid(
        row=0,
        column=0,
        sticky= tk.W
    )
    frame_right.grid(
        row=0,
        column=1,
        sticky= tk.W
    )
    
    label_image.grid(
        row=0,
        column=0,
        sticky= tk.W
    )
    button.grid(
        row=1,
        column=0,
        sticky= tk.W+ tk.E
    )

    msg.grid(
        row=0,
        column=0,
        sticky= tk.W
    )
    msg_scrollBar.grid(
        row=0,
        column=1,
        sticky= tk.N+ tk.S
    )

    #https://www.pythontutorial.net/tkinter/tkinter-event-binding/
    info_window.bind('<Up>', lambda event: keyboard_up())
    info_window.bind('<Down>', lambda event: keyboard_down()) 
    info_window.bind('<Next>', lambda event: keyboard_pageup()) 
    info_window.bind('<Prior>', lambda event: keyboard_pagedown()) 



   
def action_Show_About (
) :
    TEXT_HEIGHT=40
    TEXT_WIDTH=80


    def keyboard_up():
        msg.yview_scroll(-1,"units")

    def keyboard_down():
        msg.yview_scroll(1,"units")

    def keyboard_pageup():
        msg.yview_scroll(TEXT_HEIGHT,"units")

    def keyboard_pagedown():
        msg.yview_scroll(TEXT_HEIGHT*-1,"units")


    _padx = 10
    _pady = 10
    
	#http://effbot.org/tkinterbook/toplevel.htm
    info_window = tk.Toplevel(
        bd=10
    )
    info_window.title("About")
    info_window.iconphoto(False, tk.PhotoImage(file=RES_GFX_ICON))
    info_window.configure(background=BGCOLOR)

    frame_left = tk.Frame( info_window)
    frame_right = tk.Frame( info_window)

    #http://effbot.org/tkinterbook/message.htm
    #text
    msg = tk.Text(
        frame_right,
#        bd=10,
        relief=tk.FLAT,
        width=TEXT_WIDTH,
        height=TEXT_HEIGHT
    )

    #scrollbar
    msg_scrollBar = tk.Scrollbar(
        frame_right,
        bg=BGCOLOR
    )
    msg_scrollBar.config(command=msg.yview)
    msg.insert(tk.END, open(RES_DOC_ABOUT, encoding="utf_8").read())
    msg.config(yscrollcommand=msg_scrollBar.set)
    msg.config(state=tk.DISABLED)


    #button
    button = tk.Button(
        frame_left,
        bg=BGCOLOR,
        text="OK",
        command=info_window.destroy,
        padx=_padx,
        pady=_pady
    )
    
    #placement in grid
    frame_left.grid(
        row=0,
        column=0,
        sticky= tk.W
    )
    frame_right.grid(
        row=0,
        column=1,
        sticky= tk.W
    )
    
    label_image.grid(
        row=0,
        column=0,
        sticky= tk.W
    )
    button.grid(
        row=1,
        column=0,
        sticky= tk.W+ tk.E
    )

    msg.grid(
        row=0,
        column=0,
        sticky= tk.W
    )
    msg_scrollBar.grid(
        row=0,
        column=1,
        sticky= tk.N+ tk.S
    )

    #https://www.pythontutorial.net/tkinter/tkinter-event-binding/
    info_window.bind('<Up>', lambda event: keyboard_up())
    info_window.bind('<Down>', lambda event: keyboard_down()) 
    info_window.bind('<Next>', lambda event: keyboard_pageup()) 
    info_window.bind('<Prior>', lambda event: keyboard_pagedown()) 





def create_gui_preview(
) :
    @staticmethod
    def __callback():
        return

    global label_preview_image
    
    preview_window = tk.Toplevel(bd=10)
    preview_window.title("preview")
    preview_window.iconphoto(False, tk.PhotoImage(file=RES_GFX_ICON))
    preview_window.protocol("WM_DELETE_WINDOW", __callback)
    preview_window.resizable(0, 0)
#    preview_window.configure(background=BGCOLOR)


    label_preview_image = tk.Label(
        preview_window,
        bg=BGCOLOR
    )

    label_preview_image.grid(
        row=0,
        column=0,
        sticky= tk.W+ tk.E
    )

	
        
def create_gui_base(
):
    root.configure(
        background=BGCOLOR
    )
    create_gui_logo(
        root,
        0,  #row
        0   #column
    )

    create_gui_info(
        root,
        1,  #row
        0   #column
    )



    create_gui_control (
        root,   #root frame
        2,  #row
        0  #column
    )

    create_gui_image(
        root,
        3,  #row
        0   #column
    )



    


def _main_procedure() :

    global args
    global filename_image, filename_data
    global font_image, logo_image

    #global textvariable_filename_data, textvariable_filename_image
    
    textvariable_filename_data.set('None')
    textvariable_filename_image.set('none')

    print("%s %s *** by WolF"% (PROGNAME, VERSION))

    #https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        description='You can edit char-wise values with this.',
        epilog='Example: ./fademaid.py -i image.png -d data.bin'
    )
    parser.add_argument('-i', '--image_file', dest='image_file', help='background image filename')
    parser.add_argument('-d', '--data_file', dest='data_file', help='fademaid data filename')
    args = parser.parse_args()

            
    #main procedure
    title_string = PROGNAME+" "+VERSION+" *** by fieserWolF"
    root.title(title_string)
    root.iconphoto(False, tk.PhotoImage(file=RES_GFX_ICON))
    create_gui_drop_down_menu(root)
    create_gui_base()
    create_gui_preview()


    #https://www.pythontutorial.net/tkinter/tkinter-event-binding/
    root.bind_all("<Alt-q>", lambda event: root.quit())
    root.bind_all("<Control-q>", lambda event: root.quit())
    root.bind_all("<Alt-b>", lambda event: action_Open_Image())
    root.bind_all("<Control-b>", lambda event: action_Open_Image())
    root.bind_all("<Alt-o>", lambda event: action_Open_Data())
    root.bind_all("<Control-o>", lambda event: action_Open_Data())
    root.bind_all("<Alt-s>", lambda event: action_Save_Data())
    root.bind_all("<Control-s>", lambda event: action_Save_Data())
    root.bind_all("<Alt-S>", lambda event: action_Save_Data_As())
    root.bind_all("<Control-S>", lambda event: action_Save_Data_As())
    root.bind_all("<Alt-c>", lambda event: action_Clear_Data())
    root.bind_all("<Control-c>", lambda event: action_Clear_Data())
    root.bind_all("<Alt-r>", lambda event: action_Reload_Data())
    root.bind_all("<Control-r>", lambda event: action_Reload_Data())
    root.bind_all("<F1>", lambda event: action_Show_Help())
    root.bind_all("<F2>", lambda event: action_Show_About())
    root.bind_all("a", lambda event: action_Toggle_AutoMode())
    root.bind_all("g", lambda event: action_Toggle_Grid())
    root.bind_all("v", lambda event: action_Toggle_Values())
    root.bind_all("<Up>", lambda event: action_Value_Increase())
    root.bind_all("<Down>", lambda event: action_Value_Decrease())
    root.bind_all("<Right>", lambda event: action_Value_Increase_Big())
    root.bind_all("<Left>", lambda event: action_Value_Decrease_Big())
    root.bind_all("<Return>", lambda event: action_Preview_FadeOut())
    root.bind_all("<space>", lambda event: action_Preview_FadeIn())

#    print('Opening font-image-file "%s"...' % RES_GFX_FONT)
    font_image = PilImage.open(RES_GFX_FONT)


    action_draw_raster()

    if (args.data_file) :
        filename_data = args.data_file
        textvariable_filename_data.set("\"..."+filename_data[-30:]+"\"")
        load_data(filename_data)

    if (args.image_file) :
        filename_image = args.image_file
        textvariable_filename_image.set("\"..."+filename_image[-30:]+"\"")
        load_image(filename_image)

    update_info()

    action_refresh_view()
    
    action_show_initial_preview_window()

    tk.mainloop()
    



if __name__ == '__main__':
    _main_procedure()
