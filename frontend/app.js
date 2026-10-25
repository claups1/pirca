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
    mapAria: "Live map of the four agents, the code checks and the plan", revisionLabel: "1 revision", gateTitle: "Code checks", sceneCaption: "Each agent adds stones to your pirca",
    check_draft: "Draft", check_plan: "Final plan", check_budget: "Budget", planNode: "Plan", team: "Team",
    howTitle: "How it works", how: ["Answer 5 short sections", "Four agents check the facts", "Get your plan"],
    communique: "Communiqué", mapTitle: "Map of the eastern Pacific and Peru's coast with Piura marked",
    mapCaption: "El Niño costero: unusually warm sea water off Peru brings heavy rain to Piura.",
    source: "Source", viewSource: "View source", sourceInEnglish: "(source in English)", sourceInSpanish: "(source in Spanish)", sourcesTitle: "Sources", checksTitle: "Safety checks",
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
    mapAria: "Mapa en vivo de los cuatro agentes, los controles en código y el plan", revisionLabel: "1 revisión", gateTitle: "Controles en código", sceneCaption: "Cada agente agrega piedras a tu pirca",
    check_draft: "Borrador", check_plan: "Plan final", check_budget: "Presupuesto", planNode: "Plan", team: "Equipo",
    howTitle: "Cómo funciona", how: ["Responde 5 secciones cortas", "Cuatro agentes revisan los datos", "Recibe tu plan"],
    communique: "Comunicado", mapTitle: "Mapa del Pacífico oriental y la costa del Perú con Piura marcada",
    mapCaption: "El Niño costero: el mar frente al Perú se calienta más de lo normal y trae lluvias fuertes a Piura.",
    source: "Fuente", viewSource: "Ver fuente", sourceInEnglish: "(fuente en inglés)", sourceInSpanish: "(fuente en español)", sourcesTitle: "Fuentes", checksTitle: "Controles de seguridad",
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
const state = { meta: null, timers: [], view: null, trace: null };
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
  store.lang = b.dataset.lang; applyChrome();
  if (state.view?.rerender) state.view.rerender(); else route();  // plans switch language locally
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
        <li><b>El nivel de riesgo coincide con el cálculo:</b> el plan dice el mismo nivel de riesgo de tu negocio que el indicador, no el de tu distrito; si no coincide, el plan se corrige.</li>
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
      <li><b>Risk level matches the calculation:</b> the plan states your shop's risk level exactly as the gauge shows it, not your district's; if not, the plan is sent back.</li>
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
    else await renderHome();
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

// ---- start screen: schematic map of the eastern Pacific and northern Peru, district dots, numbers, timeline.
// Everything shown comes from /api/home (data/districts.csv, historical_impacts.csv, enfen/index.json).

Object.assign(STR.es, {
  seaLegend: "Temperatura del mar: normal → más caliente", mapNote: "Mapa esquemático, posiciones aproximadas.",
  mapTitleNew: "Mapa esquemático del Pacífico oriental y el norte del Perú con los distritos de Piura",
  dotsLegend: "Riesgo de inundación del distrito", planFor: (d) => `Hacer mi plan para ${d}`, close: "Cerrar",
  floodRisk: "Riesgo de inundación", whyTitle: "Por qué importa", timelineTitle: "El Niño en Piura",
  alertActive: "alerta activa", tapDot: "Toca un punto para ver qué pasó en cada distrito.",
  impactLabels: { business_losses: "en pérdidas por el cierre de locales en Piura (2023)", transport_cost: "subió el costo de transportar productos básicos (2023)", dengue_cases: "casos de dengue en la región Piura (2023)" },
  millionWord: "millones", riverChira: "Río Chira", riverPiura: "Río Piura",
  timelineFacts: { river_flow: (v) => `El río Piura llegó a un caudal pico de ${v} m³/s.`, flooding: (v) => `El río Piura se desbordó e inundó la ciudad; caudal pico de ${v} m³/s.`,
                   people_affected: (v) => `${v} personas afectadas por las lluvias en la región.` },
});
Object.assign(STR.en, {
  seaLegend: "Sea temperature: normal → warmer", mapNote: "Schematic map, approximate positions.",
  mapTitleNew: "Schematic map of the eastern Pacific and northern Peru with Piura's districts",
  dotsLegend: "District flood risk", planFor: (d) => `Make my plan for ${d}`, close: "Close",
  floodRisk: "Flood risk", whyTitle: "Why it matters", timelineTitle: "El Niño in Piura",
  alertActive: "alert active", tapDot: "Tap a dot to see what happened in each district.",
  impactLabels: { business_losses: "lost from closed shops in Piura (2023)", transport_cost: "rise in the cost of transporting basic goods (2023)", dengue_cases: "dengue cases in Piura region (2023)" },
  millionWord: "million", riverChira: "Chira River", riverPiura: "Piura River",
  timelineFacts: { river_flow: (v) => `The Piura River reached a peak flow of ${v} m³/s.`, flooding: (v) => `The Piura River overflowed and flooded the city; peak flow ${v} m³/s.`,
                   people_affected: (v) => `${v} people affected by the rains in the region.` },
});

// ---- start-screen map: Piura region's real district boundaries (data/geo/piura_districts.geojson via /api/home),
// colored by flood risk or by dengue cases in 2023, with a zoom inset for Piura city and the warm sea as a coastal band.

Object.assign(STR.es, {
  mapRisk: "Riesgo de inundación", mapDengue: "Casos de dengue 2023", noDataLegend: "Sin datos en Pirca",
  noDataCard: "Pirca todavía no tiene datos de inundación de este distrito.", insetTitle: "Ciudad de Piura",
  boundaryNote: "Límites distritales: INEI, edición 2022 (GeoGPS Perú, vía pe-atlas).", dengueLine: (n) => `${n} casos`,
  mapTitleReal: "Mapa de los distritos de la región Piura", tapDistrict: "Toca un distrito para ver qué pasó allí.",
  casesWord: "casos", mapModeLabel: "Qué muestra el mapa", warmBand: "Franja cálida: mar más caliente frente a la costa.",
});
Object.assign(STR.en, {
  mapRisk: "Flood risk", mapDengue: "Dengue cases 2023", noDataLegend: "No data in Pirca",
  noDataCard: "Pirca has no flood data for this district yet.", insetTitle: "Piura city",
  boundaryNote: "District boundaries: INEI, 2022 edition (GeoGPS Perú, via pe-atlas).", dengueLine: (n) => `${n} cases`,
  mapTitleReal: "Map of the districts of Piura region", tapDistrict: "Tap a district to see what happened there.",
  casesWord: "cases", mapModeLabel: "What the map shows", warmBand: "Warm band: warmer sea along the coast.",
});

const PIURA_CITY = ["Piura", "Castilla", "Veintiséis de Octubre", "Catacaos", "Cura Mori", "La Arena", "La Unión", "El Tallán"];
const MAIN_LABELS = ["Sullana", "Paita", "Talara", "Chulucanas", "Tambogrande", "Sechura"];
const RISK_FILL = { high: "#F2785C", medium: "#F2B84B" };
const NO_DATA_FILL = "#4A535E";
const DENGUE_LIGHT = [253, 231, 204], DENGUE_DARK = [168, 45, 38];
const MAP_W = 560, SEA_DEG = 1.32;  // open sea west of the coast for the warm band and the inset

function mapFrame(features) {
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  features.forEach((f) => f.coordinates.forEach((p) => p.forEach((r) => r.forEach(([x, y]) => {
    minX = Math.min(minX, x); maxX = Math.max(maxX, x); minY = Math.min(minY, y); maxY = Math.max(maxY, y);
  }))));
  const pad = 0.05, lon0 = minX - SEA_DEG, lat0 = maxY + pad;
  const k = MAP_W / (maxX + pad - lon0);  // about 5°S, so one degree of longitude ≈ one of latitude
  return { k, H: Math.round((lat0 - (minY - pad)) * k), project: ([x, y]) => [(x - lon0) * k, (lat0 - y) * k] };
}

function shapePath(coords, project) {
  return coords.map((poly) => poly.map((r) => r.map((pt, i) => {
    const [x, y] = project(pt);
    return `${i ? "L" : "M"}${x.toFixed(1)} ${y.toFixed(1)}`;
  }).join("") + "Z").join("")).join("");
}

// Label point: area-weighted centroid of the district's largest polygon.
function shapeCentroid(coords, project) {
  let best = null, bestArea = 0;
  coords.forEach((poly) => {
    const r = poly[0].map(project);
    let a = 0, cx = 0, cy = 0;
    for (let i = 0, j = r.length - 1; i < r.length; j = i++) {
      const c = r[j][0] * r[i][1] - r[i][0] * r[j][1];
      a += c; cx += (r[j][0] + r[i][0]) * c; cy += (r[j][1] + r[i][1]) * c;
    }
    if (a && Math.abs(a / 2) > bestArea) { bestArea = Math.abs(a / 2); best = [cx / (3 * a), cy / (3 * a)]; }
  });
  return best || project(coords[0][0][0]);
}

// Coastline: the westernmost boundary point in each thin band of latitude, smoothed seaward.
function coastPoints(features, project) {
  const bins = new Map();
  features.forEach((f) => f.coordinates.forEach((p) => p[0].forEach(([x, y]) => {
    const b = Math.round(y / 0.025);
    if (!bins.has(b) || x < bins.get(b)[0]) bins.set(b, [x, y]);
  })));
  const pts = [...bins.values()].sort((a, b) => b[1] - a[1]);
  return pts.map((p, i) => [Math.min(p[0], pts[i - 1]?.[0] ?? Infinity, pts[i + 1]?.[0] ?? Infinity), p[1]]).map(project);
}

function titleCaseName(name) {
  const small = new Set(["de", "la", "el", "del", "los", "las", "y"]);
  return name.toLowerCase().split(" ").map((w, i) => (i && small.has(w) ? w : w.charAt(0).toUpperCase() + w.slice(1))).join(" ");
}

function districtShape(f, project, cls = "") {
  const label = f.district || titleCaseName(f.name);
  const data = f.district ? `data-district="${esc(f.district)}"` : `data-boundary="${esc(f.ubigeo)}"`;
  return `<path class="district-shape ${cls}" d="${shapePath(f.coordinates, project)}" ${data} tabindex="0" role="button"
    aria-label="${esc(label)}, ${esc(f.province)}"/>`;
}

function homeMapSvg(home) {
  const feats = home.map.features;
  const F = mapFrame(feats), P = F.project;
  const coast = coastPoints(feats, P);
  const line = coast.map(([x, y], i) => `${i ? "L" : "M"}${x.toFixed(1)} ${y.toFixed(1)}`).join("");
  const [x0] = coast[0], [x1] = coast[coast.length - 1];
  const sea = `${line}L${x1.toFixed(1)} ${F.H}L0 ${F.H}L0 0L${x0.toFixed(1)} 0Z`;

  // Inset: the Piura city districts, zoomed into a box over the sea.
  const city = feats.filter((f) => PIURA_CITY.includes(f.district));
  let a = Infinity, b = -Infinity, c = Infinity, d = -Infinity;
  city.forEach((f) => f.coordinates.forEach((p) => p[0].forEach(([x, y]) => { a = Math.min(a, x); b = Math.max(b, x); c = Math.min(c, y); d = Math.max(d, y); })));
  const box = { x: 8, w: Math.min(200, coast.reduce((m, p) => Math.min(m, p[0]), Infinity) - 18) };
  box.h = Math.min(F.H - 120, box.w * 1.35); box.y = F.H - box.h - 8;
  const ik = Math.min((box.w - 16) / (b - a), (box.h - 34) / (d - c));
  const IP = ([x, y]) => [box.x + 8 + (x - a) * ik + ((box.w - 16) - (b - a) * ik) / 2, box.y + 26 + (d - y) * ik + ((box.h - 34) - (d - c) * ik) / 2];
  const [lx0, ly0] = P([a, d]), [lx1, ly1] = P([b, c]);
  const labels = (list, project, cls) => list.map((f) => {
    const [x, y] = shapeCentroid(f.coordinates, project);
    const words = f.district.split(" ");
    const lines = f.district.length > 12 && words.length > 1 ? [words[0], words.slice(1).join(" ")] : [f.district];
    return `<text class="map-label strong ${cls}" x="${x.toFixed(1)}" y="${(y + 3 - (lines.length - 1) * 5).toFixed(1)}" text-anchor="middle">${
      lines.map((l, i) => `<tspan x="${x.toFixed(1)}" dy="${i ? "1.1em" : 0}">${esc(l)}</tspan>`).join("")}</text>`;
  }).join("");
  const ocean = store.lang === "es" ? "Océano Pacífico" : "Pacific Ocean";
  return `<svg viewBox="0 0 ${MAP_W} ${F.H}" role="img" aria-labelledby="map-title" class="real-map">
    <title id="map-title">${esc(t("mapTitleReal"))}</title>
    <defs>
      <linearGradient id="sea-g2" x1="0" x2="1"><stop offset="0%" stop-color="#123A5A"/><stop offset="100%" stop-color="#1D5A72"/></linearGradient>
      <linearGradient id="legend-g" x1="0" x2="1"><stop offset="0%" stop-color="#2A6F97"/><stop offset="55%" stop-color="#FFB347"/><stop offset="100%" stop-color="#F2785C"/></linearGradient>
      <clipPath id="sea-clip"><path d="${sea}"/></clipPath>
      <filter id="band-blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7"/></filter>
      <clipPath id="inset-clip"><rect x="${box.x}" y="${box.y}" width="${box.w}" height="${box.h}" rx="8"/></clipPath>
    </defs>
    <rect width="${MAP_W}" height="${F.H}" class="other-land"/>
    <path d="${sea}" fill="url(#sea-g2)"/>
    <g clip-path="url(#sea-clip)" class="coast-band-group"><g filter="url(#band-blur)">
      <path d="${line}" class="coast-band outer"/><path d="${line}" class="coast-band inner"/>
    </g></g>
    <text class="map-label sea-label" x="14" y="${Math.round(box.y - 14)}">${esc(ocean)}</text>
    <g class="sea-legend" transform="translate(12 16)"><rect x="0" y="0" width="140" height="8" rx="4" fill="url(#legend-g)"/>
      <text class="map-label" x="0" y="22">${esc(t("seaLegend"))}</text></g>
    <g class="main-shapes">${feats.map((f) => districtShape(f, P)).join("")}</g>
    ${labels(feats.filter((f) => MAIN_LABELS.includes(f.district)), P, "main-label")}
    <rect class="locator" x="${lx0.toFixed(1)}" y="${ly0.toFixed(1)}" width="${(lx1 - lx0).toFixed(1)}" height="${(ly1 - ly0).toFixed(1)}"/>
    <line class="locator-line" x1="${lx0.toFixed(1)}" y1="${ly1.toFixed(1)}" x2="${box.x + box.w}" y2="${box.y}"/>
    <g class="inset">
      <rect class="inset-frame" x="${box.x}" y="${box.y}" width="${box.w}" height="${box.h}" rx="8"/>
      <g clip-path="url(#inset-clip)">${feats.map((f) => districtShape(f, IP, PIURA_CITY.includes(f.district) ? "in-city" : "context")).join("")}
        ${labels(city, IP, "inset-label")}</g>
      <text class="map-label strong inset-title" x="${box.x + 10}" y="${box.y + 16}">${esc(t("insetTitle"))}</text>
    </g>
  </svg>`;
}

function separateLabels(selector) {
  const els = [...app.querySelectorAll(selector)];
  for (let pass = 0; pass < 12; pass += 1) {
    let moved = false;
    for (let i = 0; i < els.length; i += 1) {
      for (let j = i + 1; j < els.length; j += 1) {
        let a, b;
        try { a = els[i].getBBox(); b = els[j].getBBox(); } catch { return; }
        const overlapX = Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x);
        const overlapY = Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y);
        if (overlapX > 1 && overlapY > 0) {
          const lower = a.y > b.y ? els[i] : els[j], dy = (overlapY / 2) + 1;
          [lower, lower === els[i] ? els[j] : els[i]].forEach((el, k) => {
            const shift = k ? -dy : dy;
            el.setAttribute("y", (Number(el.getAttribute("y")) + shift).toFixed(1));
          });
          moved = true;
        }
      }
    }
    if (!moved) break;
  }
}

