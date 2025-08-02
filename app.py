from flask import Flask, render_template, request
from waitress import serve
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
@app.route('/search', methods=['POST'] )
def search():

    #print('args ' + request.args.get('document_type', ''))
    #print('args ' + request.form['document_type'])

    if request.form['document_type'] == "":
    #if request.args.get('document_type', '') == "":
       document_type_input = None
    else:
       document_type_input = request.form['document_type']
       #document_type_input = request.args.get('document_type', '')

    if request.form['year'] == "": 
    #if request.args.get('year', '') == "":
       year_input = None
    else:
       year_input = request.form['year']
       #year_input = request.args.get('year', '')

    if request.form['search_term'] == "":
    #if request.args.get('search_term', '') == "":
       search_term_input = None
    else:
       #search_term_input = request.args.get('search_term', '')
       search_term_input = request.form['search_term']

    # Get page and per_page from query string
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # Calculate the offset
    offset = (page - 1) * per_page

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=False)

        cursor.callproc('GET_HISTORY_DOCUMENT', (year_input, document_type_input, search_term_input, per_page, offset))


        results = []
        for result in cursor.stored_results():
           results.append(result.fetchall())
           #results = result.fetchall()


           for row in results:
              print(row)


        cursor.close()
        conn.close()

        return render_template('results.html', results=results, page=page, per_page=per_page, document_type=document_type_input, 
                              year=year_input,search_term=search_term_input )

        
    else:
        return "Error connecting to the database."
    

@app.route('/paginate', methods=['GET'] )
def paginate():

    print('args ' + request.args.get('document_type', ''))
    #print('args ' + request.form['document_type'])

    #if request.form['document_type'] == "":
    if request.args.get('document_type', '') == "":
       document_type_input = None
    else:
       #document_type_input = request.form['document_type']
       document_type_input = request.args.get('document_type', '')

    #if request.form['year'] == "": 
    if request.args.get('year', '') == "":
       year_input = None
    else:
       #year_input = request.form['year']
       year_input = request.args.get('year', '')

    #if request.form['search_term'] == "":
    if request.args.get('search_term', '') == "":
       search_term_input = None
    else:
       search_term_input = request.args.get('search_term', '')
       #search_term_input = request.form['search_term']

    # Get page and per_page from query string
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # Calculate the offset
    offset = (page - 1) * per_page

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=False)

        cursor.callproc('GET_HISTORY_DOCUMENT', (year_input, document_type_input, search_term_input, per_page, offset))

        results = []
        for result in cursor.stored_results():
           results.append(result.fetchall())


        cursor.close()
        conn.close()

        return render_template('results.html', results=results, page=page, per_page=per_page, document_type=document_type_input, 
                              year=year_input,search_term=search_term_input )

        
    else:
        return "Error connecting to the database."
    

if __name__ == '__main__':
        serve(app, host='0.0.0.0', port=8080)
