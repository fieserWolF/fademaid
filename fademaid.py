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
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
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

        
root = Tk()

cursor_image_normal = 'tcross'
cursor_image = cursor_image_normal
cursor_image_none = 'X_cursor'

textvariable_coords = StringVar()   #position on screen (320x200)
textvariable_pos   = StringVar()    #position on char-screen (40x25)
textvariable_value   = StringVar()  #value
textvariable_filename_data   = StringVar()
textvariable_filename_image   = StringVar()
textvariable_max   = StringVar()

my_image = PilImage.new("RGB", (640, 400), "black")
image_Tk = ImageTk.PhotoImage(my_image)
label_image = Label()
label_preview_image = Label()

raster_image = PilImage.new("RGBA", (640, 400), "black")
numbers_image = PilImage.new("RGBA", (640, 400), "black")
overlay_image = PilImage.new("RGBA", (640, 400), "black")
font_image = PilImage.new("RGBA", (10, 10), "black")
logo_image = PilImage.new("RGBA", (609, 79), "black")

fadedata = SCREEN_HEIGHT*SCREEN_WIDTH*[0]

args = None

screenx = 0
screeny = 0
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


def save_data(
    filename,
    data
):
    print ("Opening file \"%s\" for writing data (%d ($%04x) bytes)..." % (filename, len(data), len(data)))
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

    return buffer



def reload_data (
) :
    global fadedata
    
    if (filename_data == '') : return None
    
    fadedata = load_data(filename_data)
    
    action_refresh_view()
    return None


    


def load_image(
    filename
):
    global label_image
    global my_image
    global image_Tk
    
    print('Opening image-file "%s"...' % filename)

    my_image = PilImage.open(filename)
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
                    numbers_image.paste(letter_image, (16*x+2+0,16*y+4), letter_image.convert('1'))
                letter_image = make_letter(low)   #low-nibble
                numbers_image.paste(letter_image, (16*x+2+8,16*y+4), letter_image.convert('1'))



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





#keyboard shortcuts
def keyboard_quit(self):
    root.quit()    
def keyboard_Open_Image(self):
    action_Open_Image()
def keyboard_Open_Data(self):
    action_Open_Data()
def keyboard_Save_Data(self):
    action_SaveData()
def keyboard_Clear_Data(self):
    action_ClearData()
def keyboard_Reload_Data(self):
    reload_data()
def keyboard_Help(self):
    action_Info()
def keyboard_Preview_FadeOut(self):
    action_Preview_FadeOut()
def keyboard_Preview_FadeIn(self):
    action_Preview_FadeIn()
def keyboard_Grid_Toggle(self):
    action_Toggle_Grid()
def keyboard_Values_Toggle(self):
    action_Toggle_Values()


def keyboard_Value_Increase(self):
    global screen_value
    if (screen_value < 256) :
        screen_value += 1
        update_info()

def keyboard_Value_Decrease(self):
    global screen_value
    if (screen_value > 0) :
        screen_value -= 1
        update_info()

def keyboard_Value_Increase_Big(self):
    global screen_value
    screen_value += 16
    if (screen_value > 255) : screen_value = 255
    update_info()

def keyboard_Value_Decrease_Big(self):
    global screen_value
    screen_value -= 16
    if (screen_value < 0) : screen_value = 0
    update_info()


def create_gui_drop_down_menu (
	root
) :
    menu = Menu(root)
    root.config(menu=menu)

    filemenu = Menu(menu)
    viewmenu = Menu(menu)
    datamenu = Menu(menu)
    infomenu = Menu(menu)

    filemenu.add_command(label="open background-image", command=action_Open_Image, underline=5, accelerator="Alt+B")
    filemenu.add_command(label="open data", command=action_Open_Data, underline=0, accelerator="Alt+O")
    filemenu.add_command(label="save data", command=action_SaveData, underline=0, accelerator="Alt+S")
    filemenu.add_separator()
    filemenu.add_command(label="quit", command=root.quit, underline=0, accelerator="Alt+Q")

    viewmenu.add_command(label="toggle grid", command=action_Toggle_Grid, underline=7, accelerator="g")
    viewmenu.add_command(label="toggle view", command=action_Toggle_Values, underline=7, accelerator="v")

    datamenu.add_command(label="reload data", command=reload_data, underline=0, accelerator="Alt-R")
    datamenu.add_separator()
    datamenu.add_command(label="clear all data", command=action_ClearData, underline=0, accelerator="Alt+C")

    infomenu.add_command(label="help", command=action_Info, accelerator="f1")

    #add all menus
    menu.add_cascade(label="menu", menu=filemenu)
    menu.add_cascade(label="view", menu=viewmenu)
    menu.add_cascade(label="data", menu=datamenu)
    menu.add_cascade(label="info", menu=infomenu)



