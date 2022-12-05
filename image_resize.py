from PIL import Image
from os import getcwd
from math import gcd

print("image source (or drop image here) : ")
src = str(input()).strip()

# check if src have '' at the beginning and the end
if src[0] == "'" and src[-1] == "'" or src[0] == '"' and src[-1] == '"' :
    src = src[1:-1]                                                             # check https://stackoverflow.com/a/59394839 and https://python-reference.readthedocs.io/en/latest/docs/brackets/slicing.html 

# check if src is full path or just a name of the file
if "/" in src :
    src_split = src.split("/")
    src_path = src_split[0:-2]
    src_path = "/".join(src_path)
    src_path += '/'
    file_name = src_split[-1]
    full_path = True
else :
    full_path = False

print("where to save (or leave it empty to let me decide where to save) : ")
save_to = str(input()).strip()
print("what aspect ratio target (16:9, 21:9, 4:3) or leave it empty to retain original ratio :")
input_ratio = str(input()).strip()

# check if input_ratio is empty, if true get original aspect ratio
if not input_ratio :
    img = Image.open(src)
    fz = img.size
    greatest_common_divisor = gcd(fz[0],fz[1])      # visit https://www.w3schools.com/python/ref_math_gcd.asp
    w = str(fz[0]/greatest_common_divisor)
    h = str(fz[1]/greatest_common_divisor)
    input_ratio = w + ":" + h
    img = img.close()
     
# split the input
ratio_wh = input_ratio.split(":")

print("what is the height target : ")
target_height = int(input())
print("\n")

def resize(src, save_to, ratio_wh, ht):
    
    # to separate image name and extension to a list
    # incase if someone put ./this/kind/of/path/here.jpeg
    if "./" in src:
        s = src.split('./')
        name_ext = s[1].split('.')
    else:
        if full_path :
            name_ext = file_name.split('.')
        else :
            name_ext = src.split('.')

    if name_ext[1].upper() == 'JPG':
        name_ext[1] = 'JPEG'

    wt = target_width_resolver(ratio_wh, target_height)         # wt : width target
    ht = int(ht)                                                # ht : height target

    # check if save_to is empty and src is not full path, if so get current working directory
    if 'src_path' in locals() :
        print("image saved to " + src_path)
    else:
        if not save_to :
            save_to = getcwd()        
            print("image saved to " + "/resized_" + save_to + name_ext[0]+ "." +name_ext[1])
        else :
            print("image saved to " + "/resized_" + save_to + name_ext[0]+ "." +name_ext[1])

    img = Image.open(src)
    new_img = img.resize([wt,ht])
    new_img.save(save_to+"/resized_"+name_ext[0],name_ext[1])
    img = img.close()
    new_img = new_img.close()


def target_width_resolver(whr, h):              # whr : width height ratio, h : height in number (720, 1080, etc)
    wr = float(whr[0])                          # width ratio
    hr = float(whr[1])                          # height ratio
    return int((h/hr)*wr)                       #return result in integer 

resize(src, save_to, ratio_wh, target_height)
