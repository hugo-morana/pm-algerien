"""Réglages › Compte : paramètres Supabase, inscription, connexion, changement d'adresse, export, suppression du compte."""
import sys
p = sys.argv[1]
h = open(p, encoding="utf8").read()

def sub(old, new):
    global h
    assert h.count(old) == 1, ("introuvable ou multiple", old[:90], h.count(old))
    h = h.replace(old, new)

# 1. config : réglages > config.js
sub('const SBCFG = window.PM_CONFIG || {};',
    '''const SBCFG_FILE = window.PM_CONFIG || {};
const SBCFG_USER = ls.get("sbcfg", null);   // réglages saisis dans l'appli (priment sur config.js)
const SBCFG = (SBCFG_USER && SBCFG_USER.supabaseUrl && SBCFG_USER.supabaseKey) ? SBCFG_USER : SBCFG_FILE;
const IN_CLAUDE = !!(window.claude && window.claude.use);''')

# 2. la fenêtre « Mon compte » disparaît : le compte vit dans Réglages
s = h.index('<div class="sheet" id="accountSheet" hidden>'); e = h.index('</div></div>', s) + len('</div></div>')
h = h[:s] + h[e:].lstrip("\n")
sub('<button class="chip" id="accountBtn" type="button" hidden>Compte</button>',
    '<button class="chip" id="accountBtn" type="button" title="Compte et synchronisation">Compte</button>')

# 3. section Compte en tête des Réglages
sub('''  <h1>Réglages</h1>
  <h2 style="margin:4px 0 0">Palais</h2>''', '''  <h1>Réglages</h1>
  <h2 id="compte" style="margin:4px 0 0">Compte</h2>
  <div id="accountBody" class="acct"></div>
  <h3>Serveur de synchronisation (Supabase)</h3>
  <div id="sbCfgBody" class="acct"></div>
  <h2 style="margin:18px 0 0">Palais</h2>''')
sub('.btn.danger { background:#a3301f; border-color:#a3301f; color:#fff }',
    '''.btn.danger { background:#a3301f; border-color:#a3301f; color:#fff }
.acct { display:flex; flex-direction:column; gap:10px }
.acct input[type=email], .acct input[type=text], .acct input[type=url], .acct input[type=password] { font:inherit; font-size:16px; flex:1; min-width:12em; padding:6px 8px; border:1px solid var(--line); border-radius:8px; background:var(--surface); color:var(--fg) }
.acct .kv { display:grid; grid-template-columns:auto 1fr; gap:4px 12px; font-size:14px; margin:0 }
.acct .kv dt { color:var(--muted) } .acct .kv dd { margin:0; overflow-wrap:anywhere }
.acct .warn { border-left:3px solid #a3301f; padding:6px 10px; margin:0; font-size:14px }
.acct details { font-size:14px } .acct details ol { margin:6px 0 0; padding-left:1.3em } .acct code { font-family:var(--mono, monospace); font-size:13px }''')

