/* Pirca frontend: plain JavaScript, no build step.
   Routes: #/  ·  #/new  ·  #/plan/PIU-XXXXXX  ·  #/plans */
"use strict";

// ------------------------------------------------------------------ strings (English + Spanish)

const STR = {
  en: {
    new: "New", help: "Help", menu: "Menu", close: "Close", language: "Language", currency: "Currency",
    myPlans: "My plans", openByCode: "Open a plan by code", planCode: "Plan code", open: "Open",
    badCode: "Codes look like PIU- followed by 6 letters or numbers.",
    heroTitle: "Prepare your shop for El Niño costero",
    heroText: "Pirca reads the latest official ENFEN alerts and Piura's 1998, 2017 and 2023 flood history, then builds a step-by-step preparation plan for your shop that fits the money you have.",
    makePlan: "Make my plan", openExample: "Open example (PIU-CAST26)",
    fact1: "Official sources", fact1b: "ENFEN, INDECI, BCRP and Piura's flood records, with every number cited.",
    fact2: "Four AI agents", fact2b: "An analyst, a planner and a critic check each other before you see the plan.",
    fact3: "Within your means", fact3b: "Pirca never recommends spending money you don't have.",
    howTitle: "How it works", how: ["Answer 5 short sections", "Four agents check the facts", "Get your plan"],
    communique: "Communiqué", mapTitle: "Map of the eastern Pacific and Peru's coast with Piura marked",
    mapCaption: "El Niño costero: unusually warm sea water off Peru brings heavy rain to Piura.",
    source: "Source", viewSource: "View source", sourcesTitle: "Sources", checksTitle: "Safety checks",
    badgeNumbers: "Every number from code", badgeSources: "Sources checked", badgeBudget: "Within your budget",
    badgeEvacuation: "No evacuation orders", badgeSuspiciousNone: "Suspicious text: none found",
    badgeSuspiciousFound: (n) => `Suspicious text found and ignored: ${n}`,
    formTitle: "Tell us about your shop", formIntro: "Five short groups. Amounts are in soles. Your answers stay with your plan code.",
    useSample: "Fill with a sample shop", addSupplier: "+ Add supplier", remove: "Remove",
    checkAnswers: "Check my answers", checking: "Checking…", fixAnswers: "Fix my answers", confirmRun: "Confirm and make my plan",
    errorsTitle: "Please fix these answers", warningsTitle: "Please check these answers",
    warningsText: "You can fix them or confirm that they are right.",
    starting: "Starting…", networkError: "Pirca could not reach the server. Check your connection and try again.",
    traceTitle: "Your plan is being prepared", replayTitle: "Replaying the saved trace",
    traceText: "You can close this page: your plan keeps running. Open it later from My plans or with its code.",
    working: "working…", waiting: "waiting", idle: "not started", done: "done",
    inTok: "Input tokens", cachedTok: "Cached", outTok: "Output tokens", cost: "Cost (USD)",
    speed: "Speed", skip: "Show the plan", backToPlan: "Back to the plan",
    viewIn: "View in English", viewing: "Translating…", replay: "Replay trace",
    risk: "Risk", riskHigh: "High", riskMedium: "Medium", riskLow: "Low",
    stockAtRisk: "Stock at risk", fundGap: "Emergency fund gap", purchases: "Purchases",
    summaryTitle: "Summary in English", usageTitle: "Tokens and cost",
    row: "", calls: "Model calls", input: "Input", cached: "Cached", output: "Output",
    runRow: "Agent run", trRow: "Translation",
    fxNote: (r, d) => `US dollar amounts use the fixed BCRP rate of S/ ${r} per US$ (${d}).`,
    stoppedTitle: "The run stopped at a safety limit", errorTitle: "The run could not finish",
    stoppedText: "No plan was produced. The trace below shows where it stopped.",
    notFound: "No plan found with that code.", loading: "Loading…",
    myPlansTitle: "My plans", myPlansEmpty: "No plans yet on this device.", myPlansNote: "Saved on this device only. Each plan can also be opened anywhere with its code.",
    statusRunning: "running", statusDone: "ready", statusStopped: "stopped", statusError: "error", statusMissing: "not found",
    translationWarn: "The automatic check found issues in this translation; compare it with the original.",
    created: "Created", toolCall: "tool call", toolCalls: "tool calls",
    runStarted: "Run started", runFinished: "Run finished", started: "started", finished: "finished",
    agents: {
      manager: ["Manager", "Coordinates the team and writes your plan."],
      risk_analyst: ["Risk Analyst", "Reads ENFEN alerts and Piura's flood history."],
      planner: ["Planner", "Works out stock, cash and suppliers, and buys within budget."],
      critic: ["Critic", "Tests the plan against tough situations."],
    },
  },
  es: {
    new: "Nuevo", help: "Ayuda", menu: "Menú", close: "Cerrar", language: "Idioma", currency: "Moneda",
    myPlans: "Mis planes", openByCode: "Abrir un plan con su código", planCode: "Código del plan", open: "Abrir",
    badCode: "Los códigos son PIU- seguido de 6 letras o números.",
    heroTitle: "Prepara tu negocio para El Niño costero",
    heroText: "Pirca lee las alertas oficiales más recientes del ENFEN y lo que pasó en Piura en 1998, 2017 y 2023, y arma un plan de preparación paso a paso para tu negocio, según el dinero que tienes.",
    makePlan: "Hacer mi plan", openExample: "Ver ejemplo (PIU-CAST26)",
    fact1: "Fuentes oficiales", fact1b: "ENFEN, INDECI, BCRP y los registros de inundaciones de Piura, con cada número citado.",
    fact2: "Cuatro agentes de IA", fact2b: "Un analista, un planificador y un revisor se controlan entre sí antes de que veas el plan.",
    fact3: "Según tu dinero", fact3b: "Pirca nunca te recomienda gastar dinero que no tienes.",
    howTitle: "Cómo funciona", how: ["Responde 5 secciones cortas", "Cuatro agentes revisan los datos", "Recibe tu plan"],
    communique: "Comunicado", mapTitle: "Mapa del Pacífico oriental y la costa del Perú con Piura marcada",
    mapCaption: "El Niño costero: el mar frente al Perú se calienta más de lo normal y trae lluvias fuertes a Piura.",
    source: "Fuente", viewSource: "Ver fuente", sourcesTitle: "Fuentes", checksTitle: "Controles de seguridad",
    badgeNumbers: "Cada número viene del código", badgeSources: "Fuentes revisadas", badgeBudget: "Dentro de tu presupuesto",
    badgeEvacuation: "Sin órdenes de evacuación", badgeSuspiciousNone: "Texto sospechoso: no se encontró",
    badgeSuspiciousFound: (n) => `Texto sospechoso detectado e ignorado: ${n}`,
    formTitle: "Cuéntanos sobre tu negocio", formIntro: "Cinco grupos cortos. Los montos van en soles. Tus respuestas quedan con el código de tu plan.",
    useSample: "Llenar con un negocio de ejemplo", addSupplier: "+ Agregar proveedor", remove: "Quitar",
    checkAnswers: "Revisar mis respuestas", checking: "Revisando…", fixAnswers: "Corregir mis respuestas", confirmRun: "Confirmar y hacer mi plan",
    errorsTitle: "Corrige estas respuestas", warningsTitle: "Revisa estas respuestas",
    warningsText: "Puedes corregirlas o confirmar que están bien.",
    starting: "Iniciando…", networkError: "Pirca no pudo conectarse con el servidor. Revisa tu conexión e inténtalo de nuevo.",
    traceTitle: "Estamos preparando tu plan", replayTitle: "Repitiendo el registro guardado",
    traceText: "Puedes cerrar esta página: tu plan sigue preparándose. Ábrelo después desde Mis planes o con su código.",
    working: "trabajando…", waiting: "esperando", idle: "sin empezar", done: "listo",
    inTok: "Tokens de entrada", cachedTok: "En caché", outTok: "Tokens de salida", cost: "Costo (USD)",
    speed: "Velocidad", skip: "Ver el plan", backToPlan: "Volver al plan",
    viewIn: "Ver en español", viewing: "Traduciendo…", replay: "Ver cómo se hizo",
    risk: "Riesgo", riskHigh: "Alto", riskMedium: "Medio", riskLow: "Bajo",
    stockAtRisk: "Mercadería en riesgo", fundGap: "Falta para tu fondo", purchases: "Compras",
    summaryTitle: "Resumen en inglés", usageTitle: "Tokens y costo",
    row: "", calls: "Llamadas al modelo", input: "Entrada", cached: "En caché", output: "Salida",
    runRow: "Agentes", trRow: "Traducción",
    fxNote: (r, d) => `Los montos en dólares usan el tipo de cambio fijo del BCRP: S/ ${r} por US$ (${d}).`,
    stoppedTitle: "El proceso se detuvo por un límite de seguridad", errorTitle: "El proceso no pudo terminar",
    stoppedText: "No se generó un plan. El registro de abajo muestra dónde se detuvo.",
    notFound: "No hay un plan con ese código.", loading: "Cargando…",
    myPlansTitle: "Mis planes", myPlansEmpty: "Todavía no hay planes en este dispositivo.", myPlansNote: "Guardados solo en este dispositivo. Cada plan también se puede abrir en cualquier lugar con su código.",
    statusRunning: "preparándose", statusDone: "listo", statusStopped: "detenido", statusError: "error", statusMissing: "no encontrado",
    translationWarn: "La revisión automática encontró problemas en esta traducción; compárala con el original.",
    created: "Creado", toolCall: "herramienta usada", toolCalls: "herramientas usadas",
    runStarted: "Inicio", runFinished: "Fin", started: "empezó", finished: "terminó",
    agents: {
      manager: ["Coordinador", "Coordina al equipo y escribe tu plan."],
      risk_analyst: ["Analista de riesgo", "Lee las alertas del ENFEN y la historia de inundaciones de Piura."],
      planner: ["Planificador", "Calcula mercadería, caja y proveedores, y compra dentro del presupuesto."],
      critic: ["Revisor", "Pone a prueba el plan con situaciones difíciles."],
    },
  },
};

