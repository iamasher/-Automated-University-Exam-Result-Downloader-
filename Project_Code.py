import pdfkit

# Function to download the webpage as a PDF for a given registration number
def download_webpage_as_pdf(registration_number):
    url = f"http://results.beup.ac.in/ResultsBTech4thSem2023_B2021Pub.aspx?Sem=IV&RegNo={registration_number}"
    try:
        filename = f"web_page_{registration_number}.pdf"
        # Specify the full path to wkhtmltopdf executable
        wkhtmltopdf_path = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'  # Full path including the executable file
        pdfkit.from_url(url, filename, configuration=pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path))
        print(f"Downloaded webpage as PDF for registration number {registration_number}")
        return filename
    except Exception as e:
        print(f"Error downloading webpage as PDF for registration number {registration_number}: {e}")

# Specify the range of registration numbers to iterate over
start_registration_number = 21105117001  # Replace with the actual starting registration number
end_registration_number = 21105117003   # Replace with the actual ending registration number

# Loop to iterate over registration numbers and download webpages as PDFs
for registration_number in range(start_registration_number, end_registration_number + 1):
    download_webpage_as_pdf(registration_number)
