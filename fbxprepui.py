####################################################################################
# Kalev Mölder       2025       https://tinkering.ee        molder.kalev@gmail.com #
####################################################################################

# simple tkinter UI to choose the input and output fbx filepaths for the blender script

import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import sys
import json

SETTINGS_FILE = "settings.json"

blender_path = r"C:/Program Files/Blender Foundation/Blender 4.5/blender.exe"
blender_script_path = os.path.join(os.path.dirname(__file__), "fbxprep.py")

dialog_filetypes = [("Speed Tree FBX", "*.fbx")]

class PathParam(tk.Frame):
    def __init__(self, parent:tk.Widget, label:str, is_save_file:bool, on_change_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.var_path:tk.StringVar = tk.StringVar(self, "")
        self.on_change_callback = on_change_callback

        self.label:tk.Label = tk.Label(self, text=label)
        self.btn:tk.Button = tk.Button(self, text="...", command=self.set_path)
        self.text:tk.Entry = tk.Entry(self, textvariable=self.var_path)

        self.is_save_file:bool = is_save_file # whether to use the askopenfilename or asksaveasfilename function

        self.label.pack(side='left', padx=4)
        self.text.pack(side='left', expand=1, fill='x', padx=4)
        self.btn.pack(side='right', padx=4)

    def set_path(self):
        if self.is_save_file:
            selected_filepath = filedialog.asksaveasfilename(
                title="Select existing fbx file to use",
                filetypes=dialog_filetypes
            )
            if selected_filepath != "":
                self.var_path.set(selected_filepath)
                self.on_change_callback()
        else:
            selected_filepath = filedialog.askopenfilename(
                title="Select output fbx file location",
                filetypes=dialog_filetypes
            )
            if selected_filepath != "":
                self.var_path.set(selected_filepath)
                self.on_change_callback()
            else:
                print("invalid file path selected")


class FBXUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.input_file_path = PathParam(self, "input fbx path", False, self.validate)
        self.output_file_path = PathParam(self, "output fbx path", True, self.validate)

        self.input_file_path.pack(side='top', expand=1, fill='x', pady=4)
        self.output_file_path.pack(side='top', expand=1, fill='x', pady=4)

        self.btn_run = tk.Button(self, text="Run!", command=self.run)
        self.btn_run.config(state=tk.DISABLED)
        self.btn_run.pack(side="bottom", expand=1, fill='x', padx=4, pady=4)

        self.load_settings()

        self.validate() # mabye loaded paths are valid already

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                print(data)
                if "input_path" in data.keys():
                    self.input_file_path.var_path.set(data["input_path"])
                if "output_path" in data.keys():
                    self.output_file_path.var_path.set(data["output_path"])
    
    def save_settings(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(
                {
                    "input_path": self.input_file_path.var_path.get(),
                    "output_path": self.output_file_path.var_path.get()
                },
                f
            )
    
    def validate(self):
        if self.input_file_path.var_path.get() != "" and self.output_file_path.var_path.get() != "":
            self.btn_run.config(state=tk.NORMAL)
        else:
            self.btn_run.config(state=tk.DISABLED)
    
    def run(self):
        cmd = ' '.join([
            "\"%s\"" % (blender_path),
            "--background",
            "--python",
            "\"%s\"" % (blender_script_path),
            "--",
            "\"%s\"" % (self.input_file_path.var_path.get()),
            "\"%s\"" % (self.output_file_path.var_path.get())
        ])
        print("running command:\n\t"+cmd)

        process = subprocess.Popen(
            cmd,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        
        process.wait()

        print("\nFbx Preparation is Done!\n")

root = tk.Tk()
root.geometry("600x120")

uiframe = FBXUI(root)
uiframe.pack(fill='x', padx=4, pady=4, expand=1)

root.mainloop()

uiframe.save_settings()