// Form fields: label and hint in both languages.
const YES_NO_UNKNOWN = { en: { yes: "Yes", no: "No", unknown: "Not sure" }, es: { yes: "Sí", no: "No", unknown: "No sé" } };
const YES_NO = { en: { yes: "Yes", no: "No" }, es: { yes: "Sí", no: "No" } };
const GROUPS = [
  { id: "business", title: { en: "Your business", es: "Tu negocio" },
    hint: { en: "Where you are and what your place is like.", es: "Dónde estás y cómo es tu local." },
    fields: [
      { name: "business_type", type: "text", list: "business-types", label: { en: "Type of business", es: "Tipo de negocio" }, hint: { en: "For example: bodega, hardware store, pharmacy", es: "Por ejemplo: bodega, ferretería, botica" } },
      { name: "district", type: "district", label: { en: "District", es: "Distrito" }, hint: { en: "Piura region", es: "Región Piura" } },
      { name: "near_water", type: "select", options: YES_NO_UNKNOWN, label: { en: "Near a river, drain or ravine?", es: "¿Cerca de un río, dren o quebrada?" }, hint: { en: "Within a few blocks", es: "A pocas cuadras" } },
      { name: "flooded_before", type: "select", options: YES_NO_UNKNOWN, label: { en: "Did it flood in 2017 or 2023?", es: "¿Se inundó en 2017 o 2023?" }, hint: { en: "Your shop or its street", es: "Tu local o tu calle" } },
      { name: "floor_level", type: "select", options: { en: { ground: "Ground floor, at street level", raised: "Raised above the street", upper: "Upper floor" }, es: { ground: "Primer piso, a nivel de la calle", raised: "Más alto que la calle", upper: "Piso alto" } }, label: { en: "Where is the shop?", es: "¿Dónde está el local?" }, hint: { en: "The floor where you sell", es: "El piso donde vendes" } },
      { name: "higher_storage", type: "select", options: { en: { second_floor: "Second floor", mezzanine: "Mezzanine", none: "None" }, es: { second_floor: "Segundo piso", mezzanine: "Altillo (mezanine)", none: "Ninguno" } }, label: { en: "A higher place to store stock?", es: "¿Un lugar más alto para guardar mercadería?" }, hint: { en: "Somewhere water can't reach", es: "Donde no llegue el agua" } },
      { name: "tenure", type: "select", options: { en: { owned: "Owned", rented: "Rented" }, es: { owned: "Propio", rented: "Alquilado" } }, label: { en: "Is the place owned or rented?", es: "¿El local es propio o alquilado?" }, hint: { en: "Some repairs need the landlord", es: "Algunos arreglos necesitan al dueño" } },
      { name: "workers", type: "number", min: 1, step: 1, label: { en: "People working, including you", es: "Personas que trabajan, contándote" }, hint: { en: "Number of people", es: "Número de personas" } },
    ] },
  { id: "stock", title: { en: "Your stock", es: "Tu mercadería" },
    hint: { en: "What you have in the shop today.", es: "Lo que tienes hoy en el local." },
    fields: [
      { name: "stock_value", type: "money", label: { en: "Value of your stock", es: "Valor de tu mercadería" }, hint: { en: "At cost, in soles", es: "A precio de costo, en soles" } },
      { name: "share_stock_below_1m", type: "percent", label: { en: "Share kept less than 1 m above the floor", es: "Parte guardada a menos de 1 m del piso" }, hint: { en: "0 to 100%", es: "De 0 a 100%" } },
      { name: "perishables", type: "select", options: YES_NO, label: { en: "Do you sell perishables?", es: "¿Vendes productos perecibles?" }, hint: { en: "Bread, dairy, fruit, meat…", es: "Pan, lácteos, fruta, carne…" } },
      { name: "days_of_stock", type: "number", min: 0, step: 1, label: { en: "Days your stock lasts without restocking", es: "Días que dura tu mercadería sin reponer" }, hint: { en: "Approximate", es: "Aproximado" } },
    ] },
  { id: "money", title: { en: "Your money", es: "Tu dinero" },
    hint: { en: "Used only to size your emergency fund and keep purchases within reach.", es: "Solo sirve para calcular tu fondo de emergencia y que las compras estén a tu alcance." },
    fields: [
      { name: "cash_on_hand", type: "money", label: { en: "Cash you have available", es: "Dinero que tienes disponible" }, hint: { en: "Savings and cash for the business", es: "Ahorros y caja del negocio" } },
      { name: "monthly_fixed_costs", type: "money", label: { en: "Fixed costs per month", es: "Gastos fijos al mes" }, hint: { en: "Rent, wages, utilities, loan payments", es: "Alquiler, sueldos, servicios, cuotas" } },
      { name: "weekly_sales", type: "money", label: { en: "Sales per week", es: "Ventas por semana" }, hint: { en: "A normal week", es: "Una semana normal" } },
    ] },
  { id: "suppliers", title: { en: "Your suppliers", es: "Tus proveedores" },
    hint: { en: "Up to 3. Pirca checks which roads were cut in past floods.", es: "Hasta 3. Pirca revisa qué carreteras se cortaron en inundaciones pasadas." }, fields: [] },
  { id: "prep", title: { en: "Your preparation", es: "Tu preparación" },
    hint: { en: "What you can spend now, and what you already have.", es: "Lo que puedes gastar ahora y lo que ya tienes." },
    fields: [
      { name: "prep_budget", type: "money", label: { en: "Budget for preparation", es: "Presupuesto para prepararte" }, hint: { en: "What you could spend in the next weeks", es: "Lo que podrías gastar en las próximas semanas" } },
    ] },
];
const SUPPLIER_PERISHABLE = { en: { "": "Detect from product", "true": "Perishable", "false": "Not perishable" },
                              es: { "": "Detectar por el producto", "true": "Perecible", "false": "No perecible" } };
const LEVEL_NOTE = { en: { UNVERIFIED: " — no sourced flood history" }, es: { UNVERIFIED: " — sin historial con fuente" } };

// Spanish versions of the server's validation warnings (the server writes them in English).
const WARNING_ES = [
  [/^District data for (.+) is UNVERIFIED.*/, (m) => `Los datos del distrito ${m[1]} no están verificados: Pirca no encontró historial de inundaciones con fuente, así que su nivel de riesgo es provisional.`],
  [/^Prep budget is larger than cash on hand.*/, () => "Tu presupuesto para prepararte es mayor que el dinero disponible; Pirca lo limitará a lo que tienes."],
  [/^Ground-floor shop with no higher storage and no prep budget.*/, () => "Local en primer piso, sin lugar alto y sin presupuesto: solo se pueden planear acciones gratuitas."],
  [/^Share of stock below 1 m is set but stock value is 0.*/, () => "Indicaste mercadería a menos de 1 m, pero el valor de la mercadería es 0."],
  [/^Monthly sales look lower than monthly fixed costs.*/, () => "Tus ventas del mes parecen menores que tus gastos fijos; revisa ambos números."],
  [/^Some flood questions were answered 'unknown'.*/, () => "Respondiste 'No sé' en alguna pregunta de inundación; Pirca la cuenta como riesgo parcial."],
  [/^The shop flooded before although its district is not rated high.*/, () => "Tu local se inundó antes aunque tu distrito no está en riesgo alto; Pirca usa la historia de tu local."],
  [/^No suppliers listed.*/, () => "No agregaste proveedores; no se puede calcular la reserva de mercadería."],
  [/^Ignoring unknown checklist items: (.+)/, (m) => `Se ignoran elementos desconocidos: ${m[1]}`],
];

// ------------------------------------------------------------------ state and storage

