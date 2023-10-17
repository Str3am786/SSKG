import subprocess


def get_pdf_title(pdf_filename):
    """
    @Param pdf_filename: Name of the pdf for the title to be found
    :returns
    Title as string if found. Else None
    """
    # Runs the pdftitle module as a subprocess and communicate with it
    command = ['pdftitle', '-p', pdf_filename]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    stdout, _ = process.communicate(input=pdf_filename)

    # Extracts and returns the pdf title from stdout
    pdf_title = stdout.strip()
    return pdf_title