template = """Table "{{ table_alias }}" has following schema:
{% for col in schema %}
{{ col[0] }}: {{ col[1] }}
{% endfor %}
Write a SQL query from the question:
{{ question }}"""
   