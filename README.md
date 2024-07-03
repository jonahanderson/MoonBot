# MoonBot

A Python script to automatically comment on Reddit posts in the cryptocurrency subreddit.

## Setup

### 1. Clone the Repository

Open your terminal (or Command Prompt on Windows) and run the following command to clone the repository:

```sh
git clone https://github.com/jonahanderson/MoonBot.git
cd MoonBot
```

### 2. Set Up Environment Variables

#### Create a .env File

The repository already includes a .env file template. You need to fill in your Reddit and OpenAI credentials.

Edit the `.env` file:

```sh
touch .env
```

Add your credentials to the `.env` file:

```sh
REDDIT_USER_AGENT=script:MoonBot:v1.0 (by /u/justjoner)
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
OPENAI_API_KEY=your_openai_api_key
```

Replace `your_client_id`, `your_client_secret`, `your_username`, `your_password`, and `your_openai_api_key` with your actual Reddit API and OpenAI API credentials.

#### How to Get Your Reddit Credentials

1. Go to [Reddit's app preferences](https://www.reddit.com/prefs/apps).
2. Click on "Create App" or "Create Another App".
3. Fill out the form:
   - **name**: Choose a name for your app.
   - **App type**: Select "script".
   - **description**: (optional) Describe your app.
   - **about url**: (optional) URL with more information about your app.
   - **redirect uri**: Set this to `http://localhost:8000` or another valid URL.
   - **permissions**: Select the necessary permissions.
4. Click "Create app".
5. Copy the `client_id` and `client_secret` from the newly created app and fill in the `.env` file.

#### How to Get Your OpenAI API Key

1. Go to [OpenAI's API key page](https://beta.openai.com/signup/).
2. Sign up for an account if you don't have one.
3. Go to the API section in your account settings.
4. Generate a new API key and copy it.
5. Add the API key to the `.env` file.

### 3. Run the Setup Script

Once everything is set up, you can run the setup script which handles environment setup and dependency installation. Make sure the setup script is executable and run it:

```sh
chmod +x setup.sh
./setup.sh
```

### 4. Run the Script

After setting up the environment and dependencies, you can run the main script:

```sh
python moonHarvester3000.py
```

### Notes

- Ensure that your `.env` file is not included in version control by making sure it is listed in `.gitignore`.
- If you encounter any issues with dependencies, ensure that your virtual environment is activated and that all required packages are installed.

### Additional Tips

- **Virtual Environment**: The setup script creates and activates a virtual environment to keep dependencies isolated. Ensure you are in the virtual environment when running the script.
- **Dependencies**: If new dependencies are added, update the `requirements.txt` file and re-run the setup script to install them.

### Troubleshooting

- If you encounter issues with Python installation or virtual environment setup, ensure that Python 3.6+ is installed on your system.
- For Windows users, consider using a PowerShell script for a similar setup process.
