from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.enums import *
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from mnemonic import Mnemonic
wordlist = Mnemonic('english').wordlist

styleSheet = getSampleStyleSheet()

labelStyle = ParagraphStyle('llab', fontFace='courier', alignment=TA_RIGHT)
labelStyleCenter = ParagraphStyle('tlab', fontFace='courier', alignment=TA_CENTER)

hex_style = ParagraphStyle('tlab', fontName='Courier-Bold', alignment=TA_LEFT, fontSize=6, spaceAfter=2, spaceBefore=0, leading=4)
word_style = ParagraphStyle('cell', alignment=TA_CENTER, fontSize=8, spaceBefore=0, spaceAfter=0, leading=8)

def cell(w):
    assert 0 <= w < 0x800
    word = wordlist[w]
    hex = ('%03x' % w).upper()

    #rv = Paragraph(f'{word}\n<br/><font face="courier">{hex}</font>', cellStyle)
    rv = []
    rv.append(Paragraph(hex, hex_style))
    rv.append(Paragraph(word, word_style))

    return rv

def left_label(x):
    return Paragraph(x, labelStyle)
def top_label(x):
    return Paragraph(x, labelStyleCenter)

def doit(fname='wordlist.pdf'):
    doc = SimpleDocTemplate(fname, pagesize=landscape(letter))

    doc.leftMargin = doc.rightMargin =  \
    doc.topMargin = doc.bottomMargin = 0.1 * inch

    # container for the 'Flowable' objects
    elements = []

    rowlen = 16
    #data = [[''] + [ top_label('+%d' % i) for i in range(rowlen)]]
        #[left_label('0x%03x'%j)] + 
    data = [ 
            [cell(j+i) for i in range(0, rowlen)]
                for j in range(0, 0x800, rowlen) ]

    t = Table(data, repeatRows=0)
    t.setStyle(TableStyle([
        #('BACKGROUND',(1,1),(-2,-2),colors.green),
        #('TEXTCOLOR',(0,0),(0,-1),colors.red),
        #('VALIGN', (0,0),(0,-1), 'MIDDLE'),
        #('ALIGN', (0,0),(0,-1), 'RIGHT'),
        #('ALIGN', (0,0),(-1,0), 'CENTER'),
        ('LEFTPADDING', (0,0),(-1,-1), 2),
        ('RIGHTPADDING', (0,0),(-1,-1), 2),
        ('TOPPADDING', (0,0),(-1,-1), 0),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4.25),
        ('GRID', (0,0),(-1,-1), 0.5, colors.grey),
        ]),
    )
    elements.append(t)

    # write the document to disk
    doc.build(elements)

doit()
