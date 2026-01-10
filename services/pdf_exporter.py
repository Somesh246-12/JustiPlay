# services/pdf_exporter.py

from xhtml2pdf import pisa
from datetime import datetime
from jinja2 import Template
import io

def generate_pdf(result: dict, output_path: str):
    """
    Generate a professionally styled PDF report for legal document analysis.
    
    Args:
        result: Analysis result dictionary from document_analyzer
        output_path: Path where PDF should be saved
    """
    now = datetime.now().strftime("%d %b %Y, %H:%M")

    # Professional HTML template with inline CSS (xhtml2pdf compatible)
    template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {
                size: letter;
                margin: 1cm;
            }
            
            body {
                font-family: Arial, Helvetica, sans-serif;
                line-height: 1.6;
                color: #1a1a1a;
                font-size: 11pt;
            }
            
            .header {
                border-bottom: 3px solid #6366f1;
                padding-bottom: 15px;
                margin-bottom: 20px;
            }
            
            h1 {
                font-size: 24pt;
                font-weight: bold;
                color: #6366f1;
                margin: 0 0 5px 0;
            }
            
            .timestamp {
                font-size: 9pt;
                color: #6b7280;
            }
            
            h2 {
                font-size: 16pt;
                font-weight: bold;
                color: #1f2937;
                margin-top: 20px;
                margin-bottom: 10px;
                border-left: 4px solid #6366f1;
                padding-left: 10px;
            }
            
            .summary-section {
                background-color: #f9fafb;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 15px;
            }
            
            .doc-type {
                font-size: 10pt;
                color: #4b5563;
                margin-bottom: 8px;
            }
            
            .doc-type strong {
                color: #1f2937;
            }
            
            .summary-text {
                font-size: 10pt;
                color: #374151;
                line-height: 1.7;
                margin: 10px 0;
            }
            
            .risk-badge {
                display: inline-block;
                padding: 5px 12px;
                border-radius: 15px;
                font-size: 10pt;
                font-weight: bold;
                margin-top: 8px;
            }
            
            .risk-high {
                background-color: #fee2e2;
                color: #991b1b;
            }
            
            .risk-medium {
                background-color: #fef3c7;
                color: #92400e;
            }
            
            .risk-low {
                background-color: #d1fae5;
                color: #065f46;
            }
            
            .drivers-list {
                margin-left: 15px;
                margin-top: 8px;
            }
            
            .drivers-list li {
                margin-bottom: 6px;
                color: #374151;
                font-size: 10pt;
                line-height: 1.6;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                font-size: 9pt;
            }
            
            th {
                background-color: #6366f1;
                color: white;
                padding: 10px;
                text-align: left;
                font-weight: bold;
                font-size: 10pt;
            }
            
            td {
                padding: 10px;
                border-bottom: 1px solid #e5e7eb;
                vertical-align: top;
            }
            
            tr:nth-child(even) {
                background-color: #f9fafb;
            }
            
            .clause-title {
                font-weight: bold;
                color: #1f2937;
            }
            
            .footer {
                margin-top: 30px;
                padding-top: 15px;
                border-top: 2px solid #e5e7eb;
                text-align: center;
            }
            
            .disclaimer {
                font-size: 8pt;
                color: #6b7280;
                font-style: italic;
                line-height: 1.5;
            }
            
            .disclaimer strong {
                color: #991b1b;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>JustiPlay Legal Document Report</h1>
            <p class="timestamp">Generated: {{ timestamp }}</p>
        </div>

        <div class="summary-section">
            <h2>Document Summary</h2>
            <p class="doc-type"><strong>Document Type:</strong> {{ result.document_type }}</p>
            <p class="summary-text">{{ result.summary }}</p>
            <div>
                <strong style="font-size: 10pt; color: #1f2937;">Overall Risk Assessment:</strong>
                <span class="risk-badge risk-{{ result.overall_risk|lower }}">
                    {{ result.overall_risk }} Risk
                </span>
            </div>
        </div>

        <h2>Risk Drivers</h2>
        <ul class="drivers-list">
        {% for d in result.risk_drivers %}
            <li>{{ d }}</li>
        {% endfor %}
        </ul>

        <h2>Clause-by-Clause Analysis</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 25%;">Clause</th>
                    <th style="width: 12%;">Risk Level</th>
                    <th style="width: 63%;">Educational Suggestion</th>
                </tr>
            </thead>
            <tbody>
            {% for c in result.clauses %}
                <tr>
                    <td class="clause-title">{{ c.title }}</td>
                    <td>
                        <span class="risk-badge risk-{{ c.risk|lower }}">
                            {{ c.risk }}
                        </span>
                    </td>
                    <td>{{ c.suggestion }}</td>
                </tr>
            {% endfor %}
            </tbody>
        </table>

        <div class="footer">
            <p class="disclaimer">
                <strong>IMPORTANT DISCLAIMER:</strong><br>
                This report is for <strong>educational and awareness purposes only</strong>. 
                It does NOT constitute legal advice and does NOT create an attorney-client relationship.<br>
                For legal guidance specific to your situation, please consult a qualified legal professional.
            </p>
        </div>
    </body>
    </html>
    """)

    html_content = template.render(result=result, timestamp=now)
    
    # Generate PDF with xhtml2pdf
    try:
        with open(output_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(
                html_content,
                dest=pdf_file
            )
        
        if pisa_status.err:
            print(f"⚠️ PDF generation had errors")
        else:
            print(f"📄 PDF report generated: {output_path}")
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        raise
