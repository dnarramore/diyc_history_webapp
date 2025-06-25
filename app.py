from flask import Flask, render_template, request
import mysql.connector


app = Flask(__name__)

# Configure your MySQL connection details (replace with your credentials)
db_config = {
    'user': 'diyc_history',
    'password': 'Diyc_1315',
    'host': 'diychistory.ca3m3odsqvx4.us-east-1.rds.amazonaws.com',
    'database': 'DIYCHISTORY'
}

# Function to connect to the database
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# Route for the home page (search form)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle search requests
@app.route('/search', methods=['POST'])
def search():

    if request.form['document_type'] == "":
       document_type_input = None
    else:
       document_type_input = request.form['document_type']

    if request.form['year'] == "": 
       year_input = None
    else:
       year_input = request.form['year']

    if request.form['search_term'] == "":
       search_term_input = None
    else:
       search_term_input = request.form['search_term']

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)

        cursor.callproc('GET_HISTORY_DOCUMENT', (year_input, document_type_input, search_term_input))

        results = []
        for result in cursor.stored_results():
           #result = ' '.join([str(item) for item in result])
           results.append(result.fetchall())


        cursor.close()
        conn.close()

        return render_template('results.html', results=results)

        # SQL query to search for products (replace 'products' and column names)
        # sql_query = "SELECT file_name, URL, document_year FROM HISTORY_DOCUMENT " \
        # "WHERE document_type_code = %(document_type)s"
        # parameters_named = {"document_type": document_type_input}
        # cursor.execute(sql_query, parameters_named)
 
        # search_results = cursor.fetchall()  # Fetch all matching rows

        

        #cursor.close()
        #conn.close()

        #return render_template('results.html', results=search_results)

        
    else:
        return "Error connecting to the database."

if __name__ == '__main__':
    app.run(debug=True)