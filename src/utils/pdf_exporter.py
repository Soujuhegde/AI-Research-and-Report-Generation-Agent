"""
PDF Exporter - Convert markdown reports to formatted PDFs using WeasyPrint.
"""
import os
import markdown
from weasyprint import HTML, CSS
from datetime import datetime
from src.config.settings import settings
from src.utils.logger import app_logger


PDF_CSS = """
@page {
    margin: 2cm;
    @top-center {
        content: "Multi-Agent Research Report";
        font-size: 10pt;
        color: #666;
    }
    @bottom-right {
        content: counter(page);
        font-size: 10pt;
    }
}

body {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #333;
}

h1 { 
    color: #1a1a2e; 
    border-bottom: 3px solid #4CAF50; 
    padding-bottom: 10px;
    font-size: 24pt;
}

h2 { 
    color: #16213e; 
    border-left: 4px solid #4CAF50; 
    padding-left: 10px;
    font-size: 16pt;
    margin-top: 20pt;
}

h3 { color: #0f3460; font-size: 13pt; }

table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
}

th {
    background-color: #4CAF50;
    color: white;
    padding: 8px 12px;
    text-align: left;
}

td {
    padding: 8px 12px;
    border-bottom: 1px solid #ddd;
}

tr:nth-child(even) { background-color: #f9f9f9; }

code { 
    background: #f4f4f4; 
    padding: 2px 6px; 
    border-radius: 3px;
    font-family: monospace;
}

blockquote {
    border-left: 4px solid #4CAF50;
    margin: 10px 0;
    padding: 10px 20px;
    background: #f9f9f9;
}

a { color: #4CAF50; }

.header {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    color: white;
    padding: 30px;
    margin-bottom: 30px;
    border-radius: 8px;
}
"""


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

    # Wrap in full HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Research Report: {topic}</title>
    </head>
    <body>
        <div class="header">
            <h1>Research Report</h1>
            <p>Topic: {topic}</p>
            <p>Generated: {datetime.now().strftime("%B %d, %Y %H:%M")}</p>
            <p>Powered by Multi-Agent AI System</p>
        </div>
        {html_content}
    </body>
    </html>
    """

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        HTML(string=full_html).write_pdf(
            output_path,
            stylesheets=[CSS(string=PDF_CSS)]
        )

        app_logger.info(f"✅ PDF exported to: {output_path}")
        return output_path

    except Exception as e:
        app_logger.error(f"❌ PDF export failed: {e}")
        raise