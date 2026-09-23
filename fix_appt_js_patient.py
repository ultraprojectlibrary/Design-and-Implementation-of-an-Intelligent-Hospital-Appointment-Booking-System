import re
filepath = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates\patients\appointments.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add badge
pattern = re.compile(r'(<span class="px-3 py-1 text-xs font-bold rounded-full uppercase tracking-wider)')
content = re.sub(pattern, r'<span class="countdown-badge hidden px-2.5 py-1 text-[10px] font-bold rounded-full bg-brand-50 text-brand-700 uppercase tracking-wider" data-datetime="{{ appt.appointment_date|date:\'Y-m-d\' }}T{{ appt.start_time|time:\'H:i\' }}"></span>\n            \1', content)

# Add js
js = '''
{% block extra_js %}
<script>
    function parseDateLocal(datetimeStr) {
        const parts = datetimeStr.split('T');
        if (parts.length !== 2) return new Date();
        const dParts = parts[0].split('-');
        const tParts = parts[1].split(':');
        return new Date(dParts[0], dParts[1]-1, dParts[2], tParts[0], tParts[1], 0, 0);
    }

    function updateCountdowns() {
        const now = new Date().getTime();
        
        const badges = document.querySelectorAll('.countdown-badge');
        badges.forEach(badge => {
            const dtStr = badge.getAttribute('data-datetime');
            const target = parseDateLocal(dtStr).getTime();
            const diff = target - now;
            
            if (diff > 0) {
                badge.classList.remove('hidden');
                badge.classList.add('inline-block');
                
                const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                if (days > 0) {
                    badge.innerText = `In ${days} day${days > 1 ? 's' : ''}`;
                } else if (hours > 0) {
                    badge.innerText = `In ${hours} hr${hours > 1 ? 's' : ''}`;
                } else {
                    const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                    badge.innerText = `In ${mins} min${mins > 1 ? 's' : ''}`;
                }
            } else {
                badge.classList.add('hidden');
                badge.classList.remove('inline-block');
            }
        });
    }
    
    updateCountdowns();
    setInterval(updateCountdowns, 1000);
</script>
{% endblock %}
'''

if '{% block extra_js %}' not in content:
    content += js

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated patient appointments page')
