import os, sqlite3, uuid
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

DB = os.environ.get("DB_PATH", "/data/vehicles.db")
FILES = os.path.join(os.path.dirname(DB), "files")
ALLOWED = {"pdf", "jpg", "jpeg", "png", "webp"}
app = Flask(__name__, static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 30 * 1024 * 1024
T = {
    "vehicles": ["name", "plate", "notes", "purchase_date", "sale_date"],
    "deadlines": ["vehicle_id", "type", "due_date", "repeat_months", "notes"],
    "records": ["vehicle_id", "date", "type", "description", "cost", "km", "place_id"],
    "places": ["name", "kind", "notes"],
}

def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

os.makedirs(os.path.dirname(DB), exist_ok=True)
with db() as c:
    for t, cols in T.items():
        c.execute(f"create table if not exists {t}(id integer primary key autoincrement,{','.join(cols)})")
        have = {r[1] for r in c.execute(f"pragma table_info({t})")}
        for k in cols:  # migrazione da versioni precedenti
            if k not in have:
                c.execute(f"alter table {t} add column {k}")
    c.execute("create table if not exists settings(key text primary key, value text)")
    c.execute("create table if not exists attachments(id integer primary key autoincrement,kind,ref_id,name,stored)")

def drop_files(c, where, args):
    for r in c.execute(f"select stored from attachments where {where}", args).fetchall():
        try: os.remove(os.path.join(FILES, r[0]))
        except OSError: pass
    c.execute(f"delete from attachments where {where}", args)

@app.get("/")
def index():
    return send_from_directory("static", "index.html")

@app.get("/api/attachments")
def alist():
    return jsonify([dict(r) for r in db().execute("select id,kind,ref_id,name from attachments")])

@app.post("/api/attachments")
def aadd():
    f, kind = request.files.get("file"), request.form.get("kind")
    if not f or kind not in ("records", "deadlines"):
        return jsonify(error="richiesta non valida"), 400
    name = secure_filename(f.filename or "")
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext not in ALLOWED:
        return jsonify(error="formato non supportato"), 400
    stored = uuid.uuid4().hex + "." + ext
    os.makedirs(FILES, exist_ok=True)
    f.save(os.path.join(FILES, stored))
    with db() as c:
        cur = c.execute("insert into attachments(kind,ref_id,name,stored) values(?,?,?,?)",
                        (kind, int(request.form["ref_id"]), name, stored))
        return jsonify(id=cur.lastrowid)

@app.delete("/api/attachments/<int:i>")
def adel(i):
    with db() as c:
        drop_files(c, "id=?", (i,))
    return jsonify(ok=1)

@app.get("/files/<int:i>")
def afile(i):
    r = db().execute("select name,stored from attachments where id=?", (i,)).fetchone()
    if not r: return "", 404
    return send_from_directory(FILES, r["stored"], download_name=r["name"])

@app.get("/api/settings")
def sget():
    return jsonify({r[0]: r[1] for r in db().execute("select key,value from settings")})

@app.put("/api/settings")
def sput():
    with db() as c:
        for k, v in (request.json or {}).items():
            c.execute("insert into settings(key,value) values(?,?) on conflict(key) do update set value=excluded.value", (str(k), str(v)))
    return jsonify(ok=1)

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
        if t == "vehicles":
            for k in ("records", "deadlines"):
                drop_files(c, f"kind=? and ref_id in (select id from {k} where vehicle_id=?)", (k, i))
            c.execute("delete from deadlines where vehicle_id=?", (i,))
            c.execute("delete from records where vehicle_id=?", (i,))
        elif t == "places":
            c.execute("update records set place_id=null where place_id=?", (i,))
        else:
            drop_files(c, "kind=? and ref_id=?", (t, i))
        c.execute(f"delete from {t} where id=?", (i,))
    return jsonify(ok=1)
