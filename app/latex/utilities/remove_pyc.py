from pathlib import Path

# Starting directory
base_dir = Path(r"C:\Users\gmccarthy\Documents\PC_RTD_GITHUB_resources\PC_flask_latex\app\latex")

# Find all __pycache__ folders and delete .pyc files inside
for pycache_dir in base_dir.rglob("__pycache__"):
    for pyc_file in pycache_dir.glob("*.pyc"):
        try:
            pyc_file.unlink()
            print(f"Deleted: {pyc_file}")
        except Exception as e:
            print(f"Failed to delete {pyc_file}: {e}")

