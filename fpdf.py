from fpdf import FPDF

name = input("Name: ")

pdf = FPDF()
pdf.add_page()

pdf.set_font("Times", size=24)
pdf.cell(0, 10, "CS50 Shirtificate", align="C")
pdf.ln(20)

pdf.image("shirtificate.png", x=40, y=60, w=130)

pdf.set_text_color(255, 255, 255)
pdf.set_xy(0, 90)

pdf.set_font("Times", "B", 24)
pdf.cell(0, 10, name, align="C")

pdf.output("shirtificate.pdf")