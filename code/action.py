import code.myGlobals as myGlobals
import code.main as main
import os
import struct
import tkinter as tk
import json

from PIL import ImageTk, ImageDraw
import PIL.Image as PilImage    #we need another name, as it collides with tkinter.Image otherwise
import tkinter.filedialog as filedialog



def save_data_real(
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

    myGlobals.fadedata = buffer



def reload_data (
) :
    if (myGlobals.filename_data == '') : return None
    load_data(myGlobals.filename_data)
    refresh_view()



def load_image(
    filename
):
    print('Opening image-file "%s"...' % filename)

    try:
        myGlobals.my_image = PilImage.open(filename)
    except IOError as err:
        print("I/O error: {0}".format(err))
        return None
        
    myGlobals.my_image = myGlobals.my_image.resize((640,400))
    myGlobals.my_image = myGlobals.my_image.convert("RGB")
        
    refresh_view()
    show_initial_preview_window()



def make_letter(
    letter_string
):
    letter = myGlobals.FONT_ABC.find(letter_string)+1
    
    LETTER_WIDTH = 7
    LETTER_HEIGHT = 8
    posx, posy = letter*LETTER_WIDTH,0
    
    box = (
        int(posx),
        int(posy),
        int(posx)+LETTER_WIDTH,
        int(posy)+LETTER_HEIGHT
    )

    return myGlobals.font_image.crop(box)



def refresh_numbers():
    HEXPRE = '0123456789abcdef'

    myGlobals.numbers_image = PilImage.new("RGBA", (640,400), "#00000000")   #clear all numbers
    blank_image = PilImage.new("RGBA", (15,15), "#000000aa")    #dark background for number

    for y in range(0,myGlobals.SCREEN_HEIGHT) :
        for x in range(0,myGlobals.SCREEN_WIDTH) :
            value = myGlobals.fadedata[y*myGlobals.SCREEN_WIDTH+x]
            if (value > 0) :
                high = HEXPRE[ (value >> 4 ) ]      # $0x high-nibble
                low = HEXPRE[ (value & 0b1111 ) ]   # $x0 low-nibble

                myGlobals.numbers_image.paste(blank_image, (16*x+1,16*y+1))   # dark background for number
                
                if (high != '0') :
                    letter_image = make_letter(high)   #high-nibble
                    myGlobals.numbers_image.paste(letter_image, (16*x+3+0,16*y+4), letter_image.convert('1'))
                    letter_image = make_letter(low)   #low-nibble
                    myGlobals.numbers_image.paste(letter_image, (16*x+1+8,16*y+4), letter_image.convert('1'))
                else :
                    letter_image = make_letter(low)   #only low-nibble
                    myGlobals.numbers_image.paste(letter_image, (16*x-3+8,16*y+4), letter_image.convert('1'))



def draw_grid():
    myGlobals.grid_image = PilImage.new("RGBA", (640,400), "#00000000")

    draw = ImageDraw.Draw(myGlobals.grid_image, 'RGBA')

    for i in range(0,myGlobals.grid_image.height,8*2) :
        draw.line(
            (
                0,
                i,
                myGlobals.grid_image.width,
                i
            ),
            fill="#88888888"
        )
        
    for i in range(0,myGlobals.grid_image.width,8*2) :
        draw.line(
            (
                i,
                0,
                i,
                myGlobals.grid_image.height
            ),
            fill="#88888888"
        )

    

def refresh_view():
    #print('refresh_view')
    refresh_numbers()

    final_image = myGlobals.my_image.copy()    
    
    if (myGlobals.show_grid) :
        final_image.paste(
            myGlobals.grid_image,
            myGlobals.grid_image.convert('RGBA')
        )

    if (myGlobals.show_values) :
        final_image.paste(
            myGlobals.numbers_image,
            myGlobals.numbers_image.convert('RGBA')
        )

    #apply the cursorbox
    if (myGlobals.keymode == True) :
        draw = ImageDraw.Draw(final_image, 'RGBA')

        draw.rectangle(
            ([
                (myGlobals.screenx*16,myGlobals.screeny*16),
                (myGlobals.screenx*16+myGlobals.CURSOR_BOX_SIZE-1, myGlobals.screeny*16+myGlobals.CURSOR_BOX_SIZE-1)
            ]),
            outline="#00ff00", width=1
        )
        
    #apply the selectbox
    if (myGlobals.selectmode == True) :
        #x
        if (myGlobals.select_box_startx < myGlobals.screenx+1) :
            #normal case
            myGlobals.select_box_x1 = myGlobals.select_box_startx
            myGlobals.select_box_x2 = myGlobals.screenx+1
        else :
            #flip
            myGlobals.select_box_x2 = myGlobals.select_box_startx
            myGlobals.select_box_x1 = myGlobals.screenx

        #y
        if (myGlobals.select_box_starty < myGlobals.screeny+1) :
            #normal case
            myGlobals.select_box_y1 = myGlobals.select_box_starty
            myGlobals.select_box_y2 = myGlobals.screeny+1
        else :
            #flip
            myGlobals.select_box_y2 = myGlobals.select_box_starty
            myGlobals.select_box_y1 = myGlobals.screeny
        
        draw = ImageDraw.Draw(final_image, 'RGBA')

        draw.rectangle(
            (
                [(
                    myGlobals.select_box_x1*16, #x1
                    myGlobals.select_box_y1*16  #y1
                ), (
                    (myGlobals.select_box_x2*16)-1, #x2
                    (myGlobals.select_box_y2*16)-1  #y2
                )]
            ),
            outline="#00ffff", width=1
        )
        myGlobals.copybuffer_width = myGlobals.select_box_x2 - myGlobals.select_box_x1
        myGlobals.copybuffer_height = myGlobals.select_box_y2 - myGlobals.select_box_y1


    tmp_image_tk = ImageTk.PhotoImage(final_image)
    myGlobals.label_image.configure(image=tmp_image_tk)
    myGlobals.label_image.image = tmp_image_tk # keep a reference!


#    update_info()

    

def show_initial_preview_window():
    #prepare preview image
    myGlobals.preview_image = myGlobals.my_image.copy().resize((640,400)).convert("RGB")

    #copy to label_preview_image
    tmp_image = ImageTk.PhotoImage(myGlobals.preview_image)
    myGlobals.label_preview_image.configure(image=tmp_image)
    myGlobals.label_preview_image.image = tmp_image # keep a reference!


#    update_info()






def value_increase():
    if (myGlobals.screen_value < 255) :
        myGlobals.screen_value += 1
        update_info()

def value_decrease():
    if (myGlobals.screen_value > 0) :
        myGlobals.screen_value -= 1
        update_info()

def value_increase_Big():
    myGlobals.screen_value += 16
    if (myGlobals.screen_value > 255) : myGlobals.screen_value = 255
    update_info()

def value_decrease_Big():
    myGlobals.screen_value -= 16
    if (myGlobals.screen_value < 0) : myGlobals.screen_value = 0
    update_info()





def waithere():
    var = tk.IntVar()
    myGlobals.root.after(myGlobals.PREVIEW_DELAY, var.set, 1)
    myGlobals.root.wait_variable(var)



def preview_fade_out(
):
    if (myGlobals.preview_in_action == True) : return None
    myGlobals.preview_in_action = True

    myGlobals.button_fade_out.configure(relief=tk.SUNKEN) #button looks activated
    
    myGlobals.original_image = myGlobals.my_image.copy().resize((640,400)).convert("RGB")

    myGlobals.preview_image = myGlobals.original_image.copy()

    blank_image = PilImage.new("RGBA", (16,16), "#00000044")    #dark background for number
    
    #print('Starting preview...')
    
    for i in range(0,myGlobals.value_max+1+16) :
        for y in range(0,myGlobals.SCREEN_HEIGHT) :
            for x in range(0,myGlobals.SCREEN_WIDTH) :
                if (myGlobals.fadedata[y*myGlobals.SCREEN_WIDTH+x] <= i) :
                    myGlobals.preview_image.paste(blank_image, ( (x*16), y*16 ), blank_image.convert('RGBA') )

        #copy to label_preview_image
        tmp_image = ImageTk.PhotoImage(myGlobals.preview_image)
        myGlobals.label_preview_image.configure(image=tmp_image)
        myGlobals.label_preview_image.image = tmp_image # keep a reference!
        myGlobals.root.update()
        #print('$%02x / $%02x'%(i,value_max))
        waithere()

    #print('done preview.')

    #show_initial_preview_window()
    
    myGlobals.preview_in_action = False
    myGlobals.button_fade_out.configure(relief=tk.RAISED) #button looks normally



def preview_fade_in(
):
    if (myGlobals.preview_in_action == True) : return None
    myGlobals.preview_in_action = True

    myGlobals.button_fade_in.configure(relief=tk.SUNKEN) #button looks activated
    
    original_image = myGlobals.my_image.copy().resize((640,400)).convert("RGB")

    myGlobals.preview_image = PilImage.new("RGB", (640,400), "#000000")
    alpha_image = PilImage.new("RGBA", (16,16), "#00000044")

    #print('Starting preview...')
    
    for i in range(0,myGlobals.value_max+1+16) :
        for y in range(0,myGlobals.SCREEN_HEIGHT) :
            for x in range(0,myGlobals.SCREEN_WIDTH) :
                if (myGlobals.fadedata[y*myGlobals.SCREEN_WIDTH+x] <= i) :
                    tmp_image = original_image.crop((
                        x*16,
                        y*16,
                        (x+1)*16,
                        (y+1)*16
                    ))
                    #preview_image.paste(tmp_image, ( (x*16), y*16 ), tmp_image.convert('RGBA') )
                    myGlobals.preview_image.paste(tmp_image, ( x*16, y*16 ), alpha_image )

        #copy to label_preview_image
        tmp_image = ImageTk.PhotoImage(myGlobals.preview_image)
        myGlobals.label_preview_image.configure(image=tmp_image)
        myGlobals.label_preview_image.image = tmp_image # keep a reference!
        myGlobals.root.update()
        #print('$%02x / $%02x'%(i,value_max))
        waithere()

    #print('done preview.')

    #show_initial_preview_window()
    
    myGlobals.preview_in_action = False

    myGlobals.button_fade_in.configure(relief=tk.RAISED) #button looks normally

    


def open_data():
    ftypes = [('Fademaid Files', '*.bin *.fade')]
    user_filename_open = filedialog.askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    myGlobals.filename_data = user_filename_open
    myGlobals.textvariable_filename_data.set("\"..."+user_filename_open[-30:]+"\"")
    load_data(user_filename_open)
    refresh_view()

    
def save_data():
    save_data_real(
        myGlobals.filename_data,
        myGlobals.fadedata
    )

    
def save_data_As():
    ftypes = [('Data Files', '*.bin *.fade')]
    user_filename_save = filedialog.asksaveasfilename(filetypes = ftypes)
    if not user_filename_save : return None
    myGlobals.filename_data = user_filename_save
    myGlobals.textvariable_filename_data.set("\"..."+user_filename_save[-30:]+"\"")
    save_data_real(user_filename_save, myGlobals.fadedata)
    
    
def open_image():   
    ftypes = [('Image Files', '*.tif *.jpg *.png *.bmp *.gif')]
    user_filename_open = filedialog.askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    myGlobals.filename_image = user_filename_open
    myGlobals.textvariable_filename_image.set("\"..."+user_filename_open[-30:]+"\"")
    load_image(user_filename_open)



def toggle_automode():
    if (myGlobals.auto_mode == True) :
        myGlobals.auto_mode = False
        myGlobals.button_toggle_automode.configure(relief=tk.RAISED) #button looks normally
    else :
        myGlobals.auto_mode = True
        myGlobals.button_toggle_automode.configure(relief=tk.SUNKEN) #button looks activated
    

def toggle_grid():
    if (myGlobals.show_grid == True) :
        myGlobals.show_grid = False
        myGlobals.button_toggle_grid.configure(relief=tk.RAISED) #button looks normally
    else :
        myGlobals.show_grid = True
        myGlobals.button_toggle_grid.configure(relief=tk.SUNKEN) #button looks activated
    
    refresh_view()
    

def toggle_values():
    if (myGlobals.show_values == True) :
        myGlobals.show_values = False
        myGlobals.button_toggle_values.configure(relief=tk.RAISED) #button looks normally
    else :
        myGlobals.show_values = True
        myGlobals.button_toggle_values.configure(relief=tk.SUNKEN) #button looks activated
    
    refresh_view()

        

def toggle_keymode():
    if (myGlobals.keymode == True) :
        #disable keymode
        myGlobals.keymode = False
        myGlobals.button_toggle_keymode.configure(relief=tk.RAISED) #button looks normally
        myGlobals.label_image.config(cursor=myGlobals.cursor_image_normal)    #enable mouse pointer
        myGlobals.keymode_last_screenx = myGlobals.screenx
        myGlobals.keymode_last_screeny = myGlobals.screeny
    else :
        #enable keymode
        myGlobals.keymode = True
        myGlobals.button_toggle_keymode.configure(relief=tk.SUNKEN) #button looks activated
        myGlobals.label_image.config(cursor=myGlobals.cursor_image_none)    #disable mouse pointer
        myGlobals.screenx = myGlobals.keymode_last_screenx
        myGlobals.screeny = myGlobals.keymode_last_screeny
    
    refresh_view()


        
def toggle_selectmode():
    if (myGlobals.selectmode == True) :
        #disable
        myGlobals.selectmode = False
        selectmode_copy()
    else :
        #enable
        myGlobals.selectmode = True
        myGlobals.select_box_startx = myGlobals.screenx
        myGlobals.select_box_starty = myGlobals.screeny
    
    refresh_view()

        



def clear_data():
    for i in range(0,myGlobals.SCREEN_HEIGHT*myGlobals.SCREEN_WIDTH) :
        myGlobals.fadedata[i] = 0
    update_info()
    refresh_view()


def mouseButton1(event):
    myGlobals.mouse_posx = event.x
    myGlobals.mouse_posy = event.y
    update_info()
    
    if (myGlobals.mouse_release_Button1 == False) :
        if (
            (myGlobals.last_screenx == myGlobals.screenx) &
            (myGlobals.last_screeny == myGlobals.screeny)
        ) :
            return None

    myGlobals.mouse_release_Button1 = False
        
    myGlobals.last_screenx = myGlobals.screenx
    myGlobals.last_screeny = myGlobals.screeny

    myGlobals.fadedata[myGlobals.screeny*myGlobals.SCREEN_WIDTH+myGlobals.screenx] = myGlobals.screen_value
    if (myGlobals.auto_mode) : value_increase()

    refresh_view()



def mouse_release_Button1(event):
    myGlobals.mouse_release_Button1 = True

def mouse_release_Button3(event):
    myGlobals.mouse_release_Button3 = True


def mouseButton3(event):
    myGlobals.mouse_posx = event.x
    myGlobals.mouse_posy = event.y
    update_info()

    if (myGlobals.mouse_release_Button3 == False) :
        if (
            (myGlobals.last_screenx == myGlobals.screenx) &
            (myGlobals.last_screeny == myGlobals.screeny)
        ) :
            return None

    myGlobals.mouse_release_Button3 = False
        
    myGlobals.last_screenx = myGlobals.screenx
    myGlobals.last_screeny = myGlobals.screeny

    if (myGlobals.auto_mode) :
        myGlobals.fadedata[myGlobals.screeny*myGlobals.SCREEN_WIDTH+myGlobals.screenx] = myGlobals.screen_value
        value_decrease()
    else :
        myGlobals.fadedata[myGlobals.screeny*myGlobals.SCREEN_WIDTH+myGlobals.screenx] = 0

    refresh_view()



def update_info():
    if (myGlobals.keymode == False) :
        tmp_posx = int(myGlobals.mouse_posx/2)
        if (tmp_posx > 319) : tmp_posx = 319
        tmp_posy = int(myGlobals.mouse_posy/2)
        if (tmp_posy > 199) : tmp_posy = 199
        
        myGlobals.screenx = int(tmp_posx/8)
        myGlobals.screeny = int(tmp_posy/8)
    else :
        tmp_posx = myGlobals.screenx*8
        tmp_posy = myGlobals.screeny*8
    
    myGlobals.value_max = max(myGlobals.fadedata)

    myGlobals.textvariable_coords.set('x=%03d y=%03d | x=$%04x y=$%02x' % (
        tmp_posx, tmp_posy,
        tmp_posx, tmp_posy
    ))

    myGlobals.textvariable_pos.set('col=%02d row=%02d | col=$%02x row=$%02x' % (
        myGlobals.screenx, myGlobals.screeny,
        myGlobals.screenx, myGlobals.screeny
    ))

    myGlobals.textvariable_value.set('%03d | $%02x' % (
        myGlobals.screen_value, myGlobals.screen_value
    ))

    myGlobals.textvariable_max.set('%03d | $%02x' % (
        myGlobals.value_max, myGlobals.value_max
    ))


def mouseMotion(event):
    myGlobals.mouse_posx = event.x
    myGlobals.mouse_posy = event.y

    update_info()
    
    if (myGlobals.selectmode == True) :
        if (
            (myGlobals.last_screenx != myGlobals.screenx) or
            (myGlobals.last_screeny != myGlobals.screeny)
        ) :
            refresh_view()
            myGlobals.last_screenx = myGlobals.screenx
            myGlobals.last_screeny = myGlobals.screeny



def reset_settings():
    for a in range(0,len(myGlobals.scale_settings_list)):
        myGlobals.scale_settings_list[a].set( myGlobals.scale_settings_list_default[a])


def key_up():
    if (myGlobals.keymode == False) :
        value_increase()
    else :
        if (myGlobals.screeny > 0) :
            myGlobals.screeny -= 1
        update_info()
        refresh_view()


def key_down():
    if (myGlobals.keymode == False) :
        value_decrease()
    else :
        if (myGlobals.screeny < myGlobals.SCREEN_HEIGHT-1) :
            myGlobals.screeny += 1
        update_info()
        refresh_view()


def key_right():
    if (myGlobals.keymode == False) :
        value_increase_Big()
    else :
        if (myGlobals.screenx < myGlobals.SCREEN_WIDTH-1) :
            myGlobals.screenx += 1
        update_info()
        refresh_view()
    
def key_left():
    if (myGlobals.keymode == False) :
        value_decrease_Big()
    else :
        if (myGlobals.screenx > 0) :
            myGlobals.screenx -= 1
        update_info()
        refresh_view()


def keymode_enter_digit(
    value
):
    if (myGlobals.keymode == True) :
        if (myGlobals.keymode_first_number == True) :
            myGlobals.screen_value = value
            myGlobals.keymode_first_number = False
        else:
            myGlobals.screen_value =  ( myGlobals.screen_value << 4) + value
            myGlobals.keymode_first_number = True
        update_info()
        
    
def keymode_delete(
) :
    myGlobals.fadedata[
        myGlobals.screeny*myGlobals.SCREEN_WIDTH+myGlobals.screenx
    ] = 0
    refresh_view()
    
    

def keymode_enter(
) :
    myGlobals.fadedata[
        myGlobals.screeny*myGlobals.SCREEN_WIDTH+myGlobals.screenx
    ] = myGlobals.screen_value

    if (myGlobals.auto_mode) :
        value_increase()
    
    myGlobals.keymode_first_number = True
    
    refresh_view()


def selectmode_copy(
) :
    myGlobals.copybuffer_data = []
    for y in range(myGlobals.select_box_y1, myGlobals.select_box_y2) :
        for x in range(myGlobals.select_box_x1, myGlobals.select_box_x2) :
            myGlobals.copybuffer_data.append(
                myGlobals.fadedata[y*myGlobals.SCREEN_WIDTH+x]
            )
            
    
def selectmode_paste(
) :
    c=0
    posx = myGlobals.screenx
    posy = myGlobals.screeny
    for y in range(0,myGlobals.copybuffer_height) :
        for x in range(0,myGlobals.copybuffer_width) :
            if (
                ((posx+x) < myGlobals.SCREEN_WIDTH) &
                ((posy+y) < myGlobals.SCREEN_HEIGHT)
            ) :
                myGlobals.fadedata[ (posy+y)*myGlobals.SCREEN_WIDTH+(posx+x) ] = myGlobals.copybuffer_data[c]
            c += 1
    refresh_view()



def selectmode_cut(
) :
    posx = myGlobals.screenx
    posy = myGlobals.screeny
    for y in range(0,myGlobals.copybuffer_height) :
        for x in range(0,myGlobals.copybuffer_width) :
            if (
                ((posx+x) < myGlobals.SCREEN_WIDTH) &
                ((posy+y) < myGlobals.SCREEN_HEIGHT)
            ) :
                myGlobals.fadedata[ (posy+y)*myGlobals.SCREEN_WIDTH+(posx+x) ] = 0
    refresh_view()

