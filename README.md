# Air Pollution Data Collection and Analysis

This project aims to collect air pollution data from multiple cities using the OpenWeatherMap API and store it in a Google BigQuery table for further analysis.

## Setup

1. **Clone the repository:**
   

3. **Install dependencies:**

Certainly! Here's the content of a single markdown file, README.md, combining the information:

markdown
Copy code
# Air Pollution Data Collection and Analysis

This project aims to collect air pollution data from multiple cities using the OpenWeatherMap API and store it in a Google BigQuery table for further analysis.

## Setup

1. **Clone the repository:**

git clone https://github.com/your-username/air-pollution-data.git

markdown
Copy code

2. **Install dependencies:**

pip install -r requirements.txt
3. **Set up Google Cloud:**

- Create a project on Google Cloud Console.
- Enable the BigQuery API and create a dataset.
- Obtain the necessary service account key in JSON format.

4. **Create a `.env` file and add your OpenWeatherMap API key:**

Certainly! Here's the content of a single markdown file, README.md, combining the information:

markdown
Copy code
# Air Pollution Data Collection and Analysis

This project aims to collect air pollution data from multiple cities using the OpenWeatherMap API and store it in a Google BigQuery table for further analysis.

## Setup

1. **Clone the repository:**

git clone https://github.com/your-username/air-pollution-data.git

markdown
Copy code

2. **Install dependencies:**

pip install -r requirements.txt

markdown
Copy code

3. **Set up Google Cloud:**

- Create a project on Google Cloud Console.
- Enable the BigQuery API and create a dataset.
- Obtain the necessary service account key in JSON format.

4. **Create a `.env` file and add your OpenWeatherMap API key:**

OPENWEATHER_API_KEY=your-api-key

## Contributions

Contributions are welkome

## Usage

Run the script `collect_data.py` to fetch air pollution data for specified cities and load it into a Google BigQuery table.

```bash
python collect_data.py
Project Structure
collect_data.py: Python script to collect air pollution data from the OpenWeatherMap API and load it into BigQuery.
README.md: Project documentation.
requirements.txt: List of Python dependencies.
secrets/: Directory to store sensitive information such as API keys.
secrets/.env: Environment variables file.
secrets/openweather-421711-1472594dde96.json: Service account key for Google Cloud authentication.
