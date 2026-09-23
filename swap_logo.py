import re

# base.html
filepath = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates\base.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'<div class="w-8 h-8 bg-brand-600.*?<span class="text-xl font-bold text-gray-900 tracking-tight">SmartCare</span>', re.DOTALL)
replacement = r'<img src="{% static \'images/smartcare_logo.jpg\' %}" alt="SmartCare Logo" class="h-8 w-auto mix-blend-multiply">'

content = re.sub(pattern, replacement, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)


# dashboard_base.html
filepath_dash = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates\dashboard_base.html'
with open(filepath_dash, 'r', encoding='utf-8') as f:
    content_dash = f.read()

pattern_dash = re.compile(r'<div class="w-8 h-8 bg-brand-600.*?<span class="text-lg font-bold text-gray-900 tracking-tight">SmartCare</span>', re.DOTALL)
replacement_dash = r'<img src="{% static \'images/smartcare_logo.jpg\' %}" alt="SmartCare Logo" class="h-8 w-auto mix-blend-multiply">'

content_dash = re.sub(pattern_dash, replacement_dash, content_dash)

with open(filepath_dash, 'w', encoding='utf-8') as f:
    f.write(content_dash)

print('Updated logos')
