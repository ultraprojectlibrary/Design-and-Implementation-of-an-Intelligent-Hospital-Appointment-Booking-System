import re

# Update dashboard_base.html
filepath = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates\dashboard_base.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add Toastify CSS
css_link = '<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css">\n    <style>body { font-family: \'Inter\', sans-serif; }</style>'
content = re.sub(r'<style>body \{ font-family: \'Inter\', sans-serif; \}</style>', css_link, content)

# Remove old messages
messages_html = r'{% if messages %}\s*{% for message in messages %}\s*<div.*?</div>\s*{% endfor %}\s*{% endif %}'
content = re.sub(messages_html, '', content, flags=re.DOTALL)

# Add Toastify JS
js_script = '''<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/toastify-js"></script>
<script>
    {% if messages %}
        {% for message in messages %}
            Toastify({
                text: "{{ message }}",
                duration: 4000,
                close: true,
                gravity: "top",
                position: "right",
                style: {
                    background: "{% if message.tags == 'error' %}#ef4444{% else %}#10b981{% endif %}",
                    borderRadius: "8px",
                    boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                    fontFamily: "'Inter', sans-serif",
                    fontSize: "14px",
                    fontWeight: "500",
                }
            }).showToast();
        {% endfor %}
    {% endif %}

    function openSidebar()  { document.getElementById('sidebar').classList.remove('-translate-x-full'); document.getElementById('sidebar-overlay').classList.remove('hidden'); }
'''
content = content.replace("    function openSidebar()  { document.getElementById('sidebar').classList.remove('-translate-x-full'); document.getElementById('sidebar-overlay').classList.remove('hidden'); }", js_script)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)


# Update base.html
filepath_base = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates\base.html'
with open(filepath_base, 'r', encoding='utf-8') as f:
    content_base = f.read()

content_base = re.sub(r'    <style>\n      /\* Smooth page transitions \*/', '<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css">\n    <style>\n      /* Smooth page transitions */', content_base)

content_base = content_base.replace('</body>', '''
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/toastify-js"></script>
    <script>
        {% if messages %}
            {% for message in messages %}
                Toastify({
                    text: "{{ message }}",
                    duration: 4000,
                    close: true,
                    gravity: "top",
                    position: "right",
                    style: {
                        background: "{% if message.tags == 'error' %}#ef4444{% else %}#10b981{% endif %}",
                        borderRadius: "8px",
                        boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                        fontFamily: "'Inter', sans-serif",
                        fontSize: "14px",
                        fontWeight: "500",
                    }
                }).showToast();
            {% endfor %}
        {% endif %}
    </script>
</body>''')

with open(filepath_base, 'w', encoding='utf-8') as f:
    f.write(content_base)

# Update login.html (remove inline messages)
filepath_login = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates\accounts\login.html'
with open(filepath_login, 'r', encoding='utf-8') as f:
    content_login = f.read()
content_login = re.sub(messages_html, '', content_login, flags=re.DOTALL)
with open(filepath_login, 'w', encoding='utf-8') as f:
    f.write(content_login)

# Update register.html (remove inline messages)
filepath_register = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates\accounts\register.html'
try:
    with open(filepath_register, 'r', encoding='utf-8') as f:
        content_reg = f.read()
    content_reg = re.sub(messages_html, '', content_reg, flags=re.DOTALL)
    with open(filepath_register, 'w', encoding='utf-8') as f:
        f.write(content_reg)
except:
    pass

print('Updated Toasts')
