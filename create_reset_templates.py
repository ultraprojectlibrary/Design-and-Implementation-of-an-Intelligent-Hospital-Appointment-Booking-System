import os

tpl_dir = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\templates\accounts'
os.makedirs(tpl_dir, exist_ok=True)

# 1. form
form_html = '''{% extends 'base.html' %}
{% block title %}Reset Password - SmartCare{% endblock %}

{% block content %}
<div class="min-h-[80vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
        <div class="text-center">
            <h2 class="mt-2 text-3xl font-extrabold text-gray-900 tracking-tight">Forgot Password?</h2>
            <p class="mt-2 text-sm text-gray-500">Enter your email address below and we'll send you a link to reset your password.</p>
        </div>
        
        <form class="mt-8 space-y-6" method="POST">
            {% csrf_token %}
            <div>
                <label for="id_email" class="block text-sm font-semibold text-gray-700 mb-1.5">Email Address</label>
                <input type="email" name="email" id="id_email" required
                    class="appearance-none relative block w-full px-4 py-3 border border-gray-200 placeholder-gray-400 text-gray-900 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent sm:text-sm transition-all"
                    placeholder="Enter your email">
            </div>

            {% if form.errors %}
            <div class="bg-red-50 text-red-500 text-sm p-4 rounded-xl border border-red-100 font-medium">
                {{ form.errors }}
            </div>
            {% endif %}

            <div>
                <button type="submit" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-bold text-white bg-brand-600 hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 transition-colors">
                    Send Reset Link
                </button>
            </div>
            
            <div class="text-center mt-4">
                <a href="{% url 'login_view' %}" class="text-sm font-semibold text-brand-600 hover:text-brand-500 transition-colors">
                    Back to Login
                </a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
'''
with open(os.path.join(tpl_dir, 'password_reset_form.html'), 'w', encoding='utf-8') as f:
    f.write(form_html)

# 2. done
done_html = '''{% extends 'base.html' %}
{% block title %}Email Sent - SmartCare{% endblock %}

{% block content %}
<div class="min-h-[80vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full text-center space-y-6 bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
        <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-green-50 mb-6">
            <svg class="h-8 w-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
            </svg>
        </div>
        <h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">Check your inbox</h2>
        <p class="text-sm text-gray-500">We've emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly.</p>
        
        <div class="pt-6">
            <a href="{% url 'login_view' %}" class="w-full inline-flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-bold text-white bg-brand-600 hover:bg-brand-700 transition-colors">
                Return to Login
            </a>
        </div>
    </div>
</div>
{% endblock %}
'''
with open(os.path.join(tpl_dir, 'password_reset_done.html'), 'w', encoding='utf-8') as f:
    f.write(done_html)

# 3. confirm
confirm_html = '''{% extends 'base.html' %}
{% block title %}Set New Password - SmartCare{% endblock %}

{% block content %}
<div class="min-h-[80vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
        <div class="text-center">
            <h2 class="mt-2 text-3xl font-extrabold text-gray-900 tracking-tight">Set New Password</h2>
            <p class="mt-2 text-sm text-gray-500">Please enter your new password twice so we can verify you typed it in correctly.</p>
        </div>
        
        {% if validlink %}
        <form class="mt-8 space-y-6" method="POST">
            {% csrf_token %}
            <div class="space-y-4">
                {% for field in form %}
                <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-1.5">{{ field.label }}</label>
                    <input type="{{ field.field.widget.input_type }}" name="{{ field.name }}" required
                        class="appearance-none relative block w-full px-4 py-3 border border-gray-200 placeholder-gray-400 text-gray-900 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent sm:text-sm transition-all">
                    {% if field.errors %}
                        <p class="text-xs text-red-500 mt-1 font-medium">{{ field.errors.0 }}</p>
                    {% endif %}
                </div>
                {% endfor %}
            </div>

            <div>
                <button type="submit" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-bold text-white bg-brand-600 hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 transition-colors">
                    Change Password
                </button>
            </div>
        </form>
        {% else %}
        <div class="bg-red-50 text-red-500 text-sm p-4 rounded-xl border border-red-100 font-medium text-center">
            The password reset link was invalid, possibly because it has already been used. Please request a new password reset.
        </div>
        <div class="text-center mt-6">
            <a href="{% url 'password_reset' %}" class="text-sm font-semibold text-brand-600 hover:text-brand-500 transition-colors">
                Request New Link
            </a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
'''
with open(os.path.join(tpl_dir, 'password_reset_confirm.html'), 'w', encoding='utf-8') as f:
    f.write(confirm_html)

# 4. complete
complete_html = '''{% extends 'base.html' %}
{% block title %}Password Reset Complete - SmartCare{% endblock %}

{% block content %}
<div class="min-h-[80vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full text-center space-y-6 bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
        <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-green-50 mb-6">
            <svg class="h-8 w-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
        </div>
        <h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">Password Reset Complete</h2>
        <p class="text-sm text-gray-500">Your password has been successfully set. You may go ahead and log in now.</p>
        
        <div class="pt-6">
            <a href="{% url 'login_view' %}" class="w-full inline-flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-bold text-white bg-brand-600 hover:bg-brand-700 transition-colors">
                Log in to your account
            </a>
        </div>
    </div>
</div>
{% endblock %}
'''
with open(os.path.join(tpl_dir, 'password_reset_complete.html'), 'w', encoding='utf-8') as f:
    f.write(complete_html)

print("Created UI templates")
