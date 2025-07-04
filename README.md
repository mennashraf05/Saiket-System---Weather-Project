# Weather CLI Application

**Author:** MennaTallah Ashraf Ali

A simple, extensible command‑line tool in Python that fetches and displays weather data using the Open‑Meteo API (no API key required). Supports current conditions, a 7‑day forecast, unit selection, multiple cities, text output, and graphical plots.

A simple, extensible command‑line tool in Python that fetches and displays weather data using the Open‑Meteo API (no API key required). Supports current conditions, a 7‑day forecast, unit selection, multiple cities, text output, and graphical plots.

## Features

* Fetch current weather for one or more cities
* 7‑day forecast (text) and optional Matplotlib chart
* Choose temperature units: Celsius or Fahrenheit
* Geocoding in different languages (`en` or `ar`)
* Robust error handling and logging to `app.log`
* Unit tests with pytest
* Installable as a CLI tool via `setup.py`
* Optional Docker container support
* (Optional) CI/CD workflow for GitHub Actions

## Prerequisites

* Python 3.10 or higher
* [pip](https://pip.pypa.io/en/stable/)
* (Optional) [Docker](https://www.docker.com/) for containerization

## Installation

1. Clone the repository:

   ```bash
   git clone <repo_url>
   cd <project_folder>
   ```
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .\.venv\Scripts\Activate.ps1  # Windows PowerShell
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Install as an editable CLI tool:

   ```bash
   pip install -e . --no-build-isolation
   ```

## Usage

Run the script directly with Python:

```bash
python weather_open_meteo.py [cities...] [options]
```

Or, if installed as CLI:

```bash
weather_open_meteo [cities...] [options]
```

### Options

* `--units {celsius,fahrenheit}`: Temperature unit (default: `celsius`)
* `--lang LANG`: Language for geocoding (default: `en`)
* `--daily`: Show 7‑day forecast (text)
* `--plot`: Plot 7‑day forecast chart (requires `--daily`)
* `-h, --help`: Show help message

### Run Scenarios

1. **Current weather (°C)**

   ```bash
   python weather_open_meteo.py Cairo
   ```
2. **Current weather (°F)**

   ```bash
   python weather_open_meteo.py Cairo --units fahrenheit
   ```
3. **7‑day forecast (text)**

   ```bash
   python weather_open_meteo.py Cairo --daily
   ```
4. **7‑day forecast + chart**

   ```bash
   python weather_open_meteo.py Cairo --daily --plot
   ```
5. **Multiple cities**

   ```bash
   python weather_open_meteo.py Cairo London "New York" --daily --plot --units fahrenheit
   ```
6. **Geocoding in Arabic**

   ```bash
   python weather_open_meteo.py القاهرة --lang ar
   ```
7. **Error handling (invalid city)**

   ```bash
   python weather_open_meteo.py InvalidCity
   ```

## Logging

All output is logged both to the console and to `app.log` in the project root. Review this file for debug and error information.

## Testing

Run the unit test suite with pytest:

```bash
pytest -v
```

## License

This project is licensed under the MIT License. Feel free to use and modify.
