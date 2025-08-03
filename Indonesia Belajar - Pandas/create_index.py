import os
import json
import re
from datetime import datetime

def extract_title_from_notebook(file_path):
    """Extract title from first markdown cell of notebook"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
            
        # Find first markdown cell
        for cell in notebook['cells']:
            if cell['cell_type'] == 'markdown' and cell['source']:
                # Get first line and clean it
                title = cell['source'][0].strip()
                # Remove markdown heading symbols
                title = re.sub(r'^#+\s*', '', title)
                # Remove number prefix if exists (like "23: ")
                title = re.sub(r'^\d+:\s*', '', title)
                return title
                
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return "Unknown Title"
    
    return "No Title Found"

def create_index():
    """Generate README.md with index of all notebooks"""
    
    print("🔍 Scanning for notebook files...")
    
    # Get all notebook files
    notebook_files = []
    for file in sorted(os.listdir('.')):
        if file.endswith('.ipynb') and not file.startswith('.'):
            notebook_files.append(file)
    
    print(f"📚 Found {len(notebook_files)} notebook files")
    
    # Extract titles and create index
    notebooks_info = []
    for file in notebook_files:
        print(f"📖 Processing: {file}")
        title = extract_title_from_notebook(file)
        
        # Extract number from filename for sorting
        match = re.search(r'IB_Pandas(\d+)', file)
        number = int(match.group(1)) if match else 0
        
        notebooks_info.append({
            'file': file,
            'title': title,
            'number': number
        })
    
    # Sort by number
    notebooks_info.sort(key=lambda x: x['number'])
    
    # Generate README content
    readme_content = f"""# Indonesia Belajar - Pandas Learning Journey 🐼

> **Learning Progress:** {len(notebook_files)}/56 Topics Completed ✅
> 
> **Last Updated:** {datetime.now().strftime('%B %d, %Y')}

## 📋 Table of Contents

| No | Topic | Notebook |
|----|-------|----------|
"""
    
    # Add table rows
    for info in notebooks_info:
        readme_content += f"| {info['number']:02d} | {info['title']} | [`{info['file']}`](./{info['file']}) |\n"
    
    readme_content += f"""
## 📊 Data Files

- [`data/iris.csv`](./data/iris.csv) - Iris flower dataset (150 rows)
- [`data/titanicfull.csv`](./data/titanicfull.csv) - Titanic passenger data (~900 rows)

## 🚀 How to Use

1. **Clone this repository:**
   ```bash
   git clone https://github.com/hanifalazis/learning-journey.git
   cd learning-journey/Indonesia-Belajar-Pandas
   ```

2. **Install requirements:**
   ```bash
   pip install pandas numpy jupyter
   ```

3. **Run Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```

4. **Start learning!** Open any notebook and follow along.

## 🎯 Learning Objectives

This series covers essential pandas operations including:
- Data manipulation and cleaning
- DataFrame operations
- Aggregation and grouping
- Memory optimization
- Advanced filtering techniques

## 📝 Notes

- Each notebook is self-contained with sample data
- Code follows Python best practices and PEP 8
- Examples use real-world datasets when possible

---

**Happy Learning!** 🎓

*Generated automatically by `create_index.py` on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # Write README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README.md generated successfully!")
    print(f"📝 Created index for {len(notebook_files)} notebooks")
    print("🔗 Check README.md for the complete index")

if __name__ == "__main__":
    print("🐼 Pandas Learning Journey Index Generator")
    print("=" * 50)
    create_index()
