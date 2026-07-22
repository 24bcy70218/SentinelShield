from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

REPORT_FOLDER = "reports"


def generate_security_report(system, alert_count, alerts):

    os.makedirs(REPORT_FOLDER, exist_ok=True)

    filename = datetime.now().strftime(
        "Security_Report_%Y%m%d_%H%M%S.pdf"
    )

    filepath = os.path.join(REPORT_FOLDER, filename)

    doc = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b><font size=18>SentinelShield Security Report</font></b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"Generated: {datetime.now()}",
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>System Status</b>", styles["Heading2"]))

    story.append(Paragraph(f"CPU Usage: {system['cpu']}%", styles["Normal"]))
    story.append(Paragraph(f"RAM Usage: {system['memory']}%", styles["Normal"]))
    story.append(Paragraph(f"Disk Usage: {system['disk']}%", styles["Normal"]))
    story.append(Paragraph(f"Processes: {system['processes']}", styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Security Summary</b>", styles["Heading2"]))

    story.append(
        Paragraph(
            f"Total Alerts: {alert_count}",
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Recent Alerts</b>", styles["Heading2"]))

    if alerts:
        for alert in alerts:
            story.append(
                Paragraph(
                    f"{alert['level']} - {alert['title']}<br/>{alert['message']}",
                    styles["Normal"]
                )
            )
    else:
        story.append(Paragraph("No alerts found.", styles["Normal"]))

    doc.build(story)

    return filename