import sqlite3

# Connessione al database SQLite
conn = sqlite3.connect("giocatori_seduti_tavolo.db")
cursor = conn.cursor()

# Creazione della tabella
cursor.execute('''CREATE TABLE IF NOT EXISTS giocatori (
                    id INTEGER PRIMARY KEY,
                    nome TEXT,
                    carta1 TEXT,
                    carta2 TEXT,
                    puntata FLOAT,
                    soldi FLOAT,
                    turno BOOLEAN,
                    blind TEXT,
                    seduto BOOLEAN,
                    posto INTEGER,
                    ip TEXT,
                    port INTEGER
                )''')

# Commit delle modifiche e chiusura della connessione
conn.commit()
conn.close()
