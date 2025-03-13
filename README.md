# SocialMediaSentiment

## Getting started

### Prerequisites

- Client ID and Client Secret to the REDDIT API ([steps to get those](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps))

### 1. Install dependencies
Optionally create a virtual environment to install the dependencies into,
```sh
python3 -m venv .venv
```
then activate.
```sh
source .venv/bin/activate
```

Install the required dependencies for the app to run.
```sh
pip install -r requirements.txt
```
### 2. Set up authentication to the Reddit API

Copy this [example .env file](.env.example) and fill in the placeholders with your `CLIENT_ID` and `CLIENT_SECRET`.

### 3. Running the application

```sh
python -m streamlit run src/main.py
```
