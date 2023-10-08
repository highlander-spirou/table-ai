template = """Table "{{ table_alias }}" has following schema:
{% for col in schema %}
{{ col[0] }}: {{ col[1] }}
{% endfor %}
Write a SQL query query "{{ table_alias }}" to answer the question:
{{ question }}"""
   