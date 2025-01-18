# Shubh Automation - Data Collection and Analysis System

This repository contains a Flask web application designed for collecting and enriching business data from multiple sources, such as Apollo API, Google Search API, and websites. It also analyzes websites using OpenAI's GPT model to provide SEO suggestions. The enriched data is stored in a MySQL database and can be displayed through a web interface. The app can be triggered manually or run on a scheduled basis to keep the database up to date.

## Features

- **Web Scraping:**
  - Scrapes business data using **Apollo API**.
  - Scrapes business information using **Google Custom Search API**.
  - Scrapes email addresses from business websites.
  
- **Data Enrichment:**
  - Uses **OpenAI GPT** to analyze websites and provide SEO improvement suggestions.

- **Database Storage:**
  - Stores the collected and enriched data in a **MySQL** database.

- **User Interface:**
  - Displays the stored data in a simple Flask web interface using **HTML templates**.

- **Automation:**
  - Supports manual or automated (scheduled) data collection processes.
  - Can trigger Telegram notifications after data processing is complete.

## Technologies Used

- **Flask**: Python web framework for building the application.
- **MySQL**: Database for storing enriched data.
- **Requests**: For making HTTP requests to external APIs and websites.
- **BeautifulSoup**: For scraping emails from websites.
- **OpenAI GPT-3**: For generating SEO suggestions and analyzing websites.
- **Apollo API**: For collecting business data by domain.
- **Google Custom Search API**: For scraping business data from search results.
- **Dotenv**: For managing environment variables securely.
- **Telegram API**: For sending notifications about the data processing.

## Installation

Follow the steps below to set up and run the project locally.

### Prerequisites

- Python 3.7 or higher
- MySQL installed and running
- Environment variables configured for API keys

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/shubh-automation.git
cd shubh-automation
