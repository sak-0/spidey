# Spidey
Spidey is a web scraping and automation project designed to extract data from websites using Scrapy and Selenium. It is configured to work with Selenium for handling dynamic content and automation.

## Project Structure
- **spidey/**: Contains the main source code for the project.
  - **auth/**: Handles authentication logic.
  - **middlewares/**: Custom middlewares for Scrapy.
  - **spiders/**: Contains the spider definitions for crawling.
  - **pipelines.py**: Defines item pipelines for processing scraped data.
  - **settings.py**: Configuration settings for Scrapy.
  - **items.py**: Defines the data structures for scraped items.
- **output/**: Directory for storing output data.
- **pyproject.toml**: Project configuration and dependencies.
- **scrapy.cfg**: Scrapy configuration file.

## Requirements
- Python >= 3.14
- poetry >= 2.1.3
- Scrapy >= 2.13.0, < 3.0.0
- Scrapy-Selenium >= 0.0.7, < 0.0.8
- Requests >= 2.32.3, < 3.0.0
- BeautifulSoup4 >= 4.13.4, < 5.0.0
- MySQL Connector Python >= 9.3.0, < 10.0.0
- Dotenv >= 0.9.9, < 0.10.0

## Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/sak-0/spidey
   cd spidey
   ```

2. **Set up a virtual environment**:
   ```bash
   poetry env activate
   ```

3. **Install dependencies**:
   ```bash
   poetry install
   ```

4. **Configure environment variables**:
   - Create a `.env` file in the root directory.
   - Add necessary environment variables as required by the project.

5. **How to run Login.py**:
   ```bash
   poetry run python spidey/auth/login.py --help
   ```

## Usage
   ```bash
   # run rep login
   poetry run python spidey/auth/login.py --rep-type=enrollprime #or nuera

   #run group login
   poetry run python spidey/auth/login.py --url=group

   #run member login
   poetry run python spidey/auth/login.py --url=member
   ```

## Author
- Sak-0 (saksham@cloudtechservice.com) 