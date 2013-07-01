import os
import sys

ROOTPATH = os.path.dirname(__file__)
DISPATCHERSPATH = os.path.join(ROOTPATH, 'src/dispatchers')
CONTROLERPATH = os.path.join(ROOTPATH, 'src/controler')
MODELPATH = os.path.join(ROOTPATH, 'src/model')

sys.path.append(DISPATCHERSPATH)
sys.path.append(CONTROLERPATH)
sys.path.append(MODELPATH)