def waithere():
    var = IntVar()
    root.after(PREVIEW_DELAY, var.set, 1)
    root.wait_variable(var)



def action_Preview_FadeOut(
):
    global preview_in_action
    
    if (preview_in_action == True) : return None
    preview_in_action = True
    
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

    return None


def action_Preview_FadeIn(
):
    global preview_in_action
    
    if (preview_in_action == True) : return None
    preview_in_action = True

    
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

    return None



def action_Open_Data():
    global fadedata, filename_data
    
    ftypes = [('Fademaid Files', '*.bin *.fade')]
    user_filename_open = askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    filename_data = user_filename_open
    textvariable_filename_data.set("\"..."+user_filename_open[-30:]+"\"")
    fadedata = load_data(user_filename_open)
    action_refresh_view()
    return None

    
def action_SaveData():
    save_data(filename_data, fadedata)
    return None
    
def action_Open_Image():
    global filename_image
    
    ftypes = [('Image Files', '*.tif *.jpg *.png *.bmp *.gif')]
    user_filename_open = askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    filename_image = user_filename_open
    textvariable_filename_image.set("\"..."+user_filename_open[-30:]+"\"")
    load_image(user_filename_open)

def action_Toggle_Grid():
    global show_grid

    if (show_grid == True) :
        show_grid = False
    else :
        show_grid = True
    
    action_refresh_view()
    

def action_Toggle_Values():
    global show_values
    
    if (show_values == True) :
        show_values = False
    else :
        show_values = True
    
    action_refresh_view()

        



def action_ClearData():
    global fadedata
    for i in range(0,SCREEN_HEIGHT*SCREEN_WIDTH) :
        fadedata[i] = 0
    action_refresh_view()

def mouseButton1(event):
    #left mouse button
    global fadedata, mouse_posx, mouse_posy
        
    mouse_posx = event.x
    mouse_posy = event.y
    update_info()

    fadedata[screeny*SCREEN_WIDTH+screenx] = screen_value
    action_refresh_view()



def mouseButton3(event):
    #right mouse button
    global fadedata, mouse_posx, mouse_posy
        
    mouse_posx = event.x
    mouse_posy = event.y
    update_info()

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
    
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    
    label_image = Label(
        frame_border,
        bg=BGCOLOR,
        cursor=cursor_image
    )
    label_image.grid(
        row=0,
        column=0,
        sticky=W+E
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
    frame_border = Frame(
        root,
        bd=_bd,
        bg=BGCOLOR
    )
    frame_border.grid(
        row=_row,
        column=_column
    )

    photo = PhotoImage(file=RES_GFX_AC)
    label_logo = Label(frame_border, image = photo)
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
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady
        )

    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR_LIGHT,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )

    label_info = Label(
		frame_inner,
        bg=BGCOLOR2,
		text = my_text,
        bd=1
	)

    label_content = Label(
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
        sticky=W,
    )

    frame_inner.grid(
        row=0,
        column=0,
        sticky=W,
    )

    label_info.grid(
        row=0,
        column=0,
        sticky=W,
    )

    label_content.grid(
        row=0,
        column=1,
        sticky=W,
    )



