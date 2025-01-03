# -Automated-University-Exam-Result-Downloader (Checkout V2 for updated code)-
"Automated University Result Downloader: A Python script to effortlessly fetch and download exam results from university websites, streamlining the process and saving time for students and administrators alike."
In the README.md section, you should provide a brief overview of your project, including its purpose, features, how to use it, and any relevant information for potential users or contributors. Here's a suggested structure for your README.md:

---

# Automated University Result Downloader

This Python script automates the process of fetching and downloading exam results from university websites.


## Usage

1. Install the required libraries: `pip install requests pdfkit`.
2. Clone the repository: `git clone https://github.com/your-username/uni-result-downloader.git`.
3. Navigate to the project directory: `cd uni-result-downloader`.
4. Modify the script to specify the range of registration numbers you want to download results for.
5. Run the script: `python main.py`.


---



```markdown
# Student Result PDF Generator

This project fetches student data (name, SGPA, fail status, and detailed result URL) from an online portal and generates a styled PDF report displaying this data in a table format. The PDF report is generated using `pdfkit` and `wkhtmltopdf`, which allows the transformation of HTML content (including CSS styling) into a PDF file.

## Features

- **Asynchronous Data Fetching**: The project fetches student data concurrently for multiple registration numbers using `aiohttp` and `asyncio`.
- **Dynamic Data Insertion**: Student data, including name, SGPA, fail status, and detailed result URL, is dynamically inserted into an HTML table.
- **Styled PDF**: The generated PDF is styled using CSS to give it a professional and visually appealing appearance.
- **Detailed Result Links**: The PDF contains clickable links that open detailed results in the browser.

## Prerequisites

Before running the project, ensure the following dependencies are installed:

- Python 3.x
- `aiohttp` for asynchronous HTTP requests
- `BeautifulSoup4` for parsing HTML content
- `pdfkit` for generating PDFs from HTML
- `wkhtmltopdf` installed on your machine (required by `pdfkit` for PDF conversion)

### Install Dependencies

To install the required dependencies, run:

```bash
pip install aiohttp beautifulsoup4 pdfkit
```

### Install `wkhtmltopdf`

You need to install `wkhtmltopdf` in your system. Follow the instructions on the [official website](https://wkhtmltopdf.org/downloads.html) to install it.

Once installed, update the path to the `wkhtmltopdf` executable in the script if necessary.

## How It Works

1. **Fetching Data**: 
   - The script fetches student data from a given URL using the registration number.
   - It retrieves the student's name, SGPA, fail status, and a link to their detailed results.
   
2. **Generating the PDF**:
   - The student data is formatted into an HTML table with CSS styling.
   - The `pdfkit` library converts the styled HTML content into a PDF file.

3. **Output**:
   - The result is saved as a PDF file (`student_results_with_urls.pdf`).

## Usage

1. Clone the repository or download the script.
2. Run the script by executing the following command:

```bash
python generate_results_pdf.py
```

The script will fetch student data for a predefined range of registration numbers and generate a styled PDF with the results.

### Example Output

The generated PDF will contain:

- A title: "SGPA Report: 6th Sem CSE (2021 - 2025)"
- A table with the following columns:
  - **Registration Number**: The student's registration number.
  - **Name**: The student's name.
  - **SGPA**: The student's SGPA.
  - **Remarks**: The fail status, if applicable.
  - **Detailed Result**: A clickable link to view the detailed result.

## Notes

- The script currently fetches data for a predefined range of registration numbers. You can modify this range in the `generate_registration_numbers` function as per your requirements.
- Ensure that the `wkhtmltopdf` path is correctly set in the script for PDF generation.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgements

- [aiohttp](https://docs.aiohttp.org/en/stable/) - Asynchronous HTTP client/server framework.
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Python library for parsing HTML and XML documents.
- [pdfkit](https://github.com/JazzCore/python-pdfkit) - Python wrapper for the `wkhtmltopdf` command line tool.
- [wkhtmltopdf](https://wkhtmltopdf.org/) - Command line tool to render HTML to PDF.

```

### Key Sections:
- **Features**: Describes the core functionality of the project.
- **Prerequisites**: Lists the required libraries and installation steps.
- **How It Works**: Explains the data fetching and PDF generation process.
- **Usage**: Instructions on how to run the script.
- **Example Output**: Describes the format of the generated PDF.
- **License**: Mentions the project's license (can be changed based on your preference).
- **Acknowledgements**: Credits the libraries used in the project.
