import sqlite3



conn = sqlite3.connect("../../digital-humans.db", check_same_thread=True)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def clear():
    cursor.execute("DROP TABLE IF EXISTS characters")
    cursor.execute("DROP TABLE IF EXISTS sessions")
    conn.commit()

def initialize():
    """Creates initial character and session database"""
    #create characters table
    cursor.execute("CREATE TABLE IF NOT EXISTS characters (characterID INTEGER PRIMARY KEY, characterName TEXT NOT NULL, characterDescription TEXT NOT NULL, parameterValues TEXT)")
    # create sessions table
    cursor.execute("CREATE TABLE IF NOT EXISTS sessions (sessionID INTEGER PRIMARY KEY, sessionName TEXT NOT NULL, sessionDescription TEXT NOT NULL, characterIDList TEXT NOT NULL, history TEXT)")
    conn.commit()

# not-used
def get_table(tableName):
    rows = cursor.execute(f"SELECT * FROM {tableName}").fetchall()
    return rows

# --------------------------------------------------------
# CHARACTER OPERATIONS
# --------------------------------------------------------

def fetch_character_schema(characterID):
    characterRows = cursor.execute(f"SELECT * FROM characters WHERE characterID = {characterID}").fetchall()
    characterSchema = [dict(r) for r in characterRows][0]
    # print("characterSchema", characterSchema)
    return characterSchema

def save_character_schema(characterSchema):
    # characterSchema in the form: {characterID: ..., characterName: ..., characterDescription: ..., parameterValues: ...}
    characterName = characterSchema["characterName"]
    characterDescription = characterSchema["characterDescription"]
    cursor.execute(f"INSERT INTO characters (characterName, characterDescription) VALUES (?, ?)", [characterName, characterDescription])
    conn.commit()

# --------------------------------------------------------
# SESSION OPERATIONS
# --------------------------------------------------------

def fetch_session_data(sessionID):
    sessionRows = cursor.execute(f"SELECT * FROM sessions WHERE sessionID = {sessionID}").fetchall()
    sessionData = [dict(r) for r in sessionRows][0]
    # print("sessionData", sessionData)
    return sessionData

def save_session_data(sessionData):
    # sessionData in the form: {sessionID: ..., sessionName: ..., sessionDescription: ...}
        sessionName = sessionData["sessionName"]
        sessionDescription = sessionData["sessionDescription"]
        characterIDList = sessionData["characterIDList"]
        initialHistory = sessionData["initialHistory"]

        cursor.execute(f"INSERT INTO sessions (sessionName, sessionDescription, characterIDList, history) VALUES (?, ?, ?, ?)", [sessionName, sessionDescription, characterIDList, initialHistory])
        conn.commit()

def update_session_data(sessionID, newHistory):
    print(newHistory)
    cursor.execute(f"UPDATE sessions SET history = ? WHERE sessionID = ?", (newHistory, sessionID))
    conn.commit()