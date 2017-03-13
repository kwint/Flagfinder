# Quinty van Dijk
# With some help form pyimagesearch.com
# Program can recognize flags. Put a flag with the filename findme.png in the same folder as this file, then run in
# Make sure you also have the flags folder, if location of this folder is different please change the folder in line 12

from skimage.measure import compare_ssim
import cv2
import os
import numpy as np

# This is the folder where the flags are located
folder = "flags"

# Ignore MSE falues above:
MSE_threshold = 8000

# Ignore SSIM falues below:
SSIM_threshold = 0.2


# Gets flags from folder, returns them in a array with strings
def get_flags():
    flags = os.listdir(path=folder)
    print(flags)
    return flags


# Makes windows to show images
def init():
    print("Start init")
    cv2.WINDOW_AUTOSIZE

    cv2.namedWindow("flag", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("flag", 0, 0)


# Returns an flag
def get_img(flag):
    return cv2.imread(folder + "/" + str(flag))


# Calculates the MSE between to images, returns int
# Source: http://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = (imageA.astype("float") - imageB.astype("float")) ** 2
    err = np.sum(err)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

#Get amount of flags in flag folder
flags = get_flags()
flagNumber = 0
flagNumberMax = len(flags)

# Get flag that needs to be recognized, show it in a window
unknownflag = cv2.imread("findme.png")

# Making arrays to store calculations
StoreMSE = []
StoreSSIM = []

# Calculate the MSE and SSIM for every flag in the flag folder
print("Getting MSE and SSIM")
for flagNumber in range(0, flagNumberMax, 1):
    # Get flag from flag folder
    currentflag = get_img(flags[flagNumber])

    # Resize the unknownflag to the same size as flag from the flag folder
    height, width = currentflag.shape[:2]
    unknownflagresize = cv2.resize(unknownflag, (width, height))

    # Store and calculate MSE and SSIM. Multichannel is for colored images. Currently the libary scikit-image has bug
    # that returns a warning when using this. This can be ignored
    StoreMSE.append(mse(currentflag, unknownflagresize))
    StoreSSIM.append(compare_ssim(currentflag, unknownflagresize, multichannel=True))

# Find out which flag has the smallest MSE (= The most equal). Store it in an tuple with the MSE and de flagNumber
smallestMSE = StoreMSE[0], 0
for flagNumber in range(0, flagNumberMax):
    if smallestMSE[0] > StoreMSE[flagNumber]:
        smallestMSE = StoreMSE[flagNumber], flagNumber

# Find out which flag has the biggest MSE (= the most equal). Store it in an tuple with the SSIM and de flagNumber
biggestSSIM = StoreSSIM[0], 0
for flagNumber in range(0, flagNumberMax):
    if biggestSSIM[0] < StoreSSIM[flagNumber]:
        biggestSSIM = StoreSSIM[flagNumber], flagNumber

# If biggestSSIM and smallestMSE are the same flag, return perfect match, print flag to window
# If SSIM and MSE are smaller of bigger then threshold this is ignored
if biggestSSIM[1] == smallestMSE[1] and biggestSSIM[0] > SSIM_threshold and smallestMSE[0] < MSE_threshold:
    print("Perfect match")
    print("Flag is: ", flags[biggestSSIM[1]], "\nMSE:", smallestMSE[0], "\nSSIM: ", biggestSSIM[0])

# Else if the SSIM of the flag with the smallest MSE is bigger then the SSIM_threshold. Return the not so perferct match
elif StoreSSIM[smallestMSE[1]] > SSIM_threshold and smallestMSE[0] < MSE_threshold:
    print("Not so perfect match, but good enough. (MSE Based)")
    print("Flag is: ", flags[smallestMSE[1]], "\nMSE:", smallestMSE[0], "\nSSIM: ", StoreSSIM[smallestMSE[1]])

    print("flag with biggest SSIM:", flags[biggestSSIM[1]], biggestSSIM[0])

# Else if the MSE of the flag with the biggestSSIM is smaller than the MSE_threshold. Return the not so perfect match
elif StoreMSE[biggestSSIM[1]] < MSE_threshold and biggestSSIM[0] > SSIM_threshold:
    print("Not so perfect match, but good enough")
    print("Flag is: ", flags[biggestSSIM[1]], "\nMSE:", StoreMSE[biggestSSIM[1]], "\nSSIM: ", biggestSSIM[0])

    print("flag with smallestMSE:", flags[smallestMSE[1]], smallestMSE[0])

# Couldn't recognize flag
else:
    print("Can't find vlag!\nFlag with smallest MSE: ", flags[smallestMSE[1]], smallestMSE[0],
          "\nFlag with biggest SSIM: ", flags[biggestSSIM[1]], biggestSSIM[0])


# For debuging
# cv2.waitKey function would work better, but that doesn't work on linux
# if int(input("1 = print data:")) == 1:
#     for flagNumber in range(0, flagNumberMax):
#         print(flags[flagNumber], ": ", StoreMSE[flagNumber], " ssim: ", StoreSSIM[flagNumber])

cv2.destroyAllWindows()
