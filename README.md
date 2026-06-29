
           cachedDesercionRows = [];
           moroDataCached = [];
                let cuotasHeaders = [];
                let cuotasHeaders = ["CUOTA", "SAN MAR", "INT MAR", "SAN ABR", "INT ABR", "SAN MAY", "INT MAY", "SAN JUL", "REP JUL", "SAN ENE"];
           let cuotasBodyRows = [];

           let totalMat = 0, totalPag = 0, totalDes = 0, totalCum = 95;

                // ==========================================
                // 1. ESCÁNER DINÁMICO DE DESERCIÓN PRINCIPAL (START i=0)
                // ==========================================
                let rCiclo = -1, cCiclo = -1;
                for (let r = 0; r < rows.length; r++) {
                    if (rows[r] && rows[r].c) {
                        for (let c = 0; c < Math.min(rows[r].c.length, 5); r++) {
                            if (safeString(rows[r].c[c]).toUpperCase() === 'CICLO') {
                                rCiclo = r;
                                cCiclo = c;
                                break;
                            }
                        }
                    }
                    if (rCiclo !== -1) break;
                }

                // Respaldo de seguridad absoluta si falla el buscador por celdas vacías
                if (rCiclo === -1) { rCiclo = 1; cCiclo = 2; }

                let colCiclo = cCiclo;
                let colTutor = cCiclo + 1;
                let colMat = cCiclo + 2;
                let colPag = cCiclo + 3;
                let colSus = cCiclo + 4;
                let colDes = cCiclo + 5;
                let colCum = cCiclo + 6;
                let colNot = cCiclo + 7;

                for (let i = rCiclo + 1; i < rows.length; i++) {
                // RECORRIDO MATRICIAL DE FILAS SEGURO (START i=0)
                for (let i = 0; i < rows.length; i++) {
               const row = rows[i];
               if (!row || !row.c) continue;

                    let cicloVal = safeString(row.c[colCiclo]);
                    let upperCiclo = cicloVal.toUpperCase();

                    if (upperCiclo.includes('TOTAL')) {
                        totalMat = getVal(row.c[colMat], true);
                        totalPag = getVal(row.c[colPag], true);
                        totalDes = getVal(row.c[colSus], true);
                        if (row.c[colCum]) {
                            let v = row.c[colCum].v;
                            totalCum = (typeof v === 'number' && v <= 1) ? v * 100 : parseFloat(v) || 95;
                        }
                        break; // Se detiene fulminantemente al llegar al total general
                    }

                    if (cicloVal !== '' && !upperCiclo.includes('VENCIMIENTO') && upperCiclo !== 'CICLO') {
                        cachedDesercionRows.push({
                            ciclo: cicloVal,
                            tutor: safeString(row.c[colTutor]),
                            matriculados: getVal(row.c[colMat], true),
                            pagantes: getVal(row.c[colPag], true),
                            suspendidos: getVal(row.c[colSus], true),
                            desercion: safePercent(row.c[colDes]),
                            cumplimiento: safePercent(row.c[colCum]),
                            nota: safeString(row.c[colNot])
                        });
                    }
                }

                // ==========================================
                // 2. ESCÁNER DE CRONOGRAMA DE CUOTAS (M4:V11)
                // ==========================================
                let rCuota = -1, cCuota = -1;
                for (let r = 0; r < rows.length; r++) {
                    if (rows[r] && rows[r].c) {
                        for (let c = 0; c < rows[r].c.length; c++) {
                            if (safeString(rows[r].c[c]).toUpperCase() === 'CUOTA') {
                                rCuota = r;
                                cCuota = c;
                                break;
                    // 1. Extraer Deserción por Ciclo (B3:J15) -> Indices fijos 1 a 9
                    let cicloName = safeString(row.c[2]); 
                    if (cicloName && cicloName.toUpperCase() !== 'CICLO') {
                        if (cicloName.toUpperCase().includes('TOTAL')) {
                            totalMat = getVal(row.c[4], true);
                            totalPag = getVal(row.c[5], true);
                            totalDes = getVal(row.c[6], true);
                            if (row.c[8]) {
                                let v = row.c[8].v;
                                totalCum = (typeof v === 'number' && v <= 1) ? v * 100 : parseFloat(v) || 95;
                       }
                        } else if (!cicloName.toUpperCase().includes('VENCIMIENTO')) {
                            cachedDesercionRows.push({
                                ciclo: cicloName,
                                tutor: safeString(row.c[3]),
                                matriculados: getVal(row.c[4], true),
                                pagantes: getVal(row.c[5], true),
                                suspendidos: getVal(row.c[6], true),
                                desercion: safePercent(row.c[7]),
                                cumplimiento: safePercent(row.c[8]),
                                nota: safeString(row.c[9])
                            });
                   }
               }
                    if (rCuota !== -1) break;
                }

                if (rCuota !== -1) {
                    let hRow = rows[rCuota];
                    for (let c = cCuota; c < hRow.c.length; c++) {
                        let hVal = safeString(hRow.c[c]);
                        if (!hVal) break;
                        cuotasHeaders.push(hVal);
                    // 2. Extraer Morosidad Completa (Y3:AE1000) -> Indices fijos 24 a 30
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

                    for (let r = rCuota + 1; r < rows.length; r++) {
                        let row = rows[r];
                        if (!row || !row.c) continue;
                        let cuotaCell = safeString(row.c[cCuota]);
                        if (!cuotaCell || isNaN(cuotaCell)) continue;

                    // 3. Extraer Cronograma de Cuotas de Pago (M5:V11) -> Indices fijos 12 a 21
                    let cuotaCell = safeString(row.c[12]); 
                    if (cuotaCell && !isNaN(cuotaCell) && cuotaCell !== '' && i >= 4 && i <= 12) {
                   let cells = [];
                        for (let k = 0; k < cuotasHeaders.length; k++) {
                            cells.push(safeString(row.c[cCuota + k]) || '-');
                        cells.push(cuotaCell);
                        for (let k = 13; k <= 21; k++) {
                            cells.push(row.c[k] ? safeString(row.c[k]) : '-');
                   }
                   cuotasBodyRows.push(cells);
               }
           }

                // ==========================================
                // 3. EXTRAER MOROSIDAD COMPLETA (Y3:AE1000)
                // ==========================================
                let rMoro = -1, cMoroDni = -1;
                for (let r = 0; r < rows.length; r++) {
                    if (rows[r] && rows[r].c) {
                        for (let c = 10; c < rows[r].c.length; c++) {
                            if (safeString(rows[r].c[c]).toUpperCase() === 'DNI') {
                                rMoro = r;
                                cMoroDni = c;
                                break;
                            }
                        }
                    }
                    if (rMoro !== -1) break;
                }

                if (rMoro !== -1) {
                    let colMoroNum = cMoroDni - 1;
                    let colMoroDni = cMoroDni;
                    let colMoroAlumno = cMoroDni + 1;
                    let colMoroCorte = cMoroDni + 2;
                    let colMoroTutor = cMoroDni + 3;
                    let colMoroCond = cMoroDni + 4;
                    let colMoroMotiv = cMoroDni + 5;

                    for (let j = rMoro + 1; j < rows.length; j++) {
                        const row = rows[j];
                        if (!row || !row.c) continue;

                        let mDni = safeString(row.c[colMoroDni]);
                        let mAlum = safeString(row.c[colMoroAlumno]);
                        if (!mDni && !mAlum) continue;
                        if (mDni.toUpperCase() === 'DNI' || mAlum.toUpperCase() === 'ALUMNO') continue;

                        moroDataCached.push({
                            num: row.c[colMoroNum] ? safeString(row.c[colMoroNum]) : (moroDataCached.length + 1),
                            dni: mDni,
                            alumno: mAlum,
                            corte: safeString(row.c[colMoroCorte]),
                            tutor: safeString(row.c[colMoroTutor]),
                            condicion: safeString(row.c[colMoroCond]),
                            motivos: safeString(row.c[colMoroMotiv])
                        });
                    }
                }

                // Renderizar KPI Globales
                // Renderizar KPI de cabecera superiores
           document.getElementById('lbl-total-mat').innerText = Math.round(totalMat);
           document.getElementById('lbl-total-pag').innerText = Math.round(totalPag);
           document.getElementById('lbl-total-des').innerText = Math.round(totalDes);
@@ -681,6 +591,7 @@
                   <td class="py-3 px-4 font-mono text-slate-400">${row.dni}</td>
                   <td class="py-3 px-4 font-bold text-slate-100">${row.alumno}</td>
                   <td class="py-3 px-4 text-center text-slate-400">${row.corte}</td>
                        <td class="py-3 px-4 text-slate-300 font-medium">${row.tutor}</td>
                   <td class="py-3 px-4 text-center">
                       <span class="px-2 py-1 rounded-md text-[10px] font-extrabold uppercase ${badgeClass}">${row.condicion}</span>
                   </td>
@@ -792,4 +703,4 @@
   setInterval(loadAllDashboardData, 60000);
</script>
</body>
</html>
</html> 
