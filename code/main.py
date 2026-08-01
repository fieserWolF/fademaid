import code.myGlobals as myGlobals
import code.gui as gui
import code.action as action
import code.gui_help as gui_help
import code.gui_about as gui_about
import sys

import tkinter as tk
import argparse

from PIL import ImageTk, ImageDraw
import PIL.Image as PilImage    #we need another name, as it collides with tkinter.Image otherwise


def init_gui (
) :
    #main procedure
    title_string = myGlobals.PROGNAME+" "+myGlobals.VERSION+" *** by fieserWolF"
    myGlobals.root.title(title_string)
    myGlobals.root.iconphoto(False, tk.PhotoImage(file=myGlobals.RES_GFX_ICON))
    gui.create_gui_drop_down_menu(myGlobals.root)
    gui.create_gui_base()
    gui.create_gui_preview()


    #https://www.pythontutorial.net/tkinter/tkinter-event-binding/
    myGlobals.root.bind_all("<Alt-q>", lambda event: gui.quit_application())
    myGlobals.root.bind_all("<Control-q>", lambda event: gui.quit_application())
    myGlobals.root.bind_all("<Alt-b>", lambda event: action.open_image())
    myGlobals.root.bind_all("<Control-b>", lambda event: action.open_image())
    myGlobals.root.bind_all("<Alt-o>", lambda event: action.open_data())
    myGlobals.root.bind_all("<Control-o>", lambda event: action.open_data())
    myGlobals.root.bind_all("<Alt-s>", lambda event: action.save_data())
    myGlobals.root.bind_all("<Control-s>", lambda event: action.save_data())
    myGlobals.root.bind_all("<Alt-S>", lambda event: action.save_data_As())
    myGlobals.root.bind_all("<Control-S>", lambda event: action.save_data_As())
    myGlobals.root.bind_all("<F1>", lambda event: action.action_Show_Help())
    myGlobals.root.bind_all("<F2>", lambda event: action.action_Show_About())
    myGlobals.root.bind_all("<Control-a>", lambda event: action.toggle_automode())
    myGlobals.root.bind_all("k", lambda event: action.toggle_keymode())
    myGlobals.root.bind_all("s", lambda event: action.toggle_selectmode())
    myGlobals.root.bind_all("<Control-c>", lambda event: action.selectmode_copy())
    myGlobals.root.bind_all("<Control-v>", lambda event: action.selectmode_paste())
    myGlobals.root.bind_all("<Control-x>", lambda event: action.selectmode_cut())
    myGlobals.root.bind_all("<Alt-c>", lambda event: action.selectmode_copy())
    myGlobals.root.bind_all("<Alt-v>", lambda event: action.selectmode_paste())
    myGlobals.root.bind_all("<Alt-x>", lambda event: action.selectmode_cut())
    myGlobals.root.bind_all("<Up>", lambda event: action.key_up())
    myGlobals.root.bind_all("<Down>", lambda event: action.key_down())
    myGlobals.root.bind_all("<Right>", lambda event: action.key_right())
    myGlobals.root.bind_all("<Left>", lambda event: action.key_left())
    myGlobals.root.bind_all("o", lambda event: action.preview_fade_out())
    myGlobals.root.bind_all("i", lambda event: action.preview_fade_in())
    myGlobals.root.bind_all("0", lambda event: action.keymode_enter_digit(0))
    myGlobals.root.bind_all("1", lambda event: action.keymode_enter_digit(1))
    myGlobals.root.bind_all("2", lambda event: action.keymode_enter_digit(2))
    myGlobals.root.bind_all("3", lambda event: action.keymode_enter_digit(3))
    myGlobals.root.bind_all("4", lambda event: action.keymode_enter_digit(4))
    myGlobals.root.bind_all("5", lambda event: action.keymode_enter_digit(5))
    myGlobals.root.bind_all("6", lambda event: action.keymode_enter_digit(6))
    myGlobals.root.bind_all("7", lambda event: action.keymode_enter_digit(7))
    myGlobals.root.bind_all("8", lambda event: action.keymode_enter_digit(8))
    myGlobals.root.bind_all("9", lambda event: action.keymode_enter_digit(9))
    myGlobals.root.bind_all("a", lambda event: action.keymode_enter_digit(10))
    myGlobals.root.bind_all("b", lambda event: action.keymode_enter_digit(11))
    myGlobals.root.bind_all("c", lambda event: action.keymode_enter_digit(12))
    myGlobals.root.bind_all("d", lambda event: action.keymode_enter_digit(13))
    myGlobals.root.bind_all("e", lambda event: action.keymode_enter_digit(14))
    myGlobals.root.bind_all("f", lambda event: action.keymode_enter_digit(15))
    myGlobals.root.bind_all("<Return>", lambda event: action.keymode_enter())
    myGlobals.root.bind_all("<BackSpace>", lambda event: action.keymode_delete())
    #myGlobals.root.bind_all("<space>", lambda event: action.preview_fade_in())

    myGlobals.root.protocol('WM_DELETE_WINDOW', gui.quit_application)

#    print('Opening font-image-file "%s"...' % RES_GFX_FONT)
    myGlobals.font_image = PilImage.open(myGlobals.RES_GFX_FONT)


    action.draw_grid()
    
    if (myGlobals.args.data_file) :
        myGlobals.filename_data = myGlobals.args.data_file
        myGlobals.textvariable_filename_data.set("\"..."+myGlobals.filename_data[-30:]+"\"")
        action.load_data(myGlobals.filename_data)

    if (myGlobals.args.image_file) :
        myGlobals.filename_image = myGlobals.args.image_file
        myGlobals.textvariable_filename_image.set("\"..."+myGlobals.filename_image[-30:]+"\"")
        action.load_image(myGlobals.filename_image)

    action.update_info()

    action.refresh_view()
    
    action.show_initial_preview_window()




def _main_procedure() :

    #global textvariable_filename_data, textvariable_filename_image
    
    myGlobals.textvariable_filename_data.set('None')
    myGlobals.textvariable_filename_image.set('none')

    print("%s %s *** by WolF"% (myGlobals.PROGNAME, myGlobals.VERSION))

    #https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        description='You can edit char-wise values with this.',
        epilog='Example: ./fademaid.py -i image.png -d data.bin'
    )
    parser.add_argument('-i', '--image_file', dest='image_file', help='background image filename')
    parser.add_argument('-d', '--data_file', dest='data_file', help='fademaid data filename')
    myGlobals.args = parser.parse_args()

            
    init_gui ()
    
    tk.mainloop()
    



if __name__ == '__main__':
    _main_procedure()
