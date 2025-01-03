import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pdfkit

# Function to fetch student's name, SGPA, fail status, and detailed result URL for a given registration number
async def fetch_student_data(session, registration_number):
    url = f"http://results.beup.ac.in/ResultsBTech6thSem2024_B2021Pub.aspx?Sem=VI&RegNo={registration_number}"
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            soup = BeautifulSoup(await response.text(), 'html.parser')

            # Fetch student name
            name_span = soup.find("span", id="ContentPlaceHolder1_DataList1_StudentNameLabel_0")
            student_name = name_span.text.strip() if name_span else "N/A"

            # Fetch SGPA
            sgpa_span = soup.find("span", id="ContentPlaceHolder1_DataList5_GROSSTHEORYTOTALLabel_0")
            sgpa = sgpa_span.text.strip() if sgpa_span else "N/A"

            # Fetch fail status
            remark_span = soup.find("span", id="ContentPlaceHolder1_DataList3_remarkLabel_0")
            fail_status = remark_span.text.strip() if remark_span and "FAIL" in remark_span.text else "PASS"

            # Construct the detailed result URL
            detailed_result_url = f"http://results.beup.ac.in/ResultsBTech6thSem2024_B2021Pub.aspx?Sem=VI&RegNo={registration_number}"

            return registration_number, student_name, sgpa, fail_status, detailed_result_url
    except Exception as e:
        print(f"Error fetching data for {registration_number}: {e}")
        return registration_number, "Error", "Error", "Error", "Error"

# Fetch data concurrently using asyncio and aiohttp
async def fetch_all_students_concurrently(registration_numbers):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_student_data(session, reg_no) for reg_no in registration_numbers]
        student_data = await asyncio.gather(*tasks)
    return student_data

# Generate registration numbers
def generate_registration_numbers():
    registration_numbers = list(range(21105117001, 21105117059 + 1))  # Range 1
    registration_numbers.extend(range(22105117901, 22105117907 + 1))  # Range 2
    registration_numbers.append(22105117008)  # Single number (Range 3)
    return registration_numbers

# Function to generate PDF from student data
def generate_pdf(student_data):
    html_content = """
    <html>
    <head>
        <title>Student Results</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 30px;
            }
            h1 {
                text-align: center;
                color: #4CAF50;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            table, th, td {
                border: 1px solid #ddd;
            }
            th, td {
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #4CAF50;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            a {
                color: #4CAF50;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>SGPA Report: 6th Sem CSE (2021 - 2025)</h1>
        <table>
            <tr>
                <th>Registration Number</th>
                <th>Name</th>
                <th>SGPA</th>
                <th>Remarks</th>
                <th>Detailed Result</th>
            </tr>
    """
    # Add rows to the table
    for data in student_data:
        registration_number, student_name, sgpa, fail_status, detailed_result_url = data
        html_content += f"""
        <tr>
            <td>{registration_number}</td>
            <td>{student_name}</td>
            <td>{sgpa}</td>
            <td>{fail_status}</td>
            <td><a href="{detailed_result_url}" target="_blank">View Result</a></td>
        </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    # Use pdfkit to generate the PDF from the HTML content
    try:
        # Set the path for wkhtmltopdf executable
        wkhtmltopdf_path = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        # Generate the PDF
        pdfkit.from_string(html_content, "SGPA_Report6thSem.pdf", configuration=config)
        print("PDF successfully generated: student_results_with_urls.pdf")
    except Exception as e:
        print(f"An error occurred while generating the PDF: {e}")

# Main script to fetch data asynchronously and generate PDF
async def main():
    registration_numbers = generate_registration_numbers()
    student_data = await fetch_all_students_concurrently(registration_numbers)

    # Debugging: Print fetched data
    for data in student_data:
        print(f"Fetched data: {data}")

    # Generate PDF from the fetched data
    generate_pdf(student_data)

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
