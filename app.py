from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
import sqlite3
import hashlib
from datetime import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'job-tracker-secret-key-2026'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def get_db():
    conn = sqlite3.connect('job_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Lütfen önce giriş yapın', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTH ROUTES ====================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hash_password(request.form['password'])
        
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                        (username, email, password))
            conn.commit()
            flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Bu kullanıcı adı veya email zaten kullanılıyor.', 'error')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?',
                           (email, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Giriş başarılı!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email veya şifre hatalı!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Çıkış yapıldı.', 'success')
    return redirect(url_for('login'))

# ==================== DASHBOARD ====================
@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    
    # Toplam başvuru sayısı
    total = conn.execute('SELECT COUNT(*) as count FROM applications WHERE user_id = ?',
                        (session['user_id'],)).fetchone()['count']
    
    # Durumlara göre dağılım
    status_counts = conn.execute('''
        SELECT status, COUNT(*) as count FROM applications 
        WHERE user_id = ? GROUP BY status''', (session['user_id'],)).fetchall()
    
    # Başarı oranı (offer + accepted) / total * 100
    success_count = conn.execute('''
        SELECT COUNT(*) as count FROM applications 
        WHERE user_id = ? AND status IN ('offer', 'accepted')''',
        (session['user_id'],)).fetchone()['count']
    
    success_rate = (success_count / total * 100) if total > 0 else 0
    
    # Son 5 başvuru
    recent = conn.execute('''
        SELECT * FROM applications WHERE user_id = ? 
        ORDER BY applied_date DESC LIMIT 5''', (session['user_id'],)).fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         total=total, 
                         status_counts=status_counts,
                         success_rate=round(success_rate, 1),
                         recent=recent)

# ==================== CRUD ROUTES ====================
@app.route('/applications')
@login_required
def applications():
    status_filter = request.args.get('status', '')
    conn = get_db()
    
    if status_filter:
        apps = conn.execute('''
            SELECT * FROM applications WHERE user_id = ? AND status = ? 
            ORDER BY applied_date DESC''', (session['user_id'], status_filter)).fetchall()
    else:
        apps = conn.execute('SELECT * FROM applications WHERE user_id = ? ORDER BY applied_date DESC',
                           (session['user_id'],)).fetchall()
    conn.close()
    return render_template('applications.html', applications=apps, current_filter=status_filter)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_application():
    if request.method == 'POST':
        company = request.form['company']
        position = request.form['position']
        status = request.form['status']
        salary_range = request.form.get('salary_range', '')
        applied_date = request.form['applied_date']
        next_action_date = request.form.get('next_action_date', '')
        notes = request.form.get('notes', '')
        
        conn = get_db()
        conn.execute('''
            INSERT INTO applications (user_id, company, position, status, salary_range, applied_date, next_action_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (session['user_id'], company, position, status, salary_range, applied_date, next_action_date or None, notes))
        conn.commit()
        conn.close()
        
        flash('Başvuru başarıyla eklendi!', 'success')
        return redirect(url_for('applications'))
    
    return render_template('add_application.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_application(id):
    conn = get_db()
    app_item = conn.execute('SELECT * FROM applications WHERE id = ? AND user_id = ?',
                           (id, session['user_id'])).fetchone()
    
    if not app_item:
        flash('Başvuru bulunamadı!', 'error')
        return redirect(url_for('applications'))
    
    if request.method == 'POST':
        company = request.form['company']
        position = request.form['position']
        status = request.form['status']
        salary_range = request.form.get('salary_range', '')
        applied_date = request.form['applied_date']
        next_action_date = request.form.get('next_action_date', '')
        notes = request.form.get('notes', '')
        
        conn.execute('''
            UPDATE applications SET company=?, position=?, status=?, salary_range=?, 
            applied_date=?, next_action_date=?, notes=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=? AND user_id=?''',
            (company, position, status, salary_range, applied_date, next_action_date or None, notes, id, session['user_id']))
        conn.commit()
        conn.close()
        
        flash('Başvuru güncellendi!', 'success')
        return redirect(url_for('applications'))
    
    conn.close()
    return render_template('edit_application.html', app=app_item)

@app.route('/delete/<int:id>')
@login_required
def delete_application(id):
    conn = get_db()
    conn.execute('DELETE FROM applications WHERE id = ? AND user_id = ?', (id, session['user_id']))
    conn.commit()
    conn.close()
    flash('Başvuru silindi!', 'success')
    return redirect(url_for('applications'))

# ==================== BUSINESS LOGIC FUNCTIONS (for testing) ====================
def calculate_success_rate(applications):
    """applications: list of dict with 'status' key"""
    if not applications:
        return 0
    total = len(applications)
    success = sum(1 for app in applications if app.get('status') in ['offer', 'accepted'])
    return round((success / total) * 100, 1)

def get_applications_by_status(applications, status):
    return [app for app in applications if app.get('status') == status]

def get_upcoming_actions(applications, days=7):
    from datetime import datetime, timedelta
    today = datetime.now().date()
    limit = today + timedelta(days=days)
    return [app for app in applications if app.get('next_action_date') and 
            datetime.strptime(app['next_action_date'], '%Y-%m-%d').date() <= limit]

if __name__ == '__main__':
    with open('database.sql', 'r', encoding='utf-8') as f:
        conn = get_db()
        conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Veritabanı başarıyla oluşturuldu!")
    app.run(debug=True)