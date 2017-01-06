from app import app
from . import wiki
from flask import render_template, request
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/query')
def manage_query():
    query = request.args.get('search')
    query_page = wiki.WikiPage(query)
    summary = query_page.content_summary
    return render_template("query.html", page_link=query_page.url, paragraphs=summary.items())


@app.route('/search/', methods=['POST', 'GET'])
def search_query():
    query = request.form['phrase']
    if query:
        search_data = wiki.get_search_data(query)
        return search_data
    else:
        return ""