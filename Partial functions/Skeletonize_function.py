
from skimage import io
from skimage.io import imread, imshow
from skimage.filters import threshold_minimum
from skimage.morphology import medial_axis, skeletonize
from skimage.transform import rescale
from skimage.util import invert
import matplotlib.pyplot as plt

import os
import numpy as np
from scipy import ndimage


image_gray = io.imread('/home/pi/Downloads/helpme/crack.jpg', as_gray=True)


image_gray = rescale(image_gray, 0.2, anti_aliasing=False)


image = invert(image_gray)


thresh_min =  threshold_minimum(image)
binary_min = image > thresh_min

fig, ax = plt.subplots(2, 2, figsize=(10, 10))

ax[0, 0].imshow(image, cmap=plt.cm.gray)
ax[0, 0].set_title('Original')

ax[0, 1].hist(image.ravel(), bins=256)
ax[0, 1].set_title('Histogram')

ax[1, 0].imshow(binary_min, cmap=plt.cm.gray)
ax[1, 0].set_title('Thresholded (min)')

ax[1, 1].hist(image.ravel(), bins=256)
ax[1, 1].axvline(thresh_min, color='r')

for a in ax[:, 0]:
    a.axis('off')
plt.show()

skeleton = skeletonize(binary_min)

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4),
                         sharex=True, sharey=True)

ax = axes.ravel()

ax[0].imshow(image_gray, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('original', fontsize=20)

ax[1].imshow(skeleton, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('skeleton', fontsize=20)

fig.tight_layout()
plt.show()

data = binary_min


skel, pixeldistance = medial_axis(data, return_distance=True)

maxnum = np.max(pixeldistance)
print("skeleton pixel distance : ", maxnum)

# Distance to the background for pixels of the skeleton


plt.figure(figsize=(8, 4))
plt.subplot(121)
plt.imshow(data, cmap=plt.cm.gray, interpolation='nearest')
plt.axis('off')
plt.subplot(122)
plt.imshow(dist_on_skel, cmap=plt.cm.gist_stern, interpolation='nearest')
plt.contour(data, [0.5], colors='w')
plt.axis('off')

plt.subplots_adjust(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0, right=1)
plt.show()
