from PIL import Image
import pytesseract
import argparse
import cv2
import os
import fpdf

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--name", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())
image = cv2.imread(args["name"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
if args["preprocess"] == "thresh":
	gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)

filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
#convert into pdf file 

pdf = fpdf.FPDF(format='letter')
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.multi_cell(200,7,txt=text, border = 0,align= 'J', fill= False)
pdf.output("test.pdf")
print("Thanks for Using it.")
exit()

# Usage
# python asmath.py --name images/image.png