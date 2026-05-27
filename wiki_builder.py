import json
import os
from datetime import date
import anthropic

SESSIONS_PATH = r"C:\Users\LENOVO\AppData\Roaming\SPB_Data\.openclaw\agents\main\sessions"
VAULT_PATH = r"D:\Aairy_brain"

def get_today_sessions():
    today = date.today().strftime("%Y-%m-%d")
    conversations = []
    
    for file in os.listdir(SESSIONS_PATH):
        if not file.endswith('.jsonl'):
            continue
        filepath = os.path.join(SESSIONS_PATH, file)
        mod_date = date.fromtimestamp(
            os.path.getmtime(filepath)
        ).strftime("%Y-%m-%d")
        
        if mod_date == today:
            print(f"Reading: {file}")
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        if data.get('type') == 'message':
                            msg = data.get('message', {})
                            role = msg.get('role', '')
                            content = msg.get('content', '')
                            if isinstance(content, str) and content:
                                conversations.append({
                                    'role': role,
                                    'content': content
                                })
                            elif isinstance(content, list):
                                for block in content:
                                    if isinstance(block, dict) and block.get('type') == 'text':
                                        text = block.get('text', '')
                                        if text:
                                            conversations.append({
                                                'role': role,
                                                'content': text
                                            })
                    except:
                        continue
    
    return conversations

def extract_and_update_vault(conversations):
    if not conversations:
        print("No conversations found!")
        return
    
    conv_text = "\n".join([
        f"{msg['role']}: {msg['content'][:200]}"
        for msg in conversations
    ])
    
    print(f"Found {len(conversations)} messages!")
    print("Sending to Claude...")
    
    client = anthropic.Anthropic()
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"""You are updating an AI agent's memory files.

Below are today's conversations. Extract ONLY real work done.
Ignore system messages, metadata, and technical noise.

Write updates for 3 files:

1. PROJECT-STATE: What real projects were worked on?
2. DAILY-LOG for {date.today().strftime("%Y-%m-%d")}: What was actually done today?
3. WORKING-CONTEXT: What is the agent working on right now?

Conversations:
{conv_text[:3000]}

Format EXACTLY like this with REAL content not placeholders:
---PROJECT-STATE---
[real update here]
---DAILY-LOG---
[real update here]
---WORKING-CONTEXT---
[real update here]"""
        }]
    )
    
    result = response.content[0].text
    print("Analysis received!")
    
    sections = result.split('---')
    updates = {}
    
    for i, section in enumerate(sections):
        if 'PROJECT-STATE' in section:
            updates['project-state'] = sections[i+1] if i+1 < len(sections) else ""
        elif 'DAILY-LOG' in section:
            updates['daily'] = sections[i+1] if i+1 < len(sections) else ""
        elif 'WORKING-CONTEXT' in section:
            updates['working-context'] = sections[i+1] if i+1 < len(sections) else ""
    
    for filename, content in updates.items():
        if filename == 'daily':
            filepath = os.path.join(VAULT_PATH, "Agent-Aairy", "daily.md")
        elif filename == 'working-context':
            filepath = os.path.join(VAULT_PATH, "Agent-Aairy", "working-context.md")
        else:
            filepath = os.path.join(VAULT_PATH, "Agent-Shared", f"{filename}.md")
        
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"\n\n## Auto-updated {date.today()}\n")
            f.write(content.strip())
        
        print(f"✅ Updated: {filename}.md")

if __name__ == "__main__":
    print("🦞 Aairy Auto Wiki Builder Starting...")
    conversations = get_today_sessions()
    extract_and_update_vault(conversations)
    print("✅ Done!")