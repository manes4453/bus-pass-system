from flask import Flask, render_template_string, request
import sqlite3

app = Flask(__name__)

# Database Create
conn = sqlite3.connect('database.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS buspass(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
college TEXT,
route TEXT,
mobile TEXT
)
''')

conn.close()

PAGE = """

<!DOCTYPE html>
<html>

<head>

<title>Cloud Bus Pass System</title>

<style>

body{
    font-family:Arial;
    background:#f0f2f5;
}

.box{
    width:400px;
    background:white;
    margin:50px auto;
    padding:40px;
    border-radius:10px;
    box-shadow:0px 0px 10px gray;
}

h1{
    text-align:center;
    color:darkblue;
}

input{
    width:95%;
    padding:10px;
    margin:10px 0;
    border-radius:5px;
    border:1px solid gray;
}

button{
    width:100%;
    background:blue;
    color:white;
    padding:10px;
    border:none;
    border-radius:5px;
}

h2{
    color:green;
    text-align:center;
}

table{
    width:100%;
    margin-top:20px;
    border-collapse:collapse;
}

table, th, td{
    border:1px solid gray;
}

th, td{
    padding:10px;
    text-align:center;
}

</style>

</head>

<body>

<div class="box">

<h1>Bus Pass Application</h1>

<form method="POST">

<input type="text" name="name" placeholder="Enter Name" required>

<input type="text" name="college" placeholder="Enter College Name" required>

<input type="text" name="route" placeholder="Enter Bus Route" required>

<input type="text" name="mobile" placeholder="Enter Mobile Number" required>

<button type="submit">Apply Bus Pass</button>

</form>

<h2>{{ message }}</h2>

<h1>Admin Panel</h1>

<table>

<tr>
<th>ID</th>
<th>Name</th>
<th>College</th>
<th>Route</th>
<th>Mobile</th>
</tr>

{% for row in data %}

<tr>
<td>{{ row[0] }}</td>
<td>{{ row[1] }}</td>
<td>{{ row[2] }}</td>
<td>{{ row[3] }}</td>
<td>{{ row[4] }}</td>
</tr>

{% endfor %}

</table>

</div>

</body>
</html>

"""

@app.route('/', methods=['GET', 'POST'])

def home():

    message = ""

    if request.method == 'POST':

        name = request.form['name']
        college = request.form['college']
        route = request.form['route']
        mobile = request.form['mobile']

        conn = sqlite3.connect('database.db')

        conn.execute(
            "INSERT INTO buspass(name, college, route, mobile) VALUES(?,?,?,?)",
            (name, college, route, mobile)
        )

        conn.commit()
        conn.close()

        message = "Bus Pass Applied Successfully"

    conn = sqlite3.connect('database.db')

    cursor = conn.execute("SELECT * FROM buspass")

    data = cursor.fetchall()

    conn.close()

    return render_template_string(PAGE, message=message, data=data)

if __name__ == '__main__':
    app.run(debug=True)