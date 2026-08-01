import code.myGlobals as myGlobals
import code.action as action
import code.gui_help as gui_help
import code.gui_about as gui_about
import tkinter as tk
import tkinter.filedialog as filedialog



def create_gui_drop_down_menu (
	root
) :
    menu = tk.Menu(root)
    root.config(menu=menu)

    filemenu = tk.Menu(menu)
    datamenu = tk.Menu(menu)
    infomenu = tk.Menu(menu)

    filemenu.add_command(label="open background-image", command=action.open_image, underline=5, accelerator="Alt+B")
    filemenu.add_command(label="open data", command=action.open_data, underline=0, accelerator="Alt+O")
    filemenu.add_command(label="save data", command=action.save_data, underline=0, accelerator="Alt+S")
    filemenu.add_command(label="save data as", command=action.save_data_As, underline=0, accelerator="Alt+Shift+S")
    filemenu.add_separator()
    filemenu.add_command(label="quit", command=quit_application, underline=0, accelerator="Alt+Q")

    datamenu.add_command(label="reload data", command=action.reload_data)
    datamenu.add_separator()
    datamenu.add_command(label="clear all data", command=action.clear_data)

    infomenu.add_command(label="help", command=gui_help.show_window, accelerator="f1")
    infomenu.add_command(label="about", command=gui_about.show_window, accelerator="f2")

    #add all menus
    menu.add_cascade(label="menu", menu=filemenu)
    menu.add_cascade(label="data", menu=datamenu)
    menu.add_cascade(label="info", menu=infomenu)




def create_gui_image (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    
    myGlobals.label_image = tk.Label(
        frame_border,
        bg=myGlobals.BGCOLOR,
        cursor=myGlobals.cursor_image
    )
    myGlobals.label_image.grid(
        row=0,
        column=0,
        sticky= tk.W+ tk.E
    )
    
    myGlobals.label_image.bind('<Motion>', action.mouseMotion)
    myGlobals.label_image.bind('<Button-1>', action.mouseButton1)
    myGlobals.label_image.bind('<Button-3>', action.mouseButton3)
    myGlobals.label_image.bind('<B1-Motion>', action.mouseButton1)
    myGlobals.label_image.bind('<B3-Motion>', action.mouseButton3)

    myGlobals.label_image.bind('<ButtonRelease-1>', action.mouse_release_Button1)
    myGlobals.label_image.bind('<ButtonRelease-3>', action.mouse_release_Button3)



def create_gui_logo (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bd=myGlobals._bd,
        bg=myGlobals.BGCOLOR
    )
    frame_border.grid(
        row=_row,
        column=_column
    )

    photo = tk.PhotoImage(file=myGlobals.RES_GFX_AC)
    label_logo = tk.Label(frame_border, image = photo)
    label_logo.image = photo # keep a reference!
    label_logo.grid( row=0, column=0)
    label_logo.configure(background=myGlobals.BGCOLOR)





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
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady
        )

    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR_LIGHT,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief= tk.RAISED
        )

    label_info = tk.Label(
		frame_inner,
        bg=myGlobals.BGCOLOR2,
		text = my_text,
        bd=1
	)

    label_content = tk.Label(
		frame_inner,
        bg=myGlobals.BGCOLOR_LIGHT,
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
        bg=myGlobals.BGCOLOR,
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
        bg=myGlobals.BGCOLOR,
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
        bg=myGlobals.BGCOLOR,
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
        myGlobals.textvariable_value,   #textvariable
        10   #text width
    )


    create_gui_infobox (
        frame_right,   #root frame
        0,  #row
        0,  #column
        'coords:',    #text
        myGlobals.textvariable_coords,   #textvariable
        30   #text width
    )

    create_gui_infobox (
        frame_left,   #root frame
        1,  #row
        0,  #column
        'max:',    #text
        myGlobals.textvariable_max,   #textvariable
        10   #text width
    )

    create_gui_infobox (
        frame_right,   #root frame
        1,  #row
        0,  #column
        'char:',    #text
        myGlobals.textvariable_pos,   #textvariable
        30   #text width
    )


    create_gui_infobox (
        frame_left,   #root frame
        2,  #row
        0,  #column
        'data:',    #text
        myGlobals.textvariable_filename_data,   #textvariable
        30   #text width
    )

    create_gui_infobox (
        frame_right,   #root frame
        2,  #row
        0,  #column
        'image:',    #text
        myGlobals.textvariable_filename_image,   #textvariable
        30   #text width
    )






