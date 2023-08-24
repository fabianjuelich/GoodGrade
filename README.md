# GoodGrade
![icons8-grades-100.png](./assets/icons8-grades-100.png)
## Easy-to-use desktop application that helps students manage their grades and export a list as a PDF file.

## Features
- __Add/edit grades__
- __View the current grade point average and total Credits__
- __Persistent storage__
- __Print overview as a PDF__

## Installation
1. Clone the repository to your local machine
2. Install the required dependencies by running `pip install -r requirements.txt`
3. Run the app using `python main.py` or optionally package with [pyinstaller.sh](pyinstaller.sh) (adjust library path to your machine) and make it executable

or visit the [download page](https://fabianjuelich.xyz/goodgrade) to download the __executables for Windows and Linux__. \
__Pro Tip:__ Configure the database path in the ___gg.ini___ that is created in the same folder as the application when you first start it, so you can store the data e.g. in your cloud, to sync the grades across devices.

## Usage
1. E.g. to add a grade, click the "Add" button to enter the Insert-mode (Similar procedure for other modes)
2. Enter a course and a grade (factor is optional) and click "OK" (Repeat for all grades and exit mode by pressing "Cancel")
4. The application will automatically calculate the average grade
5. Press the "PDF" button to print a list of all grades in PDF format (or select one in the drop down menu for insight)

## Screenshots
![appPreview](./preview/appPreview.png)

![pdfPreview](./preview/pdfPreview.png)

## Credits
- https://github.com/TomSchimansky/CustomTkinter
- https://github.com/PyFPDF/fpdf2
- https://github.com/gnikit/tkinter-tooltip
- https://icons8.com