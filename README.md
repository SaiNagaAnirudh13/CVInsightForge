

# CVInsightForge [https://cvinsightforge.onrender.com/]

CVInsightForge is an AI-powered Streamlit application designed to enhance your resume by evaluating it against a job description. Leveraging the Google Generative AI API, the application provides insights, identifies missing keywords, and offers suggestions to improve your resume's alignment with job requirements.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Configuration](#configuration)
5. [Project Structure](#project-structure)
6. [Contributing](#contributing)


## Features

- **Resume Evaluation**: Upload your resume in PDF format and paste a job description to get an evaluation.
- **Job Description Match**: Receive a percentage match score indicating how well your resume aligns with the job description.
- **Profile Summary**: Get a summarized profile based on your resume.
- **Scoring Breakdown**: Detailed scores for projects, skills, and education sections.
- **Skills Matching**: Calculate the percentage of job description skills matched in your resume.
- **Missing Keywords**: Identify missing keywords in your resume that are present in the job description.
- **Resume Formatting Tips**: Helpful tips to format your resume for better readability and ATS compatibility.

## Installation

### Prerequisites

- Python 3.7 or higher
- Streamlit
- Google Generative AI API key

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/SaiNagaAnirudh13/CVInsightForge
   cd CVInsightForge
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install the Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the project root directory and add your Google API key:

   ```plaintext
   GOOGLE_API_KEY=your_google_api_key
   ```

## Usage

1. **Run the Application**

   ```bash
   streamlit run app.py
   ```

2. **Access the Application**

   Open your web browser and navigate to `http://localhost:8501`.

3. **Evaluate Your Resume**

   - Paste the job description into the text area.
   - Upload your resume in PDF format.
   - Click the "Submit" button to get the evaluation results.

## Configuration

Ensure you have a valid Google API key with access to the Google Generative AI API. Follow these steps to obtain and configure your API key:

1. **Google Cloud Console**

   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create or select a project.
   - Enable the Google Generative AI API for your project.
   - Create credentials and generate an API key.
   - Add the API key to your `.env` file as shown above.

## Project Structure

```
CVInsightForge/
│
├── .env                   # Environment variables
├── .gitignore             # Git ignore file
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── app.py                 # Main application script
```

- `app.py`: The main application script containing all the functionality for resume evaluation, text extraction, and result display.
- `requirements.txt`: Lists all the dependencies required to run the application.

## Contributing

We welcome contributions to enhance CVInsightForge! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Open a pull request to the main repository.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

