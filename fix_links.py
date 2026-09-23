import os
import re

directory = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates'

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            new_content = content
            # Replace book_start url with doctor_list
            new_content = new_content.replace("{% url 'book_start' %}", "{% url 'doctor_list' %}")

            # Remove Find Doctors link block
            pattern = re.compile(r'<a href="{% url \'doctor_list\' %}"([^>]*?>\s*<svg[^>]*?>.*?</svg>\s*)Find Doctors\s*</a>', re.DOTALL)
            new_content = re.sub(pattern, '', new_content)

            # Same for 'All Doctors' block in some sidebars
            pattern2 = re.compile(r'<a href="{% url \'doctor_list\' %}"([^>]*?>\s*<svg[^>]*?>.*?</svg>\s*)All Doctors\s*</a>', re.DOTALL)
            new_content = re.sub(pattern2, '', new_content)

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Updated {file}')
