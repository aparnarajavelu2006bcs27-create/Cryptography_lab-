from flask import Flask, request, render_template_string

app = Flask(__name__)

# ---------------- HTML ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Manual RSA Demo</title>
<style>
body { font-family: Times New Roman; background:#eef2ff; }
.container { width:600px; margin:auto; background:white; padding:20px; }
input, button { width:100%; padding:6px; margin:4px 0; }
pre { background:#f1f5f9; padding:15px; font-size:16px; }
button { background:#1e3a8a; color:white; border:none; }
</style>
</head>
<body>
<div class="container">
<h2 align="center">Manual RSA Encryption/Decryption</h2>

<form method="post">
Plaintext (number): <input name="pt">
Prime p: <input name="p">
Prime q: <input name="q">
<button name="action" value="rsa">PROCESS RSA</button>
</form>

{% if out %}
<h3>Step-by-Step Output</h3>
<pre>{{ out }}</pre>
{% endif %}
</div>
</body>
</html>
"""

# ---------------- MANUAL FUNCTIONS ----------------
def manual_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def manual_modexp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result

def manual_modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

# ---------------- RSA PROCESS ----------------
def rsa_process(pt, p, q):
    log = []

    # Step 1: Compute n and phi
    n = p * q
    phi = (p - 1) * (q - 1)
    log.append(f"n = p * q = {p} * {q} = {n}")
    log.append(f"phi(n) = (p-1)*(q-1) = {phi}")

    # Step 2: Choose e
    e = 3
    while manual_gcd(e, phi) != 1:
        e += 2
    log.append(f"Choose e such that gcd(e, phi) = 1 → e = {e}")

    # Step 3: Compute d
    d = manual_modinv(e, phi)
    log.append(f"Compute d ≡ e^(-1) mod phi → d = {d}")

    # Step 4: Encrypt
    c = manual_modexp(pt, e, n)
    log.append(f"Ciphertext c = pt^e mod n = {pt}^{e} mod {n} = {c}")

    # Step 5: Decrypt
    dec = manual_modexp(c, d, n)
    log.append(f"Decrypted text pt = c^d mod n = {c}^{d} mod {n} = {dec}")

    return "\n".join(log)

# ---------------- ROUTE ----------------
@app.route("/", methods=["GET","POST"])
def index():
    out = None
    if request.method == "POST" and request.form["action"] == "rsa":
        pt = int(request.form["pt"])
        p = int(request.form["p"])
        q = int(request.form["q"])
        out = rsa_process(pt, p, q)
    return render_template_string(HTML, out=out)

if __name__ == "__main__":
    app.run(debug=True)