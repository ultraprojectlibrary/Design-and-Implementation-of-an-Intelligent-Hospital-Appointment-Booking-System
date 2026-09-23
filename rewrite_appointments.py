import re

# Rewrite patients/appointments.html
filepath_pat = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates\patients\appointments.html'
with open(filepath_pat, 'r', encoding='utf-8') as f:
    pat_content = f.read()

pat_list_html = r'<div class=\"space-y-4\">\s*{% for appt in appointments %}.*?{% empty %}\s*<div class=\"bg-white rounded-2xl border border-dashed border-gray-200 p-12 text-center\">.*?</div>\s*{% endfor %}\s*</div>'

pat_table_html = '''<div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
    <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
            <thead>
                <tr class="bg-gray-50 border-b border-gray-100 text-xs uppercase tracking-wider text-gray-500 font-semibold">
                    <th class="px-6 py-4">Doctor</th>
                    <th class="px-6 py-4">Date & Time</th>
                    <th class="px-6 py-4">Status</th>
                    <th class="px-6 py-4 text-right">Action</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 text-sm">
                {% for appt in appointments %}
                <tr class="hover:bg-gray-50 transition-colors">
                    <td class="px-6 py-4">
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded-full bg-brand-100 flex items-center justify-center text-brand-700 font-bold flex-shrink-0">
                                {{ appt.doctor.user.first_name|first }}{{ appt.doctor.user.last_name|first }}
                            </div>
                            <div>
                                <p class="font-semibold text-gray-900">Dr. {{ appt.doctor.user.get_full_name }}</p>
                                <p class="text-xs text-gray-500">{{ appt.doctor.department.name }}</p>
                            </div>
                        </div>
                    </td>
                    <td class="px-6 py-4">
                        <p class="font-medium text-gray-900">{{ appt.appointment_date|date:"M j, Y" }}</p>
                        <p class="text-xs text-gray-500">{{ appt.start_time|time:"g:i A" }}</p>
                        <span class="countdown-badge hidden mt-1 text-[10px] font-bold text-brand-600 uppercase tracking-wider" data-datetime="{{ appt.appointment_date|date:'Y-m-d' }}T{{ appt.start_time|time:'H:i' }}"></span>
                    </td>
                    <td class="px-6 py-4">
                        <span class="px-2.5 py-1 text-xs font-semibold rounded-lg 
                            {% if appt.status == 'Confirmed' %}bg-green-100 text-green-700
                            {% elif appt.status == 'Pending' %}bg-yellow-100 text-yellow-700
                            {% elif appt.status == 'Completed' %}bg-gray-100 text-gray-500
                            {% elif appt.status == 'Cancelled' %}bg-red-100 text-red-700
                            {% else %}bg-gray-100 text-gray-500{% endif %}">
                            {{ appt.status }}
                        </span>
                    </td>
                    <td class="px-6 py-4 text-right">
                        {% if appt.status == 'Pending' or appt.status == 'Confirmed' %}
                        <a href="{% url 'cancel_appointment' appt.id %}" class="text-xs font-semibold text-red-600 hover:text-red-700 bg-red-50 hover:bg-red-100 px-3 py-1.5 rounded-lg transition-colors">Cancel</a>
                        {% endif %}
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="4" class="px-6 py-12 text-center">
                        <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                        <h3 class="text-lg font-bold text-gray-900">No appointments found</h3>
                        <p class="text-gray-500 text-sm mt-1">You haven't booked any appointments yet.</p>
                        <a href="{% url 'doctor_list' %}" class="inline-block mt-4 px-6 py-2.5 bg-brand-600 text-white font-semibold text-sm rounded-xl hover:bg-brand-700 shadow-sm transition-colors">Book Now</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>'''

pat_content = re.sub(pat_list_html, pat_table_html, pat_content, flags=re.DOTALL)
with open(filepath_pat, 'w', encoding='utf-8') as f:
    f.write(pat_content)

# Rewrite doctors/appointments.html
filepath_doc = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates\doctors\appointments.html'
with open(filepath_doc, 'r', encoding='utf-8') as f:
    doc_content = f.read()

