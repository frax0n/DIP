# USAGE
# python opencv_inpainting.py --image examples/example01.png --mask examples/mask01.png

# import the necessary packages
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
	help="path input image on which we'll perform inpainting")
ap.add_argument("-m", "--mask", type=str, required=True,
	help="path input mask which corresponds to damaged areas")
ap.add_argument("-a", "--method", type=str, default="telea",
	choices=["telea", "ns"],
	help="inpainting algorithm to use")
ap.add_argument("-r", "--radius", type=int, default=3,
	help="inpainting radius")
ap.add_argument("-interpolation","--interpol",type=str,default="INTER_LINEAR",help="Interpolation method to be selected")
args = vars(ap.parse_args())

# initialize the inpainting algorithm to be the Telea et al. method
flags = cv2.INPAINT_TELEA

# check to see if we should be using the Navier-Stokes (i.e.,Bertalmio
# et al.) method for inpainting
if args["method"] == "ns":
	flags = cv2.INPAINT_NS

# load the (1) input image (i.e., the image we're going to perform
# inpainting on) and (2) the  mask which should have the same input
# dimensions as the input image -- zero pixels correspond to areas
# that *will not* be inpainted while non-zero pixels correspond to
# "damaged" areas that inpainting will try to correct
image = cv2.imread(args["image"])
mask = cv2.imread(args["mask"])
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

# perform inpainting using OpenCV
output = cv2.inpaint(image, mask, args["radius"], flags=flags)
scale_percent = 220 # percent of original size
width = int(output.shape[1] * scale_percent / 100)
height = int(output.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image

if args["interpol"]== "INTER_CUBIC":
	resized = cv2.resize(output, dim, interpolation = cv2.INTER_CUBIC)
else :
    resized = cv2.resize(output, dim, interpolation = cv2.INTER_LINEAR)




# show the original input image, mask, and output image after
# applying inpainting
cv2.imshow("Image", image)
cv2.imshow("Mask", mask)
cv2.imshow("Image restored", output)
cv2.imshow("Output", resized)
status = cv2.imwrite('python_grey.png',resized)
cv2.waitKey(0)