function mapLegendHtml(home, mode) {
  if (mode === "risk") {
    return `<span class="lg"><span class="sw" style="background:${RISK_FILL.high}"></span>${esc(t("riskHigh"))}</span>
      <span class="lg"><span class="sw" style="background:${RISK_FILL.medium}"></span>${esc(t("riskMedium"))}</span>
      <span class="lg"><span class="sw" style="background:${NO_DATA_FILL}"></span>${esc(t("noDataLegend"))}</span>`;
  }
  const max = Math.max(...Object.values(home.dengue).map((v) => Number(v.value)));
  return `<span class="lg dengue-scale"><span>0</span><span class="ramp" style="background:linear-gradient(90deg, rgb(${DENGUE_LIGHT}), rgb(${DENGUE_DARK}))"></span>
      <span>${esc(num(max))} ${esc(t("casesWord"))}</span></span>
    <span class="lg"><span class="sw" style="background:${NO_DATA_FILL}"></span>${esc(t("noDataLegend"))}</span>`;
}

function dengueFill(value, max) {
  const s = Math.sqrt(value / max);  // square root so smaller districts still show a difference
  return `rgb(${DENGUE_LIGHT.map((v, i) => Math.round(v + (DENGUE_DARK[i] - v) * s)).join(",")})`;
}

function applyMapMode(home, mode) {
  state.homeMapMode = mode;
  const hazard = Object.fromEntries(home.districts.map((d) => [d.name, d.hazard_level]));
  const max = Math.max(...Object.values(home.dengue).map((v) => Number(v.value)));
  app.querySelectorAll(".home-map .district-shape").forEach((p) => {
    const name = p.dataset.district;
    let fill = NO_DATA_FILL;
    if (name && mode === "risk" && RISK_FILL[hazard[name]]) fill = RISK_FILL[hazard[name]];
    if (name && mode === "dengue" && home.dengue[name]) fill = dengueFill(Number(home.dengue[name].value), max);
    p.style.fill = fill;
  });
  app.querySelectorAll("[data-map-mode]").forEach((b) => b.setAttribute("aria-checked", String(b.dataset.mapMode === mode)));
  const legend = document.getElementById("map-legend");
  if (legend) legend.innerHTML = mapLegendHtml(home, mode);
}

function noDataCardHtml(f) {
  return `<div class="dc-head"><div><b>${esc(titleCaseName(f.name))}</b><span class="muted small"> · ${esc(f.province)}</span></div>
      <button type="button" class="icon-btn dc-close" aria-label="${esc(t("close"))}">✕</button></div>
    <p class="dc-none">${esc(t("noDataCard"))}</p>`;
}

function shortFact(text, max = 150) {
  const s = String(text || "").replace(/\s+/g, " ").trim();
  if (s.length <= max) return s;
  const cut = s.slice(0, max);
  return `${cut.slice(0, cut.lastIndexOf(" ") > 80 ? cut.lastIndexOf(" ") : max)}…`;
}

// A short label from the data's "topic" column, so a quote read on its own still says what it is about.
const TOPIC_LABELS = {
  es: { flooding: "Inundación", river_flow: "Caudal del río", rainfall: "Lluvias", housing: "Viviendas", people_affected: "Personas afectadas",
        roads_bridges: "Carreteras y puentes", dengue: "Dengue", business_losses: "Comercio", economic_losses: "Pérdidas", closure_duration: "Cierres" },
  en: { flooding: "Flooding", river_flow: "River flow", rainfall: "Rain", housing: "Housing", people_affected: "People affected",
        roads_bridges: "Roads and bridges", dengue: "Dengue", business_losses: "Business", economic_losses: "Losses", closure_duration: "Closures" },
};

// Some Spanish source quotes are table rows ("DIST. CATACAOS 590 32090"). Those are shown as a short Spanish
// sentence built from the same row's value and unit (the footnote still opens the source).
const MONTHS_ES = { January: "enero", February: "febrero", March: "marzo", April: "abril", May: "mayo" };
function readableQuote(q) {
  return Boolean(q) && !/^(DIST\.|PROV\.|Tabla)/i.test(q.trim()) && (q.match(/\b[a-záéíóúñ]{4,}\b/g) || []).length >= 4;
}
function spanishFromRow(f, det) {
  const v = num(Number(String(f.value).replace(/,/g, "")));
  const month = MONTHS_ES[(det.fact_en || "").match(/January|February|March|April|May/)?.[0] || (f.unit.match(/\((\w+)\)/) || [])[1]];
  if (f.topic === "people_affected" && /^Damnificados/i.test(det.fact_en || "")) {
    const afectados = (det.fact_en.match(/;\s*([\d,]+) afectados/) || [])[1];
    return afectados ? `${v} damnificados y ${afectados} afectados por las lluvias.` : `${v} damnificados por las lluvias.`;
  }
  if (f.topic === "housing" && f.unit === "persons") return `${v} personas en viviendas damnificadas o afectadas.`;
  if (f.topic === "rainfall" && /above normal/.test(f.unit)) return `${month ? `En ${month}, ` : ""}${v}% por encima de lo normal.`;
  if (f.topic === "rainfall" && /^mm/.test(f.unit)) return `${month ? `En ${month}, ` : ""}${v} mm de lluvia.`;
  if (f.topic === "river_flow" && f.unit === "m3/s") {
    const river = ((det.fact_en || "").match(/R[íi]o (Piura|Chira)/) || [])[1];
    return `El río${river ? ` ${river}` : ""} llegó a ${v} m³/s.`;
  }
  return null;
}
function factText(f, det) {
  if (store.lang === "en") return det.fact_en;
  return readableQuote(det.fact_es) ? det.fact_es : (spanishFromRow(f, det) || det.fact_es);
}

function districtCardHtml(d, home, fn) {
  const facts = d.facts.map((f) => {
    const det = home.source_details[f.id] || {};
    const topic = TOPIC_LABELS[store.lang][f.topic];
    return `<li><b>${esc(f.event)}</b> ${topic ? `<span class="dc-topic">${esc(topic)}:</span> ` : ""}${esc(shortFact(factText(f, det)))}${footnote(f.id, fn)}</li>`;
  }).join("");
  return `<div class="dc-head"><div><b>${esc(d.name)}</b><span class="muted small"> · ${esc(d.province)}</span></div>
      <button type="button" class="icon-btn dc-close" aria-label="${esc(t("close"))}">✕</button></div>
    <div class="dc-risk ${esc(d.hazard_level)}">${esc(t("floodRisk"))}: <b>${esc(t("risk" + d.hazard_level[0].toUpperCase() + d.hazard_level.slice(1)).toLowerCase())}</b></div>
    ${facts ? `<ul class="dc-facts">${facts}</ul>` : ""}
    ${home.dengue?.[d.name] ? `<p class="dc-dengue"><b>${esc(t("mapDengue"))}:</b> ${esc(STR[store.lang].dengueLine(num(Number(home.dengue[d.name].value))))}${footnote(home.dengue[d.name].id, fn)}</p>` : ""}
    <button type="button" class="btn btn-primary dc-plan" data-plan-for="${esc(d.name)}">${esc(STR[store.lang].planFor(d.name))}</button>`;
}

// Numbers in "Why it matters": parsed from the CSV value text ("12-18", "13", "79643").
function impactParts(key, row) {
  const nums = String(row.value).split("-").map(Number);
  const fx = state.meta.pen_per_usd;
  if (key === "business_losses") {
    const usd = store.currency === "usd";
    const vals = nums.map((n) => (usd ? n / fx : n));
    return { targets: vals, format: (v) => `${usd ? "US$ " : "S/ "}${v.map((n) => (usd ? n.toFixed(1) : Math.round(n))).join("–")} ${t("millionWord")}` };
  }
  if (row.unit === "%") return { targets: nums, format: (v) => `+${Math.round(v[0])}%` };
  return { targets: nums, format: (v) => num(Math.round(v[0])) };
}

function countUpImpacts() {
  const els = [...app.querySelectorAll("[data-impact]")];
  const run = (el) => {
    const { targets, format } = el._impact;
    if (REDUCED_MOTION.matches || document.hidden) { el.textContent = format(targets); return; }
    const start = performance.now();
    const step = (now) => {
      const p = Math.min(1, (now - start) / 1100), e = 1 - Math.pow(1 - p, 3);
      el.textContent = format(targets.map((x) => x * e));
      if (p < 1) requestAnimationFrame(step); else el.textContent = format(targets);
    };
    requestAnimationFrame(step);
    setTimeout(() => { el.textContent = format(targets); }, 1300);  // final value even if frames pause
  };
  if (!("IntersectionObserver" in window)) { els.forEach(run); return; }
  const io = new IntersectionObserver((entries) => entries.forEach((en) => {
    if (en.isIntersecting) { run(en.target); io.unobserve(en.target); }
  }), { threshold: 0.4 });
  els.forEach((el) => io.observe(el));
}

function timelineHtml(home, fn) {
  const S = STR[store.lang];
  const past = home.timeline.map((r) => {
    const make = S.timelineFacts[r.topic];
    const text = make ? make(num(Number(r.value))) : shortFact(home.source_details[r.id]?.[store.lang === "es" ? "fact_es" : "fact_en"]);
    return `<li><span class="tl-dot" aria-hidden="true"></span><b>${esc(r.event)}</b><p>${esc(text)}${footnote(r.id, fn)}</p></li>`;
  }).join("");
  const e = home.enfen;
  const status = store.lang === "en" ? (ENFEN_STATUS_EN[e.status] || e.status) : e.status;
  return `${past}<li class="tl-now"><span class="pulse-dot tl-pulse" aria-hidden="true"></span><b>${esc(e.date.slice(0, 4))}: ${esc(t("alertActive"))}</b>
    <p>${esc(status)} · ${esc(t("communique"))} N° ${esc(e.number)}${footnote(e.id, fn)}</p></li>`;
}

async function homeData() { return state.home ??= await api("/api/home"); }

async function renderHome() {
  const home = await homeData();
  const fn = { order: [], details: home.source_details };
  state.view = { sourceDetails: home.source_details, rerender: () => renderHome() };
  const title = esc(t("heroTitle")).replace("El Niño costero", '<span class="warm-text">El Niño costero</span>');
  const accents = ["accent-coral", "accent-teal", "accent-sand"];
  app.innerHTML = `
    <section class="hero glass">
      <div class="hero-grid hero-text">
        <div>
          ${enfenChip()}
          <h1>${title}</h1>
          <p>${esc(t("heroText"))}</p>
          <div class="btn-row">
            <a class="btn btn-primary" href="#/new">${esc(t("makePlan"))}</a>
            <a class="btn" href="#/plan/${esc(state.meta.example_code)}">${esc(t("openExample"))}</a>
          </div>
        </div>
      </div>
      ${wavesSvg()}
    </section>
    <section class="map-section glass" aria-labelledby="map-heading">
      <h2 id="map-heading">${esc(t("mapTitleReal"))}</h2>
        <figure class="map-figure home-map">
          <div class="map-toggle" role="radiogroup" aria-label="${esc(t("mapModeLabel"))}">
            <button type="button" role="radio" data-map-mode="risk" aria-checked="true">${esc(t("mapRisk"))}</button>
            <button type="button" role="radio" data-map-mode="dengue" aria-checked="false">${esc(t("mapDengue"))}</button>
          </div>
          ${homeMapSvg(home)}
          <div class="district-card glass-read" id="district-card" role="dialog" aria-live="polite" hidden></div>
          <figcaption>
            <span class="map-legend" id="map-legend"></span>
            <span>${esc(t("tapDistrict"))}</span>
            <span class="muted">${esc(t("warmBand"))} ${esc(t("boundaryNote"))}</span>
          </figcaption>
        </figure>
    </section>
    <div class="home-land">
      <div class="facts-strip">
        ${[1, 2, 3].map((i) => `<div class="glass ${accents[i - 1]}"><b>${esc(t("fact" + i))}</b><span class="muted small">${esc(t("fact" + i + "b"))}</span></div>`).join("")}
      </div>
      <section class="why-band" aria-labelledby="why-title">
        <h2 id="why-title">${esc(t("whyTitle"))}</h2>
        <div class="why-grid">${Object.entries(home.impacts).map(([key, row]) =>
          `<div class="why-item"><b class="why-num" data-impact="${esc(key)}">—</b><span>${esc(STR[store.lang].impactLabels[key])}${footnote(row.id, fn)}</span></div>`).join("")}</div>
      </section>
      <section class="timeline-band glass" aria-labelledby="tl-title">
        <h2 id="tl-title">${esc(t("timelineTitle"))}</h2>
        <ol class="nino-timeline">${timelineHtml(home, fn)}</ol>
      </section>
      <section class="how glass" aria-labelledby="how-title">
        <h2 id="how-title">${esc(t("howTitle"))}</h2>
        <ol>${t("how").map((step, i) => `<li><span class="step">${i + 1}</span>${esc(step)}</li>`).join("")}</ol>
      </section>
    </div>`;
  app.querySelectorAll("[data-impact]").forEach((el) => {
    el._impact = impactParts(el.dataset.impact, home.impacts[el.dataset.impact]);
    el.textContent = el._impact.format(el._impact.targets.map(() => 0));
  });
  countUpImpacts();
  applyMapMode(home, state.homeMapMode || "risk");
  separateLabels(".inset-label");
  wireDistrictCards(home, fn);
}

function wireDistrictCards(home, fn) {
  const figure = app.querySelector(".home-map");
  const card = document.getElementById("district-card");
  if (!figure || !card) return;
  let pinned = null, closeTimer = null;
  const keyOf = (el) => el.dataset.district || el.dataset.boundary;
  const mark = (el) => {
    app.querySelectorAll(".district-shape.active").forEach((x) => x.classList.remove("active"));
    if (el) app.querySelectorAll(".district-shape").forEach((x) => x.classList.toggle("active", keyOf(x) === keyOf(el)));
  };
  const open = (el, pin) => {
    clearTimeout(closeTimer);
    const d = el.dataset.district && home.districts.find((x) => x.name === el.dataset.district);
    const f = !d && home.map.features.find((x) => x.ubigeo === el.dataset.boundary);
    if (!d && !f) return;
    card.innerHTML = d ? districtCardHtml(d, home, fn) : noDataCardHtml(f);
    card.hidden = false;
    mark(el);
    const fr = figure.getBoundingClientRect(), r = el.getBoundingClientRect();
    const w = card.offsetWidth, h = card.offsetHeight;
    let left = r.left - fr.left + r.width / 2 - w / 2;
    left = Math.max(0, Math.min(fr.width - w, left));
    let top = r.bottom - fr.top + 8;
    if (top + h > fr.height && r.top - fr.top - h - 8 >= 0) top = r.top - fr.top - h - 8;
    card.style.left = `${left}px`; card.style.top = `${Math.max(0, top)}px`;
    if (pin) pinned = el;
  };
  const close = () => { card.hidden = true; pinned = null; mark(null); };
  figure.addEventListener("pointerover", (e) => {
    const el = e.target.closest?.(".district-shape");
    if (el && e.pointerType === "mouse" && !pinned) open(el, false);
    if (e.target.closest?.("#district-card")) clearTimeout(closeTimer);
  });
  figure.addEventListener("pointerout", (e) => {
    if (e.pointerType !== "mouse" || pinned) return;
    if (e.target.closest?.(".district-shape") || e.target.closest?.("#district-card")) closeTimer = setTimeout(close, 300);
  });
  figure.addEventListener("click", (e) => {
    const mode = e.target.closest("[data-map-mode]");
    if (mode) { applyMapMode(home, mode.dataset.mapMode); return; }
    const el = e.target.closest(".district-shape");
    if (el) { if (pinned && keyOf(pinned) === keyOf(el)) close(); else open(el, true); return; }
    if (e.target.closest(".dc-close")) { close(); return; }
    const plan = e.target.closest("[data-plan-for]");
    if (plan) {
      store.draft = { ...draftNow(), district: plan.dataset.planFor };  // the wizard opens with this district selected
      wiz.step = 0;
      location.hash = "#/new";
    }
  });
  figure.addEventListener("keydown", (e) => {
    const el = e.target.closest?.(".district-shape");
    if (el && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); open(el, true); card.querySelector(".dc-plan, .dc-close")?.focus(); }
    if (e.key === "Escape") close();
  });
  state.homeAbort?.abort();  // one page-wide listener, replaced on each re-render
  state.homeAbort = new AbortController();
  document.addEventListener("click", (e) => {
    if (!pinned || card.hidden) return;
    if (card.contains(e.target) || e.target.closest(".district-shape") || fnPop.contains(e.target) || e.target.closest(".fn")) return;
    close();
  }, { signal: state.homeAbort.signal });
}

// ------------------------------------------------------------------ form

