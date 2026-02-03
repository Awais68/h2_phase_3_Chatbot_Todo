# OpenAI API Quota Fix

## Issue
Error code 429 - `insufficient_quota`: The OpenAI API quota has been exceeded. This typically occurs when:
- Your OpenAI account doesn't have billing set up
- Your account has hit its usage limit
- Your trial credits have expired
- Your payment method is invalid

## Error Message
```
Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details...'}}
```

## Solution Implemented

### 1. **Proper Error Handling**
The following files have been updated with comprehensive error handling:

#### [backend/src/api/chat.py](backend/src/api/chat.py)
- Added imports for `RateLimitError` and `APIError` from OpenAI SDK
- Wrapped the `agent_service.run_agent()` call with try-except blocks
- Catches both `RateLimitError` and `APIError` with quota-specific handling
- Returns user-friendly error messages instead of crashing

#### [backend/src/services/agent_service.py](backend/src/services/agent_service.py)
- Added imports for `RateLimitError` and `APIError`
- Wrapped the OpenAI API call with try-except blocks
- Detects quota errors and re-raises them with helpful context
- Proper error propagation for other API errors

### 2. **User-Friendly Responses**
When quota is exceeded, users now receive:
- Clear explanation of the issue
- Link to OpenAI billing dashboard
- HTTP 429 status code (standard for rate limits)

### 3. **Error Logging**
All quota errors are logged with `⚠️` prefix for easy debugging.

## How to Fix the Underlying Issue

### Option 1: Add Payment to OpenAI Account (Recommended)
1. Go to https://platform.openai.com/account/billing/overview
2. Click "Billing" in the left sidebar
3. Click "Set up paid account"
4. Add a valid payment method
5. Your API key should work immediately

### Option 2: Check Existing Quotas
1. Visit https://platform.openai.com/account/billing/overview
2. Check:
   - **Usage**: Current month's usage
   - **Soft limit**: Your monthly spending limit
   - **Hard limit**: Maximum you're willing to spend
3. If soft limit is too low, increase it:
   - Click "Limits" in the left sidebar
   - Increase the "Soft Limit" or "Hard Limit"

### Option 3: Use Trial Credits (if available)
1. Check if your account has trial credits
2. Trial credits typically expire after 3 months
3. You can use trial credits without adding a payment method

### Option 4: Create a New OpenAI Account
If your current account is blocked:
1. Create a new OpenAI account at https://platform.openai.com/signup
2. Get a new API key
3. Update the `OPENAI_API_KEY` in your `.env` file:
   ```bash
   OPENAI_API_KEY=sk-...your-new-key...
   ```

## Verify the Fix

### 1. Check Your OpenAI Configuration
```bash
# Verify your API key is set
echo $OPENAI_API_KEY

# Should show: sk-... (not empty)
```

### 2. Test the API
```bash
# In your backend directory
cd backend

# Run the backend
uv run uvicorn main:app --reload

# In another terminal, test the chat endpoint
curl -X POST http://localhost:8000/api/testuser@gmail.com/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a task to buy groceries"
  }'
```

### 3. Expected Responses

**If Fixed (API quota available):**
```json
{
  "conversation_id": 1,
  "response": "I'll create a task to buy groceries for you.",
  "tool_calls": [...]
}
```

**If Still Failing (No quota):**
```json
{
  "conversation_id": 1,
  "response": "I apologize, but the AI service is temporarily unavailable due to quota limits. Please check your OpenAI API billing and quota...",
  "tool_calls": []
}
```

## Troubleshooting

### Issue: Still getting 429 errors
**Solution**: 
1. Double-check your OpenAI account billing setup
2. Verify the API key is correct (starts with `sk-`)
3. Wait 5-10 minutes after adding payment (sometimes there's a delay)
4. Try creating a new API key at https://platform.openai.com/api-keys

### Issue: "Invalid API Key"
**Solution**:
1. Regenerate your API key at https://platform.openai.com/api-keys
2. Update `.env` file with new key
3. Restart the backend service

### Issue: Account locked/suspended
**Solution**:
1. Contact OpenAI support at https://help.openai.com
2. Or create a new account and start fresh

## Monitoring Usage

To prevent quota issues in the future:

### 1. Monitor Spending
- Visit https://platform.openai.com/account/billing/usage/overview
- Set up email alerts in billing settings
- Check usage weekly

### 2. Optimize API Calls
- Use caching where possible
- Reduce token usage by being specific in prompts
- Consider using cheaper models (gpt-3.5-turbo vs gpt-4o)

### 3. Set Hard Limits
- Visit https://platform.openai.com/account/billing/limits
- Set a reasonable "Hard Limit" to prevent unexpected charges

## Files Modified

1. **[backend/src/api/chat.py](backend/src/api/chat.py)**
   - Added quota error handling
   - Returns user-friendly error responses
   - HTTP 429 status for quota errors

2. **[backend/src/services/agent_service.py](backend/src/services/agent_service.py)**
   - Added API error handling
   - Proper error detection and logging
   - Error propagation to API layer

## Testing the Fix

```bash
# 1. Start the backend
cd backend
uv run uvicorn main:app --reload

# 2. In another terminal, send a test message
curl -X POST http://localhost:8000/api/testuser/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "list my tasks"}'

# 3. Check the response:
# - If successful: You'll get tasks back
# - If quota error: You'll get helpful error message
```

## Next Steps

1. **Immediate**: Fix your OpenAI API billing (see Option 1 above)
2. **Short-term**: Test the API with the curl command above
3. **Long-term**: Monitor usage to prevent future quota issues

For more help, visit:
- OpenAI Status: https://status.openai.com
- OpenAI Docs: https://platform.openai.com/docs
- OpenAI Help: https://help.openai.com
