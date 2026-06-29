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

    <!-- PANTALLA DE BIENVENIDA (SPLASH SCREEN INSTITUCIONAL) -->
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
            ⚠️ Alerta de Sincronización: No se pudieron leer los datos del servidor. Verifica los permisos de enlace público de tu Google Sheets.
        </div>
    </div>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        
        <!-- NAVEGACIÓN PRINCIPAL UNIFICADA (TRANSICIONES INSTANTÁNEAS DE 5 PESTAÑAS REALES) -->
        <nav class="grid grid-cols-2 lg:grid-cols-5 gap-4">
            <button onclick="switchTab('view-resumen')" id="btn-view-resumen" class="nav-card premium-card text-left rounded-2xl p-4 border-cyan-500/40 bg-cyan-950/20 ring-1 ring-cyan-500/20 shadow-lg shadow-cyan-500/5">
                <div class="text-2xl">📊</div>
                <div class="text-xs font-bold text-white mt-2">Resumen</div>
                <div class="text-[10px] text-cyan-300 mt-0.5">Gráficos de Control</div>
            </button>
            <button onclick="switchTab('view-clasificacion')" id="btn-view-clasificacion" class="nav-card premium-card text-left rounded-2xl p-4 hover:bg-slate-900/60 hover:border-slate-800/50">
                <div class="text-2xl">🏆</div>
                <div class="text-xs font-bold text-slate-400 mt-2">Clasificación</div>
                <div class="text-[10px] text-slate-500 mt-0.5">Ranking de Tutores</div>
            </button>
            <button onclick="switchTab('view-desercion')" id="btn-view-desercion" class="nav-card premium-card text-left rounded-2xl p-4 hover:bg-slate-900/60 hover:border-slate-800/50">
                <div class="text-2xl">📉</div>
                <div class="text-xs font-bold text-slate-400 mt-2">Deserción</div>
                <div class="text-[10px] text-slate-500 mt-0.5">Detalle por Ciclo</div>
            </button>
            <button onclick="switchTab('view-morosidad')" id="btn-view-morosidad" class="nav-card premium-card text-left rounded-2xl p-4 hover:bg-slate-900/60 hover:border-slate-800/50">
                <div class="text-2xl">👥</div>
                <div class="text-xs font-bold text-slate-400 mt-2">Morosidad</div>
                <div class="text-[10px] text-slate-500 mt-0.5">Lista de Alertas</div>
            </button>
            <button onclick="switchTab('view-tutor-filter')" id="btn-view-tutor-filter" class="nav-card premium-card text-left rounded-2xl p-4 hover:bg-slate-900/60 hover:border-slate-800/50">
                <div class="text-2xl">🔍</div>
                <div class="text-xs font-bold text-slate-400 mt-2">Filtrar por Tutor</div>
                <div class="text-[10px] text-slate-500 mt-0.5">Buscador de Alumnos</div>
            </button>
        </nav>

        <!-- TARJETAS DE INDICADORES GLOBALES (CONTEOS EN NÚMEROS ENTEROS) -->
        <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            <div class="premium-card rounded-2xl p-5 flex flex-col justify-between shadow-xl">
                <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">📊 Total Matriculados</p>
                <h3 class="text-3xl font-extrabold text-slate-100 mt-2 tracking-tight" id="lbl-total-mat">0</h3>
            </div>
            <div class="premium-card rounded-2xl p-5 flex flex-col justify-between shadow-xl">
                <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">✅ Alumnos Pagantes</p>
                <h3 class="text-3xl font-extrabold text-emerald-400 mt-2 tracking-tight" id="lbl-total-pag">0</h3>
            </div>
            <div class="premium-card rounded-2xl p-5 flex flex-col justify-between shadow-xl">
                <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">⚠️ Total Deserción (Sus.)</p>
                <h3 class="text-3xl font-extrabold text-rose-400 mt-2 tracking-tight" id="lbl-total-des">0</h3>
            </div>
            <div class="premium-card rounded-2xl p-5 flex flex-col justify-between shadow-xl">
                <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">📈 Cumplimiento General</p>
                <h3 class="text-3xl font-extrabold text-cyan-400 mt-2 tracking-tight" id="lbl-total-cum">0%</h3>
                <div class="w-full bg-slate-800 rounded-full h-1.5 mt-3 overflow-hidden">
                    <div id="bar-cum-global" class="bg-cyan-500 h-full rounded-full transition-all duration-500" style="width: 0%"></div>
                </div>
            </div>
        </section>

        <!-- VISTA 1: RESUMEN (ESTADÍSTICAS EN ENTEROS) -->
        <div id="view-resumen" class="tab-view space-y-8">
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-2 premium-card rounded-2xl p-6 shadow-xl">
                    <h3 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-5">Matriculados vs Pagantes por Ciclo</h3>
                    <div class="relative h-80"><canvas id="chartDesercionBar"></canvas></div>
                </div>
                <div class="lg:col-span-1 premium-card rounded-2xl p-6 shadow-xl flex flex-col justify-between">
                    <h3 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-5">Proporción Cumplimiento General</h3>
                    <div class="relative h-64 flex items-center justify-center"><canvas id="chartDesercionPie"></canvas></div>
                </div>
            </div>
            <!-- Cronograma incrustado en Resumen para acceso rápido -->
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

        <!-- VISTA 2: CLASIFICACIÓN (RANKING DE TUTORES) -->
        <div id="view-clasificacion" class="tab-view hidden space-y-6">
            <div class="premium-card rounded-2xl p-6 shadow-xl max-w-2xl mx-auto">
                <div class="mb-5 border-b border-slate-800/80 pb-3">
                    <h3 class="text-lg font-bold text-white tracking-tight">🏆 Ranking de Efectividad de Tutores</h3>
                </div>
                <div class="space-y-4" id="leaderboard-container"></div>
            </div>
        </div>

        <!-- VISTA 3: DETALLE DESERCION (COMPLETA DESDE LESLY) -->
        <div id="view-desercion" class="tab-view hidden space-y-6">
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
        </div>

        <!-- VISTA 4: MOROSIDAD GENERAL -->
        <div id="view-morosidad" class="tab-view hidden space-y-6">
            <div class="premium-card rounded-2xl p-6 shadow-xl">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 border-b border-slate-800/80 pb-4">
                    <div>
                        <h3 class="text-lg font-bold text-white tracking-tight">👥 Estudiantes en Estado de Alerta / Deudores</h3>
                        <p class="text-xs text-slate-400 mt-1">Lista completa consolidada de la sección derecha de la hoja</p>
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

        <!-- VISTA 5: BUSCADOR POR TUTOR -->
        <div id="view-tutor-filter" class="tab-view hidden space-y-6">
            <div class="premium-card rounded-2xl p-6 shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h3 class="text-lg font-bold text-white tracking-tight">🔍 Buscador Dinámico Aislado por Tutor</h3>
                    <p class="text-xs text-slate-400 mt-1">Filtra de inmediato las métricas y la sublista de alumnos alertas a su cargo.</p>
                </div>
                <div>
                    <select id="tutor-select-filter" onchange="onTutorFilterChange()" class="bg-slate-950 border border-slate-800 text-slate-200 text-xs rounded-xl px-4 py-2.5 w-full sm:w-64 focus:outline-none focus:border-indigo-500 transition-colors font-semibold">
                        <option value="">-- Seleccionar Tutor --</option>
                    </select>
                </div>
            </div>
            
            <div id="tutor-filtered-metrics" class="hidden grid grid-cols-1 md:grid-cols-4 gap-5">
                <div class="premium-card rounded-xl p-4 bg-slate-900/20">
                    <p class="text-[11px] font-bold text-slate-400 uppercase">Matriculados</p>
                    <h4 class="text-2xl font-black text-slate-200 mt-1" id="f-tutor-mat">0</h4>
                </div>
                <div class="premium-card rounded-xl p-4 bg-slate-900/20">
                    <p class="text-[11px] font-bold text-slate-400 uppercase">Pagantes Activos</p>
                    <h4 class="text-2xl font-black text-emerald-400 mt-1" id="f-tutor-pag">0</h4>
                </div>
                <div class="premium-card rounded-xl p-4 bg-slate-900/20">
                    <p class="text-[11px] font-bold text-slate-400 uppercase">Deserciones (Sus.)</p>
                    <h4 class="text-2xl font-black text-rose-400 mt-1" id="f-tutor-des">0</h4>
                </div>
                <div class="premium-card rounded-xl p-4 bg-slate-900/20">
                    <p class="text-[11px] font-bold text-slate-400 uppercase">Cumplimiento</p>
                    <h4 class="text-2xl font-black text-cyan-400 mt-1" id="f-tutor-cum">0%</h4>
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
        const SHEET_JSON_URL = 'https://docs.google.com/spreadsheets/d/1iwQyWd5KQZHBtURWKIMC2MXrFSNyeSF2/gviz/tq?tqx=out:json&gid=700846667';

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
                const tableData = await fetchSheetData(SHEET_JSON_URL);
                const rows = tableData.rows;

                cachedDesercionRows = [];
                moroDataCached = [];
                let cuotasHeaders = [];
                let cuotasBodyRows = [];

                let totalMat = 0, totalPag = 0, totalDes = 0, totalCum = 95;

                // 1. ESCÁNER DINÁMICO DE FILAS BASE (ÍNDICES EN UNA SOLA HOJA DE EXCEL)
                let rCiclo = 1, cCiclo = 1;
                let rCuota = 3, cCuota = 12;

                // Captura cabeceras del cronograma M4:V4 de forma exacta
                if (rows[rCuota] && rows[rCuota].c) {
                    for (let c = cCuota; c <= 21; c++) {
                        let hVal = safeString(rows[rCuota].c[c]);
                        if (hVal) cuotasHeaders.push(hVal);
                    }
                }

                // 2. EXTRACCIÓN SIMULTÁNEA DE MATRIZ COMPLETA
                let desDataStarted = false;
                for (let i = 0; i < rows.length; i++) {
                    const row = rows[i];
                    if (!row || !row.c) continue;

                    // --- TABLA A: DETALLE DESERCION POR CICLO (B3:J15) ---
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

                    // --- TABLA B: CRONOGRAMA DE CUOTAS (M5:V11) ---
                    let cuotaCell = safeString(row.c[cCuota]);
                    if (cuotaCell && !isNaN(cuotaCell) && i > rCuota && i <= rCuota + 8) {
                        let cells = [];
                        cells.push(cuotaCell);
                        for (let k = 13; k <= 21; k++) {
                            cells.push(safeString(row.c[k]) || '-');
                        }
                        cuotasBodyRows.push(cells);
                    }

                    // --- TABLA C: MOROSIDAD GENERAL (Y3:AE1000) ---
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
                }

                // Inyectar KPI superiores finales
                document.getElementById('lbl-total-mat').innerText = Math.round(totalMat);
                document.getElementById('lbl-total-pag').innerText = Math.round(totalPag);
                document.getElementById('lbl-total-des').innerText = Math.round(totalDes);
                document.getElementById('lbl-total-cum').innerText = Math.round(totalCum) + '%';
                document.getElementById('bar-cum-global').style.width = Math.round(totalCum) + '%';

                if (isFirstLoad) {
                    document.getElementById('welcome-avance').innerText = Math.round(totalCum) + '% Cumplimiento';
                    let faltaProgreso = 100 - totalCum;
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

                // Inyectores de componentes HTML
                renderDesercionTable(cachedDesercionRows);
                renderMoroTable(moroDataCached);
                renderCuotasTable(cuotasHeaders, cuotasBodyRows);
                populateTutorDropdown();
                renderCharts(cachedDesercionRows, totalCum);
                renderLeaderboard(cachedDesercionRows);

                document.getElementById('error-box').className = 'hidden';

            } catch (error) {
                console.error(error);
                document.getElementById('error-box').className = 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6 block';
                const overlay = document.getElementById('welcome-overlay');
                if (overlay) overlay.remove();
            }
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
            let ranked = [...data].sort((a,b) => b.pagantes - a.pagantes);

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
                        <p class="text-sm font-bold text-emerald-400">${row.cumplimiento}</p>
                        <p class="text-[11px] text-cyan-400 font-bold">${Math.round(row.pagantes)} pagantes</p>
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

            let tMat = 0, tPag = 0, tDes = 0;
            let tutorRows = cachedDesercionRows.filter(r => r.tutor.toLowerCase().trim() === selectedTutor.toLowerCase());
            
            tutorRows.forEach(r => {
                tMat += r.matriculados;
                tPag += r.pagantes;
                tDes += r.suspendidos;
            });

            let tCum = tMat > 0 ? (tPag / tMat) * 100 : 0;

            document.getElementById('f-tutor-mat').innerText = Math.round(tMat);
            document.getElementById('f-tutor-pag').innerText = Math.round(tPag);
            document.getElementById('f-tutor-des').innerText = Math.round(tDes);
            document.getElementById('f-tutor-cum').innerText = Math.round(tCum) + '%';
            metricsContainer.classList.remove('hidden');

            let filteredStudents = moroDataCached.filter(m => m.tutor.toLowerCase().trim() === selectedTutor.toLowerCase());
            tbodyFiltered.innerHTML = '';

            if(filteredStudents.length === 0) {
                tbodyFiltered.innerHTML = `<tr><td colspan="6" class="py-6 text-center text-emerald-400/70 font-medium bg-emerald-500/5">🎉 ¡Excelente! Este tutor no registra alumnos con deudas pendientes.</td></tr>`;
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
                        <td class="py-3 px-4 text-slate-300 font-medium">${row.tutor}</td>
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

        function renderCharts(data, complianceNum) {
            try {
                const ctxBar = document.getElementById('chartDesercionBar').getContext('2d');
                if (chartBar) chartBar.destroy();

                chartBar = new Chart(ctxBar, {
                    type: 'bar',
                    data: {
                        labels: data.map(r => r.ciclo),
                        datasets: [
                            {
                                label: 'Matriculados',
                                data: data.map(r => r.matriculados),
                                backgroundColor: 'rgba(71, 85, 105, 0.4)',
                                borderRadius: 4
                            },
                            {
                                label: 'Pagantes Activos',
                                data: data.map(r => r.pagantes),
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
                const ctxPie = document.getElementById('chartDesercionPie').getContext('2d');
                if (chartPie) chartPie.destroy();

                let rest = 100 - complianceNum;
                if (rest < 0) rest = 0;

                chartPie = new Chart(ctxPie, {
                    type: 'doughnut',
                    data: {
                        labels: ['Cumplimiento', 'Deserción'],
                        datasets: [{
                            data: [complianceNum, rest],
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
        }

        function switchTab(targetId) {
            document.querySelectorAll('.tab-view').forEach(view => view.classList.add('hidden'));
            document.getElementById(targetId).classList.remove('hidden');
            document.querySelectorAll('.nav-card').forEach(btn => {
                btn.className = "nav-card premium-card text-left rounded-2xl p-5 hover:bg-slate-900/60 hover:border-slate-800/50";
            });
            let actBtnId = 'btn-view-olim';
            if(targetId === 'view-des' || targetId === 'view-morosidad' || targetId === 'view-cuotas') {
                actBtnId = 'btn-view-des';
            } else if(targetId === 'view-tutor-filter' || targetId === 'view-clasificacion') {
                actBtnId = 'btn-view-tutor-filter';
            }
            document.getElementById(actBtnId).className = "nav-card premium-card text-left rounded-2xl p-5 border-cyan-500/40 bg-cyan-950/20 ring-1 ring-cyan-500/20 shadow-lg shadow-cyan-500/5";
        }

        loadAllDashboardData();
        setInterval(loadAllDashboardData, 60000);
    </script>
</body>
</html> 
