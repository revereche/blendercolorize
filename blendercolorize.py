import os
import bpy
import subprocess
scn = bpy.context.scene


#specify the names of the folders you're keeping colors #and lineart in, and where you want final art output to, respectively
colordir = "color"
lineartdir = "lineart"
finaldir = "final"


#specify where those folders are found
#outputs to render directory by default
output_path = scn.render.filepath


#specify the frames you want
render_frames = [0,1,2]


#if you just want frames 0-10 or any other range,
#uncomment and use the below
#render_frames = range(10)


#set to a decimal between 0 and 1
#larger values ignore gaps more
blur = "0.5"


#you should be good to go!


raw = """\
-repeat {$!/2} \
--to_rgba[0] -split_opacity. -+.. 1 -!=. 0 -*[-2,-1] \
--norm[1] -n. 0,1 --histogram. 2,0,1 \
-if {i(0)>i(1)} -*.. -1 -+.. 1 -endif -rm. \
-b. \
""" + blur + """\
% -watershed.. [-1] -rm. -rm[0] -rm[0] \
-done \
"""


rawArr = []
for i in raw.split(" "):
    rawArr.append(i)


def formatPath(f, number, name):
     return output_path + name + "/" + formatNumbers(f, number) + ".png"


def formatNumbers(number, length):
    return '%0*d' % (length, number)


def formatArr(f, color, lineart, arr):
    arr.append("-i")
    arr.append(formatPath(f, 4, color))
    arr.append(formatPath(f, 4, lineart))
    


arr = []


if os.name == 'nt':
    arr.append("gmic.exe")
else:
    arr.append("gmic")


for f in render_frames:
    formatArr(f, colordir, lineartdir, arr)


arr = arr + rawArr    
arr.append("-o")
arr.append(formatPath(f, 3, finaldir))


#print(arr)
subprocess.Popen(arr)
