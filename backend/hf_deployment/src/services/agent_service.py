"""
Agent service for OpenAI Agents SDK integration with Official MCP SDK.
"""
from typing import List, Dict, Any, Optional
from openai import OpenAI, RateLimitError, APIError
import os
import json
from dotenv import load_dotenv
# Import MCP tool functions directly from the module
import src.mcp.mcp_server as mcp_tools
import inspect

# Load environment variables from .env file
load_dotenv()


class AgentService:
    """Service for managing AI agent interactions with MCP tools."""

    def __init__(self):
        """Initialize the agent service."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        self.system_prompt = """You are a helpful task management assistant. Users will ask you to manage their todo tasks using natural language in both English and Urdu.

Your capabilities:
- Create tasks: "add", "create", "remember", "new task", "I need to"
  Urdu: "بنانا", "بنائیں", "ٹاسک بنائیں", "یاد رکھیں", "مجھے چاہیے"
- List tasks: "show", "list", "what are", "see tasks", "my tasks"  
  Urdu: "دکھائیں", "دیکھیں", "میرے ٹاسک", "فہرست", "کام دکھائیں"
- Complete tasks: "done", "complete", "finished", "mark as done"
  Urdu: "مکمل", "ہو گیا", "ختم", "مکمل کریں"
- Update/Edit tasks: "change", "update", "rename", "modify", "edit"
  Urdu: "تبدیل کریں", "اپڈیٹ", "ترمیم", "بدلیں"
- Delete tasks: "delete", "remove", "cancel"
  Urdu: "حذف کریں", "ہٹائیں", "منسوخ کریں", "ڈیلیٹ"
- Recurring tasks: "create recurring", "daily task", "weekly reminder", "monthly task"
  Urdu: "روزانہ ٹاسک", "ہفتہ وار", "ماہانہ کام"
- Analytics: "show statistics", "task analytics", "productivity", "completion rate"
  Urdu: "اعداد و شمار", "تجزیہ", "پیداواری صلاحیت"

When creating a task:
- After successfully creating a task with add_task tool, ALWAYS call list_tasks to get and show the complete details of the newly created task
- Include the full task information (ID, title, description, status, creation time) in your response
- Format the response clearly showing all task details

When showing tasks:
- Use list_tasks tool to retrieve all tasks
- Display each task with: task ID, title, description, status (✓ completed or ⏳ pending)
- Format clearly with bullets or numbers
- Show total count of tasks

When updating tasks:
- After update_task, call list_tasks to show the updated task details
- Confirm what was changed

When deleting tasks:
- Confirm deletion with task details
- Show remaining task count

When completing tasks:
- Use complete_task tool
- Show the completed task with a success indicator ✓

Language Support:
- Understand and respond to both English and Urdu commands
- Extract task details from mixed language input
- Recognize Urdu date/time expressions (کل = tomorrow, آج = today, پرسوں = day after tomorrow)
- Handle Roman Urdu (transliterated Urdu in English script)

Always:
- After creating/updating a task, retrieve and show full task details
- Confirm actions with friendly messages in the user's language
- Use status indicators (✓ for completed, ⏳ for pending, ✗ for errors)
- Format task lists clearly with numbers or bullets including task IDs
- Ask for clarification if the request is ambiguous
- Provide helpful error messages if something fails
- Be conversational and natural in both languages
- When user speaks Urdu, respond in Urdu; when English, respond in English
- Show task status, priority, category, and any other metadata when available

