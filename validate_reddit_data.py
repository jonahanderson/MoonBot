import json
from collections import defaultdict

def validate_jsonl(file_path):
    format_errors = defaultdict(int)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    ex = json.loads(line)
                    
                    if not isinstance(ex, dict):
                        format_errors["data_type"] += 1
                        continue
                        
                    messages = ex.get("messages", None)
                    if not messages:
                        format_errors["missing_messages_list"] += 1
                        continue
                        
                    for message in messages:
                        if "role" not in message or "content" not in message:
                            format_errors["message_missing_key"] += 1
                        
                        if any(k not in ("role", "content", "name", "function_call", "weight") for k in message):
                            format_errors["message_unrecognized_key"] += 1
                        
                        if message.get("role", None) not in ("system", "user", "assistant", "function"):
                            format_errors["unrecognized_role"] += 1
                            
                        content = message.get("content", None)
                        function_call = message.get("function_call", None)
                        
                        if (not content and not function_call) or (content and not isinstance(content, str)):
                            format_errors["missing_content"] += 1
                    
                    if not any(message.get("role", None) == "assistant" for message in messages):
                        format_errors["example_missing_assistant_message"] += 1

                except json.JSONDecodeError:
                    format_errors["json_decode_error"] += 1
                    continue

        if format_errors:
            print("Found errors:")
            for k, v in format_errors.items():
                print(f"{k}: {v}")
        else:
            print("No errors found")
    
    except Exception as e:
        print(f"Error opening file: {e}")

# Path to your JSONL file
file_path = 'reddit_data.jsonl'
validate_jsonl(file_path)
