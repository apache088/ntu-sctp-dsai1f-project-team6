#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from pathlib import Path
import shutil

# 1. Load root .env variables
load_dotenv()  # Loads from current directory by default

# 2. Get project paths from environment variables
projects = {
    "meltano": os.getenv("MELTANO_PROJECT_ROOT", "meltano"),
    "dbt": os.getenv("DBT_PROJECT_ROOT", "dbt"),
    "dagster": os.getenv("DAGSTER_PROJECT_ROOT", "dagster")
}

# 3. Copy root .env to each project
root_env = Path(".env")
if not root_env.exists():
    raise FileNotFoundError("Root .env file not found")

for name, path in projects.items():
    try:
        target_dir = Path(path)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        shutil.copy(str(root_env), str(target_dir / ".env"))
        print(f"✅ Copied .env to {name} project at: {target_dir}/")
        
    except Exception as e:
        print(f"❌ Failed to copy to {name} project: {str(e)}")