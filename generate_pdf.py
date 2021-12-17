from fpdf import FPDF


class PDF(FPDF):
    pass


pdf = PDF()
pdf.add_page()
pdf.output('coles_bay.pdf','F')
