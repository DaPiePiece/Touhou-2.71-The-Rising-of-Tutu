# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 14:19:26 2019

@author: user
"""

import cx_Freeze as cx

executables = [cx.Executable("v2.0.py")]

cx.setup(
        name = "Touhou 2.71 The Final Tutu",
        options = {"build_exe": {"packages":["pygame"],
                                 "include_files":["background.png","bfairy.png","bossmusic.mp3","gfairy.png","hit.wav","playerdata.txt","Reimu_small.png","rfairy.png","sans.png","stagemusic.mp3"]}},
        executables = executables
        
        )