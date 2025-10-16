from datetime import datetime, timedelta
from src.modules.reports.repository.export_repository import ExportRepository
from src.modules.reports.utils.pdf_generator import PDFGenerator

class ExportService:
    def __init__(self):
        self.repo = ExportRepository()

    async def generate_pdf(self, duration: str):
        now = datetime.utcnow()

        if duration == "1m":
            start_date = now - timedelta(days=30)
        elif duration == "6m":
            start_date = now - timedelta(days=180)
        elif duration == "1y":
            start_date = now - timedelta(days=365)
        else:
            raise ValueError("Invalid duration")

        # Fetch data
        data = await self.repo.get_data_by_date_range(start_date, now)

        # Generate PDF
        pdf_path = PDFGenerator.create_report(data, duration)

        return pdf_path
