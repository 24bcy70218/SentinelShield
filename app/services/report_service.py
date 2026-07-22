from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

from app.services.system_monitor import get_system_info
from app.services.network_monitor import get_network_status


def generate_report():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    REPORT_DIR = os.path.join(BASE_DIR, "reports")

    os.makedirs(REPORT_DIR, exist_ok=True)

    filename = os.path.join(
      REPORT_DIR,
      f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>SentinelShield Security Report</b>", styles["Title"]))
    elements.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            styles["Normal"],
        )
    )

    elements.append(Paragraph("<br/>", styles["Normal"]))

    system = get_system_info()
    network = get_network_status()

    elements.append(Paragraph("System Information", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    system_table = [
      ["Property", "Value"],
      ["CPU Usage", f"{system['cpu']} %"],
      ["Memory Usage", f"{system['memory']} %"],
      ["Disk Usage", f"{system['disk']} %"],
      ["Processes", system["processes"]],
      ["Hostname", system["hostname"]],
      ["Operating System", system["system"]],
      ["OS Release", system["release"]],
      ["Uptime", system["uptime"]],
    ]

    table = Table(system_table, colWidths=[180, 250])

    table.setStyle(TableStyle([
       ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
       ("TEXTCOLOR", (0,0), (-1,0), colors.white),
       ("GRID", (0,0), (-1,-1), 1, colors.grey),
       ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),
       ("BOTTOMPADDING", (0,0), (-1,0), 10),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("<br/>", styles["Normal"]))

    elements.append(Paragraph("Network Information", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    network_table = [
      ["Property", "Value"],
      ["Active Connections", network["active_connections"]],
      ["Listening Ports", network["listening_ports"]],
      ["Upload Speed", f"{network['upload_speed']} KB/s"],
      ["Download Speed", f"{network['download_speed']} KB/s"],
    ]

    table = Table(network_table, colWidths=[180, 250])

    table.setStyle(TableStyle([
      ("BACKGROUND", (0,0), (-1,0), colors.darkgreen),
      ("TEXTCOLOR", (0,0), (-1,0), colors.white),
      ("GRID", (0,0), (-1,-1), 1, colors.grey),
      ("BACKGROUND", (0,1), (-1,-1), colors.beige),
      ("BOTTOMPADDING", (0,0), (-1,0), 10),
    ]))

    elements.append(table)

    doc.build(elements)

    print("Saving report to:", filename)

    return filename