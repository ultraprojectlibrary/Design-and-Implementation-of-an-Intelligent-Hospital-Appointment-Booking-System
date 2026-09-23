import re

# Update patients/dashboard.html
filepath = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates\patients\dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace countdown text
content = content.replace("mainEl.innerText = 'Started/Passed';", "mainEl.innerText = 'In Progress';")

# Replace list format with table format for upcoming appointments
list_html = r'<div class=\"space-y-3\">\s*<h3 class=\"font-bold text-gray-900 text-sm uppercase tracking-wide\">Upcoming Appointments</h3>\s*{% for appt in upcoming_appointments %}.*?{% empty %}\s*<div.*?</div>\s*{% endfor %}\s*</div>'

table_html = '''<div class="space-y-3">
        <h3 class="font-bold text-gray-900 text-sm uppercase tracking-wide">Upcoming Appointments</h3>
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
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
                        {% for appt in upcoming_appointments %}
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
                            </td>
                            <td class="px-6 py-4">
                                <span class="px-2.5 py-1 text-xs font-semibold rounded-lg 
                                    {% if appt.status == 'Confirmed' %}bg-green-100 text-green-700
                                    {% elif appt.status == 'Pending' %}bg-yellow-100 text-yellow-700
                                    {% else %}bg-blue-100 text-blue-700{% endif %}">
                                    {{ appt.status }}
                                </span>
                            </td>
                            <td class="px-6 py-4 text-right">
                                <a href="{% url 'cancel_appointment' appt.id %}" class="text-xs font-semibold text-red-600 hover:text-red-700 bg-red-50 hover:bg-red-100 px-3 py-1.5 rounded-lg transition-colors">Cancel</a>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="4" class="px-6 py-8 text-center text-gray-400">No upcoming appointments.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>'''

content = re.sub(list_html, table_html, content, flags=re.DOTALL)

# Same for past appointments
past_list_html = r'<div class=\"space-y-3 mt-8\">\s*<h3 class=\"font-bold text-gray-900 text-sm uppercase tracking-wide\">Recent Past Appointments</h3>\s*{% for appt in past_appointments %}.*?{% empty %}\s*<div.*?</div>\s*{% endfor %}\s*</div>'

past_table_html = '''<div class="space-y-3 mt-8">
        <h3 class="font-bold text-gray-900 text-sm uppercase tracking-wide">Recent Past Appointments</h3>
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse opacity-75">
                    <thead>
                        <tr class="bg-gray-50 border-b border-gray-100 text-xs uppercase tracking-wider text-gray-500 font-semibold">
                            <th class="px-6 py-4">Doctor</th>
                            <th class="px-6 py-4">Date & Time</th>
                            <th class="px-6 py-4">Status</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100 text-sm">
                        {% for appt in past_appointments %}
                        <tr class="hover:bg-gray-50 transition-colors">
                            <td class="px-6 py-4">
                                <p class="font-semibold text-gray-900">Dr. {{ appt.doctor.user.get_full_name }}</p>
                            </td>
                            <td class="px-6 py-4">
                                <p class="text-gray-600">{{ appt.appointment_date|date:"M j, Y" }} at {{ appt.start_time|time:"g:i A" }}</p>
                            </td>
                            <td class="px-6 py-4">
                                <span class="px-2.5 py-1 text-xs font-semibold rounded-lg bg-gray-100 text-gray-600">
                                    {{ appt.status }}
                                </span>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="3" class="px-6 py-8 text-center text-gray-400">No past appointments.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>'''

content = re.sub(past_list_html, past_table_html, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)


# Update doctors/dashboard.html
doc_filepath = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates\doctors\dashboard.html'
with open(doc_filepath, 'r', encoding='utf-8') as f:
    doc_content = f.read()

doc_list_html = r'<div class=\"grid grid-cols-1 lg:grid-cols-2 gap-6\">\s*<!-- Today\'s Appointments -->.*?<!-- Upcoming Appointments -->.*?</div>'

