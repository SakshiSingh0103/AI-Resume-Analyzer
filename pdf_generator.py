from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(
    filename,
    score,
    skills,
    missing_skills,
    feedback
):

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph("<b>AI Resume Analysis Report</b>", styles["Title"])
    )

    story.append(
        Paragraph(f"<b>ATS Match Score:</b> {score}%", styles["BodyText"])
    )

    story.append(
        Paragraph("<br/><b>Detected Skills</b>", styles["Heading2"])
    )

    for skill in skills:
        story.append(
            Paragraph(f"• {skill.title()}", styles["BodyText"])
        )

    story.append(
        Paragraph("<br/><b>Missing Skills</b>", styles["Heading2"])
    )

    if missing_skills:

        for skill in missing_skills:
            story.append(
                Paragraph(f"• {skill.title()}", styles["BodyText"])
            )

    else:
        story.append(
            Paragraph("No Missing Skills 🎉", styles["BodyText"])
        )

    story.append(
        Paragraph("<br/><b>AI Feedback</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(feedback.replace("\n", "<br/>"), styles["BodyText"])
    )

    pdf.build(story)