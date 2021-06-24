from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
con = sqlite3.connect("midlocA_X_midA.db", check_same_thread=False)

@app.route("/poi", methods=["GET"])
def get_poi():
    year = int(request.args["year"])
    month = int(request.args["month"])
    day = int(request.args["day"])

    data = exec("SELECT * FROM midloca_x_mida mxm WHERE ({}, {}, {}) BETWEEN (styear, stmon, stday) AND (endyear, endmon, endday) ORDER BY styear ASC, stmon ASC, stday ASC".format(year, month, day))

    partic = {}
    nar = {}
    cinc_data = {}
    disputes = 0
    nations = 0
    casualties = 0

    if len(data) > 0:
      ids = ",".join([x["dispnum"] for x in data])
      partic_pre = exec("SELECT * FROM midb m LEFT JOIN ccs_iso_bridge WHERE m.ccode = ccs_iso_bridge.ccode_cow AND dispnum3 IN ({})".format(ids))

      ccs = set()

      for e in partic_pre:
        ccs.add(e["ccode"])
        dn = e["dispnum3"]
        if(dn not in partic):
          partic[dn] = []
        partic[dn].append(e)

      ccs_ids = ",".join(ccs)
      cinc_pre = exec("SELECT * FROM nmc WHERE year = {} AND ccode IN ({})".format(year, ccs_ids))
      for e in cinc_pre:
        cinc_data[e["ccode"]] = e

      nardata = exec("SELECT * FROM Narrative WHERE DispNum3 IN ({})".format(ids))

      for e in nardata:
        nar[e["DispNum3"]] = e["Story"]

      disputes = len(data)
      casualties = calcCasualties(partic_pre)
      nations = calcNations(partic_pre)
      

    return jsonify({
      "data": data,
      "partic": partic,
      "cinc_data": cinc_data,
      "nar": nar,
      "extra": {"disputes": disputes, "nations": nations, "casualties": casualties}
    })

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

mapping = [0, 25, 87, 200, 375, 750, 1000]

def calcCasualties(data):
  fatalities_area = []
  fatalities = 0
  for e in data:
    if int(e["fatalpre"]) != -9:
      fatalities = fatalities + int(e["fatalpre"])
    if int(e["fatality"]) > 0:
      fatalities_area.append(int(e["fatality"]))

  for f in fatalities_area:
    fatalities = fatalities + mapping[f]
  
  return 0 if fatalities == 0 else "> {}".format(fatalities)
  
def calcNations(data):
  x = set()
  for e in data:
    x.add(e["ccode"])
  return len(x)