def create_gui_main (
	root,
    _row,
    _column
) :    
    frame_border = Frame(
        root,
        bd=1,
        bg=BGCOLOR,
    )
    frame_border.grid(
        row=_row,
        column=_column,
        sticky=W+E
    )
    frame_border.grid_columnconfigure(0, weight=1)
    frame_border.grid_rowconfigure(0, weight=1)

    frame_left = Frame(
        frame_border,
        bd=1,
        bg=BGCOLOR,
    )
    frame_left.grid(
        row=0,
        column=0,
        sticky=W
    )
    frame_left.grid_columnconfigure(0, weight=1)
    frame_left.grid_rowconfigure(0, weight=1)


    frame_right = Frame(
        frame_border,
        bd=1,
        bg=BGCOLOR,
    )
    frame_right.grid(
        row=0,
        column=1,
        sticky=W
    )
    frame_right.grid_columnconfigure(0, weight=1)
    frame_right.grid_rowconfigure(0, weight=1)

    create_gui_infobox (
        frame_left,   #root frame
        0,  #row
        0,  #column
        'coords:',    #text
        textvariable_coords,   #textvariable
        30   #text width
    )

    create_gui_infobox (
        frame_right,   #root frame
        0,  #row
        0,  #column
        'value:',    #text
        textvariable_value,   #textvariable
        10   #text width
    )

    create_gui_infobox (
        frame_left,   #root frame
        1,  #row
        0,  #column
        'char:',    #text
        textvariable_pos,   #textvariable
        30   #text width
    )

    create_gui_infobox (
        frame_right,   #root frame
        1,  #row
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

    create_gui_infobox (
        frame_left,   #root frame
        2,  #row
        0,  #column
        'max:',    #text
        textvariable_max,   #textvariable
        10   #text width
    )



    create_gui_settings (
        frame_right,   #root frame
        2,  #row
        0  #column
    )




def create_gui_settings (
	root,
    _row,
    _column
) :
    global scale_settings_list, scale_settings_list_default

    return None
    
#scales modifiers
    frame_border = Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column,
        sticky=W
    )
    frame_inner = Frame(
        frame_border,
        bg=BGCOLOR_LIGHT,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row=0
    label = Label(
        frame_inner,
        bg=BGCOLOR_LIGHT,
        text="settings",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=0,
        sticky=W
    )

    SETTINGS = [
        #text, variable, row, column, low, high
        ("player slow down", player_speed, 1,0, 1,10),
    ]

    scale_settings_list=[]
    scale_settings_list_default=[]
    for text, var, my_row, my_column, low, high in SETTINGS:
        scale_settings = Scale(
            frame_inner,
            bg=BGCOLOR_LIGHT,
            from_=low,
            to=high,
            orient=HORIZONTAL,
            variable=var,
            label=text,
            length=200,
            cursor=CURSOR_HAND,
            #command=action_preview_scale
        )
        scale_settings.grid(
            row=my_row,
            column=my_column,
            sticky='w'
        )
        #set default value
        scale_settings.set(high/2)
        scale_settings_list.append(scale_settings)
        scale_settings_list_default.append(high/2)
        
#        last_row = my_row
 
    button_reset = Button(
        frame_inner,
        bg=BGCOLOR,
        text = "reset",
        command=action_reset_settings,
        cursor=CURSOR_HAND,
    )
    button_reset.grid(
        row=my_row+1,
        column=0,
        sticky="w"
    )
 

def action_reset_settings():
    global scale_settings_list
    for a in range(0,len(scale_settings_list)):
        scale_settings_list[a].set( scale_settings_list_default[a])






   
def action_Info (
) :
    root.bind_all("<Alt-q>", keyboard_quit)
    root.bind_all("<Alt-b>", keyboard_Open_Image)
    root.bind_all("<Alt-o>", keyboard_Open_Data)
    root.bind_all("<Alt-s>", keyboard_Save_Data)
    root.bind_all("<Alt-c>", keyboard_Clear_Data)
    root.bind_all("<Alt-r>", keyboard_Reload_Data)
    root.bind_all("<F1>", keyboard_Help)
    root.bind_all("<Up>", keyboard_Value_Increase)
    root.bind_all("<Down>", keyboard_Value_Decrease)
    root.bind_all("<Right>", keyboard_Value_Increase_Big)
    root.bind_all("<Left>", keyboard_Value_Decrease_Big)

    TEXT_HEIGHT=20
    TEXT_WIDTH=40

    def close_window():
        global info_window
        global info_window_open
        
        if (info_window_open == True) :
            info_window.destroy()
            info_window_open = False

    def close_window_key(self):
        close_window()

    def keyboard_up(event):
        msg.yview_scroll(-1,"units")

    def keyboard_down(event):
        msg.yview_scroll(1,"units")

    def keyboard_pageup(event):
        msg.yview_scroll(TEXT_HEIGHT,"units")

    def keyboard_pagedown(event):
        msg.yview_scroll(TEXT_HEIGHT*-1,"units")


    _padx = 10
    _pady = 10
    
	#http://effbot.org/tkinterbook/toplevel.htm
    info_window = Toplevel(
        bd=10
    )
    info_window.title("Help")
    info_window.configure(background=BGCOLOR)

    frame_left = Frame( info_window)
    frame_right = Frame( info_window)

    #http://effbot.org/tkinterbook/message.htm
    #text
    msg = Text(
        frame_right,
#        bd=10,
        relief=FLAT,
        width=TEXT_WIDTH,
        height=TEXT_HEIGHT
    )

    #scrollbar
    msg_scrollBar = Scrollbar(
        frame_right,
        bg=BGCOLOR
    )
    msg_scrollBar.config(command=msg.yview)
    msg.insert(END, open(RES_DOC_HELP, encoding="utf_8").read())
    msg.config(yscrollcommand=msg_scrollBar.set)
    msg.config(state=DISABLED)


    #button
    button = Button(
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
        sticky=W
    )
    frame_right.grid(
        row=0,
        column=1,
        sticky=W
    )
    
    label_image.grid(
        row=0,
        column=0,
        sticky=W
    )
    button.grid(
        row=1,
        column=0,
        sticky=W+E
    )

    msg.grid(
        row=0,
        column=0,
        sticky=W
    )
    msg_scrollBar.grid(
        row=0,
        column=1,
        sticky=N+S
    )

    #https://www.pythontutorial.net/tkinter/tkinter-event-binding/
    info_window.bind('<Up>', keyboard_up) 
    info_window.bind('<Down>', keyboard_down) 
    info_window.bind('<Next>', keyboard_pageup) 
    info_window.bind('<Prior>', keyboard_pagedown) 


def create_gui_preview(
) :
    global label_preview_image
#    global preview_window
#    global preview_window_open
    
    preview_window = Toplevel(bd=10)
    preview_window.title("preview")
#    preview_window.protocol("WM_DELETE_WINDOW", close_window)
#    preview_window.iconphoto(False, tk.PhotoImage(file=RES_GFX_ICON))
#    preview_window.configure(background=BGCOLOR)
    preview_window.resizable(0, 0)


    label_preview_image = Label(
        preview_window,
        bg=BGCOLOR
    )

    label_preview_image.grid(
        row=0,
        column=0,
        sticky=W+E
    )

#    label_preview_image.bind('<Button-1>', input_mouse_left_button_preview)
            
#    action_image_refresh_show()

	
        
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

    create_gui_main(
        root,
        1,  #row
        0   #column
    )

    create_gui_image(
        root,
        2,  #row
        0   #column
    )



    


def _main_procedure() :

    global args, fadedata
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
    create_gui_drop_down_menu(root)
    create_gui_base()
    create_gui_preview()



    #https://www.pythontutorial.net/tkinter/tkinter-event-binding/
    root.bind_all("<Alt-q>", keyboard_quit)
    root.bind_all("<Control-q>", keyboard_quit)
    root.bind_all("<Alt-b>", keyboard_Open_Image)
    root.bind_all("<Control-b>", keyboard_Open_Image)
    root.bind_all("<Alt-o>", keyboard_Open_Data)
    root.bind_all("<Control-o>", keyboard_Open_Data)
    root.bind_all("<Alt-s>", keyboard_Save_Data)
    root.bind_all("<Control-s>", keyboard_Save_Data)
    root.bind_all("<Alt-c>", keyboard_Clear_Data)
    root.bind_all("<Control-c>", keyboard_Clear_Data)
    root.bind_all("<Alt-r>", keyboard_Reload_Data)
    root.bind_all("<Control-r>", keyboard_Reload_Data)
    root.bind_all("<F1>", keyboard_Help)
    root.bind_all("g", keyboard_Grid_Toggle)
    root.bind_all("v", keyboard_Values_Toggle)
    root.bind_all("<Up>", keyboard_Value_Increase)
    root.bind_all("<Down>", keyboard_Value_Decrease)
    root.bind_all("<Right>", keyboard_Value_Increase_Big)
    root.bind_all("<Left>", keyboard_Value_Decrease_Big)
    root.bind_all("<Return>", keyboard_Preview_FadeOut)
    root.bind_all("<space>", keyboard_Preview_FadeIn)

#    print('Opening font-image-file "%s"...' % RES_GFX_FONT)
    font_image = PilImage.open(RES_GFX_FONT)


    action_draw_raster()

    if (args.data_file) :
        filename_data = args.data_file
        textvariable_filename_data.set("\"..."+filename_data[-30:]+"\"")
        fadedata = load_data(filename_data)

    if (args.image_file) :
        filename_image = args.image_file
        textvariable_filename_image.set("\"..."+filename_image[-30:]+"\"")
        load_image(filename_image)

    update_info()

    action_refresh_view()
    
    action_show_initial_preview_window()

    mainloop()
    



if __name__ == '__main__':
    _main_procedure()
