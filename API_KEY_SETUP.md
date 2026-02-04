# OpenAI API Key Setup Instructions

This project requires a valid OpenAI API key to function properly. Follow these steps to set it up:

## Step 1: Get Your OpenAI API Key

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in to your OpenAI account (create one if you don't have one)
3. Click "Create new secret key"
4. Copy the generated API key (it will look like `sk-...`)

⚠️ **Important**: Keep this key secure and never share it publicly!

## Step 2: Update the API Key in the .env File

### Option A: Using the Helper Script (Recommended)

Run the following command, replacing `<your-api-key>` with your actual API key:

```bash
./update_api_key.sh <your-api-key>
```

Example:
```bash
./update_api_key.sh sk-1234567890abcdefghijklmnopqrstuvwxyz
```

### Option B: Manual Update

1. Navigate to the backend directory:
   ```bash
   cd "/media/awais/6372445e-8fda-42fa-9034-61babd7dafd1/150 GB DATA TRANSFER/hackathon series/hackathon-2/phase-3 chatbot_todo/backend/hf_deployment/todo_chatbot"
   ```

2. Edit the `.env` file:
   ```bash
   nano .env
   ```

3. Find the line:
   ```
   OPENAI_API_KEY="sk-your-openai-api-key-here"
   ```

4. Replace it with your actual API key:
   ```
   OPENAI_API_KEY="sk-actual-key-you-copied-from-openai-platform"
   ```

5. Save and close the file

## Step 3: Restart the Server

After updating the API key, you need to restart the server to load the new environment variable:

```bash
# Kill any running server instances
pkill -f uvicorn

# Navigate to the backend directory
cd "/media/awais/6372445e-8fda-42fa-9034-61babd7dafd1/150 GB DATA TRANSFER/hackathon series/hackathon-2/phase-3 chatbot_todo/backend/hf_deployment/todo_chatbot"

# Start the server
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Step 4: Test the Chat Functionality

Once the server is running, test the chat functionality to confirm the API key is working.

## Troubleshooting

- If you still get 401 errors after updating the key, make sure you restarted the server after changing the .env file
- Verify that your API key has sufficient quota/balance on the OpenAI platform
- Check that you copied the full API key without any extra spaces or characters

## Security Note

- The `.env` file is already added to `.gitignore` to prevent committing your API key
- Never share your API key or commit it to version control
- Regularly rotate your API keys for security