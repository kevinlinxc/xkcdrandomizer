# array = imageio.imread("https://imgs.xkcd.com/comics/e_to_the_pi_minus_pi.png")
# array = pad(array,1)
# plt.imshow(array ,cmap='Greys_r')
# cv2.imwrite("xkcd2.png", array)
# plt.show()
import xkcd


comic = xkcd.getRandomComic()
print(comic.__getattribute__("number"))
print(comic.getImageLink)