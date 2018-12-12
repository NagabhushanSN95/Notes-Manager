# Image to PDF Generator

This script renames the scanned images in the `Images` directory using the data given in `Bookmarks` file. Then it 
scales the images to A4 size and converts the images into PDFs using `imagemagick` tool. Then it merges the individual 
PDF files into a single PDF file using `pdftk` tool. Then it adds meta-data and bookmarks from the respective files 
into the PDF file.

   So, in brief, this script generates a full-fledged PDF notes from scanned images.

## Dependencies
* python2
* imagemagick
* pdftk

## Meta-Data
* Default file-name is `Meta-Data.txt`
* Currently only _Title_ and _Author_ meta-datas are supported.

### Meta-Data Format:
```
Title
<TITLE>
Author
<AUTHOR>
```

## Bookmarks
* Default file-name is `Bookmarks.txt`
* You can specify titles, sub-titles, sub-sub-titles to any level. The level is determined based on braces.
* You can either specify number-of-pages and offset or specific-page-numbers or a combination of both.
* Every object be it titles, page-numbers, braces should be on a separate line.
* Every level starts with a `{` and ends with `}`.
* While specifying _number-of-pages_ and _offset_, _number-of-pages_ should be first and then _offset_.
* If _offset_ is specified, then page numbers will start from the next value after _offset_
* Default value for _offset_ is 0
* Blank lines, Indentations, trailing or leading white spaces have no effect.

### Bookmark format with example
```
{
    <TITLE 01>
    {
        <SUB-TITLE 01>
        {
            NumPages = 3
            Offset = 0
        }
        <SUB-TITLE 02>
        {
            PageNos = 3,4,6,7,9
        }
    }
    <TITLE 02>
    {
        NumPages = 5
        Offset = 2
    }
}
```

## How To Use it?
* First clone this repository and change your directory. Execute this in a terminal

  ```
  git clone https://github.com/NagabhushanSN95/Notes-Manager.git
  cd Notes-Manager/03\)\ Image\ to\ PDF\ Generator/ 
  ```
* Now copy your scanned images to this `Images` directory
* Create 2 new text files and write your `meta-data` and `bookmarks` in the given format
* Run the python program by executing the following command in the terminal
  ```
  python2 Image_To_PDF_Generator.py -md Meta-Data.txt -b Bookmarks.txt -d ./Images/
  ```
* This creates a new pdf file `<TITLE>.pdf` with your bookmarks.
* If you need to rotate all your images by a certain degree (clockwise), you can pass it using the rotate (-r) option
  ```
  python2 Image_To_PDF_Generator.py -md Meta-Data.txt -b Bookmarks.txt -d ./Images/ -r 90
  ```

### Note
* If you've saved Meta-Data, Bookmarks, Images in the default names, you can omit passing them as arguments.
* When passing meta-data or bookmarks file-names as arguments, autocomplete will not work. If you want the 
autocomplete to work, then execute the below command in terminal and then run the python program as shown
  ```
  chmod u+x Image_To_PDF_Generator.py
  ./Image_To_PDF_Generator.py -md Meta-Data.txt -b Bookmarks.txt -d ./Images/
  ```
* If bookmarks are not added in the PDF file, please check if your `pdftk` version is greater than 1.45
