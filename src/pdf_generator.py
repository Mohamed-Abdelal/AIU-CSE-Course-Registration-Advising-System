from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

class PDFGenerator:
    def __init__(self):
        self.output_dir = "reports"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_report(self, student_info, recommendations, explanations):
        filename = f"{self.output_dir}/{student_info['student_id']}_report.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        story.append(Paragraph("AIU Course Registration Report", title_style))
        story.append(Spacer(1, 20))

        # Student Information
        story.append(Paragraph("Student Information", styles['Heading2']))
        student_data = [
            ["Student ID", student_info['student_id']],
            ["Name", student_info['name']],
            ["Email", student_info['email']],
            ["Level", student_info['level']],
            ["Date", student_info['registration_date']]
        ]
        student_table = Table(student_data, colWidths=[2*inch, 4*inch])
        student_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 6)
        ]))
        story.append(student_table)
        story.append(Spacer(1, 20))

        # Course Recommendations
        story.append(Paragraph("Recommended Courses", styles['Heading2']))
        if recommendations:
            course_data = [["Course Code", "Course Name", "Credits"]] + [
                [r["Course Code"], r["Course Name"], str(r["Credits"])]
                for r in recommendations
            ]
            course_table = Table(course_data, colWidths=[2*inch, 3*inch, 1*inch])
            course_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('PADDING', (0, 0), (-1, -1), 6)
            ]))
            story.append(course_table)
            story.append(Spacer(1, 20))

            # Total Credits
            total_credits = sum(r["Credits"] for r in recommendations)
            total_style = ParagraphStyle(
                'TotalStyle',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=20,
                textColor=colors.darkblue
            )
            story.append(Paragraph(f"Total Credit Hours: {total_credits}", total_style))
            story.append(Spacer(1, 20))

        # Explanations
        story.append(Paragraph("Recommendation Explanations", styles['Heading2']))
        for explanation in explanations:
            exp_style = ParagraphStyle(
                'ExplanationStyle',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=10,
                leftIndent=20
            )
            story.append(Paragraph(explanation, exp_style))
            story.append(Spacer(1, 5))

        # Footer
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=1  # Center alignment
        )
        story.append(Spacer(1, 30))
        story.append(Paragraph("AIU CSE Course Registration System", footer_style))
        story.append(Paragraph("Generated on: " + student_info['registration_date'], footer_style))

        # Build PDF
        doc.build(story)
        return filename 