from fpdf import FPDF

def generate_pdf(reviews):
    class PDF(FPDF):
        pass


    pdf = PDF()
    pdf.add_page()
    pdf.output('coles_bay.pdf','F')
