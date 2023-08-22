from fpdf import FPDF
import src.db as db
import datetime
import webbrowser
import os

def print2pdf():

    table = db.select()

    # config
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()

    # icon
    pdf.set_xy(10, 8)
    pdf.image(os.path.join(os.path.dirname(__file__), '../assets/icons8-grades-100.png'), w=20, h=20)
    # title
    pdf.set_xy(32, 8)
    pdf.set_font('Helvetica', 'b', 32)
    pdf.cell(86, 20, 'GoodGrade')
    #link
    pdf.link(10, 8, 86, 20, 'https://github.com/fabianjuelich/goodgrade')

    # header
    # name
    pdf.set_xy(120, 12)
    pdf.set_font('Helvetica', 'b', 18)
    pdf.cell(40, 10, 'Date:')
    pdf.set_xy(120, 20)
    pdf.cell(40, 10, 'Average:')
    pdf.set_xy(120, 28)
    pdf.cell(40, 10, 'Total:')
    # value
    pdf.set_xy(160, 12)
    pdf.set_font('Helvetica', '', 18)
    pdf.cell(40, 10, str(datetime.date.today()))
    if table:
        pdf.set_xy(160, 20)
        pdf.cell(40, 10, str(round(db.avg(), 2)))
        pdf.set_xy(160, 28)
        pdf.cell(40, 10, str(db.credits()))

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
