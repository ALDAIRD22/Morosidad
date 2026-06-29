<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEDE COMAS ¡LOS MEJORES!</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Chart.js Datalabels Plugin -->
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0"></script>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: radial-gradient(circle at top right, #13113c 0%, #090d1f 60%, #02040a 100%);
        }
        .premium-card {
            background: rgba(10, 16, 32, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(20px);
        }
        .nav-card {
            transition: all 0.25s ease;
        }
        /* Barra de deslizamiento compacta e institucional */
        .custom-scroll::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .custom-scroll::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.5);
            border-radius: 8px;
        }
        .custom-scroll::-webkit-scrollbar-thumb {
            background: rgba(14, 165, 233, 0.4);
            border-radius: 8px;
        }
        .custom-scroll::-webkit-scrollbar-thumb:hover {
            background: rgba(14, 165, 233, 0.7);
        }
    </style>
</head>
<body class="text-slate-200 min-h-screen antialiased custom-scroll">

    <!-- PANTALLA DE BIENVENIDA (SPLASH SCREEN) -->
    <div id="welcome-overlay" class="fixed inset-0 z-[100] bg-slate-950 backdrop-blur-2xl flex items-center justify-center transition-opacity duration-700 opacity-100">
        <div class="text-center space-y-6 transform transition-all scale-100 animate-pulse" id="welcome-content">
            <div class="inline-flex items-center justify-center w-24 h-24 rounded-full bg-gradient-to-tr from-blue-600 to-cyan-500 shadow-[0_0_40px_rgba(14,165,233,0.4)] mb-2">
                <span class="text-5xl text-white font-black">V</span>
            </div>
            <h2 class="text-3xl font-extrabold text-white tracking-tight uppercase">SEDE COMAS ¡LOS MEJORES!</h2>
            <div class="flex flex-col items-center justify-center space-y-3 mt-6">
                <p id="welcome-loading" class="text-slate-400 font-medium tracking-widest uppercase text-sm">Procesando métricas en vivo...</p>
                <div id="welcome-stats" class="hidden flex-col items-center space-y-2 mt-2">
                    <p class="text-6xl font-black text-cyan-400 drop-shadow-[0_0_15px_rgba(34,211,238,0.3)]" id="welcome-avance">...%</p>
                    <div class="bg-cyan-500/10 border border-cyan-500/20 px-4 py-1.5 rounded-full mt-2">
                        <p class="text-sm font-bold text-cyan-400 tracking-wide" id="welcome-falta">Falta ...%</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Encabezado -->
    <header class="border-b border-slate-800 bg-slate-950/60 backdrop-blur-xl sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3.5">
                <div class="bg-indigo-600 p-2.5 rounded-xl text-white font-extrabold text-xl tracking-wider">V</div>
                <div>
                    <h1 class="text-lg font-bold text-white tracking-tight uppercase">SEDE COMAS ¡LOS MEJORES!</h1>
                    <p class="text-xs text-slate-400">Control de pagos automatizado</p>
                </div>
            </div>
            <div class="flex items-center space-x-2.5">
                <span class="flex h-2 w-2 relative">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span class="text-xs font-medium text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20 uppercase tracking-wider">Conectado en Vivo</span>
            </div>
        </div>
    </header>

    <!-- Alerta de Sincronización -->
    <div id="error-box" class="hidden max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
        <div class="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-4 rounded-xl text-sm font-medium">
            ⚠️ Alerta de Sincronización: No se pudieron leer los datos del servidor. Verifica el estado público de tu Google Sheets.
        </div>
    </div>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        
        <!-- NAVEGACIÓN PRINCIPAL: SEPARACIÓN POR PESTAÑAS REALES -->
        <nav class="grid grid-cols-2 lg:grid-cols-4 gap-5">
            <button onclick="switchTab('view-olim')" id="btn-view-olim" class="nav-card premium-card text-left rounded-2xl p-5 border-cyan-500/40 bg-cyan-950/20 ring-1 ring-cyan-500/20 shadow-lg shadow-cyan-500/5">
                <div class="text-3xl">💰</div>
                <div class="text-sm font-bold text-white mt-3">Pestaña OLIM</div>
                <div class="text-[11px] text-cyan-300 mt-1 font-medium">Control Financiero, Yape y Efectivo</div>
            </button>
            <button onclick="switchTab('view-des')" id="btn-view-des" class="nav-card premium-card text-left rounded-2xl p-5 hover:bg-slate-900/60 hover:border-slate-800/50">
                <div class="text-3xl">📉</div>
                <div class="text-sm font-bold text-slate-400 mt-3">Pestaña DES</div>
                <div class="text-[11px] text-slate-500 mt-1 font-medium">Análisis de Deserción y Cuotas</div>
            </button>
            <button onclick="switchTab('view-morosidad')" id="btn-view-morosidad" class="nav-card premium-card text-left rounded-2xl p-5 hover:bg-slate-900/60 hover:border-slate-800/50">
                <div class="text-3xl">👥</div>
                <div class="text-sm font-bold text-slate-400 mt-3">Lista de Morosidad</div>
                <div class="text-[11px] text-slate-500 mt-1 font-medium">Todos los Alumnos Alertas</div>
            </button>
            <button onclick="switchTab('view-tutor-filter')" id="btn-view-tutor-filter" class="nav-card premium-card text-left rounded-2xl p-5 hover:bg-slate-900/60 hover:border-slate-800/50">
                <div class="text-3xl">🔍</div>
                <div class="text-sm font-bold text-slate-400 mt-3">Alertas por Tutor</div>
                <div class="text-[11px] text-slate-500 mt-1 font-medium">Buscador Cruzado Individual</div>
            </button>
        </nav>

        <!-- CONTENEDOR VISTA 1: PESTAÑA OLIM -->
        <div id="view-olim" class="tab-view space-y-8">
            <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
                <div class="premium-card rounded-2xl p-5 flex flex-col justify-between shadow-xl">
                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">🎯 Meta General Dinero</p>
                    <h3 class="text-2xl font-black text-slate-100 mt-2" id="txt-meta-global">S/ 0</h3>
                </div>
                <div class="premium-card rounded-2xl p-5 flex flex-col justify-between shadow-xl">
                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">💰 Total Recaudado</p>
                    <h3 class="text-2xl font-black text-emerald-400 mt-2" id="txt-recaudado-global">S/ 0</h3>
                </div>
                <div class="premium-card rounded-2xl p-5 flex flex-col justify-between shadow-xl">
                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">⚠️ Falta Recaudar</p>
                    <h3 class="text-2xl font-black text-rose-400 mt-2" id="txt-falta-global">S/ 0</h3>
                </div>
                <div class="premium-card rounded-2xl p-5 flex flex-col justify-between shadow-xl">
                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">📈 Avance General Caja</p>
                    <h3 class="text-2xl font-black text-cyan-400 mt-2" id="txt-avance-global">0%</h3>
                </div>
            </section>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-2 premium-card rounded-2xl p-6 shadow-xl">
                    <h3 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-5">Recaudación por Tutor (Meta vs Recaudado S/)</h3>
                    <div class="relative h-80"><canvas id="chartTutors"></canvas></div>
                </div>
                <div class="lg:col-span-1 premium-card rounded-2xl p-6 shadow-xl flex flex-col justify-between">
                    <h3 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-5">Distribución Efectivo vs Yape</h3>
                    <div class="relative h-64 flex items-center justify-center"><canvas id="chartDoughnut"></canvas></div>
                </div>
            </div>

            <section class="premium-card rounded-2xl overflow-hidden shadow-2xl">
                <div class="p-5 border-b border-slate-800/80 bg-slate-950/40">
                    <h3 class="text-base font-bold text-white tracking-tight">Detalle General por Tutor (Pestaña OLIM)</h3>
                </div>
                <div class="w-full overflow-x-auto">
                    <table class="w-full text-left border-collapse text-xs">
                        <thead>
                            <tr class="bg-slate-950 text-slate-400 font-bold uppercase tracking-wider border-b border-slate-800 text-[10px]">
                                <th class="py-3.5 px-3">Tutor</th>
                                <th class="py-3.5 px-2">Ciclo</th>
                                <th class="py-3.5 px-2 text-center">Matr.</th>
                                <th class="py-3.5 px-2 text-center text-orange-400">Meta</th>
                                <th class="py-3.5 px-2 text-center text-cyan-400">Pag.</th>
                                <th class="py-3.5 px-2 text-right text-amber-400">Meta (S/)</th>
                                <th class="py-3.5 px-2 text-right text-teal-400">Efectivo</th>
                                <th class="py-3.5 px-2 text-right text-indigo-400">Yape</th>
                                <th class="py-3.5 px-2 text-right text-emerald-400">Total</th>
                                <th class="py-3.5 px-2 text-right text-rose-400">Falta</th>
                                <th class="py-3.5 px-3 text-center">Avance</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-900/60 bg-slate-950/40 font-semibold text-slate-300" id="table-body-tutors"></tbody>
                    </table>
                </div>
            </section>

            <section class="premium-card rounded-2xl p-6 shadow-xl max-w-4xl mx-auto">
                <div class="mb-5 border-b border-slate-800/80 pb-3">
                    <h3 class="text-lg font-bold text-white tracking-tight">🏆 Ranking de Recaudación Financiera de Tutores</h3>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4" id="leaderboard-container"></div>
            </section>
        </div>

        <!-- CONTENEDOR VISTA 2: PESTAÑA DES -->
        <div id="view-des" class="tab-view hidden space-y-8">
            <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
                <div class="premium-card rounded-2xl p-5 flex flex-col justify-between shadow-xl">
                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">📊 Total Matriculados</p>
                    <h3 class="text-2xl font-black text-slate-100 mt-2" id="lbl-total-mat">0</h3>
                </div>
                <div class="premium-card rounded-2xl p-5 flex flex-col justify-between shadow-xl">
                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">✅ Alumnos Pagantes actuales</p>
                    <h3 class="text-2xl font-black text-emerald-400 mt-2" id="lbl-total-pag">0</h3>
                </div>
                <div class="premium-card rounded-2xl p-5 flex flex-col justify-between shadow-xl">
                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">⚠️ Total Deserción (Suspendidos)</p>
                    <h3 class="text-2xl font-black text-rose-400 mt-2" id="lbl-total-des">0</h3>
                </div>
                <div class="premium-card rounded-2xl p-5 flex flex-col justify-between shadow-xl">
                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">📈 Cumplimiento General Metas</p>
                    <h3 class="text-2xl font-black text-indigo-400 mt-2" id="lbl-total-cum">0%</h3>
                </div>
            </section>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-2 premium-card rounded-2xl p-6 shadow-xl">
                    <h3 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-5">Matriculados vs Pagantes por Ciclo</h3>
                    <div class="relative h-80"><canvas id="chartDesercionBar"></canvas></div>
                </div>
                <div class="lg:col-span-1 premium-card rounded-2xl p-6 shadow-xl flex flex-col justify-between">
                    <h3 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-5">Proporción Cumplimiento vs Deserción</h3>
                    <div class="relative h-64 flex items-center justify-center"><canvas id="chartDesercionPie"></canvas></div>
                </div>
            </div>

            <section class="premium-card rounded-2xl overflow-hidden shadow-2xl">
                <div class="p-5 border-b border-slate-800/80 bg-slate-950/40">
                    <h3 class="text-base font-bold text-white tracking-tight">Detalle de Alumnos y Deserción por Ciclo</h3>
                </div>
                <div class="w-full overflow-x-auto">
                    <table class="w-full text-left border-collapse text-xs">
                        <thead>
                            <tr class="bg-slate-950 text-slate-400 font-bold uppercase tracking-wider border-b border-slate-800 text-[10px]">
                                <th class="py-3.5 px-4">Ciclo</th>
                                <th class="py-3.5 px-4">Tutor</th>
                                <th class="py-3.5 px-4 text-center">Matriculados</th>
                                <th class="py-3.5 px-4 text-center">Pagantes</th>
                                <th class="py-3.5 px-4 text-center">Suspendidos</th>
                                <th class="py-3.5 px-4 text-center text-rose-400">Deserción (%)</th>
                                <th class="py-3.5 px-4 text-center text-emerald-400">Cumplimiento (%)</th>
                                <th class="py-3.5 px-4 text-center">Nota</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-900/60 bg-slate-950/40 font-semibold text-slate-300" id="table-body-desercion"></tbody>
                    </table>
                </div>
            </section>

            <section class="premium-card rounded-2xl overflow-hidden shadow-2xl">
                <div class="p-5 border-b border-slate-800/80 bg-slate-950/40">
                    <h3 class="text-base font-bold text-white tracking-tight">📅 Cronograma General de Cuotas de Pagos</h3>
                </div>
                <div class="w-full overflow-x-auto custom-scroll">
                    <table class="w-full text-left border-collapse text-xs">
                        <thead>
                            <tr class="bg-slate-950 text-slate-400 font-bold uppercase tracking-wider border-b border-slate-800 text-[10px]" id="table-head-cuotas"></tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800/40 font-semibold text-slate-300" id="table-body-cuotas"></tbody>
                    </table>
                </div>
            </section>
        </div>

        <!-- CONTENEDOR VISTA 3: LISTA GENERAL DE MOROSIDAD -->
        <div id="view-morosidad" class="tab-view hidden space-y-6">
            <div class="premium-card rounded-2xl p-6 shadow-xl">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 border-b border-slate-800/80 pb-4">
                    <div>
                        <h3 class="text-lg font-bold text-white tracking-tight">👥 Estudiantes en Estado de Alerta / Deudores</h3>
                        <p class="text-xs text-slate-400 mt-1">Lista unificada extraída desde la sección derecha de la hoja</p>
                    </div>
                    <div>
                        <input type="text" id="search-moro" oninput="filterMoroTable()" placeholder="Buscar alumno o tutor..." class="bg-slate-950/60 border border-slate-800 text-slate-200 text-xs rounded-xl px-4 py-2.5 w-full md:w-64 focus:outline-none focus:border-indigo-500 transition-colors">
                    </div>
                </div>
                <div class="w-full overflow-x-auto custom-scroll">
                    <table class="w-full text-left border-collapse text-xs">
                        <thead>
                            <tr class="bg-slate-950 text-slate-400 font-bold uppercase tracking-wider border-b border-slate-800 text-[10px]">
                                <th class="py-3.5 px-4 w-12">#</th>
                                <th class="py-3.5 px-4">DNI</th>
                                <th class="py-3.5 px-4">Alumno</th>
                                <th class="py-3.5 px-4 text-center">Corte</th>
                                <th class="py-3.5 px-4">Tutor</th>
                                <th class="py-3.5 px-4 text-center">Condición de Pago</th>
                                <th class="py-3.5 px-4">Motivos / Comentarios</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800/40 font-semibold text-slate-300" id="table-body-morosidad"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- CONTENEDOR VISTA 4: ALERTAS POR TUTOR -->
        <div id="view-tutor-filter" class="tab-view hidden space-y-6">
            <div class="premium-card rounded-2xl p-6 shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h3 class="text-lg font-bold text-white tracking-tight">🔍 Buscador Cruzado Individual por Tutor</h3>
                    <p class="text-xs text-slate-400 mt-1">Aisla de forma inmediata los montos recaudados de OLIM y sus deudores de DES.</p>
                </div>
                <div>
                    <select id="tutor-select-filter" onchange="onTutorFilterChange()" class="bg-slate-950 border border-slate-800 text-slate-200 text-xs rounded-xl px-4 py-2.5 w-full sm:w-64 focus:outline-none focus:border-indigo-500 transition-colors font-semibold">
                        <option value="">-- Seleccionar Tutor --</option>
                    </select>
                </div>
            </div>
            
            <div id="tutor-filtered-metrics" class="hidden grid grid-cols-1 md:grid-cols-4 gap-5">
                <div class="premium-card rounded-xl p-4 bg-slate-900/20">
                    <p class="text-[11px] font-bold text-slate-400 uppercase">Efectivo Recaudado</p>
                    <h4 class="text-xl font-black text-slate-200 mt-1" id="f-tutor-ef">S/ 0</h4>
                </div>
                <div class="premium-card rounded-xl p-4 bg-slate-900/20">
                    <p class="text-[11px] font-bold text-slate-400 uppercase">Yape Recaudado</p>
                    <h4 class="text-xl font-black text-indigo-400 mt-1" id="f-tutor-yp">S/ 0</h4>
                </div>
                <div class="premium-card rounded-xl p-4 bg-slate-900/20">
                    <p class="text-[11px] font-bold text-slate-400 uppercase">Total Recolectado</p>
                    <h4 class="text-xl font-black text-emerald-400 mt-1" id="f-tutor-rec">S/ 0</h4>
                </div>
                <div class="premium-card rounded-xl p-4 bg-slate-900/20">
                    <p class="text-[11px] font-bold text-slate-400 uppercase">Avance Metas</p>
                    <h4 class="text-xl font-black text-cyan-400 mt-1" id="f-tutor-av">0%</h4>
                </div>
            </div>

            <div class="premium-card rounded-2xl p-6 shadow-xl">
                <h3 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-4">Lista de Alumnos Alertas en su Cargo</h3>
                <div class="w-full overflow-x-auto custom-scroll">
                    <table class="w-full text-left border-collapse text-xs">
                        <thead>
                            <tr class="bg-slate-950 text-slate-400 font-bold uppercase tracking-wider border-b border-slate-800 text-[10px]">
                                <th class="py-3.5 px-4 w-12">#</th>
                                <th class="py-3.5 px-4">DNI</th>
                                <th class="py-3.5 px-4">Alumno</th>
                                <th class="py-3.5 px-4 text-center">Corte</th>
                                <th class="py-3.5 px-4 text-center">Condición de Pago</th>
                                <th class="py-3.5 px-4">Motivos / Comentarios</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800/40 font-semibold text-slate-300" id="table-body-tutor-filtered">
                            <tr><td colspan="6" class="py-6 text-center text-slate-500 italic">Por favor, selecciona un tutor del menú desplegable superior.</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </main>

    <script>
        const SPREADSHEET_ID = '1iwQyWd5KQZHBtURWKIMC2MXrFSNyeSF2';
        const GID_DES = '700846667';
        const GID_OLIM = '1963579390';

        const URL_DES = `https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/gviz/tq?tqx=out:json&gid=${GID_DES}`;
        const URL_OLIM = `https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/gviz/tq?tqx=out:json&gid=${GID_OLIM}`;

        let cachedOlimRows = [];
        let cachedDesercionRows = [];
        let moroDataCached = [];

        function safeString(cell) {
            if (!cell) return '';
            if (cell.f !== undefined && cell.f !== null) return cell.f.trim();
            if (cell.v !== null && cell.v !== undefined) return cell.v.toString().trim();
            return '';
        }

        function getVal(cell, isNum = false) {
            let str = safeString(cell);
            if (isNum) {
                let clean = str.replace(/[^0-9.-]/g, '');
                let num = parseFloat(clean);
                return isNaN(num) ? 0 : num;
            }
            return str;
        }

        function safePercent(cell) {
            if (!cell) return '0.0%';
            if (cell.f && cell.f.includes('%')) return cell.f.trim();
            if (cell.v !== null && cell.v !== undefined) {
                let num = parseFloat(cell.v);
                if (!isNaN(num)) {
                    if (num >= -1 && num <= 1) return (num * 100).toFixed(1) + '%';
                    return num.toFixed(1) + '%';
                }
            }
            return '0.0%';
        }

        function switchTab(targetId) {
            document.querySelectorAll('.tab-view').forEach(view => view.classList.add('hidden'));
            document.getElementById(targetId).classList.remove('hidden');
            document.querySelectorAll('.nav-card').forEach(btn => {
                btn.className = "nav-card premium-card text-left rounded-2xl p-5 hover:bg-slate-900/60 hover:border-slate-800/50";
            });
            document.getElementById('btn-' + targetId).className = "nav-card premium-card text-left rounded-2xl p-5 border-cyan-500/40 bg-cyan-950/20 ring-1 ring-cyan-500/20 shadow-lg shadow-cyan-500/5";
        }

        async function fetchSheetData(url) {
            const response = await fetch(url);
            const text = await response.text();
            const startIdx = text.indexOf('{');
            const endIdx = text.lastIndexOf('}');
            const jsonString = text.substring(startIdx, endIdx + 1);
            return JSON.parse(jsonString).table;
        }

        async function loadAllDashboardData() {
            try {
                const [tableDes, tableOlim] = await Promise.all([
                    fetchSheetData(URL_DES),
                    fetchSheetData(URL_OLIM)
                ]);

                const rowsDes = tableDes.rows;
                const rowsOlim = tableOlim.rows;

                cachedDesercionRows = [];
                moroDataCached = [];
                cachedOlimRows = [];
                let cuotasHeaders = ["CUOTA", "SAN MAR", "INT MAR", "SAN ABR", "INT ABR", "SAN MAY", "INT MAY", "SAN JUL", "REP JUL", "SAN ENE"];
                let cuotasBodyRows = [];

                let gRecaudado = 0, gMetaDinero = 0, gFalta = 0, gEfectivo = 0, gYape = 0;
                let totalMatAl = 0, totalPagAl = 0;

                // ==========================================
                // 1. EXTRACTOR PESTAÑA FINANCIERA (OLIM)
                // ==========================================
                for(let i = 1; i < rowsOlim.length; i++) {
                    let row = rowsOlim[i];
                    if(!row || !row.c || !row.c[0]) continue;
                    let tName = safeString(row.c[0]);
                    if(tName.toUpperCase().includes("TOTAL")) continue;

                    let item = {
                        tutor: tName,
                        ciclo: safeString(row.c[1]),
                        mat: getVal(row.c[2], true),
                        meta: getVal(row.c[3], true),
                        pag: getVal(row.c[4], true),
                        metaDinero: getVal(row.c[5], true),
                        efectivo: getVal(row.c[6], true),
                        yape: getVal(row.c[7], true),
                        recaudado: getVal(row.c[8], true),
                        falta: getVal(row.c[9], true),
                        avance: safePercent(row.c[10])
                    };
                    cachedOlimRows.push(item);

                    gEfectivo += item.efectivo;
                    gYape += item.yape;
                    gRecaudado += item.recaudado;
                    gMetaDinero += item.metaDinero;
                    gFalta += item.falta;
                    totalMatAl += item.mat;
                    totalPagAl += item.pag;
                }
                let gAvanceNum = gMetaDinero > 0 ? (gRecaudado / gMetaDinero) * 100 : 95;

                // ==========================================
                // 2. EXTRACTOR PESTAÑA DESERCIÓN (DES DESDE LESLY)
                // ==========================================
                let desDataStarted = false;
                let totalMat = 0, totalPag = 0, totalDes = 0, totalCum = 95;

                for (let i = 0; i < rowsDes.length; i++) {
                    const row = rowsDes[i];
                    if (!row || !row.c) continue;

                    let cicloVal = safeString(row.c[1]);
                    if (cicloVal.toUpperCase() === 'CICLO') {
                        desDataStarted = true;
                        continue;
                    }
                    if (desDataStarted) {
                        if (cicloVal.toUpperCase().includes('TOTAL')) {
                            totalMat = getVal(row.c[3], true);
                            totalPag = getVal(row.c[4], true);
                            totalDes = getVal(row.c[5], true);
                            if (row.c[7]) {
                                let v = row.c[7].v;
                                totalCum = (typeof v === 'number' && v <= 1) ? v * 100 : parseFloat(v) || 95;
                            }
                            desDataStarted = false; 
                        } else if (cicloVal !== '' && !cicloVal.toUpperCase().includes('VENCIMIENTO')) {
                            cachedDesercionRows.push({
                                ciclo: cicloVal,
                                tutor: safeString(row.c[2]),
                                matriculados: getVal(row.c[3], true),
                                pagantes: getVal(row.c[4], true),
                                suspendidos: getVal(row.c[5], true),
                                desercion: safePercent(row.c[6]),
                                cumplimiento: safePercent(row.c[7]),
                                nota: safeString(row.c[8])
                            });
                        }
                    }

                    // Extraer Morosidad (Y3:AE1000)
                    let mDni = safeString(row.c[25]);
                    let mAlum = safeString(row.c[26]);
                    if (mDni && mDni.toUpperCase() !== 'DNI' && mAlum && mAlum.toUpperCase() !== 'ALUMNO') {
                        moroDataCached.push({
                            num: row.c[24] ? safeString(row.c[24]) : (moroDataCached.length + 1),
                            dni: mDni,
                            alumno: mAlum,
                            corte: safeString(row.c[27]),
                            tutor: safeString(row.c[28]),
                            condicion: safeString(row.c[29]),
                            motivos: safeString(row.c[30])
                        });
                    }

                    // Extraer Cronograma (M5:V11)
                    let cuotaCell = safeString(row.c[12]);
                    if (cuotaCell && !isNaN(cuotaCell) && cuotaCell !== '' && i >= 3 && i <= 12) {
                        let cells = [];
                        cells.push(cuotaCell);
                        for (let k = 13; k <= 21; k++) {
                            cells.push(row.c[k] ? safeString(row.c[k]) : '-');
                        }
                        cuotasBodyRows.push(cells);
                    }
                }

                // Pintar KPI Globales Financieros de OLIM
                document.getElementById('txt-meta-global').innerText = "S/ " + Math.round(gMetaDinero).toLocaleString('es-PE');
                document.getElementById('txt-recaudado-global').innerText = "S/ " + Math.round(gRecaudado).toLocaleString('es-PE');
                document.getElementById('txt-falta-global').innerText = "S/ " + Math.round(gFalta).toLocaleString('es-PE');
                document.getElementById('txt-avance-global').innerText = Math.round(gAvanceNum) + '%';
                document.getElementById('bar-avance-global').style.width = Math.round(gAvanceNum) + '%';

                // Pintar KPI de Alumnos de DES
                document.getElementById('lbl-total-mat').innerText = Math.round(totalMat);
                document.getElementById('lbl-total-pag').innerText = Math.round(totalPag);
                document.getElementById('lbl-total-des').innerText = Math.round(totalDes);
                document.getElementById('lbl-total-cum').innerText = Math.round(totalCum) + '%';

                if (isFirstLoad) {
                    document.getElementById('welcome-avance').innerText = Math.round(gAvanceNum) + '% Avance';
                    let faltaProgreso = 100 - gAvanceNum;
                    document.getElementById('welcome-falta').innerText = `Falta ${Math.round(faltaProgreso)}%`;
                    
                    document.getElementById('welcome-loading').classList.add('hidden');
                    document.getElementById('welcome-stats').classList.remove('hidden');
                    document.getElementById('welcome-stats').classList.add('flex');
                    document.getElementById('welcome-content').classList.remove('animate-pulse');

                    setTimeout(() => {
                        const overlay = document.getElementById('welcome-overlay');
                        if (overlay) {
                            overlay.classList.remove('opacity-100');
                            overlay.classList.add('opacity-0');
                            setTimeout(() => overlay.remove(), 700);
                        }
                    }, 3500);
                    isFirstLoad = false;
                }

                renderOlimTable(cachedOlimRows);
                renderDesercionTable(cachedDesercionRows);
                renderMoroTable(moroDataCached);
                renderCuotasTable(cuotasHeaders, cuotasBodyRows);
                populateTutorDropdown();
                renderCharts(cachedOlimRows, gEfectivo, gYape, totalMatAl, totalPagAl);
                renderLeaderboard(cachedOlimRows);

                document.getElementById('error-box').className = 'hidden';

            } catch (error) {
                console.error(error);
                document.getElementById('error-box').className = 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6 block';
                const overlay = document.getElementById('welcome-overlay');
                if (overlay) overlay.remove();
            }
        }

        function renderOlimTable(data) {
            const tbody = document.getElementById('table-body-tutors');
            tbody.innerHTML = '';
            data.forEach(row => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-800/30 transition-colors border-b border-slate-900/40 text-xs font-semibold";
                tr.innerHTML = `
                    <td class="py-3 px-3 text-slate-100 font-bold">${row.tutor}</td>
                    <td class="py-3 px-2 text-slate-400">${row.ciclo}</td>
                    <td class="py-3 px-2 text-center text-slate-300">${Math.round(row.mat)}</td>
                    <td class="py-3 px-2 text-center text-orange-400">${Math.round(row.meta)}</td>
                    <td class="py-3 px-2 text-center text-cyan-400">${Math.round(row.pag)}</td>
                    <td class="py-3 px-2 text-right text-amber-400">S/ ${Math.round(row.metaDinero)}</td>
                    <td class="py-3 px-2 text-right text-teal-400">S/ ${Math.round(row.efectivo)}</td>
                    <td class="py-3 px-2 text-right text-indigo-400">S/ ${Math.round(row.yape)}</td>
                    <td class="py-3 px-2 text-right text-emerald-400 font-bold">S/ ${Math.round(row.recaudado)}</td>
                    <td class="py-3 px-2 text-right text-rose-400">S/ ${Math.round(row.falta)}</td>
                    <td class="py-3 px-3 text-center"><span class="px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400">${row.avance}</span></td>
                `;
                tbody.appendChild(tr);
            });
        }

        function renderDesercionTable(data) {
            const tbody = document.getElementById('table-body-desercion');
            tbody.innerHTML = '';
            data.forEach(row => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-800/30 transition-colors border-b border-slate-800/40 text-xs font-semibold";
                tr.innerHTML = `
                    <td class="py-3 px-4 font-bold text-slate-100 whitespace-nowrap">${row.ciclo}</td>
                    <td class="py-3 px-4 text-slate-400 font-medium">${row.tutor}</td>
                    <td class="py-3 px-4 text-center font-bold">${Math.round(row.matriculados)}</td>
                    <td class="py-3 px-4 text-center text-emerald-400 font-bold">${Math.round(row.pagantes)}</td>
                    <td class="py-3 px-4 text-center text-amber-500 font-bold">${Math.round(row.suspendidos)}</td>
                    <td class="py-3 px-4 text-center text-rose-400 font-extrabold bg-rose-500/5">${row.desercion}</td>
                    <td class="py-3 px-4 text-center text-cyan-400 font-extrabold bg-cyan-500/5">${row.cumplimiento}</td>
                    <td class="py-3 px-4 text-center text-slate-400 font-normal">${row.nota}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        function renderMoroTable(data) {
            const tbody = document.getElementById('table-body-morosidad');
            tbody.innerHTML = '';
            data.forEach(row => {
                let badgeClass = "bg-slate-800 text-slate-300";
                if(row.condicion.toUpperCase().includes("VIERNES")) badgeClass = "bg-amber-500/10 text-amber-400 border border-amber-500/20";
                if(row.condicion.toUpperCase().includes("RETIRO")) badgeClass = "bg-rose-500/10 text-rose-400 border border-rose-500/20";

                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-800/30 transition-colors border-b border-slate-800/40 font-semibold";
                tr.innerHTML = `
                    <td class="py-3 px-4 font-bold text-slate-500">${row.num}</td>
                    <td class="py-3 px-4 text-slate-400 font-mono tracking-wider">${row.dni}</td>
                    <td class="py-3 px-4 font-bold text-slate-100">${row.alumno}</td>
                    <td class="py-3 px-4 text-center text-slate-400">${row.corte}</td>
                    <td class="py-3 px-4 text-slate-300 font-medium">${row.tutor}</td>
                    <td class="py-3 px-4 text-center">
                        <span class="px-2 py-1 rounded-md text-[10px] font-extrabold uppercase ${badgeClass}">${row.condicion}</span>
                    </td>
                    <td class="py-3 px-4 text-slate-400 italic font-normal">${row.motivos}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        function filterMoroTable() {
            const query = document.getElementById('search-moro').value.toLowerCase().trim();
            const filtered = moroDataCached.filter(item => 
                item.alumno.toLowerCase().includes(query) || 
                item.tutor.toLowerCase().includes(query) ||
                item.dni.toLowerCase().includes(query)
            );
            renderMoroTable(filtered);
        }

        function borderAlphaFix(index) {
            return index === 0 ? 'bg-amber-500/10 border-amber-500/30' : index === 1 ? 'bg-slate-300/10 border-slate-400/30' : index === 2 ? 'bg-amber-700/10 border-amber-700/30' : 'bg-slate-900/60 border-slate-800/80';
        }

        function renderLeaderboard(data) {
            const container = document.getElementById('leaderboard-container');
            container.innerHTML = '';
            let ranked = [...data].sort((a,b) => b.recaudado - a.recaudado);

            ranked.forEach((row, index) => {
                const item = document.createElement('div');
                item.className = `flex items-center justify-between p-4 rounded-xl border ${borderAlphaFix(index)}`;
                let medal = `<span class="text-sm font-bold text-slate-400 w-6">${index + 1}</span>`;
                if (index === 0) medal = `<span class="text-xl w-6">🥇</span>`;
                if (index === 1) medal = `<span class="text-xl w-6">🥈</span>`;
                if (index === 2) medal = `<span class="text-xl w-6">🥉</span>`;
                item.innerHTML = `
                    <div class="flex items-center space-x-3 truncate">
                        ${medal}
                        <div class="truncate">
                            <p class="text-sm font-semibold text-slate-200 truncate">${row.tutor}</p>
                            <p class="text-xs text-slate-400 truncate">${row.ciclo}</p>
                        </div>
                    </div>
                    <div class="text-right ml-2 flex-shrink-0">
                        <p class="text-sm font-bold text-emerald-400">S/ ${Math.round(row.recaudado)}</p>
                        <p class="text-[11px] text-cyan-400 font-bold">${row.avance}</p>
                    </div>
                `;
                container.appendChild(item);
            });
        }

        function populateTutorDropdown() {
            const select = document.getElementById('tutor-select-filter');
            const currentSelection = select.value;
            
            let tutorsSet = new Set();
            moroDataCached.forEach(m => { 
                if(m.tutor && isNaN(m.tutor)) {
                    let clean = m.tutor.trim();
                    if(clean && clean.toUpperCase() !== 'TUTOR') tutorsSet.add(clean);
                }
            });

            select.innerHTML = '<option value="">-- Seleccionar Tutor --</option>';
            Array.from(tutorsSet).sort().forEach(tutorName => {
                const opt = document.createElement('option');
                opt.value = tutorName;
                opt.innerText = tutorName;
                select.appendChild(opt);
            });

            if(currentSelection && tutorsSet.has(currentSelection)) {
                select.value = currentSelection;
            }
        }

        function onTutorFilterChange() {
            const selectedTutor = document.getElementById('tutor-select-filter').value.trim();
            const metricsContainer = document.getElementById('tutor-filtered-metrics');
            const tbodyFiltered = document.getElementById('table-body-tutor-filtered');

            if(!selectedTutor) {
                metricsContainer.classList.add('hidden');
                tbodyFiltered.innerHTML = `<tr><td colspan="6" class="py-6 text-center text-slate-500 italic">Por favor, selecciona un tutor del menú desplegable superior.</td></tr>`;
                return;
            }

            let tEf = 0, tYp = 0, tRec = 0, tAv = "0%";
            let oRow = cachedOlimRows.find(r => r.tutor.toLowerCase().trim() === selectedTutor.toLowerCase());
            if (oRow) {
                tEf = oRow.efectivo;
                tYp = oRow.yape;
                tRec = oRow.recaudado;
                tAv = oRow.avance;
            }

            document.getElementById('f-tutor-ef').innerText = "S/ " + Math.round(tEf);
            document.getElementById('f-tutor-yp').innerText = "S/ " + Math.round(tYp);
            document.getElementById('f-tutor-rec').innerText = "S/ " + Math.round(tRec);
            document.getElementById('f-tutor-av').innerText = tAv;
            metricsContainer.classList.remove('hidden');

            let filteredStudents = moroDataCached.filter(m => m.tutor.toLowerCase().trim() === selectedTutor.toLowerCase());
            tbodyFiltered.innerHTML = '';

            if(filteredStudents.length === 0) {
                tbodyFiltered.innerHTML = `<tr><td colspan="6" class="py-6 text-center text-emerald-400/70 font-medium bg-emerald-500/5">🎉 ¡Excelente! Este tutor no registra alumnos con alertas o deudas pendientes.</td></tr>`;
            } else {
                filteredStudents.forEach(row => {
                    let badgeClass = "bg-slate-800 text-slate-300";
                    if(row.condicion.toUpperCase().includes("VIERNES")) badgeClass = "bg-amber-500/10 text-amber-400 border border-amber-500/20";
                    if(row.condicion.toUpperCase().includes("RETIRO")) badgeClass = "bg-rose-500/10 text-rose-400 border border-rose-500/20";

                    const tr = document.createElement('tr');
                    tr.className = "hover:bg-slate-800/30 transition-colors border-b border-slate-800/40";
                    tr.innerHTML = `
                        <td class="py-3 px-4 font-bold text-slate-500">${row.num}</td>
                        <td class="py-3 px-4 font-mono text-slate-400">${row.dni}</td>
                        <td class="py-3 px-4 font-bold text-slate-100">${row.alumno}</td>
                        <td class="py-3 px-4 text-center text-slate-400">${row.corte}</td>
                        <td class="py-3 px-4 text-center">
                            <span class="px-2 py-1 rounded-md text-[10px] font-extrabold uppercase ${badgeClass}">${row.condicion}</span>
                        </td>
                        <td class="py-3 px-4 text-slate-400 italic">${row.motivos}</td>
                    `;
                    tbodyFiltered.appendChild(tr);
                });
            }
        }

        function renderCuotasTable(headers, bodyRows) {
            const thead = document.getElementById('table-head-cuotas');
            const tbody = document.getElementById('table-body-cuotas');
            thead.innerHTML = '';
            tbody.innerHTML = '';

            if (headers.length === 0) return;

            headers.forEach(h => {
                const th = document.createElement('th');
                th.className = "py-3.5 px-4 text-left font-bold text-slate-400 uppercase tracking-wider text-[10px]";
                th.innerText = h;
                thead.appendChild(th);
            });

            bodyRows.forEach(rowCells => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-800/30 transition-colors border-b border-slate-800/40 text-xs text-slate-300 font-semibold";
                
                let htmlStr = `<td class="py-3 px-4 font-bold text-indigo-400">Cuota ${rowCells[0]}</td>`;
                for (let i = 1; i < rowCells.length; i++) {
                    htmlStr += `<td class="py-3 px-4 font-mono text-slate-300">${rowCells[i] || '-'}</td>`;
                }
                tr.innerHTML = htmlStr;
                tbody.appendChild(tr);
            });
        }

        function renderCharts(data, efectivoGlobal, yapeGlobal, totalMatAl, totalPagAl) {
            try {
                const ctxBar = document.getElementById('chartTutors').getContext('2d');
                if (chartBar) chartBar.destroy();

                chartBar = new Chart(ctxBar, {
                    type: 'bar',
                    data: {
                        labels: data.map(r => r.tutor),
                        datasets: [
                            {
                                label: 'Meta asignada S/',
                                data: data.map(r => r.metaDinero),
                                backgroundColor: 'rgba(71, 85, 105, 0.4)',
                                borderRadius: 4
                            },
                            {
                                label: 'Total Recaudado S/',
                                data: data.map(r => r.recaudado),
                                backgroundColor: '#0ea5e9',
                                borderRadius: 4
                            }
                        ]
                    },
                    options: {
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { labels: { color: '#94a3b8' } },
                            datalabels: { display: false }
                        },
                        scales: {
                            x: { grid: { color: 'rgba(255, 255, 255, 0.03)' }, ticks: { color: '#94a3b8', precision: 0 } },
                            y: { ticks: { color: '#e2e8f0' } }
                        }
                    }
                });
            } catch(e) { console.error(e); }

            try {
                const ctxPie = document.getElementById('chartDoughnut').getContext('2d');
                if (chartPie) chartPie.destroy();

                chartPie = new Chart(ctxPie, {
                    type: 'doughnut',
                    data: {
                        labels: ['Efectivo', 'Yape'],
                        datasets: [{
                            data: [efectivoGlobal, yapeGlobal],
                            backgroundColor: ['#22d3ee', '#6366f1'],
                            borderColor: '#0f172a',
                            borderWidth: 3
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false }, datalabels: { display: false } },
                        cutout: '75%'
                    }
                });
            } catch(e) { console.error(e); }

            try {
                const ctxStudents = document.getElementById('chartStudents').getContext('2d');
                if (chartStudents) chartStudents.destroy();

                chartStudents = new Chart(ctxStudents, {
                    type: 'bar',
                    data: {
                        labels: ['Matriculados', 'Pagantes Actuales'],
                        datasets: [{
                            data: [totalMatAl, totalPagAl],
                            backgroundColor: ['#2563eb', '#06b6d4'],
                            borderRadius: 6,
                            barThickness: 45
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            datalabels: {
                                anchor: 'end',
                                align: 'top',
                                color: '#cbd5e1',
                                font: { family: 'Plus Jakarta Sans', weight: '800', size: 14 },
                                formatter: function(value) { return Math.round(value); }
                            }
                        },
                        scales: {
                            x: { ticks: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', weight: '600' } }, grid: { display: false } },
                            y: { grace: '15%', grid: { color: 'rgba(255, 255, 255, 0.03)' }, ticks: { color: '#94a3b8', precision: 0 } }
                        }
                    }
                });
            } catch(e) { console.error(e); }
        }

        loadAllDashboardData();
        setInterval(loadAllDashboardData, 60000);
    </script>
</body>
</html> 
