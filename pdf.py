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
    pdf.image('Assets/icons8-grades-100.png', w=20, h=20)
    # title
    pdf.set_xy(32, 10)
    pdf.set_font('Helvetica', 'b', 32)
    pdf.cell(100, 20, 'GoodGrade')
    #link
    pdf.link(10, 10, 85, 18, 'https://github.com/fabianjuelich/gg-goodgrade')

    # header
    # name
    pdf.set_xy(120, 12)
    pdf.set_font('Helvetica', 'b', 18)
    pdf.cell(40, 10, 'Date:')
    pdf.set_xy(120, 20)
    pdf.cell(40, 10, 'Average:')
    # value
    pdf.set_xy(160, 12)
    pdf.set_font('Helvetica', '', 18)
    pdf.cell(40, 10, str(datetime.date.today()))
    if table:
        pdf.set_xy(160, 20)
        pdf.cell(40, 10, str(round(db.avg(), 2)))

    # grade list
    # col
    pdf.set_xy(10, 45)
    pdf.set_font('Helvetica', 'b', 16)
    pdf.cell(103, 16, 'Course')
    pdf.cell(40, 16, 'Grade', align='r')
    pdf.cell(40, 16, 'Factor', align='r')
    # row
    if table:
        pdf.set_xy(10, 60)
        pdf.set_font('Helvetica', '', 12)
        for no, row in enumerate(table, 1):
            pdf.cell(103, 7, str(row[0]))
            pdf.cell(40, 7, str(row[1]), align='r')
            pdf.cell(40, 7, str(row[2]), align='r')
            pdf.set_xy(10, 60 + 7*no)

    # save
    file = f'gg_{datetime.date.today()}.pdf'
    pdf.output(file)
    # open
    webbrowser.open_new(os.path.abspath(file))