// ---- intake wizard: one group per screen, big choices, sliders, "why we ask", live risk preview (0 tokens)

Object.assign(STR.es, {
  stepOf: (i, n) => `Paso ${i} de ${n}`, back: "← Atrás", next: "Siguiente →", reviewTitle: "Revisa tus respuestas",
  reviewIntro: "Revisa que todo esté bien. Puedes cambiar cualquier grupo antes de hacer tu plan.",
  reviewStep: "Revisión final", edit: "Editar", makeMyPlan: "Hacer mi plan", whyAsk: "¿Por qué preguntamos esto?",
  otherType: "Otro", otherPlaceholder: "Escribe tu tipo de negocio", searchDistrict: "Buscar distrito…",
  noMatch: "Ningún distrito coincide.", previewTitle: "Tu riesgo hasta ahora",
  previewWaiting: "Responde las preguntas sobre tu local para ver tu riesgo.",
  previewDistrict: (lvl) => `Riesgo de inundación del distrito: ${lvl}`, previewStock: (m) => `Mercadería a menos de 1 m: ${m}`,
  previewFree: "Calculado con código, sin IA: 0 tokens.", missingAnswers: "Falta responder:", stepCheck: "Revisa esto:",
  notAnswered: "Sin responder", perishableAuto: "No sé (Pirca lo revisa)", levelUnverified: "sin verificar", wallLabel: "Tu pirca crece con cada paso",
  daysUnit: "días", peopleUnit: "personas", alreadyHave: "¿Qué ya tienes? (toca lo que tengas)", noneSelected: "Nada marcado",
});
Object.assign(STR.en, {
  stepOf: (i, n) => `Step ${i} of ${n}`, back: "← Back", next: "Next →", reviewTitle: "Review your answers",
  reviewIntro: "Check that everything is right. You can change any group before making your plan.",
  reviewStep: "Final review", edit: "Edit", makeMyPlan: "Make my plan", whyAsk: "Why we ask",
  otherType: "Other", otherPlaceholder: "Type your kind of business", searchDistrict: "Search district…",
  noMatch: "No district matches.", previewTitle: "Your risk so far",
  previewWaiting: "Answer the questions about your shop to see your risk.",
  previewDistrict: (lvl) => `District flood risk: ${lvl}`, previewStock: (m) => `Stock less than 1 m above the floor: ${m}`,
  previewFree: "Calculated with code, no AI: 0 tokens.", missingAnswers: "Still to answer:", stepCheck: "Please check:",
  notAnswered: "Not answered", perishableAuto: "Not sure (Pirca checks)", levelUnverified: "unverified", wallLabel: "Your pirca grows with each step",
  daysUnit: "days", peopleUnit: "people", alreadyHave: "What do you already have? (tap all that apply)", noneSelected: "Nothing ticked",
});

// One plain line under each question.
const WHY = {
  business_type: { es: "Cada negocio guarda y vende cosas distintas; así adaptamos las acciones.", en: "Each business stores and sells different things, so we adapt the actions." },
  district: { es: "Usamos la historia de inundaciones de tu distrito y los avisos del ENFEN.", en: "We use your district's flood history and ENFEN alerts." },
  near_water: { es: "Los locales cerca de ríos, drenes o quebradas se inundan más seguido.", en: "Shops near rivers, drains or ravines flood more often." },
  flooded_before: { es: "Si tu local ya se inundó, es más probable que vuelva a pasar.", en: "If your shop flooded before, it is more likely to happen again." },
  floor_level: { es: "El agua entra primero a los locales a nivel de la calle.", en: "Water reaches street-level shops first." },
  higher_storage: { es: "Un lugar alto te permite subir la mercadería sin gastar.", en: "A higher place lets you move stock up at no cost." },
  tenure: { es: "Si alquilas, algunos arreglos (techo, puerta) necesitan permiso del dueño.", en: "If you rent, some repairs (roof, door) need the landlord's permission." },
  workers: { es: "Para planear quién ayuda y qué pasa si alguien se enferma.", en: "To plan who helps and what happens if someone gets sick." },
  stock_value: { es: "Para saber cuánto podrías perder si el agua moja tu mercadería.", en: "To know how much you could lose if water reaches your stock." },
  share_stock_below_1m: { es: "Lo que está a menos de 1 metro del piso es lo que el agua puede alcanzar.", en: "What sits less than 1 meter above the floor is what water can reach." },
  perishables: { es: "Lo perecible no se puede guardar de más; para eso pedimos entregas pequeñas.", en: "Perishables can't be stocked up, so we plan small deliveries instead." },
  days_of_stock: { es: "Si se cortan las carreteras, necesitas mercadería para más días.", en: "If roads are cut, you need stock for more days." },
  cash_on_hand: { es: "Para que el plan nunca te pida gastar más de lo que tienes.", en: "So the plan never asks you to spend more than you have." },
  monthly_fixed_costs: { es: "Para calcular tu fondo de emergencia si tienes que cerrar.", en: "To size your emergency fund if you have to close." },
  weekly_sales: { es: "Para estimar cuánto dejarías de vender si cierras.", en: "To estimate the sales you would lose if you close." },
  suppliers: { es: "Revisamos si las carreteras desde esas ciudades se cortaron en inundaciones pasadas.", en: "We check whether roads from those cities were cut in past floods." },
  prep_budget: { es: "Las compras del plan se eligen para que entren en este monto.", en: "The plan's purchases are chosen to fit this amount." },
  already_have: { es: "Así no te recomendamos lo que ya tienes.", en: "So we don't recommend what you already have." },
};

const BUSINESS_TYPES = [
  ["bodega", "🏪", { es: "Bodega", en: "Corner shop (bodega)" }], ["botica", "💊", { es: "Botica", en: "Pharmacy (botica)" }],
  ["ferretería", "🔧", { es: "Ferretería", en: "Hardware store" }], ["ropa", "👕", { es: "Ropa", en: "Clothing" }],
  ["restaurante", "🍽️", { es: "Restaurante", en: "Restaurant" }],
];
const CHOICE_ICONS = { yes: "✓", no: "✕", unknown: "?", owned: "🏠", rented: "🔑" };
const PERISHABLE_ICONS = { yes: "🍞", no: "📦" };
// Slider ranges (soles or units); typing a bigger number widens the slider.
const SLIDERS = {
  stock_value: { max: 100000, step: 500 }, cash_on_hand: { max: 50000, step: 100 }, monthly_fixed_costs: { max: 30000, step: 100 },
  weekly_sales: { max: 50000, step: 100 }, prep_budget: { max: 10000, step: 50 }, workers: { min: 1, max: 30, step: 1 },
  days_of_stock: { max: 60, step: 1 },
};

// Small pictures for floor level and higher storage (simple shapes, theme colors).
const STREET = '<line x1="2" x2="78" y1="50" y2="50" class="pic-street"/>';
const WATER = '<rect x="2" y="44" width="76" height="8" class="pic-water"/>';
const PLACE_PICS = {
  ground: `${WATER}<rect x="22" y="22" width="36" height="28" class="pic-shop"/><path d="M18 22 L40 10 L62 22 Z" class="pic-roof"/>${STREET}`,
  raised: `${WATER}<rect x="16" y="40" width="48" height="10" class="pic-step"/><rect x="22" y="16" width="36" height="24" class="pic-shop"/><path d="M18 16 L40 5 L62 16 Z" class="pic-roof"/>${STREET}`,
  upper: `${WATER}<rect x="22" y="28" width="36" height="22" class="pic-wall"/><rect x="22" y="10" width="36" height="18" class="pic-shop"/><path d="M18 10 L40 2 L62 10 Z" class="pic-roof"/>${STREET}`,
  none: `<rect x="18" y="20" width="44" height="30" class="pic-wall"/><rect x="24" y="38" width="10" height="10" class="pic-box"/><rect x="36" y="38" width="10" height="10" class="pic-box"/>${STREET}`,
  mezzanine: `<rect x="18" y="14" width="44" height="36" class="pic-wall"/><line x1="18" x2="44" y1="30" y2="30" class="pic-floor"/><rect x="22" y="20" width="9" height="9" class="pic-box up"/><rect x="33" y="20" width="9" height="9" class="pic-box up"/>${STREET}`,
  second_floor: `<rect x="18" y="8" width="44" height="42" class="pic-wall"/><line x1="18" x2="62" y1="29" y2="29" class="pic-floor"/><rect x="24" y="18" width="10" height="10" class="pic-box up"/><rect x="36" y="18" width="10" height="10" class="pic-box up"/>${STREET}`,
};

const wiz = {
  get step() { return Math.min(GROUPS.length, Number(localStorage.getItem("pirca.step")) || 0); },
  set step(v) { localStorage.setItem("pirca.step", String(v)); },
  get visited() { return Number(localStorage.getItem("pirca.visited")) || 0; },
  set visited(v) { localStorage.setItem("pirca.visited", String(v)); },
  preview: null, seq: 0, timer: null,
};

const ALL_FIELDS = () => GROUPS.flatMap((g) => g.fields);
const filled = (v) => v !== null && v !== undefined && v !== "" && !(typeof v === "number" && Number.isNaN(v));
function draftNow() {
  const d = store.draft || {};
  return typeof d.perishables === "boolean" ? { ...d, perishables: d.perishables ? "yes" : "no" } : d;
}
function setDraft(name, value) { store.draft = { ...draftNow(), [name]: value }; }
function collectDraft() { return draftNow(); }
function saveDraftFromForm() { /* the wizard saves every answer as it is given */ }

function stepComplete(i, d = draftNow()) {
  const g = GROUPS[i];
  if (g.id === "suppliers") return wiz.visited > i || (d.suppliers || []).some((s) => s.product && s.city);
  return g.fields.every((f) => filled(d[f.name]));
}

// Answers sent to /api/preview: only what the owner gave (plus suppliers/checklist once those steps were reached).
function previewProfile(d) {
  const p = {};
  ALL_FIELDS().forEach((f) => { if (filled(d[f.name])) p[f.name] = d[f.name]; });
  if (filled(d.perishables)) p.perishables = d.perishables === "yes";
  const sIdx = GROUPS.findIndex((g) => g.id === "suppliers");
  const suppliers = (d.suppliers || []).filter((s) => s.product && s.city);
  if (suppliers.length || wiz.visited > sIdx) p.suppliers = suppliers;
  if (wiz.visited >= GROUPS.length - 1 || (d.already_have || []).length) p.already_have = d.already_have || [];
  return p;
}

function schedulePreview() {
  clearTimeout(wiz.timer);
  wiz.timer = setTimeout(async () => {
    const seq = ++wiz.seq;
    try {
      const res = await api("/api/preview", { method: "POST", body: JSON.stringify(previewProfile(draftNow())) });
      if (seq !== wiz.seq) return;  // a newer answer is already on its way
      wiz.preview = res;
      updatePreviewPanel(); updateStepNotice();
    } catch (e) { console.warn(e); }
  }, 250);
}

function levelWord(level) {
  if (!level) return "—";
  if (level === "UNVERIFIED") return t("levelUnverified");
  return t("risk" + level[0].toUpperCase() + level.slice(1)).toLowerCase();
}

function updatePreviewPanel() {
  const box = document.getElementById("risk-preview");
  const p = wiz.preview;
  if (!box || !p) return;
  const frac = GAUGE_FRACTION[p.risk_level];
  const fill = box.querySelector(".fill"), needle = box.querySelector(".needle"), level = box.querySelector(".level");
  if (fill) fill.style.strokeDashoffset = (ARC * (1 - (frac ?? 0))).toFixed(1);
  if (needle) needle.style.transform = `rotate(${-90 + 180 * (frac ?? 0)}deg)`;
  if (level) {
    level.className = `level ${p.risk_level ? "risk-" + p.risk_level : ""}`;
    level.innerHTML = `${esc(p.ready ? t("risk" + p.risk_level[0].toUpperCase() + p.risk_level.slice(1)) : "—")}<span>${esc(t("risk"))}</span>`;
  }
  box.querySelector(".gauge")?.setAttribute("aria-label", `${t("risk")}: ${p.ready ? levelWord(p.risk_level) : "—"}`);
  const S = STR[store.lang];
  box.querySelector(".preview-text").innerHTML = p.ready
    ? `<p>${esc(S.previewDistrict(levelWord(p.district_hazard_level)))}</p>${p.stock_at_risk !== undefined ? `<p>${esc(S.previewStock(money(p.stock_at_risk, "pen")))}</p>` : ""}`
    : `<p>${esc(t("previewWaiting"))}</p>`;
}

function stepNoticeHtml(missing) {
  const g = GROUPS[wiz.step];
  const p = wiz.preview;
  const errors = (p?.errors || []).filter((e) => e.step === g?.id);
  const warnings = (p?.warnings || []).filter((w) => w.step === g?.id);
  const parts = [];
  if (missing?.length) parts.push(`<div class="notice error glass-read" role="alert"><b>${esc(t("missingAnswers"))}</b> ${esc(missing.join(", "))}</div>`);
  if (errors.length) parts.push(`<div class="notice error glass-read" role="alert"><b>${esc(t("errorsTitle"))}</b><ul>${errors.map((e) => `<li>${esc(errorText(e.text))}</li>`).join("")}</ul></div>`);
  if (warnings.length) parts.push(`<div class="notice glass-read" role="status"><b>${esc(t("stepCheck"))}</b><ul>${warnings.map((w) => `<li>${esc(warningText(w.text))}</li>`).join("")}</ul></div>`);
  return parts.join("");
}
function updateStepNotice(missing) {
  const box = document.getElementById("step-notice");
  if (box) box.innerHTML = stepNoticeHtml(missing);
}

// The small pirca in the header: 3 stones per completed step.
function wizardWallSvg(done) {
  const rows = [5, 4, 3, 2, 1];
  let k = 0;
  const stones = rows.map((n, r) => Array.from({ length: n }, (_, i) => {
    const x = 50 - (n * 14) / 2 + i * 14, y = 46 - (r + 1) * 8;
    return `<rect class="stone ${k++ < done * 3 ? "placed" : ""}" x="${x}" y="${y}" width="12.5" height="7" rx="2" fill="${STONE_FILLS[(k * 7 + r) % STONE_FILLS.length]}"/>`;
  }).join("")).join("");
  return `<svg viewBox="0 0 100 48" class="wiz-wall" role="img" aria-label="${esc(t("wallLabel"))}">${stones}<line x1="6" x2="94" y1="46.5" y2="46.5" class="pic-street"/></svg>`;
}
function updateWizardChrome() {
  const d = draftNow();
  const done = GROUPS.filter((_, i) => stepComplete(i, d) && (i < wiz.step || wiz.step === GROUPS.length)).length;
  const wall = document.getElementById("wiz-wall");
  if (wall) wall.innerHTML = wizardWallSvg(done);
  const label = document.getElementById("wiz-step-label");
  if (label) label.textContent = wiz.step < GROUPS.length ? STR[store.lang].stepOf(wiz.step + 1, GROUPS.length) : t("reviewStep");
  const bar = document.getElementById("wiz-bar");
  if (bar) bar.style.width = `${(100 * Math.min(wiz.step, GROUPS.length)) / GROUPS.length}%`;
}