const CODE_RE = /^PIU-[23456789ABCDEFGHJKMNPQRSTUVWXYZ]{6}$/;
const store = {
  get lang() { return localStorage.getItem("pirca.lang") || "en"; },
  set lang(v) { localStorage.setItem("pirca.lang", v); },
  get currency() { return localStorage.getItem("pirca.currency") || "usd"; },
  set currency(v) { localStorage.setItem("pirca.currency", v); },
  get plans() { try { return JSON.parse(localStorage.getItem("pirca.plans")) || []; } catch { return []; } },
  set plans(v) { localStorage.setItem("pirca.plans", JSON.stringify(v)); },
  get draft() { try { return JSON.parse(localStorage.getItem("pirca.draft")); } catch { return null; } },
  set draft(v) { localStorage.setItem("pirca.draft", JSON.stringify(v)); },
};
const state = { meta: null, timers: [], view: null };
const app = document.getElementById("app");

function t(key) { return STR[store.lang][key] ?? STR.en[key] ?? key; }
function L(obj) { return obj[store.lang] ?? obj.en; }
function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function clearTimers() { state.timers.forEach((id) => { clearTimeout(id); clearInterval(id); }); state.timers = []; }
function later(fn, ms) { const id = setTimeout(fn, ms); state.timers.push(id); return id; }

async function api(path, options = {}) {
  const res = await fetch(path, { headers: { "Content-Type": "application/json" }, ...options });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) { const err = new Error(`HTTP ${res.status}`); err.status = res.status; err.body = body; throw err; }
  return body;
}
async function meta() { return state.meta ??= await api("/api/meta"); }

