from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import tempfile

class PDFGenerator:
    @staticmethod
    def create_leads_report(leads, duration: str):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf_path = tmp.name

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph(f"<b>Leads Report ({duration.upper()})</b>", styles["Title"]))
        elements.append(Spacer(1, 12))

        if not leads:
            elements.append(Paragraph("No leads found for this period.", styles["Normal"]))
        else:
            # Table header
            data = [["#", "Name", "Email", "Phone", "Source", "Status", "Created At"]]

            # Table data rows
            for i, lead in enumerate(leads, start=1):
                data.append([
                    str(i),
                    getattr(lead, "name", "-"),
                    getattr(lead, "email", "-"),
                    getattr(lead, "phone", "-"),
                    getattr(lead, "source", "-"),
                    getattr(lead, "status", "-"),
                    lead.created_at.strftime("%Y-%m-%d %H:%M") if lead.created_at else "-"
                ])

            # Table style
            table = Table(data, repeatRows=1)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.beige]),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 12))
            elements.append(Paragraph(f"<b>Total Leads:</b> {len(leads)}", styles["Normal"]))

        doc.build(elements)
        return pdf_path
