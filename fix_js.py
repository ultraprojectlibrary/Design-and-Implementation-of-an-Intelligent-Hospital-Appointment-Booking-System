import os

filepath = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates\appointments\doctor_profile.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

prefix = content.split('{% block extra_js %}')[0]

new_js = """{% block extra_js %}
<script>
    function openBookingModal(startTime, endTime) {
        document.getElementById('modalStartTime').value = startTime;
        document.getElementById('modalEndTime').value = endTime;
        const parts = startTime.split(':');
        let h = parseInt(parts[0]);
        const ampm = h >= 12 ? 'PM' : 'AM';
        h = h % 12;
        h = h ? h : 12;
        const formattedTime = h + ':' + parts[1] + ' ' + ampm;
        
        document.getElementById('modalTimeDisplay').innerText = formattedTime;
        
        const dateInputVal = document.getElementById('date-input').value;
        if(dateInputVal) {
            document.getElementById('modal-date-input').value = dateInputVal;
            const d = new Date(dateInputVal);
            document.getElementById('modalDateDisplay').innerText = d.toLocaleDateString('en-US', {month: 'short', day: 'numeric', year: 'numeric'});
        }
        
        document.getElementById('bookingModal').classList.remove('hidden');
        document.getElementById('bookingModal').classList.add('flex');
    }

    function closeBookingModal() {
        document.getElementById('bookingModal').classList.add('hidden');
        document.getElementById('bookingModal').classList.remove('flex');
    }
    
    document.getElementById('date-input').addEventListener('change', function() {
        const dateVal = this.value;
        const container = document.getElementById('slots-container');
        if(!dateVal) {
            container.innerHTML = '<div class=\"text-center py-10 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200\"><p class=\"text-gray-400 font-medium text-sm\">Select a date to check availability.</p></div>';
            return;
        }
        
        container.innerHTML = '<div class=\"text-center py-10 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200\"><p class=\"text-gray-400 font-medium text-sm\">Checking availability...</p></div>';
        
        fetch(`/appointments/doctor/{{ doctor.id }}/api/slots/?date=${dateVal}`)
            .then(res => res.json())
            .then(data => {
                if(data.error) {
                    container.innerHTML = `<div class=\"text-center py-8 bg-red-50 text-red-500 rounded-2xl\">${data.error}</div>`;
                    return;
                }
                
                let html = `<div class=\"flex items-center justify-between mb-4\"><div class=\"flex items-center gap-2\"><h3 class=\"font-bold text-gray-800 text-sm\">Slots for ${dateVal}</h3>`;
                if (data.slots && data.slots.length > 0) {
                    const available = data.slots.filter(s => s.is_available).length;
                    if(available > 0) {
                        html += `<svg class=\"w-5 h-5 text-green-500\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"/></svg></div>`;
                        html += `<span class=\"text-xs font-medium text-green-600 bg-green-50 px-2.5 py-1 rounded-full\">${available} slot(s) available</span>`;
                    } else {
                        html += `<svg class=\"w-5 h-5 text-red-500\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M6 18L18 6M6 6l12 12\"/></svg></div>`;
                    }
                } else {
                    html += `<svg class=\"w-5 h-5 text-red-500\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M6 18L18 6M6 6l12 12\"/></svg></div>`;
                }
                html += `</div>`;
                
                if (data.slots && data.slots.length > 0) {
                    html += `<div class=\"grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-2.5\">`;
                    data.slots.forEach(slot => {
                        if(slot.is_available) {
                            html += `<button type=\"button\" onclick=\"openBookingModal('${slot.start_time}', '${slot.end_time}')\" class=\"py-2.5 px-3 rounded-xl border border-green-200 text-green-700 bg-green-50 text-xs font-semibold hover:bg-green-600 hover:text-white hover:border-green-600 transition-all duration-150\">${slot.start_time_display}</button>`;
                        } else {
                            html += `<button type=\"button\" disabled class=\"py-2.5 px-3 rounded-xl border border-red-100 text-red-400 bg-red-50 text-xs font-medium line-through cursor-not-allowed\">${slot.start_time_display}</button>`;
                        }
                    });
                    html += `</div>`;
                } else {
                    html += `<div class=\"text-center py-8 bg-red-50 rounded-2xl\"><p class=\"text-red-500 font-medium text-sm\">Doctor is not available on this date.</p></div>`;
                }
                
                if (data.recommendation) {
                    html += `<div class=\"mt-6 bg-brand-50 rounded-2xl border border-brand-100 p-5\"><p class=\"font-semibold text-brand-800 text-sm\">Suggested Alternative: <strong>${data.recommendation.display}</strong></p></div>`;
                }
                
                container.innerHTML = html;
            })
            .catch(err => {
                container.innerHTML = '<div class=\"text-center py-8 bg-red-50 text-red-500 rounded-2xl\">Error fetching slots.</div>';
            });
    });

    if(document.getElementById('date-input').value) {
        document.getElementById('date-input').dispatchEvent(new Event('change'));
    }

    document.getElementById('bookingModal').addEventListener('click', function(e) {
        if (e.target === this) closeBookingModal();
    });
</script>
{% endblock %}
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(prefix + new_js)
print('Fixed javascript in doctor_profile.html')
