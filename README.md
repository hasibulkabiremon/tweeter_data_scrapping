# Tweeter Data Scrapping

Tweeter Data Scrapping is a Python script that uses Selenium to scrape Twitter posts along with their comments, replies, and other reactions. This tool is designed to help you extract detailed information from Twitter for analysis and research purposes.

## Features

- **Scrape Twitter Posts**: Extracts detailed information from Twitter posts including text, media, and metadata.
- **Comments and Replies**: Retrieves comments and replies associated with each post.
- **Reactions**: Collects data on likes, retweets, and other reactions.
- **Automation**: Uses Selenium to automate the browsing and data extraction process.

## Requirements

- Python 3.x
- Selenium
- WebDriver for your browser (e.g., ChromeDriver for Google Chrome)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/hasibulkabiremon/tweeter_data_scrapping.git
    cd tweeter_data_scrapping
    ```

2. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Download the WebDriver:**
   - For Chrome, download [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) and place it in the same directory as your script or add it to your PATH.

## Usage

1. **Configure the script:**
   - Update the `config.py` file with your Twitter login credentials and any other necessary configuration.

2. **Run the script:**
    ```bash
    python scrape_twitter.py
    ```

3. **Output:**
   - The script will generate a CSV file containing the scraped data.

## Example

Here is a simple example of what the output might look like:

| Post ID | User | Text | Comments | Replies | Likes | Retweets |
|---------|------|------|----------|---------|-------|----------|
| 123456  | @user1 | This is a tweet | 5 | 3 | 100 | 50 |

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Connect with me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/mdhasibul923853191) 
[![Twitter](https://img.shields.io/badge/Twitter-Profile-blue?style=flat-square&logo=twitter)](https://twitter.com/@hasib_kabi_emon) 
[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=flat-square&logo=github)](https://github.com/hasibulkabiremon) 
[![Facebook](https://img.shields.io/badge/Facebook-Profile-blue?style=flat-square&logo=facebook)](https://facebook.com/hasibulc0) 

Feel free to check out my other projects [here](https://github.com/hasibulkabiremon?tab=repositories).
