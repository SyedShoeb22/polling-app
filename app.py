# polling_app/app.py

import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash, g, session
from datetime import datetime # Make sure this is imported

app = Flask(__name__)
app.secret_key = 'Pass@12345' 

DATABASE = os.path.join(app.root_path, 'polling_app.db') 

# --- Database Helper Functions ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES  # Add this line
        )
        db.row_factory = sqlite3.Row # Access columns by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database using schema.sql."""
    if os.path.exists(DATABASE):
        print("Database already exists. Skipping initialization.")
        # Optionally, you could add logic here to backup or warn
        # Or, if you want to always re-initialize for development:
        # os.remove(DATABASE)
        # print("Removed existing database.")
    
    # Only initialize if DB doesn't exist, or if you explicitly want to re-init
    # For this example, let's proceed to ensure tables are there if schema.sql updated
    try:
        with app.app_context():
            db = get_db()
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
        print("Initialized the database.")
    except sqlite3.OperationalError as e:
        print(f"Error initializing database: {e}")
        print("Perhaps tables already exist or schema.sql has issues.")


# --- Flask CLI command to initialize DB ---
import click
@app.cli.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    # Ensure any existing DB file is removed to start fresh with this command
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        click.echo('Removed existing database.')
    init_db() # Call the regular init_db function
    click.echo('Initialized the database with fresh tables.')


# --- Routes ---
@app.route('/')
def index():
    db = get_db()
    try:
        cursor = db.execute('SELECT id, question, created_at FROM polls ORDER BY created_at DESC')
        polls_data = cursor.fetchall()
    except sqlite3.OperationalError: # Table might not exist yet
        polls_data = []
        flash("Database not fully initialized or polls table missing. Try running 'flask init-db'.", "error")
    return render_template('index.html', polls=polls_data)

