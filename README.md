# newsSum

[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Vue Version](https://img.shields.io/badge/vue-3.5-green.svg)](https://vuejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A high-performance news headline aggregator optimized for deployment on **Google App Engine** (Python 3 runtime). It parses RSS feeds and HTML pages to extract headlines, serving them via a unified JSON API consumed by a modern, responsive Vue 3 single-page application.

---

## 🚀 Features

- **Automated Headline Extraction**: Parses various RSS feeds and structured HTML pages dynamically.
- **Robust Fetching Engine**: Uses `curl_cffi` (with Google Chrome browser impersonation) to bypass web scraping blockages and mimic authentic browser traffic.
- **Modern SPA Frontend**: Built with Vue 3, TypeScript, Vite, and Bootstrap 5. Supports light and dark themes.
- **Dynamic Source Discovery**: Easily register new publishers by adding Python modules that extend `BaseSource`. The backend auto-detects them.
- **Scalable Caching Architecture**: Configured with smart client-side and CDN/proxy caching headers (`Cache-Control`) to minimize CPU/instance hours on App Engine without expensive caching databases.
- **Optional Suggestion Service**: Seamlessly integrates with external NLP/suggestion microservices to recommend related articles.
- **Load and Performance Tested**: Bundled with a `k6` load test suite to benchmark endpoint latency and throughput.

---

## 📁 Repository Structure

```text
├── app.yaml                 # Google App Engine deployment configuration
├── fetcher.py               # Robust HTTP client with browser impersonation
├── logger.py                # Logger helper config
├── main.py                  # Flask web application endpoints & routing
├── Makefile                 # Automation targets (linting, formatting, deployment)
├── newssum-ui/              # Frontend application directory
│   ├── src/                 # Vue 3 / TypeScript source files
│   ├── package.json         # Vite / npm dependencies and scripts
│   └── vite.config.ts       # Vite bundler configuration
├── requirements.txt         # Production backend python dependencies
├── requirements-dev.txt     # Development backend python dependencies
├── sources/                 # Extensible scrapers and RSS parsers
│   ├── base.py              # Abstract Base classes (BaseSource, RSSBase, RDFBase)
│   ├── canada.py            # Canada-specific news sources
│   ├── hk.py                # Hong Kong-specific news sources
│   ├── intl.py              # International news sources
│   ├── taiwan.py            # Taiwan-specific news sources
│   └── uk.py                # UK-specific news sources
├── static/                  # Production static assets served by Flask / GAE
├── test/                    # Performance testing suite
│   ├── k6/                  # k6 load testing scripts
│   └── run_k6.sh            # Load test runner script
└── util.py                  # Modules/source auto-loader and utility functions
```

---

## 🛠️ Getting Started

### Prerequisites

- **Python 3.13** or higher
- **Node.js** (v18+) and **npm** (v9+)
- **Docker** (optional, for load testing)

### 1. Set Up Backend

Clone the repository and set up a Python virtual environment:

```bash
git clone https://github.com/kitsook/newssum.git
cd newssum

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (production & development)
pip install -r requirements.txt -r requirements-dev.txt
```

### 2. Build the Frontend

Compile the Vue 3 production bundle and copy the static assets to the backend's static directory:

```bash
cd newssum-ui
npm install
npm run build

# Copy build output to the Flask static assets directory
cp -r dist/* ../static
cd ..
```

### 3. Run Locally

Start the Flask development server:

```bash
python main.py
```

The application will be accessible at: `http://127.0.0.1:8080`

---

## 💻 Development & Code Quality

To format and lint backend python files, run the provided Makefile commands:

```bash
# Format Python code using black and lint using flake8
make formatting
```

---

## 🧩 Extending & Adding Custom Sources

You can easily add new news publishers by creating a python file under the `sources/` directory.

### 1. Extend the Base Classes
Your source class must inherit from `BaseSource` (or helper classes like `RSSBase` or `RDFBase`) defined in `sources/base.py`.

```python
from sources.base import RSSBase

class MyNewSource(RSSBase):
    def get_id(self):
        return "my_new_source"  # Used as the API route: /my_new_source

    def get_desc(self):
        return "My New Publisher Name"

    def get_icon_url(self):
        return "https://example.com/icon.png"  # Optional icon URL

    def get_rss_links(self):
        return [
            ("Top Stories", "https://example.com/rss/top_stories.xml"),
            ("Technology", "https://example.com/rss/tech.xml"),
        ]
```

### 2. Automatic Registration
The backend dynamically registers all non-abstract subclasses of `BaseSource` in the `sources/` package via `pkgutil` and `inspect` in `util.py`. Once you save your file in the `sources/` directory, it will automatically register:
- **API Endpoint**: `[GET] /my_new_source`
- **UI Menu**: The source will appear in the UI sidebar/source lists automatically.

---

## 🔍 Integrating a Suggestion Service

To enrich the user experience, newsSum can query an external suggestion microservice. The service must support the following contract:

### Endpoints

#### 1. Health Check
Checks if the suggestion microservice is online.
* **Method**: `GET`
* **Path**: `/health`
* **Response**: `2xx OK` status code

#### 2. Search Articles
Searches for contextually related articles based on a query string.
* **Method**: `POST`
* **Path**: `/search`
* **Request Payload**:
  ```json
  {
    "query_str": "query terms"
  }
  ```
* **Response Payload**:
  ```json
  {
    "result": [
      {
        "title": "Article Title",
        "url": "https://example.com/article",
        "abstract": "A brief summary of the suggested article"
      }
    ]
  }
  ```

To point the UI to your suggestion microservice, configure the base URL in `newssum-ui/src/services/SuggestionsApi.ts`.

---

## 📈 Performance & Load Testing

A performance benchmarking suite is available in the `test/` directory.

### Run load tests with `k6`

Run the benchmark target utilizing Docker:

```bash
cd test
./run_k6.sh
```

Ensure a PostgreSQL instance configured for TimescaleDB is running locally if you want to output results to TimescaleDB, or customize `run_k6.sh` to log output to standard out.

---

## 🚀 Deployment

### Deploy to Google App Engine
Deploy the application to **Google App Engine** using the gcloud CLI:

```bash
make deploy
```
*(Or run `gcloud app deploy app.yaml` directly)*

The application's static directories and python entrypoints are preconfigured inside `app.yaml` using the modern `python313` runtime.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