doc_table_html = '''<div class="space-y-8">
    <!-- Today's Appointments -->
    <div class="space-y-3">
        <div class="flex items-center justify-between">
            <h3 class="font-bold text-gray-900 text-sm uppercase tracking-wide">Today's Appointments</h3>
            <a href="{% url 'doctor_appointments' %}" class="text-xs font-bold text-brand-600 hover:text-brand-700">View All</a>
        </div>
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-gray-50 border-b border-gray-100 text-xs uppercase tracking-wider text-gray-500 font-semibold">
                            <th class="px-6 py-4">Patient</th>
                            <th class="px-6 py-4">Time</th>
                            <th class="px-6 py-4">Reason</th>
                            <th class="px-6 py-4 text-right">Action</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100 text-sm">
                        {% for appt in todays_appointments %}
                        <tr class="hover:bg-gray-50 transition-colors">
                            <td class="px-6 py-4">
                                <p class="font-semibold text-gray-900">{{ appt.patient.user.get_full_name|default:appt.patient.user.username }}</p>
                            </td>
                            <td class="px-6 py-4">
                                <p class="font-medium text-brand-600">{{ appt.start_time|time:"g:i A" }} - {{ appt.end_time|time:"g:i A" }}</p>
                            </td>
                            <td class="px-6 py-4">
                                <p class="text-gray-600 truncate max-w-[200px]">{{ appt.reason_for_visit|default:"-" }}</p>
                            </td>
                            <td class="px-6 py-4 text-right space-x-2">
                                {% if appt.status == 'Pending' %}
                                    <form method="post" action="{% url 'update_appointment_status' appt.id %}" class="inline">
                                        {% csrf_token %}
                                        <input type="hidden" name="status" value="Confirmed">
                                        <button type="submit" class="text-xs font-semibold text-green-600 hover:text-green-700 bg-green-50 hover:bg-green-100 px-3 py-1.5 rounded-lg transition-colors">Confirm</button>
                                    </form>
                                {% else %}
                                    <span class="text-xs font-semibold text-gray-400 bg-gray-50 px-3 py-1.5 rounded-lg border border-gray-100">{{ appt.status }}</span>
                                {% endif %}
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="4" class="px-6 py-8 text-center text-gray-400">No appointments remaining today.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Upcoming Appointments -->
    <div class="space-y-3">
        <div class="flex items-center justify-between">
            <h3 class="font-bold text-gray-900 text-sm uppercase tracking-wide">Upcoming Appointments</h3>
        </div>
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-gray-50 border-b border-gray-100 text-xs uppercase tracking-wider text-gray-500 font-semibold">
                            <th class="px-6 py-4">Patient</th>
                            <th class="px-6 py-4">Date & Time</th>
                            <th class="px-6 py-4 text-right">Action</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100 text-sm">
                        {% for appt in upcoming_appointments %}
                        <tr class="hover:bg-gray-50 transition-colors">
                            <td class="px-6 py-4">
                                <p class="font-semibold text-gray-900">{{ appt.patient.user.get_full_name|default:appt.patient.user.username }}</p>
                            </td>
                            <td class="px-6 py-4">
                                <p class="font-medium text-gray-900">{{ appt.appointment_date|date:"M j, Y" }}</p>
                                <p class="text-xs text-gray-500">{{ appt.start_time|time:"g:i A" }}</p>
                            </td>
                            <td class="px-6 py-4 text-right space-x-2">
                                {% if appt.status == 'Pending' %}
                                    <form method="post" action="{% url 'update_appointment_status' appt.id %}" class="inline">
                                        {% csrf_token %}
                                        <input type="hidden" name="status" value="Confirmed">
                                        <button type="submit" class="text-xs font-semibold text-green-600 hover:text-green-700 bg-green-50 hover:bg-green-100 px-3 py-1.5 rounded-lg transition-colors">Confirm</button>
                                    </form>
                                {% else %}
                                    <span class="text-xs font-semibold text-gray-400 bg-gray-50 px-3 py-1.5 rounded-lg border border-gray-100">{{ appt.status }}</span>
                                {% endif %}
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="3" class="px-6 py-8 text-center text-gray-400">No upcoming appointments.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>'''

doc_content = re.sub(doc_list_html, doc_table_html, doc_content, flags=re.DOTALL)
with open(doc_filepath, 'w', encoding='utf-8') as f:
    f.write(doc_content)

print('Updated Dashboards')
