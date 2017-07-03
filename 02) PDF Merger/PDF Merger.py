# Merging pdfs

import os

cmd = "pdftk "
for fileName in sorted(os.listdir("./PDFs")):
	fileName1 = fileName.replace(" ", "\ ")
	cmd += "./PDFs/" + fileName1 + " "
cmd += "output merged.pdf"
print "Executing Command: " + cmd
os.system(cmd)
