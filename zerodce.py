import torch
import torch.nn as nn
import torchvision
import torch.backends.cudnn as cudnn
import torch.optim
import os
import sys
import argparse
import time
import zeromodel
import numpy as np
from torchvision import transforms
from PIL import Image
import glob
import time

def lowlight(image_path):
	scale_factor = 12
	data_lowlight = Image.open(image_path)
	data_lowlight = (np.asarray(data_lowlight)/255.0)
	data_lowlight = torch.from_numpy(data_lowlight).float()
	h=(data_lowlight.shape[0]//scale_factor)*scale_factor
	w=(data_lowlight.shape[1]//scale_factor)*scale_factor
	data_lowlight = data_lowlight[0:h,0:w,:]
	data_lowlight = data_lowlight.permute(2,0,1)
	data_lowlight = data_lowlight.unsqueeze(0)
	#data_lowlight = data_lowlight.cuda().unsqueeze(0)
	DCE_net = zeromodel.enhance_net_nopool(scale_factor)
	#DCE_net = model.enhance_net_nopool(scale_factor).cuda()
	DCE_net.load_state_dict(torch.load('DL/model/zero_dce/Epoch99.pth',map_location=torch.device('cpu')))
	#start = time.time()
	enhanced_image,params_maps = DCE_net(data_lowlight)
	#end_time = (time.time() - start)
	#print(end_time)
	torchvision.utils.save_image(enhanced_image, image_path)
