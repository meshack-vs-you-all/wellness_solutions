import os

def fix_venv_paths():
    venv_bin = '/home/meshack/src/work/wellness_solutions/venv_new/bin'
    if not os.path.exists(venv_bin):
        return
    for file in os.listdir(venv_bin):
        filepath = os.path.join(venv_bin, file)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if '/home/meshack/src/work/jpf_stretch_hub' in content:
                    new_content = content.replace('/home/meshack/src/work/jpf_stretch_hub', '/home/meshack/src/work/wellness_solutions')
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
            except Exception:
                pass

def generalize_wellness():
    replacements = {
        "wellness session": "wellness session",
        "Wellness Session": "Wellness Session",
        "wellness practitioner": "wellness practitioner",
        "Wellness Practitioner": "Wellness Practitioner",
        "wellness session": "wellness session",
        "Wellness Session": "Wellness Session",
        "wellness_type": "wellness_type",
        "'wellness'": "'wellness'",
        "\"stretch\"": "\"wellness\"",
        "wellness-therapy": "wellness-therapy",
        "wellnesssolutions.com": "wellnesssolutions.com",
    }
    for root, dirs, files in os.walk('/home/meshack/src/work/wellness_solutions'):
        if any(exclude in root for exclude in ['.git', 'node_modules', 'venv', 'venv_new', '__pycache__', 'staticfiles', '.pytest_cache', '.ruff_cache', 'media']):
            continue
        for file in files:
            if file.endswith(('.py', '.html', '.tsx', '.ts', '.js', '.md', '.json', '.yml', '.yaml', '.sh', '.rst', '.txt', '.env', '.toml')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    new_content = content
                    for old, new in replacements.items():
                        new_content = new_content.replace(old, new)
                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Generalized {filepath}")
                except Exception:
                    pass

fix_venv_paths()
generalize_wellness()
