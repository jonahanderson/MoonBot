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

Create a file named `.env` in the project directory and add your Reddit credentials to it. This file should not be shared or included in version control to keep your credentials secure.

#### Create the `.env` file:

```sh
touch .env
```

#### Add your credentials to the `.env` file:

```plaintext
REDDIT_USER_AGENT=your_user_agent
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
```

Replace `your_user_agent`, `your_client_id`, `your_client_secret`, `your_username`, and `your_password` with your actual Reddit API credentials.

### 3. Run the Script

Once everything is set up, you can run the script using the following command:

```sh
chmod +x farmMoons.sh
./farmMoons.sh
```

### Notes

- Ensure that your `.env` file is not included in version control by making sure it is listed in `.gitignore`.
- If you encounter any issues with dependencies, ensure that your virtual environment is activated and that all required packages are installed.