function money(value, currency = store.currency) {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  const amount = currency === "usd" ? value / state.meta.pen_per_usd : value;
  const decimals = Math.abs(amount) < 100 && !Number.isInteger(amount) ? 2 : 0;
  const text = Math.abs(amount).toLocaleString("en-US", { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
  return `${amount < 0 ? "-" : ""}${currency === "usd" ? "$" : "S/ "}${text}`;
}
function num(n) { return Number(n || 0).toLocaleString("en-US"); }

// ------------------------------------------------------------------ chrome: header, menu, help

function applyChrome() {
  document.documentElement.lang = store.lang;
  document.querySelectorAll("[data-t]").forEach((el) => { el.textContent = t(el.dataset.t); });
  document.querySelectorAll("[data-t-label]").forEach((el) => el.setAttribute("aria-label", t(el.dataset.tLabel)));
  document.querySelectorAll("[data-lang]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.lang === store.lang)));
  document.querySelectorAll("[data-currency]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.currency === store.currency)));
  document.getElementById("help-body").innerHTML = helpHtml();
}

const menu = document.getElementById("menu");
const menuBtn = document.getElementById("menu-btn");
function toggleMenu(open = menu.hidden) {
  menu.hidden = !open;
  menuBtn.setAttribute("aria-expanded", String(open));
}
menuBtn.addEventListener("click", (e) => { e.stopPropagation(); toggleMenu(); });
document.addEventListener("click", (e) => { if (!menu.hidden && !menu.contains(e.target)) toggleMenu(false); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape") toggleMenu(false); });
document.querySelectorAll("[data-lang]").forEach((b) => b.addEventListener("click", () => {
  saveDraftFromForm();
  store.lang = b.dataset.lang; applyChrome(); route();
}));
document.querySelectorAll("[data-currency]").forEach((b) => b.addEventListener("click", () => {
  store.currency = b.dataset.currency; applyChrome();
  if (state.view?.rerender) state.view.rerender();  // local re-render: no server call
}));
document.getElementById("my-plans-link").addEventListener("click", () => { toggleMenu(false); location.hash = "#/plans"; });
document.getElementById("code-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const input = document.getElementById("code-input");
  const code = input.value.trim().toUpperCase();
  const err = document.getElementById("code-error");
  if (!CODE_RE.test(code)) { err.textContent = t("badCode"); err.hidden = false; return; }
  err.hidden = true; input.value = ""; toggleMenu(false); location.hash = `#/plan/${code}`;
});
const help = document.getElementById("help");
document.getElementById("help-btn").addEventListener("click", () => help.showModal());
document.getElementById("help-close").addEventListener("click", () => help.close());

function helpHtml() {
  const a = STR[store.lang].agents;
  if (store.lang === "es") {
    return `<h2 id="help-title">Cómo funciona Pirca</h2>
      <ol><li>Respondes cinco grupos de preguntas sobre tu negocio.</li>
      <li>Cuatro agentes de IA usan herramientas con datos reales: alertas del ENFEN, la historia de inundaciones de Piura (1998, 2017 y 2023) y un catálogo de acciones con precios.</li>
      <li>Todos los números los calcula el código, no la IA. Un revisor automático comprueba el plan antes de mostrártelo.</li>
      <li>Recibes un plan con un código (PIU-…) que puedes abrir cuando quieras.</li></ol>
      <h3>Los cuatro agentes</h3>
      <ul>${Object.values(a).map(([n, d]) => `<li><b>${esc(n)}:</b> ${esc(d)}</li>`).join("")}</ul>
      <h3>Importante</h3>
      <p><b>Pirca no es un pronóstico oficial ni una agencia del Estado.</b> No da órdenes de evacuación. Sigue siempre los avisos del ENFEN, SENAMHI, INDECI y tu municipalidad.</p>
      <h3>Controles de seguridad</h3>
      <ul>
        <li><b>Documentos con trampas:</b> si un texto intenta darle órdenes a la IA, se ignora y se reporta.</li>
        <li><b>Números inventados:</b> el código revisa que cada número venga de un cálculo y cada fuente exista; si no, el plan se corrige.</li>
        <li><b>Solo lo que puedes pagar:</b> el plan nunca te recomienda gastar más dinero del que tienes.</li>
        <li><b>Límites de uso:</b> si la IA usa demasiado, el proceso se detiene de forma segura y te avisa.</li>
        <li><b>Sin órdenes de evacuación:</b> Pirca nunca te ordena evacuar; eso lo deciden INDECI y tu municipalidad.</li>
      </ul>
      <p class="muted small">Los costos y beneficios marcados con * son estimados, no medidos.</p>`;
  }
  return `<h2 id="help-title">How Pirca works</h2>
    <ol><li>You answer five short groups of questions about your shop.</li>
    <li>Four AI agents use tools with real data: ENFEN alerts, Piura's flood history (1998, 2017 and 2023), and a priced catalog of preparation actions.</li>
    <li>Code computes every number, not the AI. An automatic checker reviews the plan before you see it.</li>
    <li>You get a plan with a code (PIU-…) you can open any time.</li></ol>
    <h3>The four agents</h3>
    <ul>${Object.values(a).map(([n, d]) => `<li><b>${esc(n)}:</b> ${esc(d)}</li>`).join("")}</ul>
    <h3>Important</h3>
    <p><b>Pirca is not an official forecast or a government agency.</b> It never gives evacuation orders. Always follow ENFEN, SENAMHI, INDECI and your municipality.</p>
    <h3>Safety checks</h3>
    <ul>
      <li><b>Booby-trapped documents:</b> if any text tries to give the AI orders, it is ignored and reported.</li>
      <li><b>No invented numbers:</b> code checks that every number comes from a calculation and every source exists; if not, the plan is sent back.</li>
      <li><b>Only what you can afford:</b> the plan never recommends spending more money than you have.</li>
      <li><b>Usage limits:</b> if the AI uses too much, the run stops safely and tells you.</li>
      <li><b>No evacuation orders:</b> Pirca never orders you to evacuate; that is for INDECI and your municipality.</li>
    </ul>
    <p class="muted small">Costs and benefits marked with * are estimates, not measurements.</p>`;
}

// ------------------------------------------------------------------ router

window.addEventListener("hashchange", route);
async function route() {
  clearTimers();
  state.view = null;
  const hash = location.hash || "#/";
  try {
    await meta();
    const m = hash.match(/^#\/plan\/([A-Za-z0-9-]+)$/);
    if (hash === "#/new") renderForm();
    else if (hash === "#/plans") renderMyPlans();
    else if (m) await renderPlanPage(m[1].toUpperCase());
    else renderHome();
  } catch (e) {
    console.warn(e);
    app.innerHTML = `<div class="notice error glass-read" role="alert">${esc(t("networkError"))}</div>`;
  }
  window.scrollTo(0, 0);
}

// ------------------------------------------------------------------ El Niño theme helpers

const REDUCED_MOTION = window.matchMedia("(prefers-reduced-motion: reduce)");
const ENFEN_STATUS_EN = {
  "Alerta de El Niño Costero": "Coastal El Niño Alert", "Vigilancia de El Niño Costero": "Coastal El Niño Watch",
  "Alerta de La Niña Costera": "Coastal La Niña Alert", "Vigilancia de La Niña Costera": "Coastal La Niña Watch",
  "No Activo": "Not active",
};

function shortDate(iso) {
  if (!iso) return "";
  if (/^\d{4}$/.test(iso)) return iso;
  const d = new Date(`${iso}T00:00:00`);
  return Number.isNaN(d.getTime()) ? iso : d.toLocaleDateString(store.lang, { day: "numeric", month: "short", year: "numeric" });
}

// Current ENFEN status, read from data/enfen/index.json through /api/meta (never hard-coded).
function enfenChip() {
  const e = state.meta.enfen;
  if (!e) return "";
  const status = store.lang === "en" ? (ENFEN_STATUS_EN[e.status] || e.status) : e.status;
  return `<a class="enfen-chip" href="${esc(e.source_url)}" target="_blank" rel="noopener noreferrer">
    <span class="pulse-dot" aria-hidden="true"></span><span>ENFEN: <b>${esc(status)}</b></span>
    <span class="meta">${esc(t("communique"))} N° ${esc(e.number)} · ${esc(shortDate(e.date))}</span></a>`;
}

// Stylized eastern Pacific: longitude -95..-68, latitude 3..-20 projected onto a 400 x 300 box.
const px = (lon) => ((lon + 95) / 27) * 400;
const py = (lat) => ((3 - lat) / 23) * 300;
const COAST = [[-77.6, 3], [-78.9, 1.6], [-79.65, 0.97], [-80.9, -1.05], [-80.95, -2.2], [-80.2, -2.7], [-79.9, -3.0],
  [-80.45, -3.57], [-81.05, -4.1], [-81.27, -4.58], [-81.11, -5.09], [-80.85, -5.55], [-81.18, -5.79], [-80.0, -6.5],
  [-79.94, -6.84], [-79.57, -7.4], [-79.04, -8.11], [-78.6, -9.07], [-78.15, -10.07], [-77.61, -11.11], [-77.14, -12.05],
  [-76.22, -13.71], [-76.3, -13.85], [-75.15, -15.36], [-73.7, -16.2], [-72.7, -16.62], [-71.34, -17.64], [-70.32, -18.48],
  [-70.2, -20]];

function mapSvg() {
  const land = COAST.map(([lon, lat]) => `${px(lon).toFixed(1)},${py(lat).toFixed(1)}`).join(" ");
  const ocean = store.lang === "es" ? "Océano Pacífico" : "Pacific Ocean";
  return `<svg viewBox="0 0 400 300" role="img" aria-labelledby="map-title">
    <title id="map-title">${esc(t("mapTitle"))}</title>
    <defs>
      <radialGradient id="warm-g" cx="65%" cy="50%" r="60%">
        <stop offset="0%" stop-color="#FFB347" stop-opacity="0.7"/><stop offset="45%" stop-color="#F2785C" stop-opacity="0.45"/>
        <stop offset="100%" stop-color="#F2785C" stop-opacity="0"/></radialGradient>
      <linearGradient id="sea-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0E2A3D"/><stop offset="100%" stop-color="#0E3B4A"/></linearGradient>
    </defs>
    <rect width="400" height="300" fill="url(#sea-g)"/>
    <g class="warm-water"><ellipse cx="${px(-85.5)}" cy="${py(-5)}" rx="88" ry="58" fill="url(#warm-g)"/>
      <ellipse class="warm-core" cx="${px(-83)}" cy="${py(-5.2)}" rx="30" ry="20" fill="url(#warm-g)" opacity="0.6"/></g>
    <rect class="map-box" x="${px(-90)}" y="${py(0)}" width="${px(-80) - px(-90)}" height="${py(-10) - py(0)}"/>
    <text class="map-label" x="${px(-89.6)}" y="${py(0) + 14}">Niño 1+2</text>
    <polygon class="map-land" points="${land} 400,${py(-20)} 400,0 ${px(-77.6)},0"/>
    <text class="map-label" x="${px(-78.8)}" y="${py(-1.8)}">ECUADOR</text>
    <text class="map-label strong" x="${px(-76)}" y="${py(-9.5)}">${store.lang === "es" ? "PERÚ" : "PERU"}</text>
    <text class="map-label" x="${px(-93.5)}" y="${py(-15)}">${esc(ocean)}</text>
    <circle class="piura-dot" cx="${px(-80.63)}" cy="${py(-5.19)}" r="5"/>
    <text class="map-label strong" x="${px(-80.63) + 9}" y="${py(-5.19) + 4}">Piura</text>
  </svg>`;
}

function wavePath(amplitude, base) {
  // 8 periods across 2880 units; the SVG is 200% wide and slides by half for a seamless loop.
  let d = `M0 ${base}`;
  for (let i = 0; i < 8; i += 1) {
    const x = i * 360;
    d += ` C${x + 90} ${base - amplitude} ${x + 270} ${base + amplitude} ${x + 360} ${base}`;
  }
  return `${d} V80 H0 Z`;
}

function wavesSvg() {
  const layers = [["w3", 10, 40, "#2EC4B6"], ["w2", 8, 48, "#1E3A5F"], ["w1", 6, 56, "#2EC4B6"]];
  return `<div class="waves" aria-hidden="true">${layers.map(([cls, amp, base, color]) =>
    `<svg class="${cls}" viewBox="0 0 2880 80" preserveAspectRatio="none"><path d="${wavePath(amp, base)}" fill="${color}"/></svg>`).join("")}</div>`;
}

// ------------------------------------------------------------------ home

function renderHome() {
  const title = esc(t("heroTitle")).replace("El Niño costero", '<span class="warm-text">El Niño costero</span>');
  app.innerHTML = `
    <section class="hero glass">
      <div class="hero-grid">
        <div>
          ${enfenChip()}
          <h1>${title}</h1>
          <p>${esc(t("heroText"))}</p>
          <div class="btn-row">
            <a class="btn btn-primary" href="#/new">${esc(t("makePlan"))}</a>
            <a class="btn" href="#/plan/${esc(state.meta.example_code)}">${esc(t("openExample"))}</a>
          </div>
        </div>
        <figure class="map-figure">${mapSvg()}<figcaption>${esc(t("mapCaption"))}</figcaption></figure>
      </div>
      ${wavesSvg()}
    </section>
    <div class="facts-strip">
      ${[1, 2, 3].map((i) => `<div class="glass"><b>${esc(t("fact" + i))}</b><span class="muted small">${esc(t("fact" + i + "b"))}</span></div>`).join("")}
    </div>
    <section class="how glass" aria-labelledby="how-title">
      <h2 id="how-title">${esc(t("howTitle"))}</h2>
      <ol>${t("how").map((step, i) => `<li><span class="step">${i + 1}</span>${esc(step)}</li>`).join("")}</ol>
    </section>`;
}

// ------------------------------------------------------------------ form

function fieldHtml(f, value) {
  const id = `f-${f.name}`;
  const label = `<label for="${id}">${esc(L(f.label))}</label>`;
  const hint = `<span class="hint" id="${id}-hint">${esc(L(f.hint))}</span>`;
  const aria = `aria-describedby="${id}-hint"`;
  let control;
  if (f.type === "select") {
    const opts = L(f.options);
    control = `<select id="${id}" name="${f.name}" ${aria} required><option value="" disabled ${value == null ? "selected" : ""}>—</option>
      ${Object.entries(opts).map(([v, txt]) => `<option value="${v}" ${String(value) === v ? "selected" : ""}>${esc(txt)}</option>`).join("")}</select>`;
  } else if (f.type === "district") {
    const byProvince = {};
    state.meta.districts.forEach((d) => (byProvince[d.province] ??= []).push(d));
    control = `<select id="${id}" name="${f.name}" ${aria} required><option value="" disabled ${value ? "" : "selected"}>—</option>
      ${Object.entries(byProvince).map(([prov, ds]) => `<optgroup label="${esc(prov)}">${ds.map((d) =>
        `<option value="${esc(d.name)}" ${value === d.name ? "selected" : ""}>${esc(d.name)}${esc(L(LEVEL_NOTE)[d.hazard_level] || "")}</option>`).join("")}</optgroup>`).join("")}</select>`;
  } else if (f.type === "money") {
    control = `<div class="input-prefix"><span aria-hidden="true">S/</span><input id="${id}" name="${f.name}" type="number" inputmode="decimal" min="0" step="any" value="${value ?? ""}" ${aria} required></div>`;
  } else if (f.type === "percent") {
    const pct = value == null || value === "" ? "" : Math.round(value * 1000) / 10;
    control = `<input id="${id}" name="${f.name}" type="number" inputmode="decimal" min="0" max="100" step="any" value="${pct}" ${aria} required>`;
  } else if (f.type === "number") {
    control = `<input id="${id}" name="${f.name}" type="number" inputmode="numeric" min="${f.min}" step="${f.step}" value="${value ?? ""}" ${aria} required>`;
  } else {
    control = `<input id="${id}" name="${f.name}" type="text" ${f.list ? `list="${f.list}"` : ""} value="${esc(value ?? "")}" ${aria} required autocomplete="off">`;
  }
  return `<div class="field" data-field="${f.name}">${label}${control}${hint}</div>`;
}

function supplierRowHtml(s, i) {
  const pv = s.perishable === true ? "true" : s.perishable === false ? "false" : "";
  const opts = L(SUPPLIER_PERISHABLE);
  return `<div class="supplier-row" data-row="${i}">
    <div class="field"><label for="sp-${i}">${store.lang === "es" ? "Producto" : "Product"}</label>
      <input id="sp-${i}" name="product" value="${esc(s.product || "")}" placeholder="${store.lang === "es" ? "abarrotes, pan, bebidas…" : "groceries, bread, drinks…"}"></div>
    <div class="field"><label for="sc-${i}">${store.lang === "es" ? "Ciudad" : "City"}</label>
      <input id="sc-${i}" name="city" value="${esc(s.city || "")}" placeholder="Piura, Chiclayo…"></div>
    <div class="field"><label for="ss-${i}">${store.lang === "es" ? "¿Perecible?" : "Perishable?"}</label>
      <select id="ss-${i}" name="perishable">${Object.entries(opts).map(([v, txt]) => `<option value="${v}" ${pv === v ? "selected" : ""}>${esc(txt)}</option>`).join("")}</select></div>
    <button class="icon-btn" type="button" data-remove="${i}" aria-label="${esc(t("remove"))}">✕</button>
  </div>`;
}

function renderForm(draft = store.draft || {}) {
  if (typeof draft.perishables === "boolean") draft = { ...draft, perishables: draft.perishables ? "yes" : "no" };
  const suppliers = draft.suppliers?.length ? draft.suppliers : [{}];
  const have = new Set(draft.already_have || []);
  app.innerHTML = `
    <section class="panel glass">
      <h1 style="font-size:28px">${esc(t("formTitle"))}</h1>
      <p class="muted">${esc(t("formIntro"))}</p>
      <button class="btn" type="button" id="sample-btn">${esc(t("useSample"))}</button>
    </section>
    <div id="form-notice"></div>
    <form id="intake" novalidate>
      <datalist id="business-types">${["bodega", "ferretería", "botica", "librería", "restaurante", "minimarket", "panadería"].map((b) => `<option value="${b}">`).join("")}</datalist>
      ${GROUPS.map((g, gi) => `
        <fieldset class="form-group glass" style="margin-inline:0">
          <h2><span class="step">${gi + 1}</span>${esc(L(g.title))}</h2>
          <p>${esc(L(g.hint))}</p>
          ${g.fields.length ? `<div class="grid">${g.fields.map((f) => fieldHtml(f, draft[f.name])).join("")}</div>` : ""}
          ${g.id === "suppliers" ? `<div id="suppliers">${suppliers.map(supplierRowHtml).join("")}</div>
            <button class="btn" type="button" id="add-supplier" ${suppliers.length >= 3 ? "disabled" : ""}>${esc(t("addSupplier"))}</button>` : ""}
          ${g.id === "prep" ? `<h3 style="font-size:15px;margin-top:24px">${store.lang === "es" ? "¿Qué ya tienes? (marca lo que tengas)" : "What do you already have? (tick all that apply)"}</h3>
            <div class="checklist">${state.meta.actions.map((a) => `<label><input type="checkbox" name="already_have" value="${a.id}" ${have.has(a.id) ? "checked" : ""}>
              <span>${esc(store.lang === "es" ? a.name_es : a.name_en)}</span></label>`).join("")}</div>` : ""}
        </fieldset>`).join("")}
      <div class="form-actions">
        <span class="muted small">${store.lang === "es" ? "Montos en soles (S/)." : "Amounts in soles (S/)."}</span>
        <button class="btn btn-primary" type="submit" id="check-btn">${esc(t("checkAnswers"))}</button>
      </div>
    </form>`;

  const form = document.getElementById("intake");
  form.addEventListener("input", saveDraftFromForm);
  document.getElementById("sample-btn").addEventListener("click", async () => {
    const example = await api(`/api/plans/${state.meta.example_code}`);
    store.draft = example.result.form; renderForm(store.draft);
  });
  document.getElementById("add-supplier").addEventListener("click", () => {
    const d = collectDraft(); d.suppliers.push({}); store.draft = d; renderForm(d);
  });
  document.getElementById("suppliers").addEventListener("click", (e) => {
    const i = e.target.closest("[data-remove]")?.dataset.remove;
    if (i === undefined) return;
    const d = collectDraft(); d.suppliers.splice(Number(i), 1); store.draft = d; renderForm(d);
  });
  form.addEventListener("submit", (e) => { e.preventDefault(); checkAndRun(false); });
  state.view = { form: true };
}

function collectDraft() {
  const form = document.getElementById("intake");
  if (!form) return store.draft || {};
  const d = {};
  GROUPS.flatMap((g) => g.fields).forEach((f) => {
    const raw = form.elements[f.name]?.value ?? "";
    if (raw === "") { d[f.name] = null; return; }
    if (f.type === "money" || f.type === "number") d[f.name] = Number(raw);
    else if (f.type === "percent") d[f.name] = Number(raw) / 100;
    else if (f.name === "perishables") d[f.name] = raw === "yes" ? "yes" : "no";
    else d[f.name] = raw;
  });
  d.suppliers = [...form.querySelectorAll(".supplier-row")].map((row) => {
    const p = row.querySelector("[name=perishable]").value;
    return { product: row.querySelector("[name=product]").value.trim(), city: row.querySelector("[name=city]").value.trim(),
             perishable: p === "" ? null : p === "true" };
  });
  d.already_have = [...form.querySelectorAll("[name=already_have]:checked")].map((c) => c.value);
  return d;
}
function saveDraftFromForm() { if (document.getElementById("intake")) store.draft = collectDraft(); }

function toProfile(d) {
  const p = { ...d, perishables: d.perishables === "yes" || d.perishables === true,
              suppliers: (d.suppliers || []).filter((s) => s.product && s.city) };
  Object.keys(p).forEach((k) => { if (p[k] === null) delete p[k]; });
  return p;
}

function warningText(w) {
  if (store.lang !== "es") return w;
  for (const [re, fn] of WARNING_ES) { const m = w.match(re); if (m) return fn(m); }
  return w;
}

async function checkAndRun(confirmed) {
  const draft = collectDraft(); store.draft = draft;
  const profile = toProfile(draft);
  const notice = document.getElementById("form-notice");
  const btn = document.getElementById("check-btn");
  btn.disabled = true; btn.textContent = t("checking");
  document.querySelectorAll(".field.invalid").forEach((f) => f.classList.remove("invalid"));
  try {
    const v = await api("/api/validate", { method: "POST", body: JSON.stringify(profile) });
    if (!v.valid) {
      v.errors.forEach((e) => document.querySelector(`[data-field="${e.split(/[.:]/)[0]}"]`)?.classList.add("invalid"));
      notice.innerHTML = `<div class="notice error glass-read" role="alert"><b>${esc(t("errorsTitle"))}</b>
        <ul>${v.errors.map((e) => `<li>${esc(errorText(e))}</li>`).join("")}</ul></div>`;
      notice.scrollIntoView({ behavior: "smooth" });
      return;
    }
    if (v.warnings.length && !confirmed) {
      notice.innerHTML = `<div class="notice glass-read" role="alert"><b>${esc(t("warningsTitle"))}</b>
        <p class="muted small" style="margin:4px 0 0">${esc(t("warningsText"))}</p>
        <ul>${v.warnings.map((w) => `<li>${esc(warningText(w))}</li>`).join("")}</ul>
        <div class="btn-row"><button class="btn" type="button" id="fix-btn">${esc(t("fixAnswers"))}</button>
        <button class="btn btn-primary" type="button" id="confirm-btn">${esc(t("confirmRun"))}</button></div></div>`;
      notice.scrollIntoView({ behavior: "smooth" });
      document.getElementById("fix-btn").addEventListener("click", () => { notice.innerHTML = ""; document.getElementById("intake").elements[0]?.focus(); });
      document.getElementById("confirm-btn").addEventListener("click", () => checkAndRun(true));
      return;
    }
    btn.textContent = t("starting");
    const created = await api("/api/plans", { method: "POST", body: JSON.stringify({ profile, language: store.lang }) });
    store.plans = [{ code: created.code, label: `${profile.business_type} · ${profile.district}`, language: store.lang,
                     created_at: new Date().toISOString() }, ...store.plans.filter((p) => p.code !== created.code)];
    location.hash = `#/plan/${created.code}`;
  } catch (e) {
    console.warn(e);
    notice.innerHTML = `<div class="notice error glass-read" role="alert">${esc(t("networkError"))}</div>`;
  } finally {
    if (document.getElementById("check-btn")) { btn.disabled = false; btn.textContent = t("checkAnswers"); }
  }
}

function errorText(e) {
  const [field, ...rest] = e.split(":");
  const f = GROUPS.flatMap((g) => g.fields).find((x) => x.name === field.split(".")[0]);
  return f ? `${L(f.label)}: ${rest.join(":").trim()}` : e;
}

// ------------------------------------------------------------------ trace (live and replay)

const AGENTS = ["manager", "risk_analyst", "planner", "critic"];

function traceHtml(code, mode) {
  const a = STR[store.lang].agents;
  return `
    ${mode === "stopped" ? "" : `<div class="trace-head">
      <div><h1 style="font-size:24px">${esc(mode === "replay" ? t("replayTitle") : t("traceTitle"))}</h1>
        <span class="plan-code">${esc(code)}</span></div>
      <div class="btn-row" id="trace-controls"></div>
    </div>`}
    ${mode === "live" ? `<p class="muted">${esc(t("traceText"))}</p>` : ""}
    <div class="agents">${AGENTS.map((id) => `
      <div class="agent glass" id="agent-${id}">
        <h3>${esc(a[id][0])}</h3><div class="role">${esc(a[id][1])}</div>
        <div class="state" aria-live="polite">${esc(t("idle"))}</div>
        <div class="small muted" data-tools></div>
      </div>`).join("")}</div>
    <div class="counter glass">
      <div><span>${esc(t("inTok"))}</span><b id="c-in">0</b></div>
      <div><span>${esc(t("cachedTok"))}</span><b id="c-cached">0</b></div>
      <div><span>${esc(t("outTok"))}</span><b id="c-out">0</b></div>
      <div><span>${esc(t("cost"))}</span><b id="c-cost">$0.0000</b></div>
    </div>
    <ol class="timeline glass" id="timeline" aria-label="Trace"></ol>`;
}

function newTraceState() { return { stack: [], tools: Object.fromEntries(AGENTS.map((a) => [a, 0])), done: new Set() }; }

function describe(e) {
  const r = e.result || {};
  switch (e.type) {
    case "run_started": return [t("runStarted"), ""];
    case "agent_started": return [`▶ ${t("started")} (${e.run})`, ""];
    case "model_call": return [`model call · in ${num(e.call.input_tokens)} · cached ${num(e.call.cached_input_tokens)} · out ${num(e.call.output_tokens)}`, "muted"];
    case "tool_called": {
      const a = e.args || {};
      const arg = a.query ? `"${a.query}"` : a.scenario || (a.draft ? `draft, ${num(a.draft.length)} chars` : "")
        || (a.revision_notes?.length ? `${a.revision_notes.length} revision note(s)` : a.district || "");
      return [`→ ${e.tool}(${arg})`, "mono"];
    }
    case "tool_result": {
      const extra = r.error ? `error: ${r.error}` : "ok" in r ? `ok = ${r.ok}`
        : e.tool?.startsWith("run_") ? t("finished") : `${Object.keys(r.facts || {}).length} facts`;
      return [`← ${e.tool}: ${extra}`, r.error ? "limit" : "mono"];
    }
    case "agent_finished": return [`■ ${t("finished")}`, "ok"];
    case "limit_hit": return [`⛔ limit ${e.limit} (${e.action}): ${e.detail}`, "limit"];
    case "final_check": return [`verify_draft on final plan: ${e.ok ? "ok" : (e.issues || []).join(", ")}`, e.ok ? "ok" : "limit"];
    case "run_finished": return [`${t("runFinished")}: ${e.status}`, e.status?.startsWith("completed") ? "ok" : "limit"];
    default: return [e.type, ""];
  }
}

function applyEvent(ts, e) {
  if (e.type === "agent_started") ts.stack.push(e.agent);
  if (e.type === "agent_finished") { ts.stack = ts.stack.filter((a, i) => !(a === e.agent && i === ts.stack.lastIndexOf(e.agent))); ts.done.add(e.agent); }
  if (e.type === "tool_called" && ts.tools[e.agent] !== undefined) ts.tools[e.agent] += 1;
  if (e.type === "run_finished") ts.stack = [];
  const current = ts.stack[ts.stack.length - 1];
  AGENTS.forEach((id) => {
    const card = document.getElementById(`agent-${id}`);
    if (!card) return;
    const working = id === current;
    const waiting = !working && ts.stack.includes(id);
    card.classList.toggle("working", working);
    card.classList.toggle("done", !working && !waiting && ts.done.has(id));
    card.querySelector(".state").textContent = working ? t("working") : waiting ? t("waiting") : ts.done.has(id) ? t("done") : t("idle");
    card.querySelector("[data-tools]").textContent = `${ts.tools[id]} ${ts.tools[id] === 1 ? t("toolCall") : t("toolCalls")}`;
  });
  const tot = e.totals || {};
  const set = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
  set("c-in", num(tot.input_tokens)); set("c-cached", num(tot.cached_input_tokens)); set("c-out", num(tot.output_tokens));
  set("c-cost", `$${Number(tot.cost_usd || 0).toFixed(4)}`);
  const list = document.getElementById("timeline");
  if (!list) return;
  const [text, cls] = describe(e);
  const name = STR[store.lang].agents[e.agent]?.[0] || "Pirca";
  const li = document.createElement("li");
  li.innerHTML = `<span class="t">${Number(e.elapsed_s || 0).toFixed(1)}s</span><span class="who">${esc(name)}</span><span class="what ${cls}">${esc(text)}</span>`;
  list.appendChild(li);
  list.scrollTop = list.scrollHeight;
}

function startLive(code, initial) {
  app.innerHTML = traceHtml(code, "live");
  document.getElementById("trace-controls").innerHTML = `<span class="spinner" aria-hidden="true"></span>`;
  const ts = newTraceState();
  let last = 0;
  const take = (events) => events.forEach((e) => { applyEvent(ts, e); last = Math.max(last, e.seq); });
  take(initial.events || []);
  const poll = async () => {
    try {
      const s = await api(`/api/plans/${code}?after=${last}`);
      take(s.events || []);
      if (s.status !== "running") { markPlan(code, s.status); later(() => renderPlanPage(code), 800); return; }
    } catch (e) { console.warn(e); }
    later(poll, 1000);
  };
  later(poll, 1000);
}

function startReplay(code, data) {
  clearTimers();
  app.innerHTML = traceHtml(code, "replay");
  const events = data.events || [];
  let speed = 1;
  const controls = document.getElementById("trace-controls");
  controls.innerHTML = `<div class="segmented" role="group" aria-label="${esc(t("speed"))}" style="min-width:120px">
      <button type="button" data-speed="1" aria-pressed="true">1×</button><button type="button" data-speed="4" aria-pressed="false">4×</button></div>
    <button class="btn" type="button" id="skip-btn">${esc(t("skip"))}</button>`;
  const ts = newTraceState();
  let i = 0;
  const step = () => {
    if (i >= events.length) return;
    applyEvent(ts, events[i]);
    const next = events[i + 1];
    i += 1;
    if (next) later(step, Math.max(0, (next.elapsed_s - events[i - 1].elapsed_s) * 1000 / speed));
  };
  controls.querySelectorAll("[data-speed]").forEach((b) => b.addEventListener("click", () => {
    speed = Number(b.dataset.speed);
    controls.querySelectorAll("[data-speed]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    clearTimers(); later(step, 0);
  }));
  document.getElementById("skip-btn").addEventListener("click", () => { clearTimers(); renderPlanView(code, data); });
  later(step, 300);
}

// ------------------------------------------------------------------ plan view

// Citations stay as raw IDs in the saved plan, verify_draft and the trace; only the display turns
// them into numbered footnotes. fn = { order: [ids], details: {id: {...}} }.
function footnote(id, fn) {
  let n = fn.order.indexOf(id) + 1;
  if (!n) { fn.order.push(id); n = fn.order.length; }
  return `<button type="button" class="fn" data-id="${esc(id)}" aria-expanded="false" aria-label="${esc(t("source"))} ${n}">${n}</button>`;
}

function inline(text, fn) {
  let s = esc(text);
  s = s.replace(/\\\*/g, "&#42;");                                           // escaped asterisk (footnote line)
  s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  s = s.replace(/(^|\s)_([^_]+)_(?=\s|$|[.,;:])/g, "$1<em>$2</em>");
  s = s.replace(/\s*\[((?:HIST|CAT|ENFEN|BCRP)-[A-Z0-9-]+(?:,\s*(?:HIST|CAT|ENFEN|BCRP)-[A-Z0-9-]+)*)\]/g,
    (_, ids) => (fn ? ids.split(/,\s*/).map((id) => footnote(id, fn)).join("") : ""));
  return s;
}

// "What to do and when": group the bullets of section 2 into the four moments.
const PHASE_TESTS = [/^(ahora|now|antes|before|today|hoy)/i, /(durante|during)/i, /(despu[eé]s|after)/i, /(alerta|alert|aviso|warning)/i];
const PHASE_INDEX = [0, 2, 3, 1];
const PHASE_NAMES = { es: ["Ahora", "Ante una alerta del ENFEN", "Durante la inundación", "Después"],
                      en: ["Now", "On an ENFEN alert", "During flooding", "After"] };

function phaseOf(label) {
  for (let i = 0; i < PHASE_TESTS.length; i += 1) if (PHASE_TESTS[i].test(label.trim())) return PHASE_INDEX[i];
  return -1;
}

function renderSteps(items, lang, fn) {
  const phases = [0, 1, 2, 3].map(() => ({ label: null, parts: [] }));
  let current = 0;
  let labelled = 0;
  items.forEach((raw) => {
    const plain = raw.replace(/^\*\*(.+?)\*\*/, "$1");
    const m = plain.match(/^([^:]{2,60}):\s*([\s\S]*)$/);
    const phase = m ? phaseOf(m[1].replace(/\*/g, "")) : -1;
    if (phase >= 0) {
      current = phase; labelled += 1;
      phases[phase].label = phases[phase].label || m[1].replace(/\*/g, "").trim();
      phases[phase].parts.push(m[2]);
    } else {
      phases[current].parts.push(raw);
    }
  });
  if (!labelled) return `<ul>${items.map((i) => `<li>${inline(i, fn)}</li>`).join("")}</ul>`;
  return `<ol class="steps">${phases.map((p, i) => `<li>
      <div class="step-head"><span class="num">${i + 1}</span>${esc(p.label || PHASE_NAMES[lang][i])}</div>
      ${p.parts.length ? p.parts.map((x) => `<p>${inline(x, fn)}</p>`).join("") : '<p class="muted">—</p>'}
    </li>`).join("")}</ol>`;
}

function renderMarkdown(md, fn, lang) {
  const out = [];
  let list = false;
  let section = null;
  let stepItems = null;
  const close = () => { if (list) { out.push("</ul>"); list = false; } };
  const flushSteps = () => { if (stepItems) { out.push(renderSteps(stepItems, lang, fn)); stepItems = null; } };
  md.replace(/\r/g, "").split("\n").forEach((raw) => {
    const line = raw.trimEnd();
    if (/^#{1,6}\s/.test(line)) {
      close(); flushSteps();
      const heading = line.replace(/^#{1,6}\s+/, "");
      section = (heading.match(/^(\d+)[.)]/) || [])[1] || null;
      out.push(`<h3>${inline(heading, fn)}</h3>`);
      if (section === "2") stepItems = [];
      return;
    }
    if (!line.trim()) { close(); return; }
    const bullet = line.match(/^\s*[-+*]\s+(.*)$/);
    if (stepItems && bullet) { stepItems.push(bullet[1]); return; }
    if (stepItems) { flushSteps(); }
    if (/^>\s?/.test(line)) { close(); out.push(`<div class="notice warning-banner">${inline(line.replace(/^>\s?/, ""), fn)}</div>`); return; }
    if (bullet) {
      if (!list) { out.push("<ul>"); list = true; }
      out.push(`<li>${inline(bullet[1], fn)}</li>`); return;
    }
    close();
    if (/^\\\*/.test(line)) { out.push(`<p class="footnote">${inline(line, fn)}</p>`); return; }
    if (/^_.*_$/.test(line)) { out.push(`<div class="disclaimer">${inline(line, fn)}</div>`); return; }
    out.push(`<p>${inline(line, fn)}</p>`);
  });
  close(); flushSteps();
  return out.join("\n");
}

// ---- footnote popup (hover with a mouse, tap or click to pin)
const fnPop = document.createElement("div");
fnPop.className = "fn-pop";
fnPop.hidden = true;
fnPop.setAttribute("role", "tooltip");
document.body.appendChild(fnPop);
let fnPinned = null;

function sourceTitle(d) { return typeof d.title === "object" ? (d.title[store.lang] || d.title.en) : d.title; }

function showFootnote(btn) {
  const id = btn.dataset.id;
  const d = (state.view?.sourceDetails || {})[id];
  fnPop.innerHTML = d ? `<div class="t">${esc(sourceTitle(d))}</div>
      ${d.date ? `<div class="d">${esc(shortDate(d.date))}</div>` : ""}
      <q>${esc(store.lang === "es" ? d.fact_es : d.fact_en)}</q>
      ${d.url ? `<a href="${esc(d.url)}" target="_blank" rel="noopener noreferrer">${esc(t("viewSource"))} ↗</a>` : ""}`
    : `<div class="t">${esc(id)}</div>`;
  fnPop.hidden = false;
  const r = btn.getBoundingClientRect();
  const w = fnPop.offsetWidth, h = fnPop.offsetHeight;
  const left = Math.min(Math.max(12, r.left - 24), window.innerWidth - w - 12);
  const below = r.bottom + 8 + h < window.innerHeight;
  fnPop.style.left = `${left}px`;
  fnPop.style.top = `${below ? r.bottom + 8 : Math.max(12, r.top - h - 8)}px`;
  document.querySelectorAll(".fn[aria-expanded='true']").forEach((b) => b.setAttribute("aria-expanded", "false"));
  btn.setAttribute("aria-expanded", "true");
}
function hideFootnote() {
  fnPop.hidden = true; fnPinned = null;
  document.querySelectorAll(".fn[aria-expanded='true']").forEach((b) => b.setAttribute("aria-expanded", "false"));
}
document.addEventListener("click", (e) => {
  const btn = e.target.closest(".fn");
  if (btn) { e.preventDefault(); if (fnPinned === btn) hideFootnote(); else { showFootnote(btn); fnPinned = btn; } return; }
  if (!fnPop.contains(e.target)) hideFootnote();
});
document.addEventListener("pointerover", (e) => {
  const btn = e.target.closest?.(".fn");
  if (btn && e.pointerType === "mouse" && !fnPinned) showFootnote(btn);
});
document.addEventListener("pointerout", (e) => {
  if (e.target.closest?.(".fn") && e.pointerType === "mouse" && !fnPinned) hideFootnote();
});
document.addEventListener("keydown", (e) => { if (e.key === "Escape") hideFootnote(); });
window.addEventListener("scroll", () => { if (!fnPop.hidden) hideFootnote(); }, { passive: true });

// ---- gauge, badges, count-up
const GAUGE_FRACTION = { low: 0.2, medium: 0.5, high: 0.85 };
const ARC = Math.PI * 80;

function gaugeSvg(level) {
  const word = level ? t("risk" + level[0].toUpperCase() + level.slice(1)) : "—";
  return `<div class="gauge" role="img" aria-label="${esc(t("risk"))}: ${esc(word)}">
    <svg viewBox="0 0 200 112">
      <defs><linearGradient id="gauge-g" x1="0" x2="1" y1="0" y2="0"><stop offset="0%" stop-color="#FFB347"/><stop offset="100%" stop-color="#F2785C"/></linearGradient></defs>
      <path class="track" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke-width="14" stroke-linecap="round"/>
      <path class="fill" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="url(#gauge-g)" stroke-width="14" stroke-linecap="round"
            stroke-dasharray="${ARC.toFixed(1)}" stroke-dashoffset="${ARC.toFixed(1)}"/>
      <g class="needle" style="transform: rotate(-90deg)"><line x1="100" y1="100" x2="100" y2="34" stroke="#E8EEF5" stroke-width="3" stroke-linecap="round"/></g>
      <circle cx="100" cy="100" r="7" fill="#E8EEF5"/>
    </svg>
    <div class="level ${level ? "risk-" + esc(level) : ""}">${esc(word)}<span>${esc(t("risk"))}</span></div>
  </div>`;
}

function animateGauge(level) {
  const frac = GAUGE_FRACTION[level];
  if (frac === undefined) return;
  const fill = app.querySelector(".gauge .fill");
  const needle = app.querySelector(".gauge .needle");
  // A short timer (not requestAnimationFrame, which pauses in hidden tabs) so the gauge always reaches its level.
  later(() => {
    if (fill) fill.style.strokeDashoffset = (ARC * (1 - frac)).toFixed(1);
    if (needle) needle.style.transform = `rotate(${-90 + 180 * frac}deg)`;
  }, 60);
}

function countUp(animate) {
  app.querySelectorAll("[data-count]").forEach((el) => {
    const value = Number(el.dataset.count);
    if (!animate || REDUCED_MOTION.matches || document.hidden || !value) { el.textContent = money(value); return; }
    later(() => { el.textContent = money(value); }, 1000);  // guarantee the final amount even if frames are paused
    const start = performance.now();
    const step = (now) => {
      const p = Math.min(1, (now - start) / 900);
      el.textContent = money(value * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = money(value);
    };
    requestAnimationFrame(step);
  });
}

const NUMBER_ISSUES = ["raw_number", "unknown_fact_key", "invalid_placeholder", "unit_next_to_placeholder"];

function badgesFor(r) {
  const issues = r.verification?.issues || [];
  const has = (type) => issues.some((i) => i.type === type);
  const outputs = r.worker_outputs || {};
  const suspicious = [r.suspicious_content, outputs.analysis?.suspicious_content, outputs.draft?.suspicious_content,
                      outputs.critique?.suspicious_content].flat().filter(Boolean);
  const evacuation = issues.some((i) => i.type === "forbidden_content" && /evacuat/i.test(i.detail || ""));
  const budgetOk = r.affordability ? r.affordability.within_cash : !has("spending_exceeds_cash");
  return [
    { ok: !NUMBER_ISSUES.some(has), text: t("badgeNumbers") },
    { ok: !has("unknown_source_id"), text: t("badgeSources") },
    { ok: budgetOk, text: t("badgeBudget") },
    { ok: !evacuation, text: t("badgeEvacuation") },
    { ok: !suspicious.length, text: suspicious.length ? STR[store.lang].badgeSuspiciousFound(suspicious.length) : t("badgeSuspiciousNone") },
  ];
}

function sourcesListHtml(fn) {
  if (!fn.order.length) return "";
  return `<section class="sources glass" aria-labelledby="sources-title"><h4 id="sources-title">${esc(t("sourcesTitle"))}</h4><ol>
    ${fn.order.map((id) => {
      const d = fn.details[id];
      if (!d) return `<li>${esc(id)}</li>`;
      return `<li>${d.url ? `<a href="${esc(d.url)}" target="_blank" rel="noopener noreferrer">${esc(sourceTitle(d))}</a>` : esc(sourceTitle(d))}${d.date ? ` · ${esc(shortDate(d.date))}` : ""}</li>`;
    }).join("")}</ol></section>`;
}

function usageRow(label, u) {
  return `<tr><td>${esc(label)}</td><td>${num(u.model_calls)}</td><td>${num(u.input_tokens)}</td><td>${num(u.cached_input_tokens)}</td>
    <td>${num(u.output_tokens)}</td><td>$${Number(u.cost_usd || 0).toFixed(4)}</td></tr>`;
}

function renderPlanView(code, data) {
  clearTimers();
  hideFootnote();
  const r = data.result;
  const original = r.language || "es";
  const other = original === "es" ? "en" : "es";
  const view = state.view?.code === code ? state.view : { code, showing: original, counted: false };
  state.view = view;
  view.sourceDetails = r.source_details || {};
  view.rerender = () => renderPlanView(code, data);
  const showing = view.showing;
  const translation = showing === original ? null : r.translations?.[showing];
  const planText = translation ? translation.plan[store.currency] : r.plan[store.currency];
  const f = r.facts || {};
  const tr = r.translations || {};
  const toggleLabel = showing === "es" ? STR.en.viewIn : STR.es.viewIn;
  const fn = { order: [], details: view.sourceDetails };
  const body = renderMarkdown(planText, fn, showing);

  app.innerHTML = `
    <section class="plan-top glass">
      <div>
        <span class="muted small">${esc(t("planCode"))}</span><div class="plan-code">${esc(code)}</div>
        <div style="margin-top:12px">${enfenChip()}</div>
        <ul class="badges" aria-label="${esc(t("checksTitle"))}">${badgesFor(r).map((b) =>
          `<li class="${b.ok ? "" : "warn"}"><span class="icon" aria-hidden="true">${b.ok ? "✓" : "⚠"}</span>${esc(b.text)}</li>`).join("")}</ul>
      </div>
      ${gaugeSvg(r.risk_level)}
      <div class="btn-row">
        <button class="btn" type="button" id="translate-btn" lang="${showing === "es" ? "en" : "es"}">${esc(toggleLabel)}</button>
        <button class="btn" type="button" id="replay-btn">${esc(t("replay"))}</button>
      </div>
    </section>
    <div class="key-numbers">
      <div class="glass accent"><span>${esc(t("stockAtRisk"))}</span><b data-count="${Number(f.stock_at_risk || 0)}">${esc(money(0))}</b></div>
      <div class="glass accent"><span>${esc(t("fundGap"))}</span><b data-count="${Number(f.cash_gap || 0)}">${esc(money(0))}</b></div>
      <div class="glass"><span>${esc(t("purchases"))}</span><b data-count="${Number(f.total_cost || 0)}">${esc(money(0))}</b></div>
    </div>
    ${store.lang === "en" && showing === "es" && r.summary_en ? `<section class="summary glass" lang="en"><h4>${esc(t("summaryTitle"))}</h4><p style="margin:0">${esc(r.summary_en)}</p></section>` : ""}
    ${translation && !translation.verification?.ok ? `<div class="notice glass-read" role="note">${esc(t("translationWarn"))}</div>` : ""}
    <article class="plan-body glass-read" lang="${showing}">${body}</article>
    ${sourcesListHtml(fn)}
    <section class="usage glass" style="margin-top:16px">
      <h4 style="font-size:13px;text-transform:uppercase;letter-spacing:.06em">${esc(t("usageTitle"))}</h4>
      <table><thead><tr><th>${esc(t("row"))}</th><th>${esc(t("calls"))}</th><th>${esc(t("input"))}</th><th>${esc(t("cached"))}</th><th>${esc(t("output"))}</th><th>USD</th></tr></thead>
      <tbody>${r.usage ? usageRow(t("runRow"), r.usage) : ""}${Object.entries(tr).map(([lang, x]) => usageRow(`${t("trRow")} (${lang})`, x.usage)).join("")}</tbody></table>
      ${store.currency === "usd" ? `<p class="small" style="margin:8px 0 0">${esc(STR[store.lang].fxNote(state.meta.pen_per_usd, state.meta.fx_date))}</p>` : ""}
    </section>`;

  countUp(!view.counted);
  view.counted = true;
  animateGauge(r.risk_level);
  document.getElementById("replay-btn").addEventListener("click", () => startReplay(code, data));
  document.getElementById("translate-btn").addEventListener("click", async (e) => {
    const target = showing === original ? other : original;
    if (target !== original && !r.translations?.[target]) {
      e.target.disabled = true; e.target.textContent = STR[target === "en" ? "en" : "es"].viewing;
      try {
        const res = await api(`/api/plans/${code}/translate`, { method: "POST" });
        r.translations = { ...(r.translations || {}), [res.language]: res };
        // New citations may appear in the translation; refresh the source details.
        const fresh = await api(`/api/plans/${code}?after=999999`);
        r.source_details = fresh.result?.source_details || r.source_details;
      } catch (err) { console.warn(err); e.target.disabled = false; e.target.textContent = toggleLabel; return; }
    }
    view.showing = target;
    renderPlanView(code, data);
  });
}

function renderStopped(code, data) {
  const r = data.result || {};
  app.innerHTML = `<div class="notice error glass-read" role="alert"><b>${esc(data.status === "stopped" ? t("stoppedTitle") : t("errorTitle"))}</b>
    <p style="margin:8px 0 0">${esc(t("stoppedText"))}</p><p class="muted small" style="margin:8px 0 0">${esc(r.message || "")}</p></div>
    <div id="trace-slot"></div>`;
  const slot = document.getElementById("trace-slot");
  slot.innerHTML = traceHtml(code, "stopped");
  const ts = newTraceState();
  (data.events || []).forEach((e) => applyEvent(ts, e));
}

async function renderPlanPage(code) {
  if (!CODE_RE.test(code)) { app.innerHTML = `<div class="notice error glass-read">${esc(t("notFound"))}</div>`; return; }
  app.innerHTML = `<p class="muted"><span class="spinner"></span> ${esc(t("loading"))}</p>`;
  let data;
  try { data = await api(`/api/plans/${code}`); }
  catch (e) {
    if (e.status === 404) { markPlan(code, "missing"); app.innerHTML = `<div class="notice error glass-read">${esc(t("notFound"))} <span class="plan-code">${esc(code)}</span></div>`; return; }
    throw e;
  }
  markPlan(code, data.status);
  if (data.status === "running") startLive(code, data);
  else if (data.status === "done") renderPlanView(code, data);
  else renderStopped(code, data);
}

// ------------------------------------------------------------------ my plans

function markPlan(code, status) {
  const plans = store.plans;
  const p = plans.find((x) => x.code === code);
  if (p && p.status !== status) { p.status = status; store.plans = plans; }
}
const STATUS_ICON = { running: "⏳", done: "✅", stopped: "⛔", error: "⚠️", missing: "❓" };
const STATUS_KEY = { running: "statusRunning", done: "statusDone", stopped: "statusStopped", error: "statusError", missing: "statusMissing" };

function renderMyPlans() {
  const plans = store.plans;
  app.innerHTML = `<section class="panel glass-read"><h1 style="font-size:28px">${esc(t("myPlansTitle"))}</h1>
    <p class="muted small">${esc(t("myPlansNote"))}</p>
    ${plans.length ? `<ul class="plan-list">${plans.map((p) => `
      <li><span class="status" data-code="${esc(p.code)}" aria-label="${esc(t(STATUS_KEY[p.status] || "statusRunning"))}">${STATUS_ICON[p.status] || "⏳"}</span>
        <span class="label"><b>${esc(p.code)}</b><br><span class="muted small">${esc(p.label)} · ${esc(t("created"))} ${esc(new Date(p.created_at).toLocaleDateString(store.lang))}</span></span>
        <a class="btn" href="#/plan/${esc(p.code)}">${esc(t("open"))}</a></li>`).join("")}</ul>`
      : `<p>${esc(t("myPlansEmpty"))}</p><a class="btn btn-primary" href="#/new">${esc(t("makePlan"))}</a>`}
    </section>`;
  // Refresh each status from the server (a plan may have finished while the page was closed).
  plans.forEach(async (p) => {
    let status = "missing";
    try { status = (await api(`/api/plans/${p.code}?after=999999`)).status; } catch (e) { if (e.status !== 404) return; }
    markPlan(p.code, status);
    const el = app.querySelector(`.status[data-code="${p.code}"]`);
    if (el) { el.textContent = STATUS_ICON[status]; el.setAttribute("aria-label", t(STATUS_KEY[status])); }
  });
}

// ------------------------------------------------------------------ start

applyChrome();
route();
