import os, json, shutil, webbrowser
import tkinter as tk
from os import listdir
from time import strftime
from tkinter import messagebox, simpledialog
from myscrollbar import MyScrollbar #customer scroll bar
from string import ascii_letters, digits


class MintApp(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.root.title("MINT: Mobile Information & Note-taking Tool")
        self.root.columnconfigure(0, weight = 0)
        self.root.columnconfigure(1, weight = 1)
        self.root.rowconfigure(0, weight = 0)
        self.root.rowconfigure(1, weight = 1)
        #~~~~~~~~~~~~~~~~~~~< Variables Defaults >~~~~~~~~~~~~~~~~~~~~~~
        self.file_date_path = "./FileDirectory/file_data"
        self.mint_required_path = "./FileDirectory/MINT_REQUIRED_DATA_FOLDER"
        self.current_working_lib = "./FileDirectory/file_data"
        self.current_working_keys = "welcome.txt"
        self.current_saving_lib = "./FileDirectory/file_data"
        self.library_list = []
        self.theme_options = []
        self.current_file_path = ""
    #< MINT Theme setting >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.py_bg_color = "#{:02x}{:02x}{:02x}".format(0, 34, 64)
        self.py_frame_color = "#{:02x}{:02x}{:02x}".format(0, 23, 45)
        self.main_bg_color = "#{:02x}{:02x}{:02x}".format(64,89,82)
        self.text_bg_color = "#{:02x}{:02x}{:02x}".format(0, 23, 45)
        self.txt_color = "#{:02x}{:02x}{:02x}".format(175, 167, 157)
        self.root.config(bg = self.py_frame_color)
        self.color_path = "./Colors/"
        self.current_working_button_color = "orange"
        self.selected_text_color = "orange"
        self.selected_bg_color = "#%02x%02x%02x"
        self.post_update = False
        self.text_wordwrap = False
        self.base_bg_image = tk.PhotoImage(file = "./Colors/pybgbase.png")
        self.bg_lable = tk.Label(self.root, image= self.base_bg_image)
        self.bg_lable.place(x = 0, y = 0)
        self.bg_lable.config(image = self.base_bg_image)
        self.bg_lable.image = self.base_bg_image
        self.current_text_color = 'orange'
        
        #~~~~~~~~~~~~~~~~~~~< USE TO open all files in Directory >~~~~~~
        self.text_frame = tk.Frame(root, borderwidth = 0, highlightthickness = 0)
        self.text_frame.grid(row = 0, column = 1, columnspan = 1, rowspan = 2, padx = 0, pady = 0, sticky = 'nsew')
        self.text_frame.columnconfigure(0, weight = 1)
        self.text_frame.rowconfigure(0, weight = 1)
        self.text_frame.columnconfigure(1, weight = 0)
        self.text_frame.rowconfigure(1, weight = 0)
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.grid(row = 0, column = 0, columnspan = 1, rowspan = 1, padx = 0, pady = 0, sticky = 'nsew')
        self.entry_frame.columnconfigure(0, weight = 0)
        self.entry_frame.columnconfigure(1, weight = 0)
        self.entry_frame.rowconfigure(0, weight = 0)
        self.entry_frame.rowconfigure(1, weight = 0)
        self.entry_frame.rowconfigure(2, weight = 0)
        self.kw_list_frame = tk.Frame(self.root, borderwidth = 0, highlightthickness = 0)
        self.kw_list_frame.grid(row = 1, column = 0, columnspan = 1, rowspan = 1, padx = 0, pady = 0, sticky = 'nsew')
        self.kw_list_frame.columnconfigure(0, weight = 1)
        self.sub_kw_list_frame = tk.Frame(self.kw_list_frame, borderwidth = 0, highlightthickness = 0)
        self.sub_kw_list_frame.grid(row = 0, column = 0, sticky = 'nsew')
        self.root.text_side_left = tk.Text(self.kw_list_frame, width = 10, height = 20)
        self.status_frame = tk.Frame(root)
        self.status_frame.grid(row = 3, column = 0,columnspan = 2, rowspan = 3, padx =0, pady =0, sticky = 'nsew')
        self.status_frame.columnconfigure(0, weight = 1)
        self.status_frame.columnconfigure(1, weight = 1)
        self.status_frame.rowconfigure(0, weight = 0)
        self.root.text = tk.Text(self.text_frame, undo = True)
        self.root.text.grid(row = 0, column = 0,columnspan = 1, rowspan = 1, padx = 0, pady = 0, sticky = 'nsew')
        self.root.text.config(wrap = 'none')
        self.root.text.bind('<Control-s>', self.append_notes)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.status_w = tk.Label(self.status_frame, relief = 'sunken', anchor = 'w')
        self.status_w.grid(row = 0, column = 0, padx = 1, pady = 1, sticky = 'sw')
        self.status_w.config(text = "Operation Status")
        self.status_e = tk.Label(self.status_frame, relief = 'sunken', anchor = 'e')
        self.status_e.grid(row = 0, column = 1, padx = 1, pady = 1, sticky = 'se')
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.search_label = tk.Label(self.entry_frame)
        self.search_label.grid(row = 1, column = 0, padx = 5, pady = 5)
        self.search_label.config(text = "Search")
        self.search_entry = tk.Entry(self.entry_frame, width = 20)
        self.search_entry.bind("<Return>", self.search_textbox)
        self.search_entry.bind("<Shift-Return>", self.next_match)
        self.search_entry.bind("<Control-Return>", self.prev_match)
        self.search_entry.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.update_keywords_button = tk.Button(self.entry_frame, fg = 'Black', text = "Update Notes", command = self.append_notes)
        self.update_keywords_button.grid(row = 2, column = 0, columnspan = 2, padx = 5, pady = 5)
        self.library_menu()
        self.status_clock()
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
        self.root.text.tag_config("marg", lmargin1 = 15, lmargin2 = 15)
        with open("{}/welcome.txt".format(self.mint_required_path), "r") as w:
            self.root.text.insert("1.0", w.read(),("marg"))
            self.root.text.edit_modified(False)
        self.get_immediate_subdirectories(self.file_date_path)
    #< Bindings list for quick commands >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.root.bind("<Control-D>", self.delete_current_note)
        self.root.bind("<Control-d>", self.delete_current_note)
        self.root.bind("<Control-N>", self.create_note_in_current_library)
        self.root.bind("<Control-n>", self.create_note_in_current_library)
        self.root.bind("<Alt-N>", self.create_library_folder)
        self.root.bind("<Alt-n>", self.create_library_folder)
        self.root.bind("<Alt-D>", self.delete_library_folder)
        self.root.bind("<Alt-d>", self.delete_library_folder)
    #< MINT Theme setting >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.entrybg_image = tk.Label(self.entry_frame, image = self.base_bg_image,
                              borderwidth = 0, highlightthickness = 0)
        self.entrybg_image.image = self.base_bg_image
        self.entrybg_image.place(x = 0, y = 0)
        self.entrybg_image.config(image = self.base_bg_image)
        self.kw_bg_image = tk.Label(self.kw_list_frame, image = self.base_bg_image,
                                    borderwidth = 0, highlightthickness = 0)
        self.kw_bg_image.image = self.base_bg_image
        self.kw_bg_image.place(x = 0, y = 0)
        self.kw_bg_image.config(image = self.base_bg_image)
        self.mint_theme_default(self.main_bg_color, self.text_bg_color,
                            self.txt_color, "./Colors/pybgbase.png")
    #< Lift widgets over background until I can find a fix >~~~~~~~~~~~~~~~~~~~~~~
        self.search_entry.lift()
        self.search_label.lift()
    #< Check File Data for Libraries >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_immediate_subdirectories(self, a_dir):
        self.library_list = []
        for name in os.listdir(a_dir):
            if os.path.isdir(os.path.join(a_dir, name)):
                self.library_list.append(name)
        for name in self.library_list:
            self.lib_menu.add_command(label = "{}".format(name), command = lambda n=name: self.set_working_library(n))
    #< Set working library >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def set_working_library(self, lib_name):
        if self.root.text.edit_modified() == False:
            new = "./FileDirectory/file_data/{}".format(lib_name)
            if self.current_working_lib == new:
                print("Current working library is already set to {}".format(lib_name))
            else:
                self.current_working_lib = "./FileDirectory/file_data/{}".format(lib_name)
                self.reset_quick_file_selections()

    def update_textbox(self, file_name):
        if self.root.text.edit_modified() == False:
            self.update_textbox_step2(file_name)
        else:
            answer = messagebox.askquestion("Changing Files", "You are about to chance files without saving.")
            if answer == "yes":
                self.update_textbox_step2(file_name)
    
    def update_textbox_step2(self, file_name):
        self.current_working_keys = file_name
        self.current_saving_lib = self.current_working_lib
        self.root.text.delete("1.0", "end")
        with open("{}/{}".format(self.current_working_lib, file_name), "r") as w:
            self.root.text.insert("1.0", w.read(),("marg"))
            self.root.text.edit_modified(False)
            self.current_file_path = "{}/{}".format(self.current_working_lib, file_name)
                
    def append_notes(self, Event=None):
        print(self.current_saving_lib)
        path = "{}/{}".format(self.current_saving_lib, self.current_working_keys)
        with open(path, "w") as w:
            w.write(self.root.text.get(1.0, "end"))
            self.root.text.edit_modified(False)

    def reset_quick_file_selections(self, **kwargs):
        keys_to_be_updated = []
        for x in os.listdir(self.current_working_lib):
            if x.endswith(".txt"):
                keys_to_be_updated.append(x)
                
        tbc = self.text_bg_color
        tc = self.txt_color
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == 'tbc':
                    tbc = value
                elif key == 'tc':
                    tc = value
                    
        self.sub_kw_list_frame.destroy()
        self.sub_kw_list_frame = tk.Frame(self.kw_list_frame, background = tbc, borderwidth = 0, highlightthickness = 0)
        self.sub_kw_list_frame.grid(row = 0, column = 0, sticky = 'ns')
        countr = 0; r = 0; c = 0

        for item in sorted(keys_to_be_updated):
            if countr < 2:
                key_button = tk.Button(self.sub_kw_list_frame, text = ('.').join(item.split('.')[:-1]),
                                        fg = tc, bg = tbc, command = lambda i = item: self.update_textbox(i))
                key_button.grid(row = r, column = c, sticky = 'nsew')
                if c == 0:
                    c = 1; countr += 1
                else:
                    c = 0; r += 1; countr += 1   
            else:
                key_button = tk.Button(self.sub_kw_list_frame, text = ('.').join(item.split('.')[:-1]),
                                        fg = tc, bg = tbc, command = lambda i = item: self.update_textbox(i))
                key_button.grid(row = r, column = c, sticky = 'nsew')
                if c == 0:
                    c = 1
                else:
                    c = 0; r += 1; countr = 0
    #~~~~~~~~~~~~~~~~~~~< Lock/Unlock Library >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def search_textbox(self, event = None):
        self.root.text.tag_delete("search")
        self.root.text.tag_configure("search", background="green")
        start = "1.0"
        if len(self.search_entry.get()) > 0:
            try:
                self.root.text.mark_set("insert", self.root.text.search(self.search_entry.get(), start, nocase = 1))
                self.root.text.see("insert")
                while True:
                    pos = self.root.text.search(self.search_entry.get(), start, 'end', nocase = 1)
                    if pos == "": 
                        break       
                    start = pos + "+%dc" % len(self.search_entry.get()) 
                    self.root.text.tag_add("search", pos, "%s + %dc" % (pos, len(self.search_entry.get())))
            except:
                print("String not in text box!")
        else:
            print("Nothing here but us chickens!")

    def next_match(self, event = None):
        while self.root.text.compare("insert", "<", "end") and "search" in self.root.text.tag_names("insert"):
            self.root.text.mark_set("insert", "insert+1c")
        next_match = self.root.text.tag_nextrange("search", "insert")
        if next_match:
            self.root.text.mark_set("insert", next_match[0])
            self.root.text.see("insert")
        return "break"

    def prev_match(self, event = None):
        while self.root.text.compare("insert", "<", "end") and "search" in self.root.text.tag_names("insert"):
            self.root.text.mark_set("insert", "insert-1c")
        prev_match = self.root.text.tag_prevrange("search", "insert")
        if prev_match:
            self.root.text.mark_set("insert", prev_match[0])
            self.root.text.see("insert")
        return "break"
    #< Scroll Bar >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.v_scroll_bar = tk.Scrollbar(self.text_frame, command = root.text.yview)
        self.v_scroll_bar.grid(row = 0, column = 2, columnspan = 1, rowspan = 1, padx = 0, pady = 0, sticky = 'nse')
        self.h_scroll_bar = tk.Scrollbar(self.text_frame, orient="horizontal", command = root.text.xview)
        self.h_scroll_bar.grid(row = 1 , column = 0, columnspan = 1, rowspan = 1, padx = 0, pady = 0, sticky = 'sew')
        self.root.text.config(xscrollcommand=self.h_scroll_bar.set, yscrollcommand=self.v_scroll_bar.set)
    #< Toggle Word wrap >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    def toggle_word_wrap(self):
        if self.text_wordwrap == False:
            self.root.text.config(wrap = 'char')
            self.text_wordwrap = True
        else:
            self.root.text.config(wrap = 'none')
            self.text_wordwrap = False
    #< Menu function >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def do_nothing(self):
        pass

    def create_library_folder(self, Event=None):
        a_name = simpledialog.askstring("Create New Library", "Alphanumeric and '_' only", initialvalue = "Name_Here")
        if a_name != None:
            a_name.strip()
            valid_chars = "-_.() {}{}".format(ascii_letters, digits)
            self.valid_filename = ("".join(c for c in a_name if c in valid_chars)).replace(" ", "_").lower()
            if self.valid_filename != "" and self.valid_filename != "name_here":
                if self.valid_filename not in self.library_list:
                    os.mkdir("{}/{}".format(self.file_date_path, self.valid_filename))
                    self.library_menu()
                    self.get_immediate_subdirectories(self.file_date_path)
                else:
                    print ("Library already exist")
            else:
                print ("No Name Given")
            
    def create_note_in_current_library(self, Event=None):
        if os.path.basename(self.current_working_lib) != "MINT_REQUIRED_DATA_FOLDER" and os.path.basename(self.current_working_lib) != "file_data":   
            a_name = simpledialog.askstring("Create new note page!", "Alphanumeric and '_' only", initialvalue = "Name_Here")
            valid_chars = "-_.() {}{}".format(ascii_letters, digits)
            self.valid_filename = ("".join(c for c in a_name if c in valid_chars)).replace(" ", "_").lower()
            if self.valid_filename != "" and self.valid_filename != "name_here":
                if os.path.isfile('{}/{}.txt'.format(self.current_working_lib,self.valid_filename)) != True:
                    print("create new file")
                    with open('{}/{}.txt'.format(self.current_working_lib,self.valid_filename), "w") as new_note:
                        new_note.write("{}".format(self.valid_filename))
                    self.reset_quick_file_selections()
    
    def delete_current_note(self, Event=None):
        if self.current_file_path != "":
            passw = simpledialog.askstring("Verifying deletion request", "In order to delete {} please type DELETE in all caps.".format(os.path.basename(self.current_working_lib)), initialvalue = "")
            if passw == "DELETE":
                print("attempt to delete file!")
                try:
                    os.remove(self.current_file_path)
                    print("{} has been delete!".format(self.current_file_path))
                    self.reset_quick_file_selections()
                except:
                    print("File not found!")
                
    def delete_library_folder(self, Event=None):
        if os.path.basename(self.current_working_lib) != "MINT_REQUIRED_DATA_FOLDER" and os.path.basename(self.current_working_lib) != "file_data":
            answer = messagebox.askquestion("Deleting the {} Library!".format(os.path.basename(self.current_working_lib)), "Are you sure you want to delete the {} Library?".format(os.path.basename(self.current_working_lib)))
            if answer == "yes":
                passw = simpledialog.askstring("Verifying deletion request", "In order to delete {} please type DELETE in all caps.".format(os.path.basename(self.current_working_lib)), initialvalue = "")
                if passw == "DELETE":
                    print("attempt to delete")
                    shutil.rmtree("{}".format(self.current_working_lib), ignore_errors=False, onerror=None)
                    self.library_menu()
                    self.get_immediate_subdirectories(self.file_date_path)
                    self.current_working_lib = "./FileDirectory/file_data"
                else:
                    print("No Library has been deleted!")
            else:
                print("No Library has been deleted!")

    def library_menu(self):
        fpath = "./FileDirectory/MINT_REQUIRED_DATA_FOLDER/ThemePage.txt"
        self.theme_options = []
        with open (fpath, "r") as f:
            d = f.read(); theme_dict = json.loads(d)
            for key in theme_dict:
                self.theme_options.append(key)
        self.menu = tk.Menu(self.root)
        self.root.config(menu = self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = "File", menu = self.file_menu)
        self.file_menu.add_command(label = "New Note", command = self.create_note_in_current_library)
        self.file_menu.add_command(label = "Delete Note", command = self.delete_current_note)
        self.file_menu.add_command(label = "Save", command = self.do_nothing)
        self.file_menu.add_separator()
        self.file_menu.add_command(label = "Exit", command = lambda: self.close_program())
        self.lib_menu = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = "Libraries", menu = self.lib_menu)
        self.lib_menu.add_command(label = "New Library - Alpha", command = self.create_library_folder)
        self.lib_menu.add_command(label = "Lock/unlock Library - Not implemented", command = self.do_nothing)
        self.lib_menu.add_command(label = "Delete Library - Alpha", command = self.delete_library_folder)
        self.lib_menu.add_separator()
        self.pref_menu = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = "Preferences", menu = self.pref_menu)
        for name in self.theme_options:
            self.pref_menu.add_command(label = name, command=lambda x=name:self.apply_new_theme(x))
        self.lib_menu.add_separator()
        self.pref_menu.add_command(label = "Toggle Word-Wrap", command = self.do_nothing)
        self.help_menu = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = "Help", menu = self.help_menu)
        self.help_menu.add_command(label = "Info", command = self.do_nothing)
        self.site_menu = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = "Bookmark's", menu = self.site_menu)
        with open("./SupportFiles/url_list", "r") as f:
            url_list = json.load(f)
            for site in url_list:
                self.site_menu.add_command(label = "%s" % (site), command = lambda url = url_list[site]: webbrowser.open_new(url))
    #~~~~~~~~~~~~~~~~~~~< Close >~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def close_program(self):     
        if self.current_working_lib == '':
            self.root.destroy()
        else:
            self.close_program_else()

    def close_program_else(self):
        if self.root.text.edit_modified() != False:
            answer = messagebox.askquestion("Leaving MINT?", "Are you sure you want to leave MINT?")
            if answer == "yes":
                answer = messagebox.askquestion("Save work?", "Would you like to save before you exit MINT?")
                if answer == "yes":
                    print("append notes now")
                    self.append_notes()
                    self.root.destroy()
                else:
                    self.root.destroy()
            else:
                messagebox.showinfo("MINTy Fresh!", "Welcome Back XD")
        else:
            self.root.destroy()

    def status_clock(self):
        self.status_e.config(text ="{}".format(strftime("%H:%M:%S")))
        self.status_w.config(text = "Operation Status: Currently editing {}".format(self.current_working_keys))
        self.status_e.after(1000, lambda: self.status_clock())
    #~~~~~~~~~~~~~~~~~~~< Preset Themes >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def mint_theme_default(self, main_bg, text_bg, txt_color, bg_image):
        self.currentTextColor = txt_color
        themebg_image = tk.PhotoImage(file = bg_image)
        self.text_frame.config(bg = text_bg)
        self.entrybg_image.config(image = themebg_image)
        self.entrybg_image.image = themebg_image
        self.kw_bg_image.config(image = themebg_image)
        self.kw_bg_image.image = themebg_image
        self.bg_lable.config(image = themebg_image)
        self.bg_lable.image = themebg_image
        self.root.config(bg = main_bg)
        self.root.text.config(bg = text_bg, fg = txt_color)
        self.search_entry.config(fg = txt_color, bg = text_bg)
        #self.keyword_entry.config(fg = txt_color, bg = text_bg)
        self.status_frame.config(bg = text_bg)
        self.status_e.config(fg = txt_color, bg = text_bg)
        self.status_w.config(fg = txt_color, bg = text_bg)
        self.search_label.config(fg = txt_color, bg = text_bg)
        #self.keyword_label.config(fg = txt_color, bg = text_bg)
        self.update_keywords_button.config(fg = txt_color, bg = text_bg)
        #self.update_kw_display(tbc = text_bg, tc = txt_color)
    #~~~~~~~~~~~~~~~~~~< Custom Scroll Bar >~~~~~~~~~~~~~~~~~~~
        self.v_scroll_bar = MyScrollbar(self.text_frame, width = 15, command = root.text.yview,
                                        troughcolor = text_bg, buttontype = 'square',
                                        thumbcolor = txt_color, buttoncolor = main_bg)
        self.v_scroll_bar.grid(row = 0, column = 2, columnspan = 1,
                               rowspan = 1, padx = 0, pady = 0, sticky = 'nse')
        self.root.text.configure(yscrollcommand = self.v_scroll_bar.set)
        self.v_scroll_bar.config(background = main_bg)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.h_scroll_bar = MyScrollbar(self.text_frame, height = 15, command = root.text.xview,
                                        orient = 'horizontal', troughcolor = text_bg,
                                        buttontype = 'square', thumbcolor = txt_color,
                                        buttoncolor = main_bg)
        self.h_scroll_bar.grid(row = 1 , column = 0, columnspan = 1,
                               rowspan = 1, padx = 0, pady = 0, sticky = 'sew')
        self.root.text.configure(xscrollcommand = self.h_scroll_bar.set)
        self.h_scroll_bar.config(background = main_bg)
    #~~~~~~~~~~~~~~~~~~< Theme Manager >~~~~~~~~~~~~~~~~~~~~~~~~
    def apply_new_theme(self, key_name):
        fpath = "./FileDirectory/MINT_REQUIRED_DATA_FOLDER/ThemePage.txt"
        with open (fpath, "r") as f:
            d = f.read()
            theme_dict = json.loads(d)
            for key in theme_dict:
                if key_name == key:
                    self.mint_theme_default(theme_dict[key][0],
                    theme_dict[key][1], theme_dict[key][2], theme_dict[key][3])

if __name__ == "__main__":
    root = tk.Tk() 
    MyApp = MintApp(root)
    tk.mainloop()