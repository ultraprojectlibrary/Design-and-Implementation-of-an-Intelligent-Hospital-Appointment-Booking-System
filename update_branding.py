import os

def update_branding():
    # Base directory of your project
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Update templates
    templates_dir = os.path.join(base_dir, 'templates')
    if os.path.exists(templates_dir):
        for root, dirs, files in os.walk(templates_dir):
            for file in files:
                if file.endswith('.html') or file.endswith('.txt'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace logos
                    new_content = content.replace('smartcare_logo.png', 'regal_logo.png')
                    new_content = new_content.replace('smartcare_logo.jpg', 'regal_logo.png')
                    # Replace text
                    new_content = new_content.replace('SmartCare', 'Regal')
                    new_content = new_content.replace('smartcare', 'regal')
                    
                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f'Updated {filepath}')
    else:
        print(f"Could not find templates directory at {templates_dir}")

    # 2. Update accounts/views.py
    views_path = os.path.join(base_dir, 'accounts', 'views.py')
    if os.path.exists(views_path):
        with open(views_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content.replace('SmartCare', 'Regal')
        
        if new_content != content:
            with open(views_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {views_path}')
    else:
        print(f"Could not find {views_path}")

if __name__ == '__main__':
    update_branding()
    print("Branding update complete!")