@app.route('/create', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'POST':
        question = request.form.get('question')
        poll_type = request.form.get('poll_type') # 'dropdown' or 'yesno'

        # --- CHANGE IS HERE ---
        # Use getlist() to get all inputs named 'options' as a list.
        # Also, filter out any empty strings if a user adds an option but leaves it blank.
        options = [opt.strip() for opt in request.form.getlist('options') if opt.strip()]
        
        # --- The rest of the validation now works correctly ---
        if not question or not options:
            flash('Question and at least one option are required!', 'error')
            return redirect(url_for('create_poll'))

        # Validation for other types
        elif len(options) < 2:
            flash('Please provide at least two options.', 'error')
            return redirect(url_for('create_poll'))

        db = get_db()
        try:
            cursor = db.execute(
                'INSERT INTO polls (question, poll_type) VALUES (?, ?)',
                (question, poll_type)
            )
            poll_id = cursor.lastrowid

            # This loop now works perfectly because `options` is a correct list.
            for option_text in options:
                db.execute(
                    'INSERT INTO options (poll_id, option_text, votes) VALUES (?, ?, 0)',
                    (poll_id, option_text)
                )

            db.commit()
            flash(f'Poll "{question}" created successfully!', 'success')
            return redirect(url_for('index')) # Assuming you have an 'index' route
        except sqlite3.Error as e:
            db.rollback()
            flash(f'Database error: {e}', 'error')
            return redirect(url_for('create_poll'))

    return render_template('create_poll.html')
@app.route('/poll/<int:poll_id>', methods=['GET', 'POST'])
def poll_detail(poll_id):
    db = get_db()
    poll_data = db.execute('SELECT id, question,poll_type FROM polls WHERE id = ?', (poll_id,)).fetchone()

    if not poll_data:
        flash('Poll not found!', 'error')
        return redirect(url_for('index'))

    options_data = db.execute('SELECT id, option_text FROM options WHERE poll_id = ? ORDER BY id',
                              (poll_id,)).fetchall()

    if request.method == 'POST':
        selected_option_id_str = request.form.get('option')
        if not selected_option_id_str:
            flash('Please select an option to vote.', 'error')
            return render_template('poll_detail.html', poll_id=poll_id, poll=poll_data, options_list=options_data)
        
        try:
            selected_option_id = int(selected_option_id_str)
            # Verify the option belongs to this poll
            option_check = db.execute('SELECT id FROM options WHERE id = ? AND poll_id = ?', 
                                      (selected_option_id, poll_id)).fetchone()
            if not option_check:
                flash('Invalid option selected for this poll.', 'error')
            else:
                db.execute('UPDATE options SET votes = votes + 1 WHERE id = ?', (selected_option_id,))
                db.commit()
                flash('Your vote has been recorded!', 'success')
                return redirect(url_for('results', poll_id=poll_id))
        except ValueError:
            flash('Invalid option ID.', 'error')
        except sqlite3.Error as e:
            db.rollback()
            flash(f'Database error during voting: {e}', 'error')
        # If vote fails or is invalid, show the poll page again
        return render_template('poll_detail.html', poll_id=poll_id, poll=poll_data, options_list=options_data)

    return render_template('poll_detail.html', poll_id=poll_id, poll=poll_data, options_list=options_data)


@app.route('/results/<int:poll_id>')
def results(poll_id):
    db = get_db()
    poll_data = db.execute('SELECT id, question FROM polls WHERE id = ?', (poll_id,)).fetchone()

    if not poll_data:
        flash('Poll not found!', 'error')
        return redirect(url_for('index'))

    options_from_db = db.execute(
        'SELECT option_text, votes FROM options WHERE poll_id = ? ORDER BY id', # or votes DESC
        (poll_id,)
    ).fetchall()

    if not options_from_db: # Should not happen if poll exists, but good check
        flash('No options found for this poll.', 'info')
        return render_template('results.html', poll_id=poll_id, poll=poll_data, results_data=[], total_votes=0)

    total_votes = sum(opt['votes'] for opt in options_from_db)
    
    results_display_data = []
    for opt in options_from_db:
        percentage = (opt['votes'] / total_votes * 100) if total_votes > 0 else 0
        results_display_data.append({
            'text': opt['option_text'],
            'votes': opt['votes'],
            'percentage': round(percentage, 2)
        })

    return render_template('results.html', poll_id=poll_id, poll=poll_data, results_data=results_display_data, total_votes=total_votes)



# --- NEW DASHBOARD ROUTE ---
@app.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        # Only show dashboard.html with passcode prompt if not logged in
        return render_template('dashboard.html', require_passcode=True)
    
    # All your existing logic here
    db = get_db()
    polls = db.execute('SELECT id, question FROM polls ORDER BY created_at DESC').fetchall()
    options = db.execute('SELECT poll_id, option_text, votes FROM options').fetchall()

    polls_with_results = {}
    for poll in polls:
        polls_with_results[poll['id']] = {
            'id': poll['id'],
            'question': poll['question'],
            'total_votes': 0,
            'options': []
        }

    for option in options:
        poll_id = option['poll_id']
        if poll_id in polls_with_results:
            polls_with_results[poll_id]['options'].append({
                'text': option['option_text'],
                'votes': option['votes']
            })
            polls_with_results[poll_id]['total_votes'] += option['votes']

    for poll_id, poll_data in polls_with_results.items():
        total_votes = poll_data['total_votes']
        for option in poll_data['options']:
            percentage = (option['votes'] / total_votes * 100) if total_votes > 0 else 0
            option['percentage'] = round(percentage, 2)

    return render_template('dashboard.html', polls_data=list(polls_with_results.values()), require_passcode=False)
@app.route('/check-passcode', methods=['POST'])
def check_passcode():
    data = request.get_json()
    if data.get('passcode') == '1234':
        session['admin_logged_in'] = True
        return {'success': True}
    return {'success': False}


# --- NEW DELETE ROUTE ---
@app.route('/poll/<int:poll_id>/delete', methods=['POST'])
def delete_poll(poll_id):
    """Deletes a poll and its associated options."""
    db = get_db()
    try:
        # Thanks to "ON DELETE CASCADE", we only need to delete the poll.
        # The database will automatically delete its options.
        poll = db.execute('SELECT question FROM polls WHERE id = ?', (poll_id,)).fetchone()
        if poll:
            db.execute('DELETE FROM polls WHERE id = ?', (poll_id,))
            db.commit()
            flash(f'Poll "{poll["question"]}" was successfully deleted.', 'success')
        else:
            flash('Poll not found or already deleted.', 'error')
    except sqlite3.Error as e:
        db.rollback()
        flash(f'Database error occurred: {e}', 'error')
        
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    # Check if DB exists, if not, initialize it.
    # This is a simple check for first run. For robust deployment, `flask init-db` is better.
    if not os.path.exists(DATABASE):
        print("Database not found. Attempting to initialize...")
        init_db() # Call init_db to create schema if db file doesn't exist
    app.run(debug=True)