// ---- controls
function why(name) { return WHY[name] ? `<p class="why"><b>${esc(t("whyAsk"))}</b> ${esc(L(WHY[name]))}</p>` : ""; }
function question(f, control) {
  return `<div class="q" data-field="${f.name}"><div class="q-label" id="q-${f.name}">${esc(L(f.label))}</div>
    <div class="q-hint">${esc(L(f.hint))}</div>${control}${why(f.name)}</div>`;
}
function choiceCards(name, options, value, cls = "") {
  return `<div class="choices ${cls}" role="radiogroup" aria-labelledby="q-${name}">${options.map(([v, icon, label]) =>
    `<button type="button" class="choice" role="radio" data-name="${name}" data-value="${esc(v)}" aria-checked="${String(value) === String(v)}">
      ${icon ? `<span class="choice-icon" aria-hidden="true">${icon}</span>` : ""}<span>${esc(label)}</span></button>`).join("")}</div>`;
}
function sliderControl(f, value, unit) {
  const r = SLIDERS[f.name] || { max: 100, step: 1 };
  const v = filled(value) ? Number(value) : "";
  const max = Math.max(r.max, Number(v) || 0);
  return `<div class="slider-row">
      <div class="${f.type === "money" ? "input-prefix" : ""}">${f.type === "money" ? '<span aria-hidden="true">S/</span>' : ""}
        <input class="num" id="f-${f.name}" data-name="${f.name}" type="number" inputmode="decimal" min="${r.min ?? 0}" step="any" value="${v}" aria-labelledby="q-${f.name}"></div>
      <input class="range" type="range" data-name="${f.name}" min="${r.min ?? 0}" max="${max}" step="${r.step}" value="${v === "" ? (r.min ?? 0) : v}" aria-labelledby="q-${f.name}">
    </div>
    <div class="slider-value" id="sv-${f.name}" aria-live="polite">${esc(sliderText(f, v, unit))}</div>`;
}
function sliderText(f, v, unit) {
  if (v === "" || v === null || v === undefined) return t("notAnswered");
  return f.type === "money" ? money(Number(v), "pen") : `${num(v)} ${unit || ""}`.trim();
}
function shareShelfSvg(share) {
  const s = Math.max(0, Math.min(1, Number(share) || 0));
  const low = Math.round(8 * s);
  const boxes = Array.from({ length: 8 }, (_, i) => {
    const isLow = i < low;
    const slot = isLow ? i : i - low;                            // low boxes fill the two bottom shelves
    const row = isLow ? 3 - Math.floor(slot / 4) : Math.floor(slot / 4);
    const x = 46 + (slot % 4) * 27;
    return `<rect x="${x}" y="${18 + row * 30}" width="23" height="20" rx="3" class="${isLow ? "box wet" : "box"}"/>`;
  }).join("");
  const lineY = 78, floorY = 138, waterTop = floorY - (floorY - lineY) * s;
  return `<svg viewBox="0 0 200 146" class="pic share-pic" aria-hidden="true">
    <rect x="${40}" y="10" width="120" height="128" rx="4" class="shelf-frame"/>
    ${[38, 68, 98, 128].map((y) => `<line x1="40" x2="160" y1="${y + 10}" y2="${y + 10}" class="shelf-board"/>`).join("")}
    ${boxes}
    <rect x="30" y="${waterTop.toFixed(1)}" width="140" height="${(floorY - waterTop).toFixed(1)}" class="water share-water"/>
    <line x1="22" x2="178" y1="${lineY}" y2="${lineY}" class="water-line"/>
    <text x="176" y="${lineY - 4}" text-anchor="end" class="pic-label">${esc(t("meter"))}</text>
    <line x1="30" x2="170" y1="${floorY}" y2="${floorY}" class="floor"/></svg>`;
}

function fieldControl(f, d) {
  const v = d[f.name];
  if (f.name === "business_type") {
    const known = BUSINESS_TYPES.some(([b]) => b === v);
    const other = filled(v) && !known;
    return question(f, `${choiceCards("business_type", [...BUSINESS_TYPES.map(([b, icon, label]) => [b, icon, L(label)]), ["__other", "✏️", t("otherType")]],
      other ? "__other" : v, "choices-wide")}
      <input class="other-input" id="f-business_type_other" type="text" placeholder="${esc(t("otherPlaceholder"))}" value="${other ? esc(v) : ""}" ${other ? "" : "hidden"} aria-labelledby="q-business_type">`);
  }
  if (f.name === "district") {
    const byProvince = {};
    state.meta.districts.forEach((x) => (byProvince[x.province] ??= []).push(x));
    return question(f, `<input class="district-search" id="f-district-search" type="search" placeholder="${esc(t("searchDistrict"))}" aria-labelledby="q-district" autocomplete="off">
      <div class="district-list" role="radiogroup" aria-labelledby="q-district">${Object.entries(byProvince).map(([prov, ds]) =>
        `<div class="district-prov" data-prov="${esc(prov)}"><div class="prov-name">${esc(prov)}</div>${ds.map((x) =>
          `<button type="button" class="choice district" role="radio" data-name="district" data-value="${esc(x.name)}" aria-checked="${v === x.name}">
            ${esc(x.name)}<small>${esc(L(LEVEL_NOTE)[x.hazard_level] || "")}</small></button>`).join("")}</div>`).join("")}
        <p class="no-match muted" hidden>${esc(t("noMatch"))}</p></div>`);
  }
  if (f.name === "near_water" || f.name === "flooded_before")
    return question(f, choiceCards(f.name, Object.entries(L(YES_NO_UNKNOWN)).map(([k, label]) => [k, CHOICE_ICONS[k], label]), v, "choices-big"));
  if (f.name === "floor_level" || f.name === "higher_storage")
    return question(f, `<div class="choices choices-pics" role="radiogroup" aria-labelledby="q-${f.name}">${Object.entries(L(f.options)).map(([k, label]) =>
      `<button type="button" class="choice pic-choice" role="radio" data-name="${f.name}" data-value="${k}" aria-checked="${v === k}">
        <svg viewBox="0 0 80 56" aria-hidden="true">${PLACE_PICS[k]}</svg><span>${esc(label)}</span></button>`).join("")}</div>`);
  if (f.name === "tenure")
    return question(f, choiceCards(f.name, Object.entries(L(f.options)).map(([k, label]) => [k, CHOICE_ICONS[k], label]), v, "choices-big"));
  if (f.name === "perishables")
    return question(f, choiceCards(f.name, Object.entries(L(YES_NO)).map(([k, label]) => [k, PERISHABLE_ICONS[k], label]), v, "choices-big"));
  if (f.name === "share_stock_below_1m") {
    const pct = filled(v) ? Math.round(v * 1000) / 10 : "";
    return question(f, `<div class="share-wrap"><div id="share-pic">${shareShelfSvg(v)}</div><div>
      <div class="slider-row"><input class="num" id="f-share" data-name="share_stock_below_1m" type="number" inputmode="decimal" min="0" max="100" step="any" value="${pct}" aria-labelledby="q-share_stock_below_1m">
        <input class="range" type="range" data-name="share_stock_below_1m" min="0" max="100" step="5" value="${pct === "" ? 0 : pct}" aria-labelledby="q-share_stock_below_1m"></div>
      <div class="slider-value" id="sv-share_stock_below_1m" aria-live="polite">${pct === "" ? esc(t("notAnswered")) : `${pct}%`}</div></div></div>`);
  }
  if (f.type === "money") return question(f, sliderControl(f, v));
  if (f.name === "workers") return question(f, sliderControl(f, v, t("peopleUnit")));
  if (f.name === "days_of_stock") return question(f, sliderControl(f, v, t("daysUnit")));
  return question(f, `<input id="f-${f.name}" data-name="${f.name}" type="text" value="${esc(v ?? "")}" aria-labelledby="q-${f.name}">`);
}

function supplierRowHtml(s, i) {
  const pv = s.perishable === true ? "true" : s.perishable === false ? "false" : "";
  const opts = L(SUPPLIER_PERISHABLE);
  return `<div class="supplier-row" data-row="${i}">
    <div class="field"><label for="sp-${i}">${store.lang === "es" ? "Producto" : "Product"}</label>
      <input id="sp-${i}" name="product" value="${esc(s.product || "")}" placeholder="${store.lang === "es" ? "abarrotes, pan, bebidas…" : "groceries, bread, drinks…"}"></div>
    <div class="field"><label for="sc-${i}">${store.lang === "es" ? "Ciudad" : "City"}</label>
      <input id="sc-${i}" name="city" value="${esc(s.city || "")}" placeholder="Piura, Chiclayo…"></div>
    <button class="icon-btn supplier-remove" type="button" data-remove="${i}" aria-label="${esc(t("remove"))}">✕</button>
    <div class="field perishable-field"><span class="label-like" id="spp-${i}">${store.lang === "es" ? "¿Perecible?" : "Perishable?"}</span>
      <div class="segmented-3" role="radiogroup" aria-labelledby="spp-${i}">${["true", "false", ""].map((k) =>
        `<button type="button" class="chip" role="radio" data-perishable="${k}" aria-checked="${pv === k}">${esc(k === "" ? t("perishableAuto") : opts[k])}</button>`).join("")}</div></div>
  </div>`;
}

function stepHtml(i, d) {
  const g = GROUPS[i];
  const suppliers = d.suppliers?.length ? d.suppliers : [{}];
  const have = new Set(d.already_have || []);
  return `<fieldset class="form-group glass wizard-step" data-step="${g.id}">
    <h2><span class="step">${i + 1}</span>${esc(L(g.title))}</h2>
    <p>${esc(L(g.hint))}</p>
    ${g.fields.map((f) => fieldControl(f, d)).join("")}
    ${g.id === "suppliers" ? `<div class="q"><div id="suppliers">${suppliers.map(supplierRowHtml).join("")}</div>
      <button class="btn" type="button" id="add-supplier" ${suppliers.length >= 3 ? "disabled" : ""}>${esc(t("addSupplier"))}</button>${why("suppliers")}</div>` : ""}
    ${g.id === "prep" ? `<div class="q"><div class="q-label" id="q-already_have">${esc(t("alreadyHave"))}</div>
      <div class="have-grid">${state.meta.actions.map((a) => `<button type="button" class="choice have" role="checkbox" data-have="${a.id}" aria-checked="${have.has(a.id)}">
        <span class="choice-icon" aria-hidden="true">${CAT_ICONS[a.id] || "✅"}</span><span>${esc(store.lang === "es" ? a.name_es : a.name_en)}</span></button>`).join("")}</div>${why("already_have")}</div>` : ""}
    <div id="step-notice"></div>
    <div class="wiz-nav">
      <button class="btn" type="button" id="wiz-back" ${i === 0 ? "disabled" : ""}>${esc(t("back"))}</button>
      <button class="btn btn-primary" type="button" id="wiz-next">${esc(t("next"))}</button>
    </div>
  </fieldset>`;
}

function answerText(f, v) {
  if (!filled(v)) return `<span class="muted">${esc(t("notAnswered"))}</span>`;
  if (f.name === "business_type") { const b = BUSINESS_TYPES.find(([x]) => x === v); return esc(b ? L(b[2]) : v); }
  if (f.name === "near_water" || f.name === "flooded_before") return esc(L(YES_NO_UNKNOWN)[v] || v);
  if (f.name === "perishables") return esc(L(YES_NO)[v] || v);
  if (f.options) return esc(L(f.options)[v] || v);
  if (f.type === "money") return esc(money(Number(v), "pen"));
  if (f.type === "percent") return `${Math.round(v * 1000) / 10}%`;
  if (f.name === "days_of_stock") return esc(`${num(v)} ${t("daysUnit")}`);
  return esc(String(v));
}

function reviewHtml(d) {
  const sup = (d.suppliers || []).filter((s) => s.product && s.city);
  const opts = L(SUPPLIER_PERISHABLE);
  const names = Object.fromEntries(state.meta.actions.map((a) => [a.id, store.lang === "es" ? a.name_es : a.name_en]));
  return `<section class="form-group glass wizard-step review">
    <h2>${esc(t("reviewTitle"))}</h2><p>${esc(t("reviewIntro"))}</p>
    ${GROUPS.map((g, i) => `<div class="review-group">
      <div class="review-head"><h3><span class="step">${i + 1}</span>${esc(L(g.title))}</h3>
        <button class="btn btn-small" type="button" data-edit="${i}">✎ ${esc(t("edit"))}</button></div>
      <dl>${g.fields.map((f) => `<div><dt>${esc(L(f.label))}</dt><dd>${answerText(f, d[f.name])}</dd></div>`).join("")}
      ${g.id === "suppliers" ? `<div><dt>${esc(L(g.title))}</dt><dd>${sup.length ? sup.map((s) => esc(`${s.product} — ${s.city}${s.perishable === null || s.perishable === undefined ? "" : ` (${opts[String(s.perishable)]})`}`)).join("<br>") : `<span class="muted">${esc(t("notAnswered"))}</span>`}</dd></div>` : ""}
      ${g.id === "prep" ? `<div><dt>${esc(t("alreadyHave").replace(/\s*\(.*\)$/, ""))}</dt><dd>${(d.already_have || []).length ? d.already_have.map((id) => esc(names[id] || id)).join(", ") : `<span class="muted">${esc(t("noneSelected"))}</span>`}</dd></div>` : ""}
      </dl></div>`).join("")}
    <div id="form-notice"></div>
    <div class="wiz-nav">
      <button class="btn" type="button" id="wiz-back">${esc(t("back"))}</button>
      <button class="btn btn-primary" type="button" id="check-btn">${esc(t("makeMyPlan"))}</button>
    </div>
  </section>`;
}

function renderForm() {
  const d = draftNow();
  const i = wiz.step;
  app.innerHTML = `
    <section class="panel glass wizard-head">
      <div class="wiz-title"><h1 style="font-size:28px">${esc(t("formTitle"))}</h1><p class="muted">${esc(t("formIntro"))}</p>
        <button class="btn" type="button" id="sample-btn">${esc(t("useSample"))}</button></div>
      <div id="wiz-wall" class="wiz-wall-box"></div>
      <div class="wiz-progress"><span id="wiz-step-label" class="check-count"></span><div class="progress-bar" aria-hidden="true"><span id="wiz-bar"></span></div></div>
    </section>
    <div class="wizard-layout">
      <form id="intake" class="wizard-main" novalidate>${i < GROUPS.length ? stepHtml(i, d) : reviewHtml(d)}</form>
      <aside class="risk-preview glass" id="risk-preview" aria-live="polite">
        <h2>${esc(t("previewTitle"))}</h2>${gaugeSvg(null)}<div class="preview-text"></div>
        <p class="muted small">${esc(t("previewFree"))}</p></aside>
    </div>`;
  state.view = { form: true, rerender: renderForm };
  wireWizard();
  updateWizardChrome();
  updatePreviewPanel();
  updateStepNotice();
  schedulePreview();
}

function goStep(i) {
  wiz.step = i;
  wiz.visited = Math.max(wiz.visited, i);
  renderForm();
  document.querySelector(".wizard-main")?.scrollIntoView({ block: "start", behavior: REDUCED_MOTION.matches ? "auto" : "smooth" });
}

function onAnswer() { updateWizardChrome(); schedulePreview(); }

function wireWizard() {
  const form = document.getElementById("intake");
  // A district chosen earlier (or from the home map) is scrolled into view inside its list.
  const list = form.querySelector(".district-list"), picked = list?.querySelector(".choice.district[aria-checked=true]");
  if (list && picked) list.scrollTop = picked.offsetTop - list.offsetTop - 40;
  document.getElementById("sample-btn").addEventListener("click", async () => {
    const example = await api(`/api/plans/${state.meta.example_code}`);
    store.draft = example.result.form;
    wiz.visited = GROUPS.length;
    goStep(GROUPS.length);  // straight to the review screen
  });
  form.addEventListener("submit", (e) => e.preventDefault());
  form.addEventListener("click", (e) => {
    const choice = e.target.closest(".choice[data-name]");
    if (choice) {
      const name = choice.dataset.name;
      const q = choice.closest(".q");
      q.querySelectorAll(`.choice[data-name="${name}"]`).forEach((c) => c.setAttribute("aria-checked", String(c === choice)));
      q.classList.remove("invalid");
      if (name === "business_type") {
        const other = document.getElementById("f-business_type_other");
        other.hidden = choice.dataset.value !== "__other";
        if (!other.hidden) { setDraft(name, other.value.trim() || null); other.focus(); } else setDraft(name, choice.dataset.value);
      } else setDraft(name, choice.dataset.value);
      onAnswer(); return;
    }
    const have = e.target.closest("[data-have]");
    if (have) {
      const on = have.getAttribute("aria-checked") !== "true";
      have.setAttribute("aria-checked", String(on));
      const set = new Set(draftNow().already_have || []);
      if (on) set.add(have.dataset.have); else set.delete(have.dataset.have);
      setDraft("already_have", [...set]); onAnswer(); return;
    }
    const chip = e.target.closest("[data-perishable]");
    if (chip) {
      chip.parentElement.querySelectorAll(".chip").forEach((c) => c.setAttribute("aria-checked", String(c === chip)));
      saveSuppliers(); return;
    }
    const remove = e.target.closest("[data-remove]");
    if (remove) { const s = readSuppliers(); s.splice(Number(remove.dataset.remove), 1); setDraft("suppliers", s); renderForm(); return; }
    if (e.target.closest("#add-supplier")) { const s = readSuppliers(); s.push({}); setDraft("suppliers", s); renderForm(); return; }
    const edit = e.target.closest("[data-edit]");
    if (edit) { goStep(Number(edit.dataset.edit)); return; }
    if (e.target.closest("#wiz-back")) { goStep(Math.max(0, wiz.step - 1)); return; }
    if (e.target.closest("#wiz-next")) { tryNext(); return; }
    if (e.target.closest("#check-btn")) checkAndRun(false);
  });
  form.addEventListener("input", (e) => {
    const el = e.target;
    if (el.id === "f-business_type_other") { setDraft("business_type", el.value.trim() || null); onAnswer(); return; }
    if (el.id === "f-district-search") { filterDistricts(el.value); return; }
    if (el.closest(".supplier-row")) { saveSuppliers(); return; }
    const name = el.dataset.name;
    if (!name) return;
    const row = el.closest(".q");
    const raw = el.value;
    if (name === "share_stock_below_1m") {
      const pct = raw === "" ? null : Math.max(0, Math.min(100, Number(raw)));
      row.querySelectorAll("[data-name]").forEach((x) => { if (x !== el) x.value = pct ?? 0; });
      setDraft(name, pct === null ? null : pct / 100);
      document.getElementById("share-pic").innerHTML = shareShelfSvg(pct === null ? 0 : pct / 100);
      document.getElementById("sv-share_stock_below_1m").textContent = pct === null ? t("notAnswered") : `${pct}%`;
    } else {
      const f = ALL_FIELDS().find((x) => x.name === name);
      const v = raw === "" ? null : Number(raw);
      row.querySelectorAll("[data-name]").forEach((x) => {
        if (x === el) return;
        if (x.type === "range" && v !== null && v > Number(x.max)) x.max = String(v);  // widen the slider for big numbers
        x.value = v ?? (x.type === "range" ? x.min : "");
      });
      setDraft(name, v);
      document.getElementById(`sv-${name}`).textContent = sliderText(f, v ?? "", name === "workers" ? t("peopleUnit") : name === "days_of_stock" ? t("daysUnit") : "");
    }
    row.classList.remove("invalid");
    onAnswer();
  });
}

