template = """Table "{{ table_alias }}" has following schema:
{% for col in schema %}
{{ col[0] }}: {{ col[1] }}
{% endfor %}


Write a SQL query to answer the question:
{{ question }}
{% if column_to_query != None %}
Select the following columns: {{ select }}
{% endif %}
"""
