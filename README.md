# MoonBot

A Python script to automatically comment on Reddit posts in the cryptocurrency subreddit.

## Setup Instructions for Windows:

Download and Set Up WSL on Windows
1. **Open PowerShell as Administrator**

   Press `Win + X`, then select Windows PowerShell (Admin).

**Install WSL and Set Up Ubuntu**

2. **In the PowerShell window, run the following command to install WSL and set up Ubuntu:**

   ```sh
   wsl --install
   ```

   This command will:
   
   * Enable the necessary WSL feature.
   * Download and install the latest WSL Linux kernel.
   * Set WSL 2 as the default.
   * Download and install Ubuntu as the default Linux distribution.

3. **Restart Your Computer**

   Follow the prompt to restart your computer.

4. **Complete Ubuntu Setup**

   After your computer restarts, Ubuntu will launch and prompt you to complete the installation. Set up your user account and password as prompted.

## Using WSL to Run the Setup Script

1. **Open Ubuntu (WSL)**

   After setting up Ubuntu, open it from the Start menu.

2. **Update and Upgrade Packages**

   In the Ubuntu terminal, update and upgrade the package lists:
   
   ```sh
   sudo apt update
   sudo apt upgrade -y
   ```

3. **Install Git**


   Install Git to clone the repository:
   
   ```sh
   sudo apt install git -y
   ```

# 1. Clone the Repository

Open your terminal and run the following command to clone the repository:

```sh
git clone https://github.com/jonahanderson/MoonBot.git
cd MoonBot
```

# 2. Set Up Environment Variables

#### Create a .env File

Create a file named `.env` in the project directory and add your Reddit and OpenAI credentials to it. This file should not be shared or included in version control to keep your credentials secure.

Create the `.env` file:

```sh
touch .env
```
Add your credentials to the `.env` file:

```sh
REDDIT_USER_AGENT=script:MoonBot:v1.0
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

<img width="909" alt="Screenshot 2025-06-12 at 12 33 20 PM" src="https://github.com/user-attachments/assets/d3693e08-d029-400e-9426-012c99a2756e" />


#### How to Get Your OpenAI API Key

1. Go to [OpenAI's API key page](https://beta.openai.com/signup/).
2. Sign up for an account if you don't have one.
3. Go to the API section in your account settings.
4. Generate a new API key and copy it.
5. Add the API key to the `.env` file.

NOTE: You may need Open AI Usage Tier 1 or above to use the generative features of this bot. See [OpenAI API Usage Tiers](https://platform.openai.com/docs/guides/rate-limits/usage-tiers)

## 3. Run the Setup Script

Once everything is set up, you can run the setup script which handles environment setup, dependency installation, and starts the MoonBot. Make sure the setup script is executable and run it:

```sh
chmod +x farmMoons.sh
./farmMoons.sh
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