# 4. logique du compte
s = h.index('/* Fenêtre « Compte » (version GitHub Pages) */'); e = h.index('async function grade(')
ACCOUNT = r'''/* ============ Réglages › Compte ============ */
const AC = { step: "", email: "" };   // étape en cours : "" | "code" | "email" | "delete"
const msgEl = () => $("#sbMsg");
const acSay = t => { const m = msgEl(); if (m) m.textContent = t; };
const dateFr = d => { try { return new Date(d).toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" }); } catch { return "—"; } };
function renderAccount(step) {
  if (step !== undefined) AC.step = step;
  const b = $("#accountBody"); if (!b) return;
  const btn = $("#accountBtn"); if (btn) btn.textContent = store.kind ? "Compte ✓" : "Compte";
  if (store.kind === "claude") {
    b.innerHTML = `<p style="margin:0">Connecté avec ton <b>compte Claude</b> : ta progression est enregistrée sur ce compte et te suit d'un appareil à l'autre. Rien à configurer.</p>
      <div class="btns"><button class="btn alt" type="button" id="acSync">Synchroniser maintenant</button><button class="btn alt" type="button" id="acExport">Copier ma progression</button></div><p class="pr" id="sbMsg" style="margin:0"></p>`;
    return;
  }
  if (!store.sb) {
    b.innerHTML = `<p style="margin:0">Pas de compte : ta progression reste <b>sur cet appareil</b>.</p>
      <p class="pr" style="margin:0">${IN_CLAUDE ? "Dans Claude, la progression suit ton compte Claude dès qu'il est disponible." : "Pour créer un compte et retrouver ta progression sur tous tes appareils, renseigne d'abord le serveur Supabase ci-dessous."}</p>`;
    return;
  }
  if (store.kind === "sb") {
    const u = store.user || {};
    if (AC.step === "email") {
      b.innerHTML = `<p style="margin:0">Nouvelle adresse e-mail. Un lien de confirmation est envoyé à l'ancienne et à la nouvelle adresse ; le changement se fait quand tu les as validés.</p>
        <div class="frow"><label for="acNewEmail">Nouvelle adresse</label><input id="acNewEmail" type="email" autocomplete="email" placeholder="prenom@exemple.fr"></div>
        <div class="btns"><button class="btn" type="button" id="acEmailGo">Changer l'adresse</button><button class="btn alt" type="button" id="acCancel">Annuler</button></div><p class="pr" id="sbMsg" style="margin:0"></p>`;
      setTimeout(() => $("#acNewEmail") && $("#acNewEmail").focus(), 50); return;
    }
    if (AC.step === "delete") {
      b.innerHTML = `<p class="warn">Supprimer le compte <b>${esc(store.email)}</b> efface définitivement ta progression enregistrée en ligne (cartes de révision, historique, notes) et ton identifiant. C'est irréversible. La copie de ta progression sur cet appareil est gardée.</p>
        <div class="frow"><label for="acDelConfirm">Tape <b>SUPPRIMER</b> pour confirmer</label><input id="acDelConfirm" type="text" autocomplete="off" autocapitalize="characters"></div>
        <div class="btns"><button class="btn danger" type="button" id="acDelGo">Supprimer définitivement</button><button class="btn alt" type="button" id="acCancel">Annuler</button></div><p class="pr" id="sbMsg" style="margin:0"></p>`;
      setTimeout(() => $("#acDelConfirm") && $("#acDelConfirm").focus(), 50); return;
    }
    b.innerHTML = `<dl class="kv"><dt>Connecté avec</dt><dd><b>${esc(store.email)}</b></dd>
        <dt>Inscrit le</dt><dd>${u.created_at ? dateFr(u.created_at) : "—"}</dd>
        <dt>Dernière connexion</dt><dd>${u.last_sign_in_at ? dateFr(u.last_sign_in_at) : "—"}</dd>
        <dt>Synchronisation</dt><dd>${AC.lastSync ? "à " + new Date(AC.lastSync).toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" }) : "automatique"}</dd></dl>
      <div class="btns"><button class="btn alt" type="button" id="acSync">Synchroniser maintenant</button><button class="btn alt" type="button" id="acEmail">Changer d'adresse e-mail</button><button class="btn alt" type="button" id="acExport">Exporter ma progression</button><button class="btn alt" type="button" id="sbOut">Se déconnecter</button></div>
      <div class="btns"><button class="btn danger" type="button" id="acDel">Supprimer mon compte…</button></div><p class="pr" id="sbMsg" style="margin:0"></p>`;
    return;
  }
  if (AC.step === "code") {
    b.innerHTML = `<p style="margin:0">Un code à 6 chiffres a été envoyé à <b>${esc(AC.email)}</b>. Il peut mettre une minute à arriver ; pense aux courriers indésirables.</p>
      <div class="frow"><label for="sbCode">Code</label><input id="sbCode" type="text" inputmode="numeric" autocomplete="one-time-code" maxlength="6" style="font:inherit;font-size:20px;letter-spacing:.3em;width:7em;padding:6px 8px;border:1px solid var(--line);border-radius:8px"></div>
      <div class="btns"><button class="btn" type="button" id="sbVerify">Valider</button><button class="btn alt" type="button" id="sbResend">Renvoyer le code</button><button class="btn alt" type="button" id="acCancel">Changer d'adresse</button></div><p class="pr" id="sbMsg" style="margin:0"></p>`;
    setTimeout(() => $("#sbCode") && $("#sbCode").focus(), 50); return;
  }
  b.innerHTML = `<p style="margin:0">Crée un compte ou connecte-toi pour retrouver ta progression sur tous tes appareils. Pas de mot de passe : tu reçois un code par e-mail.</p>
    <div class="frow"><label for="sbEmail">E-mail</label><input id="sbEmail" type="email" autocomplete="email" placeholder="prenom@exemple.fr" value="${esc(AC.email)}"></div>
    <div class="btns"><button class="btn" type="button" id="sbSignup">Créer un compte</button><button class="btn alt" type="button" id="sbSend">Se connecter</button></div><p class="pr" id="sbMsg" style="margin:0"></p>`;
}
async function sbSend(create) {
  const email = ($("#sbEmail") ? $("#sbEmail").value : AC.email || "").trim();
  if (!/^\S+@\S+\.\S+$/.test(email)) { acSay("Adresse e-mail invalide."); return; }
  acSay("Envoi…");
  const { error } = await store.sb.auth.signInWithOtp({ email, options: { shouldCreateUser: !!create } });
  if (error) {
    if (!create && /signups? not allowed|not found|otp_disabled/i.test(error.message || "")) { acSay("Aucun compte avec cette adresse : utilise « Créer un compte »."); return; }
    acSay(error.status === 429 ? "Trop d'envois rapprochés : réessaie dans quelques minutes." : "Envoi impossible : " + error.message); return;
  }
  AC.email = email; AC.create = !!create; renderAccount("code");
}
async function sbVerify() {
  const token = ($("#sbCode").value || "").replace(/\D/g, ""); if (token.length < 6) { acSay("Le code fait 6 chiffres."); return; }
  acSay("Vérification…"); const { data, error } = await store.sb.auth.verifyOtp({ email: AC.email, token, type: "email" });
  if (error || !data.session) { acSay("Code incorrect ou expiré. Redemande un code."); return; }
  AC.step = ""; await useSession(data.session);
}
async function sbOut() {
  await store.sb.auth.signOut(); store.kind = null; store.uid = null; store.user = null; store.cache = {}; AC.step = "";
  renderAccount(); toast("Déconnecté : la progression reste aussi sur cet appareil");
}
async function acSync() {
  acSay("Synchronisation…");
  try { store.cache = {}; await afterLogin(); AC.lastSync = Date.now(); renderAccount(); toast("Progression synchronisée"); }
  catch (e) { acSay("Synchronisation impossible : " + (e.message || e)); }
}
async function acEmailGo() {
  const email = ($("#acNewEmail").value || "").trim(); if (!/^\S+@\S+\.\S+$/.test(email)) { acSay("Adresse e-mail invalide."); return; }
  acSay("Envoi…"); const { error } = await store.sb.auth.updateUser({ email });
  if (error) { acSay("Changement impossible : " + error.message); return; }
  acSay("C'est envoyé : valide le lien reçu sur l'ancienne et la nouvelle adresse.");
}
function progressDump() {
  const o = { palais: "Dar ed-Darja", date: new Date().toISOString(), compte: store.email || null, notes: ls.get("notes", {}), historique: ls.get("hist", []), cartes: {} };
  for (const id of allRoomIds()) { const c = ls.get("srs_" + id, {}); if (Object.keys(c).length) o.cartes[id] = c; }
  return JSON.stringify(o);
}
async function acExport() {
  const txt = progressDump(), name = "dar-ed-darja-progression-" + new Date().toISOString().slice(0, 10) + ".json";
  if (!IN_CLAUDE) {
    try { const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([txt], { type: "application/json" })); a.download = name; document.body.appendChild(a); a.click(); a.remove(); acSay("Fichier « " + name + " » téléchargé."); return; } catch (e) {}
  }
  try { await navigator.clipboard.writeText(txt); acSay("Progression copiée dans le presse-papiers (format JSON)."); } catch { acSay("Copie impossible sur cet appareil."); }
}
async function acDelGo() {
  if (($("#acDelConfirm").value || "").trim().toUpperCase() !== "SUPPRIMER") { acSay("Tape SUPPRIMER pour confirmer."); return; }
  acSay("Suppression…");
  const { error } = await store.sb.rpc("delete_my_account");
  if (error) {
    // fonction absente du serveur : on efface au moins la progression en ligne
    const { error: e2 } = await store.sb.from("progress").delete().eq("user_id", store.uid);
    if (e2) { acSay("Suppression impossible : " + error.message); return; }
    acSay("Ta progression en ligne est effacée, mais l'identifiant n'a pas pu être supprimé : le serveur n'a pas la fonction delete_my_account (voir l'aide ci-dessous).");
    await store.sb.auth.signOut(); store.kind = null; store.uid = null; store.user = null; store.cache = {}; AC.step = ""; ls.set("owner", null);
    setTimeout(renderAccount, 4000); return;
  }
  try { await store.sb.auth.signOut(); } catch (e) {}
  store.kind = null; store.uid = null; store.user = null; store.cache = {}; AC.step = ""; AC.email = ""; ls.set("owner", null);
  renderAccount(); toast("Compte supprimé. La progression reste sur cet appareil.");
}
/* Serveur Supabase : URL + clé publique, saisis ici ou dans config.js */
function renderSbCfg() {
  const b = $("#sbCfgBody"); if (!b) return;
  if (IN_CLAUDE) { b.innerHTML = `<p class="pr" style="margin:0">Dans Claude, la progression passe par ton compte Claude. Le serveur Supabase sert à la version publiée sur GitHub Pages (connexion par e-mail).</p>`; return; }
  const src = (SBCFG_USER && SBCFG_USER.supabaseUrl) ? "saisi dans ces réglages" : (SBCFG_FILE.supabaseUrl ? "fichier config.js" : "");
  const cur = SBCFG.supabaseUrl ? SBCFG : { supabaseUrl: "", supabaseKey: "" };
  b.innerHTML = `<p style="margin:0">${src ? `Serveur actif : <b>${esc(cur.supabaseUrl.replace(/^https?:\/\//, ""))}</b> (${src}).` : "Aucun serveur : la connexion par e-mail est désactivée."}</p>
    <div class="frow"><label for="cfgUrl">URL du projet</label><input id="cfgUrl" type="url" inputmode="url" autocomplete="off" spellcheck="false" placeholder="https://xxxx.supabase.co" value="${esc(cur.supabaseUrl)}"></div>
    <div class="frow"><label for="cfgKey">Clé publique (anon)</label><input id="cfgKey" type="password" autocomplete="off" spellcheck="false" placeholder="eyJhbGciOi… ou sb_publishable_…" value="${esc(cur.supabaseKey)}"><button class="chip" type="button" id="cfgShow">Afficher</button></div>
    <div class="btns"><button class="btn" type="button" id="cfgSave">Enregistrer et se connecter</button><button class="btn alt" type="button" id="cfgTest">Tester</button>${SBCFG_USER ? `<button class="btn alt" type="button" id="cfgClear">Revenir à config.js</button>` : ""}</div>
    <p class="pr" id="cfgMsg" style="margin:0"></p>
    <details><summary>Créer son serveur Supabase (gratuit)</summary><ol>
      <li>Crée un projet sur <a href="https://supabase.com" target="_blank" rel="noopener">supabase.com</a>.</li>
      <li>Dans <i>SQL Editor</i>, colle et exécute le script <code>supabase/schema.sql</code> du dépôt <button class="chip" type="button" id="cfgSql">Copier le script</button> : il crée la table de progression, ses règles de sécurité et la fonction de suppression de compte.</li>
      <li>Dans <i>Authentication › Email Templates › Magic Link</i>, colle le modèle <code>supabase/email-code.html</code> (il affiche le code à 6 chiffres).</li>
      <li>Dans <i>Project Settings › API</i>, copie l'URL du projet et la clé <i>anon public</i>, puis colle-les ci-dessus.</li>
    </ol><p class="pr" style="margin:6px 0 0">La clé « anon » est faite pour être publique : les règles de la table empêchent chacun de lire la progression des autres. N'utilise jamais la clé « service_role » ici.</p></details>`;
}
const cfgSay = t => { const m = $("#cfgMsg"); if (m) m.textContent = t; };
function cfgRead() {
  const url = ($("#cfgUrl").value || "").trim().replace(/\/+$/, ""), key = ($("#cfgKey").value || "").trim();
  if (!/^https:\/\/[a-z0-9.-]+$/i.test(url)) { cfgSay("URL invalide : elle ressemble à https://xxxx.supabase.co"); return null; }
  if (key.length < 20) { cfgSay("Clé trop courte : copie la clé « anon public » en entier."); return null; }
  if (/service_role/.test(atobSafe(key))) { cfgSay("C'est la clé service_role, secrète : utilise la clé « anon public »."); return null; }
  return { supabaseUrl: url, supabaseKey: key };
}
function atobSafe(k) { try { return atob((k.split(".")[1] || "").replace(/-/g, "+").replace(/_/g, "/")); } catch { return ""; } }
async function cfgTest(c) {
  c = c || cfgRead(); if (!c) return false;
  cfgSay("Test…");
  try {
    const r = await fetch(c.supabaseUrl + "/auth/v1/settings", { headers: { apikey: c.supabaseKey } });
    if (!r.ok) { cfgSay(r.status === 401 ? "Clé refusée par le serveur." : "Le serveur répond " + r.status + "."); return false; }
    const t = await fetch(c.supabaseUrl + "/rest/v1/progress?select=key&limit=1", { headers: { apikey: c.supabaseKey, Authorization: "Bearer " + c.supabaseKey } });
    cfgSay(t.ok ? "Serveur joignable, table de progression trouvée." : "Serveur joignable, mais la table « progress » est absente : exécute supabase/schema.sql.");
    return true;
  } catch (e) { cfgSay("Serveur injoignable : vérifie l'URL."); return false; }
}
async function cfgSave() {
  const c = cfgRead(); if (!c) return;
  if (!(await cfgTest(c))) return;
  ls.set("sbcfg", c); cfgSay("Enregistré. Rechargement…"); setTimeout(() => { location.hash = "compte"; location.reload(); }, 600);
}
function cfgClear() { ls.set("sbcfg", null); cfgSay("Réglages effacés. Rechargement…"); setTimeout(() => location.reload(), 600); }
async function cfgSql() {
  try { const t = await (await fetch("supabase/schema.sql")).text(); await navigator.clipboard.writeText(t); cfgSay("Script SQL copié."); }
  catch { cfgSay("Copie impossible : ouvre supabase/schema.sql dans le dépôt."); }
}
function openAccount() { setView("reglages"); renderAccount(); renderSbCfg(); setTimeout(() => { const c = $("#compte"); if (c) c.scrollIntoView({ block: "start" }); }, 60); }
'''
h = h[:s] + ACCOUNT + h[e:]