doc_list_html = r'<div class=\"space-y-4\">\s*{% for appt in appointments %}.*?{% empty %}\s*<div class=\"bg-white rounded-2xl border border-dashed border-gray-200 p-12 text-center\">.*?</div>\s*{% endfor %}\s*</div>'

doc_table_html = '''<div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
    <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
            <thead>
                <tr class="bg-gray-50 border-b border-gray-100 text-xs uppercase tracking-wider text-gray-500 font-semibold">
                    <th class="px-6 py-4">Patient</th>
                    <th class="px-6 py-4">Date & Time</th>
                    <th class="px-6 py-4">Status</th>
                    <th class="px-6 py-4 text-right">Action</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 text-sm">
                {% for appt in appointments %}
                <tr class="hover:bg-gray-50 transition-colors">
                    <td class="px-6 py-4">
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded-full bg-brand-100 flex items-center justify-center text-brand-700 font-bold flex-shrink-0">
                                {{ appt.patient.user.first_name|first|default:appt.patient.user.username|first }}
                            </div>
                            <div>
                                <p class="font-semibold text-gray-900">{{ appt.patient.user.get_full_name|default:appt.patient.user.username }}</p>
                                <p class="text-xs text-gray-500 truncate max-w-[150px]">{{ appt.reason_for_visit|default:"No reason provided" }}</p>
                            </div>
                        </div>
                    </td>
                    <td class="px-6 py-4">
                        <p class="font-medium text-gray-900">{{ appt.appointment_date|date:"M j, Y" }}</p>
                        <p class="text-xs text-gray-500">{{ appt.start_time|time:"g:i A" }}</p>
                        <span class="countdown-badge hidden mt-1 text-[10px] font-bold text-brand-600 uppercase tracking-wider" data-datetime="{{ appt.appointment_date|date:'Y-m-d' }}T{{ appt.start_time|time:'H:i' }}"></span>
                    </td>
                    <td class="px-6 py-4">
                        <span class="px-2.5 py-1 text-xs font-semibold rounded-lg 
                            {% if appt.status == 'Confirmed' %}bg-green-100 text-green-700
                            {% elif appt.status == 'Pending' %}bg-yellow-100 text-yellow-700
                            {% elif appt.status == 'Completed' %}bg-gray-100 text-gray-500
                            {% elif appt.status == 'Cancelled' %}bg-red-100 text-red-700
                            {% else %}bg-gray-100 text-gray-500{% endif %}">
                            {{ appt.status }}
                        </span>
                    </td>
                    <td class="px-6 py-4 text-right">
                        {% if appt.status == 'Pending' %}
                            <form method="post" action="{% url 'update_appointment_status' appt.id %}" class="inline">
                                {% csrf_token %}
                                <input type="hidden" name="status" value="Confirmed">
                                <button type="submit" class="text-xs font-semibold text-green-600 hover:text-green-700 bg-green-50 hover:bg-green-100 px-3 py-1.5 rounded-lg transition-colors">Confirm</button>
                            </form>
                        {% elif appt.status == 'Confirmed' %}
                            <form method="post" action="{% url 'update_appointment_status' appt.id %}" class="inline">
                                {% csrf_token %}
                                <input type="hidden" name="status" value="Completed">
                                <button type="submit" class="text-xs font-semibold text-gray-600 hover:text-gray-700 bg-gray-50 hover:bg-gray-100 px-3 py-1.5 rounded-lg border border-gray-200 transition-colors">Mark Done</button>
                            </form>
                        {% endif %}
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="4" class="px-6 py-12 text-center">
                        <svg class="w-12 h-12 text-gray-300 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                        <h3 class="text-lg font-bold text-gray-900">No appointments found</h3>
                        <p class="text-gray-500 text-sm mt-1">You don't have any appointments in this list.</p>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>'''

doc_content = re.sub(doc_list_html, doc_table_html, doc_content, flags=re.DOTALL)
with open(filepath_doc, 'w', encoding='utf-8') as f:
    f.write(doc_content)

print('Updated Appointments tables')