function filterDistricts(q) {
  const needle = q.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLowerCase().trim();
  let shown = 0;
  document.querySelectorAll(".district-prov").forEach((prov) => {
    let any = false;
    prov.querySelectorAll(".choice.district").forEach((b) => {
      const name = b.dataset.value.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLowerCase();
      const match = !needle || name.includes(needle) || prov.dataset.prov.toLowerCase().includes(needle);
      b.hidden = !match; any ||= match; shown += match ? 1 : 0;
    });
    prov.hidden = !any;
  });
  document.querySelector(".no-match").hidden = shown > 0;
}

function readSuppliers() {
  return [...document.querySelectorAll(".supplier-row")].map((row) => {
    const p = row.querySelector(".chip[aria-checked=true]")?.dataset.perishable ?? "";
    return { product: row.querySelector("[name=product]").value.trim(), city: row.querySelector("[name=city]").value.trim(),
             perishable: p === "" ? null : p === "true" };
  });
}
function saveSuppliers() { setDraft("suppliers", readSuppliers()); onAnswer(); }

function tryNext() {
  const i = wiz.step, g = GROUPS[i], d = draftNow();
  const missing = g.fields.filter((f) => !filled(d[f.name]));
  missing.forEach((f) => document.querySelector(`.q[data-field="${f.name}"]`)?.classList.add("invalid"));
  const errors = (wiz.preview?.errors || []).filter((e) => e.step === g.id);
  if (missing.length || errors.length) {
    updateStepNotice(missing.map((f) => L(f.label)));
    document.getElementById("step-notice").scrollIntoView({ block: "center", behavior: REDUCED_MOTION.matches ? "auto" : "smooth" });
    return;
  }
  goStep(i + 1);
}

async function checkAndRun(confirmed) {
  const profile = toProfile(draftNow());
  const notice = document.getElementById("form-notice");
  const btn = document.getElementById("check-btn");
  btn.disabled = true; btn.textContent = t("checking");
  const stepOfField = (field) => Math.max(0, GROUPS.findIndex((g) => g.fields.some((f) => f.name === field) || g.id === field));
  try {
    const v = await api("/api/validate", { method: "POST", body: JSON.stringify(profile) });
    if (!v.valid) {
      notice.innerHTML = `<div class="notice error glass-read" role="alert"><b>${esc(t("errorsTitle"))}</b>
        <ul>${v.errors.map((e) => `<li>${esc(errorText(e))} <button class="btn btn-small" type="button" data-edit="${stepOfField(e.split(/[.:]/)[0])}">✎ ${esc(t("edit"))}</button></li>`).join("")}</ul></div>`;
      notice.scrollIntoView({ behavior: "smooth" });
      return;
    }
    if (v.warnings.length && !confirmed) {
      const steps = Object.fromEntries((wiz.preview?.warnings || []).map((w) => [w.text, GROUPS.findIndex((g) => g.id === w.step)]));
      notice.innerHTML = `<div class="notice glass-read" role="alert"><b>${esc(t("warningsTitle"))}</b>
        <p class="muted small" style="margin:4px 0 0">${esc(t("warningsText"))}</p>
        <ul>${v.warnings.map((w) => `<li>${esc(warningText(w))}${steps[w] >= 0 ? ` <button class="btn btn-small" type="button" data-edit="${steps[w]}">✎ ${esc(t("edit"))}</button>` : ""}</li>`).join("")}</ul>
        <div class="btn-row"><button class="btn btn-primary" type="button" id="confirm-btn">${esc(t("confirmRun"))}</button></div></div>`;
      notice.scrollIntoView({ behavior: "smooth" });
      document.getElementById("confirm-btn").addEventListener("click", () => checkAndRun(true));
      return;
    }
    btn.textContent = t("starting");
    const created = await api("/api/plans", { method: "POST", body: JSON.stringify({ profile, language: store.lang }) });
    store.plans = [{ code: created.code, label: `${profile.business_type} · ${profile.district}`, language: store.lang,
                     created_at: new Date().toISOString() }, ...store.plans.filter((p) => p.code !== created.code)];
    wiz.step = 0; wiz.visited = 0;
    location.hash = `#/plan/${created.code}`;
  } catch (e) {
    console.warn(e);
    notice.innerHTML = `<div class="notice error glass-read" role="alert">${esc(t("networkError"))}</div>`;
  } finally {
    if (document.getElementById("check-btn")) { btn.disabled = false; btn.textContent = t("makeMyPlan"); }
  }
}

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

function errorText(e) {
  const [field, ...rest] = e.split(":");
  const f = GROUPS.flatMap((g) => g.fields).find((x) => x.name === field.split(".")[0]);
  return f ? `${L(f.label)}: ${rest.join(":").trim()}` : e;
}

// ------------------------------------------------------------------ trace (live and replay)

const AGENTS = ["manager", "risk_analyst", "planner", "critic"];
const WORKERS = ["risk_analyst", "planner", "critic"];

// ---- live agent map: Manager on top, the three workers below, then Code checks -> Plan.
const MAP_LAYOUTS = {
  wide: {
    view: "0 0 680 320", toolChars: 24,
    nodes: { manager: { x: 200, y: 62, w: 180, h: 84 }, gate: { x: 440, y: 62, w: 150, h: 84 }, plan: { x: 610, y: 62, w: 110, h: 84 },
             risk_analyst: { x: 95, y: 215, w: 172, h: 84 }, planner: { x: 300, y: 215, w: 172, h: 84 }, critic: { x: 505, y: 215, w: 172, h: 84 } },
    toGate: "M290 62 H365", toPlan: "M515 62 H555",
    revision: "M505 257 C505 297, 300 297, 300 257", revLabel: [402.5, 306], team: [665, 122], teamAnchor: "end",
  },
  narrow: {
    view: "0 0 360 540", toolChars: 15,
    nodes: { manager: { x: 180, y: 52, w: 190, h: 84 }, gate: { x: 180, y: 380, w: 220, h: 84 }, plan: { x: 180, y: 480, w: 150, h: 64 },
             risk_analyst: { x: 62, y: 200, w: 114, h: 92 }, planner: { x: 180, y: 200, w: 114, h: 92 }, critic: { x: 298, y: 200, w: 114, h: 92 } },
    toGate: "M85 52 H12 V380 H70", toPlan: "M180 422 V448",
    revision: "M298 246 C298 282, 180 282, 180 246", revLabel: [239, 292], team: [180, 528], teamAnchor: "middle",
  },
};

const MAP_NARROW = window.matchMedia("(max-width: 720px)");
function mapLayout() { return MAP_NARROW.matches ? MAP_LAYOUTS.narrow : MAP_LAYOUTS.wide; }

// The layout is chosen when the map is drawn; if the window crosses the phone width
// (rotating a phone, resizing), redraw it and re-apply the events seen so far, without pulses.
window.addEventListener("resize", () => { if (state.trace) rebuildMap(state.trace); });
function rebuildMap(ts) {
  const old = document.getElementById("agent-map");
  if (!old || old.dataset.layout === (MAP_NARROW.matches ? "narrow" : "wide")) return;
  old.outerHTML = agentMapHtml();
  fitMapText();
  const fresh = newTraceState(false);
  ts.seen.forEach((e) => { trackEvent(fresh, e); mapApply(fresh, e); });
  Object.assign(ts, fresh, { animate: ts.animate, seen: ts.seen });
}

// ---- Piura scene behind the map (decoration only): Río Piura, a shop on the bank, and a dry-stone
// wall (pirca) that builds itself as the run goes. Driven by the same events as the map.
const PIRCA_ROWS = [8, 7, 6, 5, 4];                      // 30 stones, bottom row first
const PIRCA_STONES = PIRCA_ROWS.reduce((a, b) => a + b, 0);
const STONES_PER_STEP = 3;                               // an agent finishes or a code check passes
const SCENES = {
  wide: { w: 680, bankX: 430, wallX: 534, stoneW: 13, shopX: 634 },
  narrow: { w: 360, bankX: 170, wallX: 228, stoneW: 10, shopX: 312 },
};
const STONE_FILLS = ["#D9C7A3", "#C49A5B", "#B86B47", "#A99B84"];  // beige, ochre, terracotta, gray-beige

function riverWavePath(w, y, amp, period) {
  let d = `M${-period} ${y}`;
  for (let x = -period; x < w + period; x += period) d += ` q${period / 4} ${-amp} ${period / 2} 0 t${period / 2} 0`;
  return `${d} V90 H${-period} Z`;
}

function sceneHtml(narrow) {
  const S = narrow ? SCENES.narrow : SCENES.wide;
  const base = 56, h = 7;
  let k = 0;
  const stones = PIRCA_ROWS.map((count, r) => Array.from({ length: count }, (_, i) => {
    const x = S.wallX - (count * S.stoneW) / 2 + i * S.stoneW;
    const fill = STONE_FILLS[(k * 7 + r) % STONE_FILLS.length];
    return `<rect class="stone" data-k="${k++}" x="${x.toFixed(1)}" y="${base - (r + 1) * h}" width="${S.stoneW - 1.5}" height="${h - 1}" rx="2" fill="${fill}"/>`;
  }).join("")).join("");
  const s = S.shopX;
  const waves = [[66, 2.5, 60, "a"], [74, 2, 80, "b"], [82, 1.8, 50, "c"]]
    .map(([y, amp, p, c]) => `<path class="wave wave-${c}" style="--p:${-p}px" d="${riverWavePath(S.w, y, amp, p)}"/>`).join("");
  return `<div class="scene-sun" aria-hidden="true"></div>
    <svg class="scene-ground" viewBox="0 0 ${S.w} 90" preserveAspectRatio="xMidYMax meet" aria-hidden="true">
      ${waves}
      <path class="bank" d="M${S.bankX - 40} 90 C${S.bankX - 10} 90, ${S.bankX - 12} ${base}, ${S.bankX + 20} ${base} H${S.w} V90 Z"/>
      <g class="shop">
        <rect x="${s - 26}" y="${base - 28}" width="52" height="28" class="shop-body"/>
        <path d="M${s - 32} ${base - 28} L${s} ${base - 44} L${s + 32} ${base - 28} Z" class="shop-roof"/>
        <rect x="${s - 22}" y="${base - 23}" width="44" height="5" class="shop-awning"/>
        <rect x="${s - 6}" y="${base - 15}" width="12" height="15" class="shop-door"/>
        <rect x="${s - 19}" y="${base - 14}" width="9" height="7" class="shop-window"/>
      </g>
      <g class="pirca">${stones}</g>
    </svg>`;
}

// Stones, sun height and rain follow ts.stones (0..30); a stopped run keeps the wall unfinished and the sun low.
function sceneApply(ts, e, map) {
  const ok = (e.type === "agent_finished")
    || (e.type === "tool_result" && e.tool === "verify_draft" && e.result?.ok === true)
    || ((e.type === "code_check" || e.type === "final_check") && e.ok === true);
  if (ok && !ts.sceneEnd) ts.stones = Math.min(PIRCA_STONES - STONES_PER_STEP, ts.stones + STONES_PER_STEP);
  if (e.type === "run_finished") {
    ts.sceneEnd = e.status === "completed" ? "done" : e.status === "completed_with_warning" ? "warn" : "stopped";
    if (ts.sceneEnd !== "stopped") ts.stones = PIRCA_STONES;
  }
  if (e.type === "limit_hit" && e.action === "stopped") ts.sceneEnd = "stopped";
  map.classList.toggle("scene-instant", !ts.animate || REDUCED_MOTION.matches);
  let batch = 0;
  map.querySelectorAll(".stone").forEach((stone) => {
    const placed = Number(stone.dataset.k) < ts.stones;
    if (placed && !stone.classList.contains("placed")) stone.style.transitionDelay = `${(batch++) * 90}ms`;
    stone.classList.toggle("placed", placed);
  });
  let p = ts.stones / PIRCA_STONES;
  if (ts.sceneEnd === "stopped") p = Math.min(p, 0.12);
  // Sun arc (percent of the panel): up the free left margin, then along the top toward the middle.
  const q = (a, b, c) => (1 - p) ** 2 * a + 2 * (1 - p) * p * b + p ** 2 * c;
  map.style.setProperty("--sun-x", `${(5 + 43 * p ** 3).toFixed(1)}%`);  // stays in the free left margin, then crosses the top
  map.style.setProperty("--sun-y", `${q(72, -6, 4).toFixed(1)}%`);
  map.style.setProperty("--day", (ts.sceneEnd === "stopped" ? 0.15 : 0.15 + 0.85 * p).toFixed(2));  // the afternoon brightens
  map.style.setProperty("--rain", Math.max(0, Math.min(1, 1 - (p - 0.55) / 0.4)).toFixed(2));
  map.classList.toggle("scene-done", ts.sceneEnd === "done");
  map.classList.toggle("scene-stopped", ts.sceneEnd === "stopped");
}

function linkPath(L, id) {
  const m = L.nodes.manager, a = L.nodes[id];
  return `M${m.x} ${m.y + m.h / 2} L${a.x} ${a.y - a.h / 2}`;
}