# 5. session : garder l'utilisateur (dates) et rafraîchir la section
sub('store.kind = "sb"; store.uid = session.user.id; store.email = session.user.email || "";',
    'store.kind = "sb"; store.uid = session.user.id; store.email = session.user.email || ""; store.user = session.user;')
sub('await afterLogin(); renderAccount(); $("#accountBtn").textContent = "Compte ✓"; toast("Connecté : " + store.email);',
    'await afterLogin(); AC.lastSync = Date.now(); renderAccount(); toast("Connecté : " + store.email);')

# 6. évènements
s = h.index('  $("#accountBtn").onclick = () => { $("#accountSheet").hidden = false; renderAccount(); };')
e = h.index('\n', h.index('$("#accountSheet").addEventListener("keydown"', s)) + 1
h = h[:s] + '''  $("#accountBtn").onclick = openAccount;
  $("#reglages").addEventListener("click", e => {
    const id = e.target.id;
    const A = { sbSend: () => sbSend(false), sbSignup: () => sbSend(true), sbResend: () => sbSend(AC.create), sbVerify, sbOut, acSync, acExport,
      acEmail: () => renderAccount("email"), acEmailGo, acDel: () => renderAccount("delete"), acDelGo, acCancel: () => renderAccount(""),
      cfgSave, cfgClear, cfgSql, cfgTest: () => cfgTest(), cfgShow: () => { const k = $("#cfgKey"); k.type = k.type === "password" ? "text" : "password"; e.target.textContent = k.type === "password" ? "Afficher" : "Masquer"; } };
    if (A[id]) { e.preventDefault(); A[id](); }
  });
  $("#reglages").addEventListener("keydown", e => {
    if (e.key !== "Enter") return; const id = e.target.id;
    if (id === "sbEmail") sbSend(false); if (id === "sbCode") sbVerify(); if (id === "acNewEmail") acEmailGo(); if (id === "acDelConfirm") acDelGo(); if (id === "cfgKey" || id === "cfgUrl") cfgSave();
  });
''' + h[e:]

sub('  setView(ls.get("view", "palais")); setTimeout(updateTestBadge, 1500);',
    '  setView(ls.get("view", "palais")); setTimeout(updateTestBadge, 1500);\n  if (location.hash === "#compte") setTimeout(openAccount, 300);')

# 7. ouvrir les réglages sur le compte : rendu à chaque passage
sub('  if (v === "reglages") renderTests();', '  if (v === "reglages") { renderTests(); renderAccount(); renderSbCfg(); }')
sub('      $("#accountBtn").hidden = false;\n', '')

open(p, "w", encoding="utf8").write(h)
print("ok")
