import re
filepath = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates\doctors\dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

banner = '''
<!-- Next Appointment Banner -->
{% if next_appointment %}
<div class="bg-gradient-to-r from-brand-600 to-indigo-600 rounded-2xl p-5 sm:p-6 mb-6 text-white shadow-lg">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
            <p class="text-blue-100 text-xs font-semibold uppercase tracking-wider mb-1">Next Appointment</p>
            <h2 class="text-xl font-bold">{{ next_appointment.patient.user.get_full_name|default:next_appointment.patient.user.username }}</h2>
            <p class="text-blue-100 text-sm mt-0.5">{{ next_appointment.reason_for_visit }}</p>
            <div class="flex flex-wrap gap-4 mt-3 text-sm">
                <span class="flex items-center gap-1.5">
                    <svg class="w-4 h-4 opacity-75" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                    {{ next_appointment.appointment_date|date:"l, F j" }}
                </span>
                <span class="flex items-center gap-1.5">
                    <svg class="w-4 h-4 opacity-75" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                    {{ next_appointment.start_time|time:"g:i A" }}
                </span>
            </div>
            <div class="mt-4 bg-white/10 rounded-xl p-3 inline-block">
                <p class="text-[10px] text-blue-200 uppercase tracking-widest font-bold mb-1">Starts In</p>
                <div id="next-appt-countdown" data-datetime="{{ next_appointment.appointment_date|date:'Y-m-d' }}T{{ next_appointment.start_time|time:'H:i' }}" class="text-xl sm:text-2xl font-mono font-bold tracking-tight">
                    Calculating...
                </div>
            </div>
        </div>
    </div>
</div>
{% endif %}
'''

content = content.replace('</div>\n\n<!-- Content Grid -->', '</div>\n' + banner + '\n<!-- Content Grid -->')

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
        const mainEl = document.getElementById('next-appt-countdown');
        if (mainEl) {
            const dtStr = mainEl.getAttribute('data-datetime');
            const target = parseDateLocal(dtStr).getTime();
            const diff = target - now;
            
            if (diff > 0) {
                const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                const secs = Math.floor((diff % (1000 * 60)) / 1000);
                
                let text = '';
                if (days > 0) text += days + 'd ';
                text += hours.toString().padStart(2, '0') + 'h ';
                text += mins.toString().padStart(2, '0') + 'm ';
                text += secs.toString().padStart(2, '0') + 's';
                
                mainEl.innerText = text;
            } else {
                mainEl.innerText = 'Started/Passed';
            }
        }
    }
    updateCountdowns();
    setInterval(updateCountdowns, 1000);
</script>
{% endblock %}
'''

if '{% block extra_js %}' not in content:
    content = content + js

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated doctor dashboard html')