Example responses:
- After creating: "✓ Task created! Here are the details:\n  📋 Task #123: Buy groceries\n  📝 Description: Milk, bread, eggs\n  ⏳ Status: Pending\n  📅 Created: 2024-02-07 10:30 AM"
- After listing: "You have 5 tasks:\n  ⏳ Task #1: Write report\n  ✓ Task #2: Call client\n  ⏳ Task #3: Buy groceries"
"""
        
        # Map of available MCP tools
        self.mcp_tool_map = {
            'add_task': mcp_tools.add_task,
            'list_tasks': mcp_tools.list_tasks,
            'complete_task': mcp_tools.complete_task,
            'delete_task': mcp_tools.delete_task,
            'update_task': mcp_tools.update_task,
            'create_recurring_task': mcp_tools.create_recurring_task,
            'list_recurring_tasks': mcp_tools.list_recurring_tasks,
            'pause_recurring_task': mcp_tools.pause_recurring_task,
            'resume_recurring_task': mcp_tools.resume_recurring_task,
            'delete_recurring_task': mcp_tools.delete_recurring_task,
            'get_task_statistics': mcp_tools.get_task_statistics,
            'get_tasks_over_time': mcp_tools.get_tasks_over_time,
            'get_completion_analytics': mcp_tools.get_completion_analytics,
            'get_productivity_hours': mcp_tools.get_productivity_hours,
        }

    def _get_mcp_tools_for_openai(self) -> List[Dict[str, Any]]:
        """
        Convert MCP tools to OpenAI function calling format.
        
        Returns:
            List of tool definitions in OpenAI format
        """
        tools = []
        
        for tool_name, tool_func in self.mcp_tool_map.items():
            try:
                sig = inspect.signature(tool_func)
                doc = inspect.getdoc(tool_func) or f"{tool_name} tool"
                
                # Build parameters schema
                parameters = {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
                
                for param_name, param in sig.parameters.items():
                    if param_name in ['self', 'session']:
                        continue
                        
                    param_type = "string"
                    if param.annotation != inspect.Parameter.empty:
                        if param.annotation == int:
                            param_type = "integer"
                        elif param.annotation == bool:
                            param_type = "boolean"
                        elif param.annotation == float:
                            param_type = "number"
                    
                    parameters["properties"][param_name] = {
                        "type": param_type,
                        "description": f"{param_name} parameter"
                    }
                    
                    # Add to required if no default value
                    if param.default == inspect.Parameter.empty:
                        parameters["required"].append(param_name)
                
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool_name,
                        "description": doc.split('\n')[0],  # First line of docstring
                        "parameters": parameters
                    }
                })
            except Exception as e:
                print(f"Warning: Could not process tool {tool_name}: {e}")
                continue
        
        return tools

    def _execute_mcp_tool(self, tool_name: str, arguments: Dict[str, Any], 
                         user_id: int) -> Dict[str, Any]:
        """
        Execute a tool by calling the function directly.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments
            user_id: User ID
        
        Returns:
            Tool execution result
        """
        # Add user_id to arguments
        arguments["user_id"] = user_id
        
        # Get the tool function from our map
        tool_func = self.mcp_tool_map.get(tool_name)
        if not tool_func:
            return {"error": "TOOL_NOT_FOUND", "message": f"Tool {tool_name} not found"}
        
        try:
            # Execute tool directly
            result = tool_func(**arguments)
            return result
        except Exception as e:
            return {"error": "EXECUTION_ERROR", "message": str(e)}

    def run_agent(
        self,
        messages: List[Dict[str, str]],
        user_id: int,
        session: Any = None
    ) -> Dict[str, Any]:
        """
        Run the AI agent with conversation history and MCP tools.

        Args:
            messages: Conversation history (list of message dicts)
            user_id: User ID for tool execution
            session: Database session for tool execution

        Returns:
            Dict with response and tool_calls
        """
        # Get tool definitions in OpenAI format
        tools = self._get_mcp_tools_for_openai()

        # Add system prompt
        full_messages = [{"role": "system", "content": self.system_prompt}] + messages

        # Call OpenAI API with proper error handling
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                tools=tools,
                tool_choice="auto"
            )
        except RateLimitError as e:
            # Handle rate limits and quota errors
            error_msg = str(e)
            print(f"⚠️  OpenAI Rate Limit/Quota Error: {error_msg}")
            if "insufficient_quota" in error_msg or "quota" in error_msg.lower():
                raise RateLimitError(
                    f"OpenAI API quota exceeded: {error_msg}. "
                    f"Please check your billing at https://platform.openai.com/account/billing/overview"
                )
            raise
        except APIError as e:
            # Handle other API errors
            error_msg = str(e)
            if "insufficient_quota" in error_msg or "quota" in error_msg.lower():
                raise RateLimitError(
                    f"OpenAI API quota exceeded: {error_msg}. "
                    f"Please check your billing at https://platform.openai.com/account/billing/overview"
                )
            raise

        message = response.choices[0].message
        tool_calls = []

        # Execute tool calls if any
        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Execute tool
                try:
                    result = self._execute_mcp_tool(tool_name, tool_args, user_id)
                    tool_calls.append({
                        "tool": tool_name,
                        "arguments": tool_args,
                        "result": result
                    })
                except Exception as e:
                    tool_calls.append({
                        "tool": tool_name,
                        "arguments": tool_args,
                        "error": str(e)
                    })

        return {
            "response": message.content or "",
            "tool_calls": tool_calls
        }


# Global agent service instance
agent_service = AgentService()
