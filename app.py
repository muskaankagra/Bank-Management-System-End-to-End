from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
con = pymysql.connect(
    host="localhost",
    user="root",
    cursorclass=pymysql.cursors.DictCursor,
    database="bank_management"
)
cursor = con.cursor()

# Ensure the users table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    account_no INT NOT NULL UNIQUE,
    contact_details VARCHAR(255),
    email_address VARCHAR(255)
)
""")
con.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        account_no = request.form['account_no']
        contact = request.form['contact']
        email = request.form['email']

        try:
            cursor.execute("""
            INSERT INTO users (username, name, account_no, contact_details, email_address)
            VALUES (%s, %s, %s, %s, %s)
            """, (username, name, account_no, contact, email))
            con.commit()
            flash("User registered successfully!", "success")
            return redirect(url_for('index'))
        except pymysql.err.IntegrityError:
            flash("Account number already exists!", "danger")
    return render_template('new_user.html')

@app.route('/existing_user', methods=['GET', 'POST'])
def existing_user():
    if request.method == 'POST':
        account_no = request.form['account_no']
        cursor.execute("SELECT * FROM users WHERE account_no = %s", (account_no,))
        user = cursor.fetchone()
        if user:
            return redirect(url_for('dashboard', account_no=account_no))
        else:
            flash("Account not found!", "danger")
    return render_template('existing_user.html')

@app.route('/dashboard/<account_no>')
def dashboard(account_no):
    cursor.execute("SELECT * FROM users WHERE account_no = %s", (account_no,))
    user = cursor.fetchone()
    if user:
        return render_template('dashboard.html', user=user)
    else:
        flash("User not found!", "danger")
        return redirect(url_for('index'))

@app.route('/update_balance/<account_no>', methods=['POST'])
def update_balance(account_no):
    # Placeholder for updating balance
    flash("Balance updated successfully!", "success")
    return redirect(url_for('dashboard', account_no=account_no))

@app.route('/debit/<account_no>', methods=['POST'])
def debit(account_no):
    # Placeholder for debiting amount
    flash("Amount debited successfully!", "success")
    return redirect(url_for('dashboard', account_no=account_no))

@app.route('/credit/<account_no>', methods=['POST'])
def credit(account_no):
    # Placeholder for crediting amount
    flash("Amount credited successfully!", "success")
    return redirect(url_for('dashboard', account_no=account_no))

if __name__ == '__main__':
    app.run(debug=True)




#####################################################################
###################################################################