def create_gui_control (
	root,
    _row,
    _column
) :
    #global button_toggle_automode, button_toggle_grid, button_toggle_values, button_fade_in, button_fade_out
    
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column,
        sticky= tk.W
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR_LIGHT,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief= tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
 
    myGlobals.button_fade_in = tk.Button(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text = "fade in",
        command=action.preview_fade_in,
        cursor=myGlobals.CURSOR_HAND,
    )
    myGlobals.button_fade_in.grid(
        row=0,
        column=0,
        sticky="w"
    )
 
    myGlobals.button_fade_out = tk.Button(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text = "fade out",
        command=action.preview_fade_out,
        cursor=myGlobals.CURSOR_HAND,
    )
    myGlobals.button_fade_out.grid(
        row=0,
        column=1,
        sticky="w"
    )

 
    myGlobals.button_toggle_automode = tk.Button(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text = "auto-mode",
        command=action.toggle_automode,
        cursor=myGlobals.CURSOR_HAND,
    )
    myGlobals.button_toggle_automode.grid(
        row=0,
        column=2,
        sticky="w"
    )


    myGlobals.button_toggle_keymode = tk.Button(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text = "keymode",
        command=action.toggle_keymode,
        cursor=myGlobals.CURSOR_HAND,
        #relief=tk.SUNKEN,
    )
    myGlobals.button_toggle_keymode.grid(
        row=0,
        column=3,
        sticky="w"
    )

 
    myGlobals.button_toggle_grid = tk.Button(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text = "show grid",
        command=action.toggle_grid,
        cursor=myGlobals.CURSOR_HAND,
        relief=tk.SUNKEN,
    )
    myGlobals.button_toggle_grid.grid(
        row=0,
        column=4,
        sticky="w"
    )
 
 
    myGlobals.button_toggle_values = tk.Button(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text = "show values",
        command=action.toggle_values,
        cursor=myGlobals.CURSOR_HAND,
        relief=tk.SUNKEN,
    )
    myGlobals.button_toggle_values.grid(
        row=0,
        column=5,
        sticky="w"
    )
 





def create_gui_preview(
) :
    @staticmethod
    def __callback():
        return

    #global label_preview_image
    
    preview_window = tk.Toplevel(bd=10)
    preview_window.title("preview")
    preview_window.iconphoto(False, tk.PhotoImage(file=myGlobals.RES_GFX_ICON))
    preview_window.protocol("WM_DELETE_WINDOW", __callback)
    preview_window.resizable(0, 0)
#    preview_window.configure(background=BGCOLOR)


    myGlobals.label_preview_image = tk.Label(
        preview_window,
        bg=myGlobals.BGCOLOR
    )

    myGlobals.label_preview_image.grid(
        row=0,
        column=0,
        sticky= tk.W+ tk.E
    )

	
        
def create_gui_base(
):
    myGlobals.root.configure(
        background=myGlobals.BGCOLOR
    )
    create_gui_logo(
        myGlobals.root,
        0,  #row
        0   #column
    )

    create_gui_info(
        myGlobals.root,
        1,  #row
        0   #column
    )



    create_gui_control (
        myGlobals.root,   #root frame
        2,  #row
        0  #column
    )

    create_gui_image(
        myGlobals.root,
        3,  #row
        0   #column
    )



def quit_application():
    myGlobals.root.quit()

"""    
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):

        if (myGlobals.image_is_saved == False) :
            if tk.messagebox.askokcancel("Save", "Do you want to save?"):
                save_as_petscii_json()

        myGlobals.root.quit()
"""
