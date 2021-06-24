import sqlite3

con = sqlite3.connect("midlocA_X_midA.db", check_same_thread=False)

def exec(query):
    cursor = con.cursor()
    cursor.execute(query)
    rows = [x for x in cursor]
    cols = [x[0] for x in cursor.description]
    data = []
    for row in rows:
      rec = {}
      for prop, val in zip(cols, row):
        rec[prop] = val
      data.append(rec)
    return data

def update(query):
    cur = con.cursor()
    cur.execute(query)
    con.commit()

data = exec("SELECT * FROM ccs_iso_bridge cib LEFT JOIN ccs_translate ON LOWER(cib.name_cow) = LOWER(ccs_translate.name) WHERE cib.iso_code IS NULL AND ccs_translate.id IS NOT NULL")
for e in data:
    update("UPDATE ccs_iso_bridge SET iso_code = '{}' WHERE abr_cow = '{}';".format(e["alpha3"], e["abr_cow"]))