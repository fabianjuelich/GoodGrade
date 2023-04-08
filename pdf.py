from fpdf import FPDF
import db
import datetime
import webbrowser
import os

def print2pdf():

    table = db.select()

    # config
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()

    # icon
    pdf.set_xy(10, 10)
    pdf.image('./icons8-grades-100.png', w=20, h=20)
    # title
    pdf.set_xy(32, 10)
    pdf.set_font('Helvetica', 'b', 32)
    pdf.cell(100, 20, 'GoodGrade')
    #link
    pdf.link(10, 10, 85, 18, 'https://github.com/fabianjuelich/gg-goodgrade')

    # info name
    pdf.set_xy(120, 12)
    pdf.set_font('Helvetica', 'b', 18)
    pdf.cell(40, 10, 'Date:')
    pdf.set_xy(120, 20)
    pdf.cell(40, 10, 'Average:')
    # info value
    pdf.set_xy(160, 12)
    pdf.set_font('Helvetica', '', 18)
    pdf.cell(40, 10, str(datetime.date.today()))
    pdf.set_xy(160, 20)
    pdf.cell(40, 10, str(round(db.avg(), 2)))

    # col
    pdf.set_xy(10, 45)
    pdf.set_font('Helvetica', 'b', 16)
    pdf.cell(103, 16, 'Module')
    pdf.cell(40, 16, 'Grade', align='r')
    pdf.cell(40, 16, 'CP', align='r')
    # row
    pdf.set_xy(10, 60)
    pdf.set_font('Helvetica', '', 12)
    for no, row in enumerate(table, 1):
        pdf.cell(103, 7, str(row[0]))
        pdf.cell(40, 7, str(row[1]), align='r')
        pdf.cell(40, 7, str(row[2]), align='r')
        pdf.set_xy(10, 60 + 7*no)

    pdf.output('test.pdf')
    webbrowser.open_new(rf'{os.path.abspath("test.pdf")}')