function agentMapHtml() {
  const L = mapLayout();
  const names = STR[store.lang].agents;
  const box = (n) => `<rect x="${n.x - n.w / 2}" y="${n.y - n.h / 2}" width="${n.w}" height="${n.h}" rx="10"/>`;
  const agentNode = (id) => {
    const n = L.nodes[id], top = n.y - n.h / 2, left = n.x - n.w / 2 + 14, bw = n.w - 28;
    return `<g class="map-node" id="node-${id}">${box(n)}
      <text class="node-name" x="${n.x}" y="${top + 21}" text-anchor="middle">${esc(names[id][0])}</text>
      <text class="node-status" id="status-${id}" x="${n.x}" y="${top + 39}" text-anchor="middle">${esc(t("idle"))}</text>
      <rect class="bar-track" x="${left}" y="${top + 50}" width="${bw}" height="5" rx="2.5"/>
      <rect class="bar-fill" id="bar-${id}" x="${left}" y="${top + 50}" width="0" height="5" rx="2.5" fill="url(#bar-g)" data-max="${bw}"/>
      <text class="node-tokens" id="tok-${id}" x="${n.x}" y="${top + 72}" text-anchor="middle">0 tok · $0.0000</text></g>`;
  };
  const g = L.nodes.gate, gt = g.y - g.h / 2, p = L.nodes.plan, pt = p.y - p.h / 2;
  const checks = ["draft", "plan", "budget"];
  return `<div class="agent-map glass" id="agent-map" data-layout="${L === MAP_LAYOUTS.narrow ? "narrow" : "wide"}">
    ${sceneHtml(L === MAP_LAYOUTS.narrow)}
    <div class="rain" aria-hidden="true">${Array.from({ length: 14 }, (_, i) =>
      `<span style="left:${((i * 7.3) + 3) % 100}%;animation-delay:${((i * 0.37) % 2.4).toFixed(2)}s;animation-duration:${(1.6 + (i % 5) * 0.25).toFixed(2)}s"></span>`).join("")}</div>
    <svg viewBox="${L.view}" role="img" aria-label="${esc(t("mapAria"))}">
      <defs>
        <linearGradient id="bar-g" x1="0" x2="1"><stop offset="0%" stop-color="#F2785C"/><stop offset="100%" stop-color="#FFB347"/></linearGradient>
        ${["dim", "lit"].map((v) => `<marker id="rev-arrow-${v}" viewBox="0 0 10 10" refX="10" refY="5" markerUnits="userSpaceOnUse"
          markerWidth="10" markerHeight="10" orient="auto"><path d="M0 0 L10 5 L0 10 z" class="rev-head-${v}"/></marker>`).join("")}
      </defs>
      ${WORKERS.map((id) => `<path class="map-link" id="link-${id}" d="${linkPath(L, id)}"/>`).join("")}
      <path class="map-link" id="link-gate" d="${L.toGate}"/><path class="map-link" id="link-plan" d="${L.toPlan}"/>
      <path class="map-rev" id="rev-path" d="${L.revision}" marker-end="url(#rev-arrow-dim)"/>
      <g class="rev-badge" id="rev-badge"><rect class="rev-pill" id="rev-pill" rx="8"/>
        <text class="rev-label" id="rev-label" x="${L.revLabel[0]}" y="${L.revLabel[1]}" text-anchor="middle" dominant-baseline="middle">${esc(t("revisionLabel"))}</text></g>
      ${AGENTS.map(agentNode).join("")}
      <g class="map-node gate" id="node-gate">${box(g)}
        <text class="node-name" x="${g.x}" y="${gt + 20}" text-anchor="middle">${esc(t("gateTitle"))}</text>
        ${checks.map((c, i) => `<text class="check" id="check-${c}" x="${g.x}" y="${gt + 40 + i * 15}" text-anchor="middle">${esc(t("check_" + c))} —</text>`).join("")}</g>
      <g class="map-node plan" id="node-plan">${box(p)}
        <text class="node-name" x="${p.x}" y="${pt + 26}" text-anchor="middle">${esc(t("planNode"))}</text>
        <text class="node-status" id="status-plan" x="${p.x}" y="${pt + 46}" text-anchor="middle">—</text></g>
      <text class="team-total" id="team-total" x="${L.team[0]}" y="${L.team[1]}" text-anchor="${L.teamAnchor}">${esc(t("team"))}: 0 tok · $0.0000</text>
    </svg></div>`;
}

function fitMapText() {
  const label = document.getElementById("rev-label"), pill = document.getElementById("rev-pill");
  try {
    const b = label.getBBox();
    pill.setAttribute("x", (b.x - 9).toFixed(1)); pill.setAttribute("y", (b.y - 4).toFixed(1));
    pill.setAttribute("width", (b.width + 18).toFixed(1)); pill.setAttribute("height", (b.height + 8).toFixed(1));
  } catch { /* not rendered yet */ }
  document.querySelectorAll("#agent-map .node-name, #agent-map .node-status").forEach((el) => {
    const node = el.closest(".map-node")?.querySelector("rect");
    const max = node ? Number(node.getAttribute("width")) - 14 : 0;
    try { if (max && el.getComputedTextLength() > max) { el.setAttribute("textLength", max); el.setAttribute("lengthAdjust", "spacingAndGlyphs"); } } catch { /* not rendered yet */ }
  });
}

function pulse(pathId, reverse, ts) {
  if (!ts.animate || REDUCED_MOTION.matches || document.hidden) return;
  const path = document.getElementById(pathId);
  const svg = path?.ownerSVGElement;
  if (!path || !svg) return;
  const len = path.getTotalLength();
  const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  dot.setAttribute("r", "5"); dot.setAttribute("class", "pulse");
  svg.appendChild(dot);
  const start = performance.now();
  const step = (now) => {
    const p = Math.min(1, (now - start) / 650);
    const pt = path.getPointAtLength(len * (reverse ? 1 - p : p));
    dot.setAttribute("cx", pt.x); dot.setAttribute("cy", pt.y);
    dot.setAttribute("opacity", String(p < 0.85 ? 1 : (1 - p) / 0.15));
    if (p < 1) requestAnimationFrame(step); else dot.remove();
  };
  requestAnimationFrame(step);
  setTimeout(() => dot.remove(), 1500);  // never leave a dot behind if frames pause
}

function setCheck(name, ok) {
  const el = document.getElementById(`check-${name}`);
  if (!el) return;
  el.textContent = `${t("check_" + name)} ${ok ? "✓" : "✗"}`;
  el.setAttribute("class", `check ${ok ? "check-ok" : "check-bad"}`);
}

const SPENDING_ISSUES = ["spending_exceeds_cash", "zero_stock_up_mentioned", "affordability_unknown"];

function mapApply(ts, e) {
  const map = document.getElementById("agent-map");
  if (!map) return;
  const node = (id) => document.getElementById(`node-${id}`);
  const status = (id, text) => { const el = document.getElementById(`status-${id}`); if (el) el.textContent = text; };
  if (e.type === "run_started") map.classList.add("raining");
  if (e.type === "agent_started" && WORKERS.includes(e.agent)) {
    document.getElementById(`link-${e.agent}`)?.classList.add("active");
    pulse(`link-${e.agent}`, false, ts);
    if (e.agent === "planner" && e.run > 1) {  // the Critic asked for a revision
      const rev = document.getElementById("rev-path");
      rev?.classList.add("lit");
      rev?.setAttribute("marker-end", "url(#rev-arrow-lit)");
      document.getElementById("rev-label")?.classList.add("lit");
      document.getElementById("rev-badge")?.classList.add("lit");
      pulse("rev-path", false, ts);
    }
  }
  if (e.type === "agent_finished" && WORKERS.includes(e.agent)) {
    pulse(`link-${e.agent}`, true, ts);
    later(() => document.getElementById(`link-${e.agent}`)?.classList.remove("active"), 700);
  }
  if (e.type === "tool_called" && AGENTS.includes(e.agent) && !e.tool.startsWith("run_")) {
    const L = mapLayout();
    status(e.agent, e.tool.length > L.toolChars ? `${e.tool.slice(0, L.toolChars - 1)}…` : e.tool);
    ts.toolShown[e.agent] = true;
  }
  if (e.type === "model_call" && ts.usage[e.agent]) {
    const u = ts.usage[e.agent];
    u.tokens += (e.call.input_tokens || 0) + (e.call.output_tokens || 0);
    u.cost += e.call.cost_usd || 0;
    const scale = Math.max(0.008, ...AGENTS.map((a) => ts.usage[a].cost));
    AGENTS.forEach((a) => {
      const bar = document.getElementById(`bar-${a}`);
      if (bar) bar.setAttribute("width", (Number(bar.dataset.max) * Math.min(1, ts.usage[a].cost / scale)).toFixed(1));
      const tok = document.getElementById(`tok-${a}`);
      if (tok) tok.textContent = `${num(ts.usage[a].tokens)} tok · $${ts.usage[a].cost.toFixed(4)}`;
    });
  }
  if (e.type === "tool_result" && e.tool === "verify_draft" && "ok" in (e.result || {})) {
    setCheck(e.agent === "critic" ? "draft" : "plan", e.result.ok);
    pulseGate();
  }
  if (e.type === "code_check") { setCheck("draft", e.ok); pulseGate(); }
  if (e.type === "final_check") {
    setCheck("plan", e.ok);
    setCheck("budget", !(e.issues || []).some((i) => SPENDING_ISSUES.includes(i)));
    pulse("link-gate", false, ts); pulseGate();
  }
  if (e.type === "run_finished") {
    map.classList.remove("raining");
    const cls = e.status === "completed" ? "plan-ok" : e.status === "completed_with_warning" ? "plan-warn" : "plan-stop";
    node("plan")?.classList.add(cls);
    status("plan", e.status === "completed" ? `✓ ${t("done")}` : e.status === "completed_with_warning" ? `⚠ ${t("done")}` : "⛔");
    if (e.status?.startsWith("completed")) pulse("link-plan", false, ts);
  }
  if (e.type === "translation" && !e.error) status("plan", "✓ ES + EN");
  if (e.type === "limit_hit" && e.action === "stopped") { map.classList.remove("raining"); node("plan")?.classList.add("plan-stop"); status("plan", "⛔"); }
  sceneApply(ts, e, map);
  // node states
  const current = ts.stack[ts.stack.length - 1];
  AGENTS.forEach((id) => {
    const el = node(id);
    if (!el) return;
    const working = id === current;
    const waiting = !working && ts.stack.includes(id);
    el.classList.toggle("working", working);
    el.classList.toggle("done", !working && !waiting && ts.done.has(id));
    if (!working) status(id, waiting ? t("waiting") : ts.done.has(id) ? t("done") : t("idle"));
    else if (!ts.toolShown[id]) status(id, t("working"));
  });
  if (e.totals) {
    const team = document.getElementById("team-total");
    if (team) team.textContent = `${t("team")}: ${num(e.totals.total_tokens)} tok · $${Number(e.totals.cost_usd || 0).toFixed(4)}`;
  }
}

function pulseGate() {
  const gate = document.getElementById("node-gate");
  if (!gate) return;
  gate.classList.add("flash");
  setTimeout(() => gate.classList.remove("flash"), 900);
}

function traceHtml(code, mode) {
  return `
    ${mode === "stopped" ? "" : `<div class="trace-head">
      <div><h1 style="font-size:24px">${esc(mode === "replay" ? t("replayTitle") : t("traceTitle"))}</h1>
        <span class="plan-code">${esc(code)}</span></div>
      <div class="btn-row" id="trace-controls"></div>
    </div>`}
    ${mode === "live" ? `<p class="muted">${esc(t("traceText"))}</p>` : ""}
    ${agentMapHtml()}
    <p class="map-caption">${esc(t("sceneCaption"))}</p>
    <div class="counter glass">
      <div><span>${esc(t("inTok"))}</span><b id="c-in">0</b></div>
      <div><span>${esc(t("cachedTok"))}</span><b id="c-cached">0</b></div>
      <div><span>${esc(t("outTok"))}</span><b id="c-out">0</b></div>
      <div><span>${esc(t("cost"))}</span><b id="c-cost">$0.0000</b></div>
    </div>
    <ol class="timeline glass" id="timeline" aria-label="Trace"></ol>`;
}

function newTraceState(animate = true) {
  return { stack: [], done: new Set(), animate, toolShown: {}, seen: [], stones: 0, sceneEnd: null,
           usage: Object.fromEntries(AGENTS.map((a) => [a, { tokens: 0, cost: 0 }])) };
}

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
    case "code_check": return [`code check of the draft: ${e.ok ? "ok" : (e.issues || []).join(", ")}`, e.ok ? "ok" : "limit"];
    case "translation": return [e.error ? `translation failed: ${e.error}` : `translation → ${e.language}: ${num(e.usage?.output_tokens)} out · $${Number(e.usage?.cost_usd || 0).toFixed(4)}`, e.error ? "limit" : "ok"];
    case "run_finished": return [`${t("runFinished")}: ${e.status}`, e.status?.startsWith("completed") ? "ok" : "limit"];
    default: return [e.type, ""];
  }
}

function trackEvent(ts, e) {
  if (e.type === "agent_started") { ts.stack.push(e.agent); ts.toolShown[e.agent] = false; }
  if (e.type === "agent_finished") { ts.stack = ts.stack.filter((a, i) => !(a === e.agent && i === ts.stack.lastIndexOf(e.agent))); ts.done.add(e.agent); }
  if (e.type === "run_finished") ts.stack = [];
}

