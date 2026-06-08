"""
PDF Exporter - Convert markdown reports to formatted PDFs using xhtml2pdf.
"""
import os
import markdown
from xhtml2pdf import pisa
from datetime import datetime
from src.config.settings import settings
from src.utils.logger import app_logger


def export_to_pdf(
    markdown_content: str,
    topic: str,
    output_path: str = None,
) -> str:
    """
    Convert markdown report to PDF.
    
    Args:
        markdown_content: Report in markdown format
        topic: Report topic (used for filename)
        output_path: Optional custom output path
    
    Returns:
        Path to generated PDF file
    """
    app_logger.info(f"📄 Generating PDF for topic: '{topic}'")

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join(c if c.isalnum() or c in " -_" else "_" for c in topic)
    safe_topic = safe_topic[:50].strip()
    filename = f"{safe_topic}_{timestamp}.pdf"

    output_path = output_path or os.path.join(settings.reports_dir, filename)

    # Convert markdown to HTML
    html_content = markdown.markdown(
        markdown_content,
        extensions=['tables', 'fenced_code', 'toc', 'nl2br']
    )

    # Basic CSS inline in HTML for xhtml2pdf
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Research Report: {topic}</title>
        <style>
            @page {{
                margin: 2cm;
                @frame footer_frame {{
                    -pdf-frame-content: footer_content;
                    left: 50pt; width: 512pt; top: 772pt; height: 20pt;
                }}
            }}
            body {{
                font-family: Helvetica, Arial, sans-serif;
                font-size: 12pt;
                color: #333333;
                line-height: 1.5;
            }}
            h1 {{ color: #1a1a2e; border-bottom: 2px solid #4CAF50; padding-bottom: 5px; page-break-before: always; }}
            h1:first-of-type {{ page-break-before: avoid; }}
            h2 {{ color: #16213e; margin-top: 20px; margin-bottom: 10px; }}
            h3 {{ color: #0f3460; margin-top: 15px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 10px; }}
            th, td {{ border: 1px solid #dddddd; padding: 6px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            code {{ background-color: #f4f4f4; padding: 2px; font-family: monospace; }}
            .header-box {{
                background-color: #1a1a2e;
                color: #ffffff;
                padding: 20px;
                margin-bottom: 20px;
            }}
            .header-box h1 {{ color: #ffffff; border-bottom: none; }}
        </style>
    </head>
    <body>
        <div id="footer_content" style="text-align: right; font-size: 9pt; color: #666666;">
            Page <pdf:pagenumber> of <pdf:pagecount>
        </div>
        
        <div class="header-box">
            <h1>Research Report</h1>
            <p><strong>Topic:</strong> {topic}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime("%B %d, %Y %H:%M")}</p>
        </div>
        
        {html_content}
    </body>
    </html>
    """

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w+b") as result_file:
            # Convert HTML to PDF
            pisa_status = pisa.CreatePDF(
                full_html,
                dest=result_file
            )

        if pisa_status.err:
            raise Exception("PDF generation failed with internal xhtml2pdf errors.")

        app_logger.info(f"✅ PDF exported to: {output_path}")
        return output_path

    except Exception as e:
        app_logger.error(f"❌ PDF export failed: {e}")
        raise