#import libraries.
import sys,os
#set the correct path. this game needs both access to Graphics and Controllers.
cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd+"/patterns/Graphics/")
sys.path.append(cwd+"/patterns/Controllers/")
from SuperPixelBros import *
