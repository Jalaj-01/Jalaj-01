import json
import os
import subprocess
from datetime import datetime, timedelta, timezone

def run_cmd(args):
    try:
        return subprocess.check_output(args, stderr=subprocess.DEVNULL).decode('utf-8').strip()
    except Exception:
        return "N/A"

def get_git_info():
    commit_hash = run_cmd(["git", "rev-parse", "--short", "HEAD"])
    commit_msg = run_cmd(["git", "log", "-1", "--format=%s"])
    branch = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return commit_hash, commit_msg, branch

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))
    
    now_json_path = os.path.join(repo_root, "now.json")
    readme_path = os.path.join(repo_root, "README.md")
    
    # Load now.json details
    if os.path.exists(now_json_path):
        with open(now_json_path, "r", encoding="utf-8") as f:
            now_data = json.load(f)
    else:
        now_data = {
            "building": "Product Engineering projects",
            "learning": "Distributed Systems",
            "reading": "Technical blogs & engineering books",
            "listening": "Lofi focus tracks"
        }
        
    commit_hash, commit_msg, branch = get_git_info()
    
    # Calculate Kolkata time (UTC + 5:30)
    tz_kolkata = timezone(timedelta(hours=5, minutes=30))
    time_str = datetime.now(tz_kolkata).strftime("%b %d, %Y %I:%M %p (IST)")
    
    # Generate new Markdown for the Now section
    now_markdown = f"""
| Attribute | Current Activity / Status |
| :--- | :--- |
| 🚀 **Building** | {now_data.get('building', 'N/A')} |
| 📚 **Learning** | {now_data.get('learning', 'N/A')} |
| 📖 **Reading** | {now_data.get('reading', 'N/A')} |
| 🎧 **Listening to** | {now_data.get('listening', 'N/A')} |
| 📅 **Last Updated** | `{time_str}` |
| 🌿 **Branch** | `{branch}` |
| 💻 **Latest Commit** | `{commit_hash}` — *{commit_msg}* |
"""

    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        start_tag = "<!-- START_SECTION:now -->"
        end_tag = "<!-- END_SECTION:now -->"
        
        start_idx = content.find(start_tag)
        end_idx = content.find(end_tag)
        
        if start_idx != -1 and end_idx != -1:
            new_content = (
                content[:start_idx + len(start_tag)] + 
                "\n" + now_markdown.strip() + "\n" + 
                content[end_idx:]
            )
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("Successfully updated README.md")
        else:
            print("Placeholder tags not found in README.md")
    else:
        print("README.md not found")

if __name__ == "__main__":
    main()
