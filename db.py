import sqlite3

# Function to initialize the SQLite database
def init_db():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            location TEXT PRIMARY KEY,
            history TEXT,
            year TEXT,
            details TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert data into the SQLite database
def insert_into_db(location, data):
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    
    # Extract data from JSON
    history = data.get('history', '')
    imp_events = data.get('impEvents', [])
    
    for event in imp_events:
        year = event.get('Year', '')
        details = event.get('Details', '')
        c.execute('INSERT OR REPLACE INTO history (location, history, year, details) VALUES (?, ?, ?, ?)', (location, history, year, details))
    
    conn.commit()
    conn.close()

# Example usage:
if __name__ == "__main__":
    init_db()
    location = "New York City"
    data = {
        "history": "A brief history of New York City.",
        "impEvents": [
            {"Year": "1624", "Details": "Dutch settlers establish New Amsterdam."},
            {"Year": "1898", "Details": "Consolidation of the five boroughs into New York City."},
        ]
    }
    insert_into_db(location, data)
