from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "rahasia-akademik"


# =========================
# DATABASE
# =========================

def get_db():
    conn = sqlite3.connect("akademik.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS mahasiswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nim TEXT NOT NULL,
            nama TEXT NOT NULL,
            prodi TEXT NOT NULL,
            semester INTEGER NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS matakuliah (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kode TEXT NOT NULL,
            nama TEXT NOT NULL,
            sks INTEGER NOT NULL,
            semester INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================
# LOGIN
# =========================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "12345":
            session["login"] = True
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Username atau password salah!"
        )

    return render_template("login.html")


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    if "login" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================
# MAHASISWA
# =========================

@app.route("/mahasiswa")
def mahasiswa():

    if "login" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    data = conn.execute("""
        SELECT * FROM mahasiswa
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "mahasiswa.html",
        mahasiswa=data
    )


@app.route("/mahasiswa/tambah", methods=["POST"])
def tambah_mahasiswa():

    if "login" not in session:
        return redirect(url_for("login"))

    nim = request.form.get("nim")
    nama = request.form.get("nama")
    prodi = request.form.get("prodi")
    semester = request.form.get("semester")

    conn = get_db()

    conn.execute("""
        INSERT INTO mahasiswa
        (nim, nama, prodi, semester)
        VALUES (?, ?, ?, ?)
    """, (nim, nama, prodi, semester))

    conn.commit()
    conn.close()

    return redirect(url_for("mahasiswa"))


@app.route("/mahasiswa/hapus/<int:id>")
def hapus_mahasiswa(id):

    if "login" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    conn.execute(
        "DELETE FROM mahasiswa WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("mahasiswa"))


# =========================
# MATA KULIAH
# =========================

@app.route("/matakuliah")
def matakuliah():

    if "login" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    data = conn.execute("""
        SELECT * FROM matakuliah
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "matakuliah.html",
        matakuliah=data
    )


@app.route("/matakuliah/tambah", methods=["POST"])
def tambah_matakuliah():

    if "login" not in session:
        return redirect(url_for("login"))

    kode = request.form.get("kode")
    nama = request.form.get("nama")
    sks = request.form.get("sks")
    semester = request.form.get("semester")

    # Pastikan semua data diisi
    if not kode or not nama or not sks or not semester:
        return redirect(url_for("matakuliah"))

    conn = get_db()

    conn.execute("""
        INSERT INTO matakuliah
        (kode, nama, sks, semester)
        VALUES (?, ?, ?, ?)
    """, (kode, nama, sks, semester))

    conn.commit()
    conn.close()

    return redirect(url_for("matakuliah"))


@app.route("/matakuliah/hapus/<int:id>")
def hapus_matakuliah(id):

    if "login" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    conn.execute(
        "DELETE FROM matakuliah WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("matakuliah"))


# =========================
# JALANKAN PROGRAM
# =========================

if __name__ == "__main__":

    init_db()

    app.run(debug=True)
