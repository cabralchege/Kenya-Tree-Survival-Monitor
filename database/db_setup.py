import sqlite3

def create_database():
    conn = sqlite3.connect('forest_impact.db')
    cursor = conn.cursor()
    
    # Plantings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS plantings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        species TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        location TEXT NOT NULL,
        date_planted DATE NOT NULL,
        season TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Survival checks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS survival_checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        planting_id INTEGER NOT NULL,
        check_date DATE NOT NULL,
        alive_count INTEGER NOT NULL,
        dead_count INTEGER,
        health_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (planting_id) REFERENCES plantings(id)
    )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("✅ Database created successfully!")