function applyEvent(ts, e) {
  trackEvent(ts, e);
  ts.seen.push(e);
  mapApply(ts, e);
  const tot = e.totals || {};
  const set = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
  if (e.totals) {
    set("c-in", num(tot.input_tokens)); set("c-cached", num(tot.cached_input_tokens)); set("c-out", num(tot.output_tokens));
    set("c-cost", `$${Number(tot.cost_usd || 0).toFixed(4)}`);
  }
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
  fitMapText();
  document.getElementById("trace-controls").innerHTML = `<span class="spinner" aria-hidden="true"></span>`;
  const ts = state.trace = newTraceState(false);  // events that already happened are drawn without pulses
  let last = 0;
  const take = (events) => events.forEach((e) => { applyEvent(ts, e); last = Math.max(last, e.seq); });
  take(initial.events || []);
  ts.animate = true;
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
  fitMapText();
  const events = data.events || [];
  let speed = 1;
  const controls = document.getElementById("trace-controls");
  controls.innerHTML = `<div class="segmented" role="group" aria-label="${esc(t("speed"))}" style="min-width:120px">
      <button type="button" data-speed="1" aria-pressed="true">1×</button><button type="button" data-speed="4" aria-pressed="false">4×</button></div>
    <button class="btn" type="button" id="skip-btn">${esc(t("skip"))}</button>`;
  const ts = state.trace = newTraceState();
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

// "consulta sus canales…" -> "Consulta sus canales…."; citations in brackets don't count as text.
function asSentence(text) {
  let s = text.trim().replace(/^([\s*_"“(¿¡]*)(\p{Ll})/u, (m, lead, ch) => lead + ch.toUpperCase());
  const prose = s.replace(/\s*\[[^\]]*\]/g, "").trim();
  if (prose && !/[.!?…:]["”)]*$/.test(prose)) s += ".";
  return s;
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
      ${p.parts.length ? p.parts.map((x) => `<p>${inline(asSentence(x), fn)}</p>`).join("") : '<p class="muted">—</p>'}
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

function languageNote(textLang) {
  if (!textLang || textLang === store.lang) return "";
  return `<div class="d">${esc(t(textLang === "en" ? "sourceInEnglish" : "sourceInSpanish"))}</div>`;
}

function sourceTitle(d) { return typeof d.title === "object" ? (d.title[store.lang] || d.title.en) : d.title; }

function showFootnote(btn) {
  const id = btn.dataset.id;
  const d = (state.view?.sourceDetails || {})[id];
  fnPop.innerHTML = d ? `<div class="t">${esc(sourceTitle(d))}</div>
      ${d.date ? `<div class="d">${esc(shortDate(d.date))}</div>` : ""}
      <q>${esc(store.lang === "es" ? d.fact_es : d.fact_en)}</q>${languageNote(store.lang === "es" ? d.lang_es : d.lang_en)}
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

// ------------------------------------------------------------------ plan view for every owner
// Big cards, checklist, pictures, glossary, read-aloud, text size, share and print. Everything comes
// from the saved plan (its filled text, facts and source details): nothing here calls the model.

Object.assign(STR.es, {
  topTitle: "Lo más importante esta semana", noCost: "Sin costo", costLabel: "Costo",
  checklistTitle: "Tu lista de acciones", progress: (d, n) => `${d} de ${n} hechas`,
  allDone: "¡Listo! Hiciste todas las acciones de tu plan. Tu negocio está mejor preparado.",
  purchasesGroup: "Compras", listen: "Escuchar el plan", pauseListen: "Pausar", resumeListen: "Seguir", stopListen: "Detener",
  speedLabel: "Velocidad", textSmaller: "Letra más pequeña", textBigger: "Letra más grande",
  shareWhatsApp: "Compartir por WhatsApp", print: "Imprimir", fullDetails: "Ver todo el detalle",
  numbersTitle: "Tus números en dibujos", glossaryTitle: "¿Qué significa?",
  shelfCaption: (a, b) => `${a} de ${b} de tu mercadería está a menos de 1 metro del piso.`,
  jarCaption: (a, b, w) => `Después de tus compras tienes ${a}. Tu fondo para ${w} debe llegar a ${b}.`,
  jarFull: "Tu fondo de emergencia está completo.", gapLabel: "Faltan", goalLabel: "Meta",
  budgetCaption: (a, b, c) => `Gastas ${a} de tu presupuesto de ${b}; te quedan ${c}.`, leftLabel: "Queda",
  waIntro: (code) => `Mi plan Pirca para El Niño costero (código ${code}). Lo más importante esta semana:`,
  waOpen: "Ver el plan completo:", printTitle: "Mi plan Pirca", meter: "1 m",
});
Object.assign(STR.en, {
  topTitle: "Most important this week", noCost: "No cost", costLabel: "Cost",
  checklistTitle: "Your action checklist", progress: (d, n) => `${d} of ${n} done`,
  allDone: "Done! You completed every action in your plan. Your shop is better prepared.",
  purchasesGroup: "Purchases", listen: "Listen to the plan", pauseListen: "Pause", resumeListen: "Resume", stopListen: "Stop",
  speedLabel: "Speed", textSmaller: "Smaller text", textBigger: "Bigger text",
  shareWhatsApp: "Share on WhatsApp", print: "Print", fullDetails: "See full details",
  numbersTitle: "Your numbers in pictures", glossaryTitle: "What does it mean?",
  shelfCaption: (a, b) => `${a} of your ${b} of stock is less than 1 meter above the floor.`,
  jarCaption: (a, b, w) => `After your purchases you have ${a}. Your fund for ${w} should reach ${b}.`,
  jarFull: "Your emergency fund is complete.", gapLabel: "Gap", goalLabel: "Goal",
  budgetCaption: (a, b, c) => `You spend ${a} of your ${b} budget; ${c} is left.`, leftLabel: "Left",
  waIntro: (code) => `My Pirca plan for coastal El Niño (code ${code}). Most important this week:`,
  waOpen: "See the full plan:", printTitle: "My Pirca plan", meter: "1 m",
});

// Plain-words explanations (no figures), tap to open.
const GLOSSARY = {
  es: [
    ["ENFEN", "El comité oficial del Perú que vigila El Niño y La Niña en el mar. Publica comunicados con el estado de alerta."],
    ["El Niño costero", "Cuando el mar frente a la costa norte del Perú se calienta. Puede traer lluvias fuertes, ríos desbordados e inundaciones en Piura, como pasó en 1998 y 2017."],
    ["SENAMHI", "El servicio oficial del clima del Perú. Da los avisos de lluvias fuertes y del nivel de los ríos."],
    ["INDECI", "El Instituto Nacional de Defensa Civil. Coordina la ayuda en emergencias. Si hay que evacuar, lo indican INDECI y tu municipalidad."],
    ["Fondo de emergencia", "Dinero que separas para pagar tus gastos fijos (alquiler, sueldos, servicios) si tienes que cerrar unas semanas por una inundación."],
    ["Mercadería en riesgo", "El valor de los productos que guardas a menos de 1 metro del piso. Es lo que el agua podría mojar si entra a tu tienda."],
  ],
  en: [
    ["ENFEN", "Peru's official committee that watches El Niño and La Niña in the ocean. It publishes statements with the current alert level."],
    ["Coastal El Niño", "When the sea off Peru's northern coast gets warmer. It can bring heavy rain, overflowing rivers and floods in Piura, as in 1998 and 2017."],
    ["SENAMHI", "Peru's official weather service. It issues warnings about heavy rain and river levels."],
    ["INDECI", "Peru's National Civil Defense Institute. It coordinates help in emergencies. If people must evacuate, INDECI and your municipality say so."],
    ["Emergency fund", "Money you set aside to pay your fixed costs (rent, wages, utilities) if you have to close for a few weeks because of a flood."],
    ["Stock at risk", "The value of the goods you keep less than 1 meter above the floor. It is what water could reach if it enters your shop."],
  ],
};

const CAT_ICONS = { "CAT-01": "🗄️", "CAT-02": "🧱", "CAT-03": "📦", "CAT-04": "🚪", "CAT-05": "⬆️", "CAT-06": "💰", "CAT-07": "💾",
  "CAT-08": "🛒", "CAT-09": "🦟", "CAT-10": "🛡️", "CAT-11": "🏠", "CAT-12": "⚡", "CAT-13": "🎒", "CAT-14": "📱", "CAT-15": "🔦" };
const WORD_ICONS = [[/proveedor|supplier|entrega|deliver/i, "🚚"], [/caja|cash|fondo|fund|ahorra|save/i, "💰"],
  [/indeci|senamhi|enfen|alerta|alert|aviso|municipal/i, "📢"], [/agua|water|inund|flood/i, "💧"], [/luz|power|el[eé]ctric/i, "⚡"],
  [/mercader|stock/i, "📦"]];
const PHASE_ICONS = ["⏰", "📢", "🌧️", "🧹"];
const CAT_RE = /CAT-\d{2}/g;
const SENTENCE_SPLIT = /(?<=[.!?](?:\s*\[[^\]]*\])?)\s+(?=[\p{Lu}¿¡])/u;

function plainText(text) {
  return text.replace(/\s*\[[^\]]*\]/g, "").replace(/\*/g, "").replace(/\s+/g, " ").trim();
}

function planSections(md) {
  const secs = {};
  let cur = null;
  md.replace(/\r/g, "").split("\n").forEach((line) => {
    const h = line.match(/^##\s+(\d+)[.)]\s*(.*)$/);
    if (h) { cur = h[1]; secs[cur] = { title: h[2].trim(), lines: [] }; return; }
    if (cur && !/^\\\*|^_.*_$/.test(line.trim())) secs[cur].lines.push(line);  // not the footnote/disclaimer
  });
  return secs;
}

// Actions from the filled plan: section 2 sentences (grouped by moment) and section 6 purchases.
// IDs are positions (s<phase>-<n>) or catalog IDs, the same in both languages, so the checklist survives a language switch.
function planActions(md, facts) {
  const secs = planSections(md);
  const steps = [];
  const counters = {};
  let phase = 0;
  (secs["2"]?.lines || []).forEach((line) => {
    const b = line.match(/^\s*[-+*]\s+(.*)$/);
    if (!b) return;
    const raw = b[1].replace(/^\*\*(.+?)\*\*/, "$1");
    const m = raw.match(/^([^:]{2,60}):\s*([\s\S]*)$/);
    const p = m ? phaseOf(m[1].replace(/\*/g, "")) : -1;
    if (p >= 0) phase = p;
    (p >= 0 ? m[2] : raw).split(SENTENCE_SPLIT).forEach((s) => {
      const text = plainText(s);
      if (!text.replace(/[.\s]/g, "")) return;
      counters[phase] = (counters[phase] || 0) + 1;
      steps.push({ id: `s${phase}-${counters[phase]}`, phase, text: asSentence(text), cats: [...new Set(s.match(CAT_RE) || [])] });
    });
  });
  const buys = [];
  (secs["6"]?.lines || []).forEach((line) => {
    const b = line.match(/^\s*[-+*]\s+(.*)$/);
    const cat = b && (b[1].match(CAT_RE) || [])[0];
    if (!cat) return;
    const costText = (b[1].match(/\(([^)]*)\)\s*(?:\[|$)/) || [])[1] || "";
    const name = plainText(b[1].replace(/\s*\([^)]*\)\s*(?=\[|$)/, ""));
    buys.push({ id: `buy-${cat}`, cat, name, costText, cost: facts[`cat_${cat.slice(4)}_cost`], text: name });
  });
  return { steps, buys };
}

function actionIcon(a) {
  for (const c of a.cats || [a.cat]) if (CAT_ICONS[c]) return CAT_ICONS[c];
  return (WORD_ICONS.find(([re]) => re.test(a.text)) || [null, "✅"])[1];
}

// The cost a card shows: catalog actions it cites that have a price in the plan's facts.
function actionCost(a, buys, facts, details) {
  const priced = (a.cats || [a.cat]).filter((c) => facts[`cat_${c.slice(4)}_cost`] !== undefined);
  if (!priced.length) return t("noCost");
  const total = priced.reduce((sum, c) => sum + Number(facts[`cat_${c.slice(4)}_cost`]), 0);
  const names = priced.map((c) => buys.find((b) => b.cat === c)?.name || sourceTitle(details[c] || { title: c }));
  return a.cat ? (a.costText || money(total)) : `${money(total)} · ${names.join(", ")}`;
}

function topActions(actions) {
  const now = actions.steps.filter((s) => s.phase === 0);
  return [...now, ...actions.buys].slice(0, 3);
}

const checksKey = (code) => `pirca.checks.${code}`;
function loadChecks(code) { try { return new Set(JSON.parse(localStorage.getItem(checksKey(code))) || []); } catch { return new Set(); } }
function saveChecks(code, set) { localStorage.setItem(checksKey(code), JSON.stringify([...set])); }

function checklistHtml(actions, checks, lang) {
  const groups = [0, 1, 2, 3].map((p) => ({ title: PHASE_NAMES[lang][p], icon: PHASE_ICONS[p], items: actions.steps.filter((s) => s.phase === p) }))
    .concat([{ title: t("purchasesGroup"), icon: "🛒", items: actions.buys }]).filter((g) => g.items.length);
  const item = (a) => `<li><label class="check-item">
      <input type="checkbox" data-action="${esc(a.id)}" ${checks.has(a.id) ? "checked" : ""}>
      <span class="check-box" aria-hidden="true"></span>
      <span class="check-text">${esc(a.text)}${a.costText ? ` <span class="muted">(${esc(a.costText)})</span>` : ""}</span></label></li>`;
  return groups.map((g) => `<div class="check-group"><h4><span aria-hidden="true">${g.icon}</span> ${esc(g.title)}</h4>
    <ul>${g.items.map(item).join("")}</ul></div>`).join("");
}

// ---- pictures (inline SVG, colors from the Warm Pacific theme)
function shelfSvg(f) {
  const total = Number(f.stock_value || 0), risk = Number(f.stock_at_risk || 0);
  const below = total ? Math.round(8 * Math.min(1, risk / total)) : 0;
  const boxes = Array.from({ length: 8 }, (_, i) => {
    const row = 3 - Math.floor(i / 2), x = 52 + (i % 2) * 46, y = 22 + row * 30;
    const wet = i < below;   // boxes are numbered from the floor up
    return `<rect x="${x}" y="${y}" width="38" height="22" rx="3" class="${wet ? "box wet" : "box"}"/>`;
  }).join("");
  return `<svg viewBox="0 0 200 150" class="pic" role="img" aria-label="${esc(STR[store.lang].shelfCaption(money(risk), money(total)))}">
    <rect x="40" y="10" width="110" height="128" rx="4" class="shelf-frame"/>
    ${[44, 74, 104, 134].map((y) => `<line x1="40" x2="150" y1="${y}" y2="${y}" class="shelf-board"/>`).join("")}
    ${boxes}
    <rect x="30" y="82" width="140" height="56" class="water"/>
    <line x1="22" x2="178" y1="82" y2="82" class="water-line"/>
    <text x="176" y="78" text-anchor="end" class="pic-label">${esc(t("meter"))}</text>
    <line x1="30" x2="170" y1="138" y2="138" class="floor"/>
  </svg>`;
}

function jarSvg(f) {
  const goal = Number(f.buffer_needed || 0), have = Math.max(0, Number(f.cash_after_purchases ?? f.cash_on_hand ?? 0));
  const frac = goal ? Math.min(1, have / goal) : 1;
  const top = 30, bottom = 136, h = bottom - top, fillY = bottom - h * frac;
  return `<svg viewBox="0 0 200 150" class="pic" role="img" aria-label="${esc(t("fundGap"))}">
    <defs><clipPath id="jar-clip"><path d="M62 30 H138 Q150 30 150 44 V128 Q150 136 140 136 H60 Q50 136 50 128 V44 Q50 30 62 30 Z"/></clipPath></defs>
    <g clip-path="url(#jar-clip)">
      ${frac < 1 ? `<rect x="50" y="${top}" width="100" height="${(fillY - top).toFixed(1)}" class="jar-gap"/>` : ""}
      <rect x="50" y="${fillY.toFixed(1)}" width="100" height="${(bottom - fillY).toFixed(1)}" class="jar-fill"/>
    </g>
    <path d="M62 30 H138 Q150 30 150 44 V128 Q150 136 140 136 H60 Q50 136 50 128 V44 Q50 30 62 30 Z" class="jar"/>
    <rect x="66" y="18" width="68" height="12" rx="3" class="jar-lid"/>
    <line x1="44" x2="156" y1="${top}" y2="${top}" class="goal-line"/>
    <text x="158" y="${top + 4}" class="pic-label">${esc(t("goalLabel"))}</text>
    ${frac < 1 ? `<text x="100" y="${((top + fillY) / 2 + 4).toFixed(1)}" text-anchor="middle" class="pic-label gap-text">${esc(t("gapLabel"))} ${esc(money(Number(f.cash_gap || 0)))}</text>` : ""}
  </svg>`;
}

// Purchases are colored by what they protect (a classification of the catalog actions, shown in the key).
const PROTECT_GROUPS = [
  { id: "stock", color: "#2EC4B6", cats: ["CAT-01", "CAT-03", "CAT-05", "CAT-08"], label: { es: "Mercadería", en: "Stock" } },
  { id: "building", color: "#E9C46A", cats: ["CAT-02", "CAT-04", "CAT-10", "CAT-11"], label: { es: "Tu local", en: "Shop building" } },
  { id: "power", color: "#6EC3E8", cats: ["CAT-07", "CAT-12", "CAT-15"], label: { es: "Luz y registros", en: "Power and records" } },
  { id: "health", color: "#F2785C", cats: ["CAT-09", "CAT-13"], label: { es: "Salud", en: "Health" } },
];
const OTHER_GROUP = { id: "other", color: "#A9B6C6", cats: [], label: { es: "Otros", en: "Other" } };
const protectGroup = (cat) => PROTECT_GROUPS.find((g) => g.cats.includes(cat)) || OTHER_GROUP;
const byProtectGroup = (buys) => [...PROTECT_GROUPS, OTHER_GROUP]
  .map((g) => ({ group: g, items: buys.filter((b) => protectGroup(b.cat) === g) })).filter((x) => x.items.length);

function budgetSvg(f, buys) {
  const budget = Number(f.budget || 0) || buys.reduce((s, b) => s + Number(b.cost || 0), 0) + Number(f.money_left || 0);
  const W = 180;
  let x = 10;
  const parts = byProtectGroup(buys).flatMap(({ group, items }) => items.map((b) => {
    const w = budget ? (W * Number(b.cost || 0)) / budget : 0;
    const seg = `<rect x="${x.toFixed(1)}" y="52" width="${Math.max(0, w - 1).toFixed(1)}" height="40" rx="3" class="buy" fill="${group.color}"
      data-buy="${esc(b.cat)}" tabindex="0" role="button" aria-label="${esc(b.name)}: ${esc(money(Number(b.cost || 0)))}"><title>${esc(b.name)}: ${esc(money(Number(b.cost || 0)))}</title></rect>`;
    x += w;
    return seg;
  })).join("");
  return `<svg viewBox="0 0 200 150" class="pic budget-pic" role="img" aria-label="${esc(t("purchases"))}">
    <rect x="10" y="52" width="${W}" height="40" rx="4" class="budget-track"/>
    ${parts}
    <text x="10" y="40" class="pic-label">0</text>
    <text x="190" y="40" text-anchor="end" class="pic-label">${esc(money(budget))}</text>
    ${Number(f.money_left || 0) > 0 ? `<line x1="${x.toFixed(1)}" x2="${x.toFixed(1)}" y1="94" y2="104" class="goal-line"/>
      <text x="190" y="116" text-anchor="end" class="pic-label">${esc(t("leftLabel"))} ${esc(money(Number(f.money_left)))}</text>` : ""}
  </svg>`;
}

// Key under the bar: one line per purchase (color dot, name, cost), grouped by what it protects.
function budgetKeyHtml(buys) {
  return `<div class="budget-key">${byProtectGroup(buys).map(({ group, items }) => `<div class="key-group">
    <div class="key-group-name"><span class="key-dot" style="background:${group.color}" aria-hidden="true"></span>${esc(L(group.label))}</div>
    <ul>${items.map((b) => `<li data-buy="${esc(b.cat)}" tabindex="0"><span class="key-dot" style="background:${group.color}" aria-hidden="true"></span>
      <span class="key-name">${esc(b.name)}</span><span class="key-cost">${esc(money(Number(b.cost || 0)))}</span></li>`).join("")}</ul></div>`).join("")}</div>`;
}

// Hover or tap a block (or a key line) to highlight both; tapping again or elsewhere clears it.
function wireBudgetKey() {
  const fig = app.querySelector(".budget-figure");
  if (!fig) return;
  let pinned = null;
  const show = (cat) => {
    fig.classList.toggle("has-focus", Boolean(cat));
    fig.querySelectorAll("[data-buy]").forEach((el) => el.classList.toggle("focus", el.dataset.buy === cat));
  };
  fig.addEventListener("pointerover", (e) => { const el = e.target.closest?.("[data-buy]"); if (el && e.pointerType === "mouse" && !pinned) show(el.dataset.buy); });
  fig.addEventListener("pointerout", (e) => { if (e.target.closest?.("[data-buy]") && e.pointerType === "mouse" && !pinned) show(null); });
  fig.addEventListener("click", (e) => {
    const el = e.target.closest("[data-buy]");
    pinned = el && pinned !== el.dataset.buy ? el.dataset.buy : null;
    show(pinned);
  });
  fig.addEventListener("focusin", (e) => { const el = e.target.closest?.("[data-buy]"); if (el) show(el.dataset.buy); });
  fig.addEventListener("focusout", () => { if (!pinned) show(null); });
}

// ---- read aloud with the browser's own voices (speechSynthesis); hidden when there is no voice for the language
const speech = { queue: [], index: 0, playing: false, paused: false, rate: 1, token: 0 };

function voiceFor(lang) {
  const voices = window.speechSynthesis?.getVoices() || [];
  const mine = voices.filter((v) => v.lang?.toLowerCase().startsWith(lang));
  const prefer = lang === "es" ? ["es-pe", "es-419", "es-us", "es-mx", "es-es"] : ["en-us", "en-gb"];
  return prefer.map((p) => mine.find((v) => v.lang.toLowerCase() === p)).find(Boolean) || mine[0] || null;
}

// What is read: the displayed plan, without footnote IDs, asterisks or Markdown marks; amounts read as words.
// One sentence per utterance, so pausing and resuming loses little and long lines are never cut off.
const AMOUNT = "(\\d[\\d,]*(?:\\.\\d+)?)";
function speechChunks(md, lang) {
  const currencyWords = lang === "es" ? ["soles", "dólares"] : ["soles", "dollars"];
  return md.replace(/\r/g, "").split("\n")
    .map((line) => line.replace(/^>\s?/, "").replace(/^#{1,6}\s+\d+[.)]\s*/, "").replace(/^#{1,6}\s+/, "").replace(/^\s*[-+*]\s+/, ""))
    .map((line) => line.replace(/\\\*/g, "").replace(/\s*\[[^\]]*\]/g, "").replace(/\*\*|\*|_/g, "")
      .replace(new RegExp(`S/\\s?${AMOUNT}`, "g"), `$1 ${currencyWords[0]}`)
      .replace(new RegExp(`(?:US)?\\$\\s?${AMOUNT}`, "g"), `$1 ${currencyWords[1]}`).trim())
    .flatMap((line) => line.split(/(?<=[.!?])\s+/))
    .filter((line) => line.replace(/[—\-–\s.]/g, ""));
}

function stopSpeech() {
  speech.playing = false; speech.paused = false; speech.token += 1;
  if (window.speechSynthesis) window.speechSynthesis.cancel();
  updateListenUi();
}

function speakFrom(i) {
  const synth = window.speechSynthesis;
  if (!synth || i >= speech.queue.length) { stopSpeech(); return; }
  speech.index = i;
  const token = speech.token;  // a cancel (stop, new speed) fires "end" on the old sentence; ignore it
  const u = new SpeechSynthesisUtterance(speech.queue[i]);
  u.voice = speech.voice; u.lang = speech.voice?.lang || speech.lang; u.rate = speech.rate;
  u.onend = () => { if (token === speech.token && speech.playing) speakFrom(i + 1); };
  synth.speak(u);
}

function updateListenUi() {
  const btn = document.getElementById("listen-btn");
  if (!btn) return;
  btn.textContent = speech.playing ? (speech.paused ? `▶ ${t("resumeListen")}` : `⏸ ${t("pauseListen")}`) : `🔊 ${t("listen")}`;
  btn.setAttribute("aria-pressed", String(speech.playing && !speech.paused));
  const stop = document.getElementById("listen-stop");
  if (stop) stop.hidden = !speech.playing;
}

function setupListen(md, lang) {
  const wrap = document.getElementById("listen-wrap");
  if (!wrap || !window.speechSynthesis) return;
  const ready = () => {
    const voice = voiceFor(lang);
    wrap.hidden = !voice;
    Object.assign(speech, { voice, lang, queue: speechChunks(md, lang) });
  };
  ready();
  window.speechSynthesis.addEventListener("voiceschanged", ready, { once: true });
  document.getElementById("listen-btn").addEventListener("click", () => {
    const synth = window.speechSynthesis;
    if (!speech.playing) { speech.token += 1; synth.cancel(); speech.playing = true; speech.paused = false; speakFrom(0); }
    // Pause = stop after remembering the sentence; resume = say that sentence again (pause() is unreliable in some browsers).
    else if (speech.paused) { speech.paused = false; speakFrom(speech.index); }
    else { speech.paused = true; speech.token += 1; synth.cancel(); }
    updateListenUi();
  });
  document.getElementById("listen-stop").addEventListener("click", stopSpeech);
  document.getElementById("listen-rate").addEventListener("change", (e) => {
    speech.rate = Number(e.target.value);
    if (speech.playing && !speech.paused) { const i = speech.index; speech.token += 1; window.speechSynthesis.cancel(); speakFrom(i); }
  });
  updateListenUi();
}
window.addEventListener("hashchange", () => stopSpeech());

// ---- text size (zoom on the plan view), remembered
const TEXT_SIZES = [0.9, 1, 1.15, 1.3, 1.5];
function textSize() { const v = Number(localStorage.getItem("pirca.textSize")); return TEXT_SIZES.includes(v) ? v : 1; }
function applyTextSize() { const el = document.getElementById("plan-easy"); if (el) el.style.zoom = String(textSize()); }

function updateProgress(actions, checks, celebrate) {
  const all = [...actions.steps, ...actions.buys];
  const done = all.filter((a) => checks.has(a.id)).length;
  const label = document.getElementById("check-progress");
  if (label) label.textContent = STR[store.lang].progress(done, all.length);
  const bar = document.getElementById("check-bar");
  if (bar) bar.style.width = `${all.length ? (100 * done) / all.length : 0}%`;
  const box = document.getElementById("all-done");
  if (box) {
    const finished = all.length > 0 && done === all.length;
    box.hidden = !finished;
    box.classList.toggle("celebrate", finished && celebrate && !REDUCED_MOTION.matches);
  }
}

function wirePlanEasy(code, actions, top, checks, planText, lang) {
  updateProgress(actions, checks, false);
  app.querySelectorAll(".action-list input[type=checkbox]").forEach((box) => box.addEventListener("change", () => {
    if (box.checked) checks.add(box.dataset.action); else checks.delete(box.dataset.action);
    saveChecks(code, checks);
    updateProgress(actions, checks, true);
  }));
  const step = (dir) => {
    const i = TEXT_SIZES.indexOf(textSize());
    localStorage.setItem("pirca.textSize", String(TEXT_SIZES[Math.max(0, Math.min(TEXT_SIZES.length - 1, i + dir))]));
    applyTextSize();
  };
  document.getElementById("text-smaller").addEventListener("click", () => step(-1));
  document.getElementById("text-bigger").addEventListener("click", () => step(1));
  // WhatsApp opens only on tap: a wa.me link with the plan code and the top 3 actions.
  document.getElementById("wa-btn").addEventListener("click", () => {
    window.open(`https://wa.me/?text=${encodeURIComponent(whatsappText(code, top))}`, "_blank", "noopener");
  });
  document.getElementById("print-btn").addEventListener("click", () => window.print());
  setupListen(planText, lang);
}

// ---- share and print
function whatsappText(code, top) {
  const lines = top.map((a, i) => `${i + 1}. ${a.text}`);
  return [STR[store.lang].waIntro(code), ...lines, "", `${t("waOpen")} ${location.origin}${location.pathname}#/plan/${code}`].join("\n");
}
window.addEventListener("beforeprint", () => document.documentElement.classList.add("printing"));
window.addEventListener("afterprint", () => document.documentElement.classList.remove("printing"));

function renderPlanView(code, data) {
  clearTimers();
  stopSpeech();
  hideFootnote();
  const r = data.result;
  const original = r.language || "es";
  const other = original === "es" ? "en" : "es";
  const view = state.view?.code === code ? state.view : { code, counted: false };
  state.view = view;
  view.sourceDetails = r.source_details || {};
  view.rerender = () => renderPlanView(code, data);
  // Every plan is saved in both languages; show the one that matches the interface.
  const available = (lang) => lang === original || Boolean(r.translations?.[lang]);
  const showing = available(store.lang) ? store.lang : original;
  const missing = showing !== store.lang;  // only older plans: the translation was never made
  const translation = showing === original ? null : r.translations?.[showing];
  const planText = translation ? translation.plan[store.currency] : r.plan[store.currency];
  const f = r.facts || {};
  const tr = r.translations || {};
  const toggleLabel = STR[store.lang].viewIn;
  const fn = { order: [], details: view.sourceDetails };
  const body = renderMarkdown(planText, fn, showing);
  const actions = planActions(planText, f);
  const top = topActions(actions);
  const checks = loadChecks(code);
  const S = STR[store.lang];
  const weeks = (planSections(planText)["4"]?.lines.join(" ").match(/\d+\s+(?:semanas?|weeks?)/) || [`${f.weeks_closed}`])[0];

  app.innerHTML = `<div id="plan-easy" class="plan-easy">
    <section class="plan-top glass">
      <div>
        <span class="muted small">${esc(t("planCode"))}</span><div class="plan-code">${esc(code)}</div>
        <div style="margin-top:12px">${enfenChip()}</div>
        <ul class="badges" aria-label="${esc(t("checksTitle"))}">${badgesFor(r).map((b) =>
          `<li class="${b.ok ? "" : "warn"}"><span class="icon" aria-hidden="true">${b.ok ? "✓" : "⚠"}</span>${esc(b.text)}</li>`).join("")}</ul>
      </div>
      ${gaugeSvg(r.risk_level)}
      <div class="btn-row">
        ${missing ? `<button class="btn" type="button" id="translate-btn">${esc(toggleLabel)}</button>` : ""}
        <button class="btn" type="button" id="replay-btn">${esc(t("replay"))}</button>
      </div>
    </section>
    <div class="easy-tools glass no-print" role="toolbar" aria-label="${esc(t("listen"))}">
      <span id="listen-wrap" class="tool-group" hidden>
        <button class="btn" type="button" id="listen-btn" aria-pressed="false">🔊 ${esc(t("listen"))}</button>
        <button class="btn" type="button" id="listen-stop" hidden>■ ${esc(t("stopListen"))}</button>
        <label class="small">${esc(t("speedLabel"))}
          <select id="listen-rate">${[0.8, 1, 1.2].map((v) => `<option value="${v}" ${v === speech.rate ? "selected" : ""}>${v}×</option>`).join("")}</select></label>
      </span>
      <span class="tool-group">
        <button class="btn" type="button" id="text-smaller" aria-label="${esc(t("textSmaller"))}" title="${esc(t("textSmaller"))}">A−</button>
        <button class="btn" type="button" id="text-bigger" aria-label="${esc(t("textBigger"))}" title="${esc(t("textBigger"))}">A+</button>
      </span>
      <span class="tool-group">
        <button class="btn" type="button" id="wa-btn">💬 ${esc(t("shareWhatsApp"))}</button>
        <button class="btn" type="button" id="print-btn">🖨️ ${esc(t("print"))}</button>
      </span>
    </div>
    <div class="print-head">${esc(t("printTitle"))} · <span class="plan-code">${esc(code)}</span></div>
    <section class="top-actions" aria-labelledby="top-title">
      <h2 id="top-title">${esc(t("topTitle"))}</h2>
      <ol class="top-cards">${top.map((a, i) => `<li class="top-card glass-read">
        <span class="top-icon" aria-hidden="true">${actionIcon(a)}</span>
        <div><span class="top-num">${i + 1}</span><p>${esc(a.text)}</p>
        <span class="top-cost">${esc(t("costLabel"))}: <b>${esc(actionCost(a, actions.buys, f, view.sourceDetails))}</b></span></div></li>`).join("")}</ol>
    </section>
    <section class="key-pictures" aria-label="${esc(t("numbersTitle"))}">
      <figure class="glass accent"><figcaption><span>${esc(t("stockAtRisk"))}</span><b data-count="${Number(f.stock_at_risk || 0)}">${esc(money(0))}</b></figcaption>
        ${shelfSvg(f)}<p class="pic-caption">${esc(S.shelfCaption(money(Number(f.stock_at_risk || 0)), money(Number(f.stock_value || 0))))}</p></figure>
      <figure class="glass accent"><figcaption><span>${esc(t("fundGap"))}</span><b data-count="${Number(f.cash_gap || 0)}">${esc(money(0))}</b></figcaption>
        ${jarSvg(f)}<p class="pic-caption">${esc(Number(f.cash_gap || 0) > 0 ? S.jarCaption(money(Number(f.cash_after_purchases ?? f.cash_on_hand ?? 0)), money(Number(f.buffer_needed || 0)), weeks) : t("jarFull"))}</p></figure>
      <figure class="glass budget-figure"><figcaption><span>${esc(t("purchases"))}</span><b data-count="${Number(f.total_cost || 0)}">${esc(money(0))}</b></figcaption>
        ${budgetSvg(f, actions.buys)}${budgetKeyHtml(actions.buys)}<p class="pic-caption">${esc(S.budgetCaption(money(Number(f.total_cost || 0)), money(Number(f.budget || 0)), money(Number(f.money_left || 0))))}</p></figure>
    </section>
    <section class="action-list glass-read" aria-labelledby="check-title">
      <div class="check-head"><h2 id="check-title">${esc(t("checklistTitle"))}</h2><span id="check-progress" class="check-count" aria-live="polite"></span></div>
      <div class="progress-bar" aria-hidden="true"><span id="check-bar"></span></div>
      ${checklistHtml(actions, checks, showing)}
      <div id="all-done" class="all-done" role="status" hidden>🎉 ${esc(t("allDone"))}</div>
    </section>
    <section class="glossary glass no-print" aria-labelledby="glossary-title">
      <h2 id="glossary-title">${esc(t("glossaryTitle"))}</h2>
      ${GLOSSARY[store.lang].map(([term, text]) => `<details><summary>${esc(term)}</summary><p>${esc(text)}</p></details>`).join("")}
    </section>
    <details class="plan-details no-print" id="plan-details" ${MAP_NARROW.matches ? "" : "open"}>
    <summary>${esc(t("fullDetails"))}</summary>
    ${store.lang === "en" && showing === "es" && r.summary_en ? `<section class="summary glass" lang="en"><h4>${esc(t("summaryTitle"))}</h4><p style="margin:0">${esc(r.summary_en)}</p></section>` : ""}
    ${translation && !translation.verification?.ok ? `<div class="notice glass-read" role="note">${esc(t("translationWarn"))}</div>` : ""}
    <article class="plan-body glass-read" lang="${showing}">${body}</article>
    ${sourcesListHtml(fn)}
    <section class="usage glass" style="margin-top:16px">
      <h4 style="font-size:13px;text-transform:uppercase;letter-spacing:.06em">${esc(t("usageTitle"))}</h4>
      <table><thead><tr><th>${esc(t("row"))}</th><th>${esc(t("calls"))}</th><th>${esc(t("input"))}</th><th>${esc(t("cached"))}</th><th>${esc(t("output"))}</th><th>USD</th></tr></thead>
      <tbody>${r.usage ? usageRow(t("runRow"), r.usage) : ""}${Object.entries(tr).map(([lang, x]) => usageRow(`${t("trRow")} (${lang})`, x.usage)).join("")}</tbody></table>
      ${store.currency === "usd" ? `<p class="small" style="margin:8px 0 0">${esc(STR[store.lang].fxNote(state.meta.pen_per_usd, state.meta.fx_date))}</p>` : ""}
    </section>
    </details></div>`;

  applyTextSize();
  wirePlanEasy(code, actions, top, checks, planText, showing);
  wireBudgetKey();

  countUp(!view.counted);
  view.counted = true;
  animateGauge(r.risk_level);
  document.getElementById("replay-btn").addEventListener("click", () => startReplay(code, data));
  // Fallback only: a plan saved before automatic translation can still be translated once.
  document.getElementById("translate-btn")?.addEventListener("click", async (e) => {
    e.target.disabled = true; e.target.textContent = t("viewing");
    try {
      const res = await api(`/api/plans/${code}/translate`, { method: "POST" });
      r.translations = { ...(r.translations || {}), [res.language]: res };
      // New citations may appear in the translation; refresh the source details.
      const fresh = await api(`/api/plans/${code}?after=999999`);
      r.source_details = fresh.result?.source_details || r.source_details;
    } catch (err) { console.warn(err); e.target.disabled = false; e.target.textContent = toggleLabel; return; }
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
  fitMapText();
  const ts = state.trace = newTraceState(false);
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
