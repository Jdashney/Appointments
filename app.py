import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
    
app = Flask(__name__)
app.config.from_pyfile('config.py')

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit() 

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
@app.route('/')
def show_entries():
    cur = g.db.execute('select id, name, aptdate, batch from apts order by id')
    apts = [dict(id=(row[0]), name=str(row[1]), aptdate=str(row[2]), batch=row[3]) for row in cur.fetchall()]
    
    '''
    returned_id = 
    returned_name = 
    returned_aptdate = 
    returned_batch = 
    '''
    
    return render_template('show_entries.html', apts=apts)        
      

    
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    decoded_name = str(request.form['name'])
    decoded_aptdate = str(request.form['aptdate'])
    
    g.db.execute('insert into apts (name, aptdate, batch) values (?, ?, ?)',
                 [request.form['name'], request.form['aptdate'], request.form['batch']])
    g.db.commit()
    flash('New entry was successfully posted '+ decoded_name + ' ' + decoded_aptdate)
    return redirect(url_for('show_entries'))        

@app.route('/search')
def show_apts():
    return render_template('search.html')    
    
@app.route('/show', methods=['POST'])
def show_entry():
    searched_name = str(request.form['name'])
    searched_batch = str(request.form['batch'])
    
    cur = g.db.execute('select id, name, aptdate, batch from apts where name in (?) and batch in (?)', (searched_name, searched_batch))
    
    found = [dict(id=(row[0]), name=str(row[1]), aptdate=str(row[2]), batch=row[3]) for row in cur.fetchall()]
    
    
    """
    display_found = []
    
    for i in found:
        if request.form['name'] or request.form['aptdate'] or request.form['batch'] in found:
            display_found.append(i)
    """
    return render_template('search.html', apts=found) #display_found
    
    
    decoded_name = str(request.form['name'])
    decoded_aptdate = str(request.form['aptdate'])
    
    g.db.execute('insert into apts (name, aptdate, batch) values (?, ?, ?)',
                 [request.form['name'], request.form['aptdate'], request.form['batch']])
    g.db.commit()
    flash('New entry was successfully posted '+ decoded_name + ' ' + decoded_aptdate)
    return redirect(url_for('show_entries'))     

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


def create_appointment():   
    pass

def delete_appointment():
    pass

def edit_appointment():
    pass

    
if __name__ == '__main__':
    app.run()
 