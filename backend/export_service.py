"""
Export service for generating reports in various formats.
"""
from typing import Dict, List
import json
import csv
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

class ExportService:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def to_json(self, data: Dict) -> str:
        """
        Export analysis results to JSON format.
        
        Args:
            data (Dict): Analysis results to export
            
        Returns:
            str: JSON string
        """
        return json.dumps(data, indent=2)

    def to_csv(self, data: Dict) -> str:
        """
        Export analysis results to CSV format.
        
        Args:
            data (Dict): Analysis results to export
            
        Returns:
            str: CSV string
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow(['URL', 'Title', 'Status', 'Content Length', 'Topics', 'Key Points'])
        
        # Write data
        if isinstance(data, list):
            # Batch analysis results
            for item in data:
                self._write_csv_row(writer, item)
        else:
            # Single analysis result
            self._write_csv_row(writer, data)
        
        return output.getvalue()

    def _write_csv_row(self, writer: csv.writer, data: Dict):
        """Helper method to write a single row of analysis data to CSV"""
        if data.get('status') == 'success':
            analysis = data.get('analysis', {})
            content = data.get('content', {})
            writer.writerow([
                data.get('url', 'N/A'),
                content.get('title', 'N/A'),
                data.get('status', 'N/A'),
                len(content.get('main_content', '')),
                self._extract_topics(analysis),
                self._extract_key_points(analysis)
            ])

    def to_pdf(self, data: Dict) -> bytes:
        """
        Export analysis results to PDF format.
        
        Args:
            data (Dict): Analysis results to export
            
        Returns:
            bytes: PDF document
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        elements.append(Paragraph("Web Content Analysis Report", title_style))
        elements.append(Spacer(1, 12))
        
        # Add timestamp
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 12))

        if isinstance(data, list):
            # Batch analysis results
            for item in data:
                elements.extend(self._create_pdf_section(item, styles))
        else:
            # Single analysis result
            elements.extend(self._create_pdf_section(data, styles))

        doc.build(elements)
        return buffer.getvalue()

    def _create_pdf_section(self, data: Dict, styles: Dict) -> List:
        """Helper method to create PDF elements for a single analysis"""
        elements = []
        
        if data.get('status') == 'success':
            content = data.get('content', {})
            analysis = data.get('analysis', {})
            
            # URL and title
            elements.append(Paragraph(f"URL: {data.get('url')}", styles['Heading2']))
            elements.append(Paragraph(f"Title: {content.get('title')}", styles['Heading3']))
            elements.append(Spacer(1, 12))
            
            # Content statistics
            stats_data = [
                ['Content Length', str(len(content.get('main_content', '')))],
                ['Links Found', str(len(content.get('links', [])))],
                ['Analysis Status', data.get('status')]
            ]
            
            stats_table = Table(stats_data, colWidths=[200, 300])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(stats_table)
            elements.append(Spacer(1, 12))
            
            # AI Analysis
            if analysis:
                elements.append(Paragraph("AI Analysis", styles['Heading3']))
                elements.append(Paragraph(str(analysis.get('analysis', 'No analysis available')), styles['Normal']))
            
            elements.append(Spacer(1, 20))
        
        return elements

    def _extract_topics(self, analysis: Dict) -> str:
        """Extract topics from AI analysis"""
        if isinstance(analysis, dict) and 'analysis' in analysis:
            text = analysis['analysis']
            if 'Topics:' in text:
                topics_section = text.split('Topics:')[1].split('\n')[0]
                return topics_section.strip()
        return 'N/A'

    def _extract_key_points(self, analysis: Dict) -> str:
        """Extract key points from AI analysis"""
        if isinstance(analysis, dict) and 'analysis' in analysis:
            text = analysis['analysis']
            if 'Key points:' in text:
                points_section = text.split('Key points:')[1].split('\n')[0]
                return points_section.strip()
        return 'N/A'

