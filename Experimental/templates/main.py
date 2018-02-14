from flask import Flask, render_template, request, session

app = Flask(__name__)


def log_request(req, res):
    """Log details of the web request and the results"""
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log
                  (phrase, letters, ip, browser_string, results)
                  values
                  (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res, ))


def analyzeSite(siteurl='https://github.com/', name='John'):
    """Return a set of the 'letters' found in 'phrase'."""
    # return set(letters).intersection(set(phrase))


@app.route('/analyze', methods=['POST'])
def do_search():
    siteurl = request.form['siteurl']
    username = request.form['username']
    title = 'Here are your results:'
    results = str(analyzeSite(siteurl, username))
    try:
        log_request(request, results)
    except Exception as err:
        print('***** Logging failed with this error:', str(err))
    return render_template('results.html',
                           the_siteurl=siteurl,
                           the_username=username,
                           # the_title=title,
                           the_results=results,)


@app.route('/')
@app.route('/entry')
def entry_page():
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')
