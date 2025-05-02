import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pdfkit
import os

# Semaphore to limit concurrent requests
MAX_CONCURRENT_REQUESTS = 20

# Fetch student data from the URL
async def fetch_student_data(session, semaphore, registration_number):
    url = f"https://results.beup.ac.in/ResultsBTech6thSem2024_B2021Pub.aspx?Sem=VI&RegNo={registration_number}"
    async with semaphore:
        try:
            async with session.get(url) as response:
                response.raise_for_status()  # Ensure the request was successful
                soup = BeautifulSoup(await response.text(), 'html.parser')

                # Extract Name
                name_span = soup.find("span", id="ContentPlaceHolder1_DataList1_StudentNameLabel_0")
                student_name = name_span.text.strip() if name_span else "N/A"

                # Extract CGPA and Remarks
                sgpa_table = soup.find("table", id="ContentPlaceHolder1_GridView3")
                semester_cgpa = ["NA"] * 8
                current_cgpa = "NA"
                if sgpa_table:
                    rows = sgpa_table.find_all("tr")
                    if len(rows) >= 2:
                        values = [td.text.strip() for td in rows[1].find_all("td")]
                        if len(values) == 9:
                            semester_cgpa = values[:8]
                            current_cgpa = values[8]

                # Extract Remarks
                remark_span = soup.find("span", id="ContentPlaceHolder1_DataList3_remarkLabel_0")
                remark = remark_span.text.strip() if remark_span else "N/A"

                return [registration_number, student_name, *semester_cgpa, current_cgpa, remark, url]
        except aiohttp.ClientError as e:
            print(f"Error fetching data for {registration_number}: {e}")
            return [registration_number, "Error", *["Error"] * 9, "Error", "Error"]
        except Exception as e:
            print(f"Error processing data for {registration_number}: {e}")
            return [registration_number, "Error", *["Error"] * 9, "Error", "Error"]

# Fetch all student data concurrently with a semaphore limit
async def fetch_all_students_concurrently(registration_numbers):
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)  # Limit concurrent requests
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_student_data(session, semaphore, reg_no) for reg_no in registration_numbers]
        return await asyncio.gather(*tasks)

# Generate the three specified ranges of registration numbers
def generate_registration_numbers():
    range1 = list(range(21105117001, 21105117060))  # 21105117001 to 21105117059
    range2 = list(range(22105117901, 22105117908))  # 22105117901 to 22105117907
    range3 = [22105117008]  # Just 22105117008
    return range1 + range2 + range3

# Generate the PDF report
def generate_pdf(student_data):
    html_content = """
    <html>
    <head>
        <title>Student Results</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            h1 {
                text-align: center;
                color: black;
                font-size: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                font-size: 12px;
            }
            th, td {
                border: 1px solid #000;
                padding: 6px;
                text-align: center;
            }
            th {
                background-color: #f2f2f2;
            }
            a {
                color: blue;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Marks Report: All Semesters | CSE | 2021-25</h1>
        <table>
            <tr>
                <th>Registration Number</th>
                <th>Name</th>
                <th>Semester I</th>
                <th>Semester II</th>
                <th>Semester III</th>
                <th>Semester IV</th>
                <th>Semester V</th>
                <th>Semester VI</th>
                <th>Semester VII</th>
                <th>Semester VIII</th>
                <th>Current CGPA</th>
                <th>Remarks (Most recent Semester)</th>
                <th>Detailed Result</th>
            </tr>
    """

    for data in student_data:
        (reg_no, name, sem1, sem2, sem3, sem4, sem5, sem6, sem7, sem8, cgpa, remark, url) = data
        html_content += f"""
            <tr>
                <td>{reg_no}</td>
                <td>{name}</td>
                <td>{sem1}</td>
                <td>{sem2}</td>
                <td>{sem3}</td>
                <td>{sem4}</td>
                <td>{sem5}</td>
                <td>{sem6}</td>
                <td>{sem7}</td>
                <td>{sem8}</td>
                <td>{cgpa}</td>
                <td>{remark}</td>
                <td><a href="{url}">View Result</a></td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    try:
        wkhtmltopdf_path = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'  # Adjust if needed
        if not os.path.exists(wkhtmltopdf_path):
            raise FileNotFoundError(f"wkhtmltopdf not found at {wkhtmltopdf_path}")

        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        options = {
            'orientation': 'Landscape',
            'page-size': 'A4',
            'encoding': 'UTF-8',
            'enable-local-file-access': ''
        }

        pdfkit.from_string(html_content, "Student_Result_Report97.pdf", configuration=config, options=options)
        print("PDF successfully generated in landscape: Student_Result_Report97.pdf")
    except Exception as e:
        print(f"Error generating PDF: {e}")



# Main function to run the script
async def main():
    reg_numbers = generate_registration_numbers()
    student_data = await fetch_all_students_concurrently(reg_numbers)
    
    for data in student_data:
        print(f"Fetched data: {data}")
    
    generate_pdf(student_data)

# Run the script
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        print(f"Error: {e}")
