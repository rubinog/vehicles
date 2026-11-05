import os, sqlite3
from flask import Flask, jsonify, request, send_from_directory

DB = os.environ.get("DB_PATH", "/data/vehicles.db")
app = Flask(__name__, static_folder="static")
T = {
    "vehicles": ["name", "plate", "notes"],
    "deadlines": ["vehicle_id", "type", "due_date", "repeat_months", "notes"],
    "records": ["vehicle_id", "date", "type", "description", "cost", "km"],
}

def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

os.makedirs(os.path.dirname(DB), exist_ok=True)
with db() as c:
    for t, cols in T.items():
        c.execute(f"create table if not exists {t}(id integer primary key autoincrement,{','.join(cols)})")

@app.get("/")
def index():
    return send_from_directory("static", "index.html")

@app.get("/api/<t>")
def lst(t):
    if t not in T: return "", 404
    return jsonify([dict(r) for r in db().execute(f"select * from {t}")])

@app.post("/api/<t>")
def add(t):
    if t not in T: return "", 404
    b = request.json or {}
    ks = [k for k in T[t] if k in b]
    with db() as c:
        cur = c.execute(f"insert into {t}({','.join(ks)}) values({','.join('?'*len(ks))})", [b[k] for k in ks])
        return jsonify(id=cur.lastrowid)

@app.put("/api/<t>/<int:i>")
def upd(t, i):
    if t not in T: return "", 404
    b = request.json or {}
    ks = [k for k in T[t] if k in b]
    with db() as c:
        c.execute(f"update {t} set {','.join(k+'=?' for k in ks)} where id=?", [b[k] for k in ks] + [i])
    return jsonify(ok=1)

@app.delete("/api/<t>/<int:i>")
def rm(t, i):
    if t not in T: return "", 404
    with db() as c:
        c.execute(f"delete from {t} where id=?", (i,))
        if t == "vehicles":
            c.execute("delete from deadlines where vehicle_id=?", (i,))
            c.execute("delete from records where vehicle_id=?", (i,))
    return jsonify(ok=1)
