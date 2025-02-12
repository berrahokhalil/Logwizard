import google.generativeai as genai
from django.conf import settings
from django.db.models import Count, Min, Max

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
def preprocess(filtered_logs, max_errors):
    total_errors_count = filtered_logs.count()

    # 2. Time Range of the Errors
    time_range = filtered_logs.aggregate(
        start_time=Min('time'),
        end_time=Max('time')
    )

    # 3. Top 5 Error Names and Codes
    top_5_errors = filtered_logs.values('code', 'name').annotate(count=Count('code')).order_by('-count')[:5]
    top_5_error_codes = [entry['code'] for entry in top_5_errors]
    top_5_error_counts = [entry['count'] for entry in top_5_errors]

    # 4. Urgent Errors Count and Code
    urgent_errors = filtered_logs.filter(priority='urgent')
    urgent_errors_count = urgent_errors.count()

    urgent_errors_codes = urgent_errors.values('code').annotate(count=Count('code')).order_by('code')
    urgent_codes = [entry['code'] for entry in urgent_errors_codes]
    urgent_counts = [entry['count'] for entry in urgent_errors_codes]
    summary = f"""
    Total Errors: {total_errors_count}
    Time Range: from {time_range['start_time'].strftime('%Y-%m-%d %H:%M:%S')} to {time_range['end_time'].strftime('%Y-%m-%d %H:%M:%S')}
    Top 5 error codes: {', '.join(str(code) for code in top_5_error_codes)}
    Top 5 error codes count: {', '.join(str(count) for count in top_5_error_counts)} respectively
    Urgent Errors: {urgent_errors_count}
    Urgent Errors Codes : {', '.join(str(code) for code in urgent_codes)}
    Urgent Errors Count : {', '.join(str(count) for count in urgent_counts)} respectively
    """
    return summary


def summarize_errors(filtered_logs, max_errors=1000):
    
    summary = preprocess(filtered_logs, max_errors)
    prompt = f"""
    Analyze the following error data from our server logs and provide a summary in simple, understandable terms for a casual user:
    {summary}
    
    Please include:
    1. Overall assessment of system health based on these errors
    2. Most common error types and their potential impacts
    3. Any critical issues that need immediate attention
    4. General trends or patterns in the errors
    5. Basic recommendations for addressing the top issues
    
    i want a chatty response thats limited to 15 sentences and that is very friendly so you can use phrases like hey there, i have something to tell you etc..
    """
    response = model.generate_content(prompt)
    return response.text

