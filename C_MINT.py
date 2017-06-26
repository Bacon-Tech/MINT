import json
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from os import listdir
from time import strftime
import tkinter.messagebox
from string import ascii_letters, digits
from MINT.myscrollbar import MyScrollbar #customer scroll bar

class MintApp(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.py_bg_color = "#{:02x}{:02x}{:02x}".format(0, 34, 64)
        self.py_frame_color = "#{:02x}{:02x}{:02x}".format(0, 23, 45)
        self.root.title("MINT: Mobile Information & Note-taking Tool")
        self.root.config(bg = self.py_frame_color)
        self.root.columnconfigure(0, weight = 0)
        self.root.columnconfigure(1, weight = 1)
        self.root.rowconfigure(0, weight = 0)
        self.root.rowconfigure(1, weight = 1)
        self.main_bg_color = "#%02x%02x%02x" % (64,89,82)
        self.text_bg_color = "#%02x%02x%02x" % (0, 23, 45)
        self.txt_color = "#%02x%02x%02x" % (175, 167, 157)
        #~~~~~~~~~~~~~~~~~~~< Variables Defaults >~~~~~~~~~~~~~~~~~~~~~~~
        self.path = "./NotesKeys/"
        self.color_path = "./Colors/"
        self.notebook = dict()
        self.compare_notebook = dict()
        self.current_working_lib = ""
        self.current_working_keys = ""
        self.list_of_all_filenames = []
        self.current_working_button_color = "orange"
        self.selected_text_color = "orange"
        self.selected_bg_color = "#%02x%02x%02x"
        self.post_update = False
        self.text_wordwrap = False
        self.valid_filename = ""
        self.current_keyword = ""
        self.compare_recent_keyword = ""
        self.text_is_edited = False
        #~~~~~~~~~~~~~~~~~~~< USE TO open all files in Directory >~~~~~~
        with open("{}{}".format(self.path, "list_of_all_filenames"), "r") as listall:
            self.list_of_all_filenames = json.load(listall)

        self.open_files_in_path(self.path)
        self.open_files_in_path_compare(self.path)
        self.base_bg_image = tk.PhotoImage(file = "./Colors/pybgbase.png")
        self.bg_lable = tk.Label(self.root, image= self.base_bg_image)
        self.bg_lable.place(x = 0, y = 0)
        
        self.bg_lable.config(image = self.base_bg_image)
        self.bg_lable.image = self.base_bg_image
        self.current_text_color = 'orange'

        self.text_frame = tk.Frame(root, borderwidth = 0,
                                   highlightthickness = 0)
        self.text_frame.grid(row = 0, column = 1, columnspan = 1,
                             rowspan = 2, padx = 0, pady = 0, sticky = 'nsew')
        
        self.text_frame.columnconfigure(0, weight = 1)
        self.text_frame.rowconfigure(0, weight = 1)
        self.text_frame.columnconfigure(1, weight = 0)
        self.text_frame.rowconfigure(1, weight = 0)
        
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.grid(row = 0, column = 0, columnspan = 1,
                              rowspan = 1, padx = 0, pady = 0, sticky = 'nsew')
        
        self.entry_frame.columnconfigure(0, weight = 0)
        self.entry_frame.columnconfigure(1, weight = 0)
        self.entry_frame.rowconfigure(0, weight = 0)
        self.entry_frame.rowconfigure(1, weight = 0)
        self.entry_frame.rowconfigure(2, weight = 0)
        
        self.entrybg_image = tk.Label(self.entry_frame,
                                      image = self.base_bg_image,
                                      borderwidth = 0, highlightthickness = 0)
        
        self.entrybg_image.image = self.base_bg_image
        self.entrybg_image.place(x = 0, y = 0)
        self.entrybg_image.config(image = self.base_bg_image)
        
        self.kw_list_frame = tk.Frame(self.root, borderwidth = 0, highlightthickness = 0)
        self.kw_list_frame.grid(row = 1, column = 0, columnspan = 1, rowspan = 1,
                                padx = 0, pady = 0, sticky = 'nsew')
        self.kw_list_frame.columnconfigure(0, weight = 1)
        
        self.sub_kw_list_frame = tk.Frame(self.kw_list_frame, borderwidth = 0,
                                          highlightthickness = 0)
        self.sub_kw_list_frame.grid(row = 0, column = 0, sticky = 'nsew')
        
        
        
        self.kw_bg_image = tk.Label(self.kw_list_frame,
                                    image= self.base_bg_image,
                                    borderwidth = 0, highlightthickness = 0)
        
        self.kw_bg_image.image = self.base_bg_image
        self.kw_bg_image.place(x = 0, y = 0)
        self.kw_bg_image.config(image = self.base_bg_image)
        
        self.root.text_side_left = tk.Text(self.kw_list_frame,
                                           width = 10, height = 20)
        
        #self.root.text_side_left.place( x = 5, y = 5)
        self.root.text_side_left.config(wrap = 'none')
        self.root.text_side_right = tk.Text(self.kw_list_frame,
                                            width = 10, height = 20)
        
        #self.root.text_side_right.place( x = 95, y = 5)
        self.root.text_side_right.config(wrap = 'none')
        
        self.status_frame = tk.Frame(root)
        self.status_frame.config(bg = self.py_frame_color)
        self.status_frame.grid(row = 3, column = 0,columnspan = 2,
                               rowspan = 3, padx =0, pady =0, sticky = 'nsew')
        
        self.status_frame.columnconfigure(0, weight = 1)
        self.status_frame.columnconfigure(1, weight = 1)
        self.status_frame.rowconfigure(0, weight = 0)
        
        self.root.text = tk.Text(self.text_frame, undo = True)
        self.root.text.bind('<Key>', self.is_text_edited)
        self.root.text.grid(row = 0, column = 0,columnspan = 1,
                            rowspan = 1, padx = 0, pady = 0, sticky = 'nsew')
        
        self.root.text.config(bg = self.py_frame_color, fg = "white",
                              font = ('times', 16), insertbackground = "orange")
        
        self.root.text.config(wrap = 'none')
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.status_w = tk.Label(self.status_frame,
                                 font=("times", 16, "bold"),
                                 fg = "white", bg = "black",
                                 relief = 'sunken', anchor = 'w')
        
        self.status_w.grid(row = 0, column = 0, padx = 1, pady = 1, sticky = 'sw')
        self.status_w.config(text = "Operation Status",
                             bg = "#%02x%02x%02x" % (0, 23, 45))
        
        self.status_e = tk.Label(self.status_frame, 
                                 font=("times", 16, "bold"),
                                 fg = "white", bg = "black",
                                 relief = 'sunken', anchor = 'e')
        
        self.status_e.grid(row = 0, column = 1, padx = 1, pady = 1, sticky = 'se')
        self.status_e.config(bg = "#%02x%02x%02x" % (0, 23, 45))
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.search_label = tk.Label(self.entry_frame)
        self.search_label.grid(row = 1, column = 0, padx = 5, pady = 5)
        self.search_label.config(text = "Search Text Field")
        
        self.search_entry = tk.Entry(self.entry_frame, width = 20)
        self.search_entry.bind("<Return>", self.search_textbox)
        self.search_entry.bind("<Shift-Return>", self.next_match)
        self.search_entry.bind("<Control-Return>", self.prev_match)
        self.search_entry.grid(row = 1, column = 1, padx = 5, pady = 5)
        
        self.keyword_label = tk.Label(self.entry_frame)
        self.keyword_label.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.keyword_label.config(text = "Keyword Search")
        
        self.keyword_entry = tk.Entry(self.entry_frame, width = 20)
        self.keyword_entry.bind("<Return>", self.kw_entry)
        self.keyword_entry.grid(row = 0, column = 1, padx = 5, pady = 5)
        
        self.update_keywords_button = tkinter.Button(self.entry_frame,
                                                     fg = 'Black', bg = 'Orange',
                                                     text = "Update Notes",
                                                     command = self.append_notes)

        self.update_keywords_button.grid(row = 2, column = 0, padx = 5, pady = 5)

        self.library_menu()
        self.mint_theme_default(self.main_bg_color, self.text_bg_color,
                        self.txt_color, tk.PhotoImage(file = "./Colors/pybgbase.png"))
        self.status_clock()
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
    
    def is_text_edited(self,*args):
        if self.text_is_edited == False:
            self.text_is_edited = True
            
    def open_files_in_path(self, path):
        for filename in listdir(path):
            with open("{}{}".format(path, filename), "r") as f:
                self.notebook[filename] = json.load(f)
        self.compare_notebook = self.notebook

        
    def open_files_in_path_compare(self, path):
        for filename in listdir(path):
            with open("{}{}".format(path, filename), "r") as f:
                self.compare_notebook[filename] = json.load(f)
        print("Did This Print Anything?: {}".format(self.compare_notebook))

    def new_lib_prompt(self):
        a_name = simpledialog.askstring("Create New Note Library",
                                           "Alphanumeric and '_' only",
                                           initialvalue = "Name_Here")
        
        valid_chars = "-_.() {}{}".format(ascii_letters, digits)
        self.valid_filename = ("".join(c for c in a_name if c in valid_chars)).replace(" ", "_").lower()
        if self.valid_filename != "" and self.valid_filename != "name_here":
            if self.valid_filename not in self.list_of_all_filenames:
                self.create_notes_and_keys(self.valid_filename)
                self.list_of_all_filenames.append(self.valid_filename)
                with open("%s%s"%(self.path, "list_of_all_filenames"), "r+" ) as f:
                        json.dump(self.list_of_all_filenames, f, indent = "")
                self.library_menu()
            else:
                print ("Library already exist")
        else:
            print ("No Name Given")
    
    def create_notes_and_keys(self, name):
        n_name = name+"_notes"
        k_name = name+"_keys"
        with open("./NotesKeys/default_notes", "r") as n:
            n_base = json.load(n)
        with open("./NotesKeys/default_keys", "r") as k:
            k_base = json.load(k)
        with open("%s%s" % (self.path,n_name), "w") as new_n:
            json.dump(n_base, new_n, indent = "")
        with open("%s%s" % (self.path,k_name), "w") as new_k:
            json.dump(k_base, new_k, indent = "")
        self.open_files_in_path(self.path, self.notebook, "list_of_all_filenames")
    #~~~~~~~~~~~~~~~~~~~< UPDATE keyword display >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def update_kw_display(self, **kwargs):
        list_to_pass = ["chose a library",
                        " chose a library_keys",
                        "chose a library_notes",
                        ""]
        
        tbc = self.text_bg_color
        tc = self.txt_color
        
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == 'tbc':
                    tbc = value
                elif key == 'tc':
                    tc = value
     
        if self.current_working_keys not in list_to_pass:
            keys_to_be_updated = self.notebook[self.current_working_keys]
            self.root.text_side_left.delete(1.0, "end-1c")
            self.root.text_side_right.delete(1.0, "end-1c")
            self.sub_kw_list_frame.destroy()
            self.sub_kw_list_frame = tk.Frame(self.kw_list_frame, background = tbc,
                                              borderwidth = 0, highlightthickness = 0)
            self.sub_kw_list_frame.grid(row = 0, column = 0, sticky = 'ns')
            countr = 0
            r = 0
            c = 0
            for item in keys_to_be_updated:
                if countr < 2:
                    key_button = tk.Button(self.sub_kw_list_frame, text = item, fg = tc, bg = tbc,
                                           command = lambda i = item: self.update_kw_entry_and_textbox(i))
                    key_button.grid(row = r, column = c, sticky = 'nsew')
                    if c == 0:
                        c = 1
                        countr += 1
                    else:
                        c = 0
                        r += 1
                        countr += 1   
                else:
                    key_button = tk.Button(self.sub_kw_list_frame, text = item, fg = tc, bg = tbc,
                                           command = lambda i = item: self.update_kw_entry_and_textbox(i))
                    key_button.grid(row = r, column = c, sticky = 'nsew')
                    if c == 0:
                        c = 1
                    else:
                        c = 0
                        r += 1
                        countr = 0
        else:
            print("In the list to pass")
            
    def update_kw_entry_and_textbox(self, i):
        self.keyword_entry.delete(0, tk.END)
        self.keyword_entry.insert(0, i)
        self.kw_entry()
        
        
#     def update_kw_display(self):
#         list_to_pass = ["chose a library",
#                         " chose a library_keys",
#                         "chose a library_notes",
#                         ""]
# 
#         if self.current_working_keys not in list_to_pass:
#             keys_to_be_updated = self.notebook[self.current_working_keys]
#             self.root.text_side_left.delete(1.0, "end-1c")
#             self.root.text_side_right.delete(1.0, "end-1c")
#             contr = 0
#             for item in keys_to_be_updated:
#                 if contr == 0:
#                     self.root.text_side_left.insert("end-1c",item + "\n")
#                     self.root.text_side_left.see("end-1c")
#                     contr = 1
#                 else:
#                     self.root.text_side_right.insert("end-1c",item + "\n")
#                     self.root.text_side_right.see("end-1c")
#                     contr = 0
#         else:
#             print("In the list to pass")
    #~~~~~~~~~~~~~~~~~~~< Search for words and highlight >~~~~~~~~~~~~~~~~~~~~~~~~
    def search_textbox(self, event = None):
        self.root.text.tag_delete("search")
        self.root.text.tag_configure("search", background="green")
        start = "1.0"
        if len(self.search_entry.get()) > 0:
            self.root.text.mark_set("insert",
                                    self.root.text.search(self.search_entry.get(),
                                    start, nocase = None))
            
            self.root.text.see("insert")
            while True:
                pos = self.root.text.search(self.search_entry.get(),
                                            start, 'end',
                                            nocase = None) 
                if pos == "": 
                    break       
                start = pos + "+%dc" % len(self.search_entry.get()) 
                self.root.text.tag_add("search", pos,
                                       "%s + %dc" % (pos, len(self.search_entry.get())))
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
    #~~~~~~~~~~~~~~~~~~~< UPDATE selected_notes! >~~~~~~~~~~~~~~~~~~~
    def lock_unlock_libs(self):
        with open("./NotesKeys/locked_libraries","r+") as f:
            ll = json.load(f)
        if self.current_working_lib in ll:
            working_list = ll[self.current_working_lib]
            if working_list[0] == "yes":
                lock_unlock = messagebox.askquestion("MINT Lock Manager", "This library is locked for editing. Do you want to unlock this library?")
                if lock_unlock =="yes":
                    count = 0
                    while count < 3:
                        pass_attempt = simpledialog.askstring("MINT Lock Manager", "What is the password for this library?")
                        if pass_attempt == working_list[1]:
                            working_list[0]= "no"
                            with open("./NotesKeys/locked_libraries","r+") as f:
                                json.dump(ll, f, indent = "")
                            count = 3
                        else:
                            count += 1
                else:
                    return "locked"
                        
    def append_notes(self):
        check_lock = self.lock_unlock_libs()
        print(check_lock)
        if check_lock == "locked":
            print(check_lock)            
        else:
            e1_current = self.keyword_entry.get().lower()
            e1_all_case = self.keyword_entry.get()
            e2_current = self.root.text.get(1.0, "end-1c")
            answer = messagebox.askquestion("Update Notes!",
                                                    "Are you sure you want update your Notes for {} This cannot be undone!".format(e1_all_case))
            if answer == "yes":
                if e1_current in self.notebook[self.current_working_lib]:
                    self.status_e.config(text = "Updating Keyword & Notes for the {} Library!".format(self.current_working_lib))
                    
                    dict_to_be_updated = self.notebook[self.current_working_lib]
                    dict_to_be_updated[e1_current] = e2_current
                    with open("%s%s" % (self.path, self.current_working_lib),"w") as working_temp_var:
                        json.dump(dict_to_be_updated, working_temp_var, indent = "")
                    self.status_e.config(text = "Update Complete")          
                else:
                    self.status_e.config(text= "Creating New Keyword & Notes for the {} Library!".format(self.current_working_lib))
                    
                    dict_to_be_updated = self.notebook[self.current_working_lib]
                    dict_to_be_updated[e1_current] = e2_current
                    with open("%s%s" % (self.path, self.current_working_lib), "w" ) as working_temp_var:
                        json.dump(dict_to_be_updated, working_temp_var, indent = "")
                    keys_to_be_updated = self.notebook[self.current_working_keys]
                    keys_to_be_updated.append(e1_all_case)
                    with open("{}{}".format(self.path, self.current_working_keys),
                              "w" ) as working_temp_keys:
                        
                        json.dump(keys_to_be_updated, working_temp_keys, indent = "")
                    self.status_e.config(text = "Update Complete")
                self.update_kw_display()            
            else:
                messagebox.showinfo("...", "That was close!")      
    #~~~~~~~~~~~~~~~~~~~< Entry Widget >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def kw_entry(self, event = None):
        e1_current = self.keyword_entry.get().lower()
        if self.current_keyword == e1_current:
            print("Already editing current keyword")
            self.compare_recent_keyword = e1_current
        else:
            if self.root.text.edit_modified() == False:
            # if self.root.text.compare("end-1c", "==", "1.0"):
                self.update_text_box(e1_current)
                self.compare_recent_keyword = e1_current
                self.root.text.edit_modified(False)
            else:
                answer = messagebox.askquestion("Changing Notes!",
                    "Are you sure you want change the current Notes section to {}? Any unsaved changed will be lost!".format(e1_current))
                if answer == "yes":
                    self.update_text_box(e1_current)
                    
                else:
                    print("pass")
    
    def update_text_box(self, e1_current):
        if self.current_working_lib in self.notebook:
            note_var = self.notebook[self.current_working_lib]
            if e1_current in note_var:
                self.root.text.delete(1.0, "end-1c")
                self.root.text.insert("end-1c", note_var[e1_current])
                self.root.text.see("end-1c")
                self.current_keyword = e1_current
            else:
                self.root.text.delete(1.0, "end-1c")
                self.root.text.insert("end-1c", "Not a Keyword")
                self.root.text.see("end-1c")
                self.current_keyword = e1_current
        else:
            self.root.text.delete(1.0, "end-1c")
            self.root.text.insert("end-1c", "No Library Selected")
            self.root.text.see("end-1c")
    #~~~~~~~~~~~~~~~~~~~< Preset Themes >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    
    def mint_theme_default(self, main_bg, text_bg, txt_color, bg_image):
        self.currentTextColor = txt_color
        themebg_image = bg_image
        self.text_frame.config(bg = text_bg)
        self.entrybg_image.config(image = themebg_image)
        self.entrybg_image.image = themebg_image
        self.kw_bg_image.config(image = themebg_image)
        self.kw_bg_image.image = themebg_image
        self.bg_lable.config(image = themebg_image)
        self.bg_lable.image = themebg_image
        self.root.config(bg = main_bg)
        self.root.text.config(bg = text_bg, fg = txt_color)
        self.root.text_side_left.config(bg = text_bg, fg = txt_color)
        self.root.text_side_right.config(bg = text_bg, fg = txt_color)
        self.search_entry.config(fg = txt_color, bg = text_bg)
        self.keyword_entry.config(fg = txt_color, bg = text_bg)
        self.status_frame.config(bg = text_bg)
        self.status_e.config(fg = txt_color, bg = text_bg)
        self.status_w.config(fg = txt_color, bg = text_bg)
        self.search_label.config(fg = txt_color, bg = text_bg)
        self.keyword_label.config(fg = txt_color, bg = text_bg)
        self.update_keywords_button.config(fg = txt_color, bg = text_bg)
        self.update_kw_display(tbc = text_bg, tc = txt_color)
    #~~~~~~~~~~~~~~~~~~< Custom Scroll Bar >~~~~~~~~~~~~~~~~~~~
        self.v_scroll_bar = MyScrollbar(self.text_frame, width = 15,
                                        command = root.text.yview,
                                        troughcolor = text_bg,
                                        buttontype = 'square',
                                        thumbcolor = txt_color,
                                        buttoncolor = main_bg)
        
        self.v_scroll_bar.grid(row = 0, column = 2, columnspan = 1,
                               rowspan = 1, padx = 0, pady = 0, sticky = 'nse')
        
        self.root.text.configure(yscrollcommand = self.v_scroll_bar.set)
        self.v_scroll_bar.config(background = main_bg)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.h_scroll_bar = MyScrollbar(self.text_frame, height = 15,
                                        command = root.text.xview,
                                        orient = 'horizontal',
                                        troughcolor = text_bg,
                                        buttontype = 'square',
                                        thumbcolor = txt_color,
                                        buttoncolor = main_bg)
        
        self.h_scroll_bar.grid(row = 1 , column = 0, columnspan = 1,
                               rowspan = 1, padx = 0, pady = 0, sticky = 'sew')
        
        self.root.text.configure(xscrollcommand = self.h_scroll_bar.set)
        self.h_scroll_bar.config(background = main_bg)
    #~~~~~~~~~~~~~~~~~~< Theme Manager >~~~~~~~~~~~~~~~~~~~~~~~~
    def mint_theme1(self):
        self.main_bg_color = "#%02x%02x%02x" % (64, 89, 82)
        self.text_bg_color = "#%02x%02x%02x" % (17, 41, 41)
        self.txt_color = "#%02x%02x%02x" % (175, 167, 157)
        bg_image = tk.PhotoImage(file = "./Colors/theme1bg.png")
        self.mint_theme_default(self.main_bg_color, self.text_bg_color, self.txt_color, bg_image)

    def mint_theme2(self):
        self.main_bg_color = "#%02x%02x%02x" % (14, 51, 51)
        self.text_bg_color = "#%02x%02x%02x" % (4, 22, 22)
        self.txt_color = "#%02x%02x%02x" % (223, 171, 111)
        bg_image = tk.PhotoImage(file="./Colors/theme2bg.png")
        self.mint_theme_default(self.main_bg_color, self.text_bg_color, self.txt_color, bg_image)
        
    #~~~~~~~~~~~~~~~~~~~< Toggle Wordwrap >~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    def toggle_word_wrap(self):
        if self.text_wordwrap == False:
            self.root.text.config(wrap = 'char')
            self.text_wordwrap = True
        else:
            self.root.text.config(wrap = 'none')
            self.text_wordwrap = False
    #~~~~~~~~~~~~~~~~~~~< Menu function >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def update_working_lib_keys(self, filename):
        self.current_keyword = ''
        self.current_working_lib = "{}_notes".format(filename).lower()
        self.current_working_keys = "{}_keys".format(filename).lower()
        self.update_kw_display()
    def do_nothing(self):
        pass
    def library_menu(self):
        self.menu = tk.Menu(self.root)
        self.root.config(menu = self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = "File", menu = self.file_menu)
        self.file_menu.add_command(label = "Save", command = self.do_nothing)
        self.file_menu.add_command(label = "Save As", command = self.do_nothing)
        self.file_menu.add_separator()
        self.file_menu.add_command(label = "Exit",
                                   command = lambda: self.close_program())
        
        self.lib_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label = "Note Libraries", menu = self.lib_menu)
        self.lib_menu.add_command(label = "Library Help Page - Not Implemented Yet",
                                  command = self.do_nothing)
        
        self.lib_menu.add_separator()
        self.lib_menu.add_command(label = "New Library",
                                  command = self.new_lib_prompt)
        
        self.lib_menu.add_command(label = "Lock Library - Not Implemented Yet",
                                  command = self.do_nothing)
        
        self.lib_menu.add_command(label = "Delete Library! - Not Implemented Yet",
                                  command = self.do_nothing)
        
        self.lib_menu.add_separator()
        
        self.pref_menu = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = "Preferences", menu = self.pref_menu)
        self.pref_menu.add_command(label = "Mint Theme 1",
                                   command = self.mint_theme1)
        
        self.pref_menu.add_command(label = "Mint Theme 2",
                                   command = self.mint_theme2)
        
        self.lib_menu.add_separator()
        self.pref_menu.add_command(label = "Toggle Word-Wrap",
                                   command = self.toggle_word_wrap)
        
        self.help_menu = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = "Help", menu = self.help_menu)
        self.help_menu.add_command(label = "Info", command = self.do_nothing)
    
        for filename in self.list_of_all_filenames:
            self.lib_menu.add_command(label = "%s" % (filename),
                command = lambda filename = filename: self.update_working_lib_keys(filename))
    #~~~~~~~~~~~~~~~~~~~< Close >~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def close_program(self):     
        if self.current_working_lib == '':
            self.root.destroy()
        else:
            self.close_program_else()

    def close_program_else(self):
        answer = tkinter.messagebox.askquestion("Leaving MINT?",
            "Are you sure you want to leave MINT")
        if answer == "yes":
            answer = tkinter.messagebox.askquestion("Save work?",
                "Would you like to save before you exit MINT?")
            if answer == "yes":
                self.append_notes
                self.root.destroy()
            else:
                self.root.destroy()
        else:
            tkinter.messagebox.showinfo("MINTy Fresh!",
                                        "Welcome Back XD")

    def status_clock(self):
        self.status_e.config(text ="{}".format(strftime("%H:%M:%S")))
        self.status_e.after(200, lambda: self.status_clock())


if __name__ == "__main__":
    root = tk.Tk() 
    MyApp = MintApp(root)

    tk.mainloop()
