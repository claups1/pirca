# Pirca data sources

Every number in `data/`, with its source and status. Generated 2026-10-24.

**Status legend**
- **verified**: read in an official / primary / peer-reviewed document saved in `data/raw/`, and spot-checked against that file.
- **sourced**: read in a real source, but a secondary one (press, chamber of commerce, retail listing), or used as a proxy / derived value.
- **illustrative estimate**: no source found; a placeholder for the app's math. Replace when you find a source.
- **UNVERIFIED**: no source found; needs your check before use.

## 1. ENFEN communiqués (`data/enfen/`)

All four are official PDFs from the Comisión Multisectorial ENFEN (verified). Status in all four: **Alerta de El Niño Costero**.

| ID | Date | Number(s) quoted | Status | Source |
|---|---|---|---|---|
| ENFEN-2026-18 | 2026-10-16 | Reservoirs at 58% of national hydraulic capacity | verified | [PDF](https://enfen.imarpe.gob.pe/download/comunicado-oficial-enfen-n-18-2026/?wpdmdl=2165) |
| ENFEN-2026-17 | 2026-09-28 | — | verified | [PDF](https://enfen.imarpe.gob.pe/download/comunicado-oficial-enfen-n-17-2026/?wpdmdl=2161) |
| ENFEN-2026-16 | 2026-09-14 | — | verified | [PDF](https://enfen.imarpe.gob.pe/download/comunicado-oficial-enfen-n-16-2026/?wpdmdl=2158) |
| ENFEN-2026-15 | 2026-08-28 | ≥62% probability of extraordinary magnitude Sep 2026–Jan 2027 (Niño 1+2); ≥58% very strong (Niño 3.4) | verified | [PDF](https://enfen.imarpe.gob.pe/download/comunicado-oficial-enfen-n-15-2026/?wpdmdl=2145) |

Next communiqué announced for 2026-10-30; re-check https://enfen.imarpe.gob.pe/comunicados/ before relying on these.

## 2. Exchange rate (`data/exchange_rate.json`)

| Number | Meaning | Status | Source |
|---|---|---|---|
| 3.447 | S/ per US$, Tipo de cambio - TC Interbancario (S/ por US$) - Venta, 2026-10-22 (raw 3.44671428571429) | verified | [BCRPData PD04638PD](https://estadisticas.bcrp.gob.pe/estadisticas/series/diarias/resultados/PD04638PD/html/2026-10-01/2026-10-24/) |

## 3. Historical impacts (`data/historical_impacts.csv`)

| ID | District | Value | Unit | Fact | Status | Source |
|---|---|---|---|---|---|---|
| HIST-1998-01 | Piura region | 4424 | m3/s | Río Piura instantaneous peak flow at Puente Sánchez Cerro on 12 Mar 1998 (1982-83 peak: 2,478 m3/s) | verified | [CAF](https://dipecholac.net/docs/files/996-publicacion-caf-peru-nino-97-98.pdf) |
| HIST-1998-02 | Piura region | 601.1 | m3/s (mean) | Río Piura mean flow at Puente Sánchez Cerro, 721% above normal | verified | [CAF](https://dipecholac.net/docs/files/996-publicacion-caf-peru-nino-97-98.pdf) |
| HIST-1998-03 | Piura region | 1497 | m3/s | Río Chira peak flow in April 1998 | verified | [CAF](https://dipecholac.net/docs/files/996-publicacion-caf-peru-nino-97-98.pdf) |
| HIST-1998-04 | Piura | 412.2 | mm (February) | Rainfall in Piura city in February 1998; areas east of the city exceeded 1,000 mm | verified | [OPS/PAHO](https://iris.paho.org/server/api/core/bitstreams/de64679b-b1c7-44ca-8c40-1fc09f42e666/content) |
| HIST-1998-05 | Piura region | 26000 | % anomaly | January 1998 rainfall anomaly on Piura's coastal strip | verified | [CAF](https://dipecholac.net/docs/files/996-publicacion-caf-peru-nino-97-98.pdf) |
| HIST-1998-06 | Piura region | 3 | months | Panamericana between Tumbes and Piura cut; special flights needed | verified | [CAF](https://dipecholac.net/docs/files/996-publicacion-caf-peru-nino-97-98.pdf) |
| HIST-1998-07 | Chulucanas | several | weeks | Piura–Lambayeque Panamericana cut at Mórrope for several weeks; Motupe–Chulucanas–Piura detour also cut by a bridge collapse | verified | [CAF](https://dipecholac.net/docs/files/996-publicacion-caf-peru-nino-97-98.pdf) |
| HIST-1998-08 | Piura | 9 | bridges named | Bridges named as collapsed include Bolognesi and San Miguel de Piura in Piura city; Piura–La Arena–Sullana road damaged (count is of names listed) | verified | [CAF](https://dipecholac.net/docs/files/996-publicacion-caf-peru-nino-97-98.pdf) |
| HIST-1998-09 | Talara | 10 | road sections | Paita–Talara road cut in 10 sections (Panamericana Km 1048-1084) | verified | [CAF](https://dipecholac.net/docs/files/996-publicacion-caf-peru-nino-97-98.pdf) |
| HIST-1998-10 | Talara | several | weeks | Mudflows destroyed the water pipeline feeding Talara; town without water | verified | [CAF](https://dipecholac.net/docs/files/996-publicacion-caf-peru-nino-97-98.pdf) |
| HIST-1998-11 | Sullana | 900 | families | Overflow of the canal vía (quebradas El Alacrán and Cieneguillo) left families damnificadas | verified | [CAF](https://dipecholac.net/docs/files/996-publicacion-caf-peru-nino-97-98.pdf) |
| HIST-1998-12 | Cura Mori;Tambogrande;El Tallán | 12 | localities named | Prolonged flooding of homes, isolation and evacuation in 12 named localities | verified | [CAF](https://dipecholac.net/docs/files/996-publicacion-caf-peru-nino-97-98.pdf) |
| HIST-1998-13 | Piura region | 172 | health facilities | Health facilities damaged (most affected department); PAHO gives 123 | verified | [CAF](https://dipecholac.net/docs/files/996-publicacion-caf-peru-nino-97-98.pdf) |
| HIST-1998-14 | Peru (national) | 410 | suspected cases | Dengue was minor in 1998 nationally: 410 suspected, 61 lab-confirmed (contrast with 2017) | verified | [OPS/PAHO](https://iris.paho.org/server/api/core/bitstreams/de64679b-b1c7-44ca-8c40-1fc09f42e666/content) |
| HIST-2017-01 | Piura | 3468 | m3/s | Río Piura overflowed from 25 Mar 2017, peaking at 3,468 m3/s, with complete flooding of Piura city | verified | [INDECI](https://cdn.www.gob.pe/uploads/document/file/1396530/R.J.%20N%C2%B0%20044-2017-INDECI.pdf) |
| HIST-2017-02 | Piura;Castilla;Catacaos | 2754.5 | m3/s (daily mean) | Río Piura daily mean flow at Puente Sánchez Cerro on 27 Mar 2017; sudden discharges flooded Piura, Castilla, Catacaos and Bajo Piura | verified | [Proyecto Especial Chira-Piura (GORE Piura)](https://cdn.www.gob.pe/uploads/document/file/3274125/Informes%20T%C3%A9cnicos%20hidro%20N%C2%B0%2000003-2017.pdf) |
| HIST-2017-03 | Chulucanas | 1154.6 | mm (March) | March 2017 rainfall (normal 100.1 mm) | verified | [Proyecto Especial Chira-Piura (GORE Piura)](https://cdn.www.gob.pe/uploads/document/file/3274125/Informes%20T%C3%A9cnicos%20hidro%20N%C2%B0%2000003-2017.pdf) |
| HIST-2017-04 | Tambogrande | 1149.8 | mm (March) | March 2017 rainfall (normal 50.1 mm; daily max 180 mm) | verified | [Proyecto Especial Chira-Piura (GORE Piura)](https://cdn.www.gob.pe/uploads/document/file/3274125/Informes%20T%C3%A9cnicos%20hidro%20N%C2%B0%2000003-2017.pdf) |
| HIST-2017-05 | Piura | 456.0 | mm (March) | March 2017 rainfall (normal 31.8 mm; daily max 84.6 mm) | verified | [Proyecto Especial Chira-Piura (GORE Piura)](https://cdn.www.gob.pe/uploads/document/file/3274125/Informes%20T%C3%A9cnicos%20hidro%20N%C2%B0%2000003-2017.pdf) |
| HIST-2017-06 | Sullana | 423.4 | mm (March) | March 2017 rainfall (normal 31.2 mm) | verified | [Proyecto Especial Chira-Piura (GORE Piura)](https://cdn.www.gob.pe/uploads/document/file/3274125/Informes%20T%C3%A9cnicos%20hidro%20N%C2%B0%2000003-2017.pdf) |
| HIST-2017-07 | Catacaos | 30196 | persons | People living in damnificada/afectada homes (highest district in Peru) | verified | [INEI](https://www.mesadeconcertacion.org.pe/sites/default/files/archivos/2017/documentos/09/censo_el_nino_costero_2017.pdf) |
| HIST-2017-08 | Tambogrande | 13282 | persons | People living in damnificada/afectada homes | verified | [INEI](https://www.mesadeconcertacion.org.pe/sites/default/files/archivos/2017/documentos/09/censo_el_nino_costero_2017.pdf) |
| HIST-2017-09 | La Arena | 7469 | persons | People living in damnificada/afectada homes | verified | [INEI](https://www.mesadeconcertacion.org.pe/sites/default/files/archivos/2017/documentos/09/censo_el_nino_costero_2017.pdf) |
| HIST-2017-10 | Castilla | 7249 | persons | People living in damnificada/afectada homes | verified | [INEI](https://www.mesadeconcertacion.org.pe/sites/default/files/archivos/2017/documentos/09/censo_el_nino_costero_2017.pdf) |
| HIST-2017-11 | Cura Mori | 5602 | persons | People living in damnificada/afectada homes | verified | [INEI](https://www.mesadeconcertacion.org.pe/sites/default/files/archivos/2017/documentos/09/censo_el_nino_costero_2017.pdf) |
| HIST-2017-12 | Chulucanas | 5177 | persons | People living in damnificada/afectada homes | verified | [INEI](https://www.mesadeconcertacion.org.pe/sites/default/files/archivos/2017/documentos/09/censo_el_nino_costero_2017.pdf) |
| HIST-2017-13 | Piura | 4099 | persons | People living in damnificada/afectada homes | verified | [INEI](https://www.mesadeconcertacion.org.pe/sites/default/files/archivos/2017/documentos/09/censo_el_nino_costero_2017.pdf) |
| HIST-2017-14 | Veintiséis de Octubre | 3590 | persons | People living in damnificada/afectada homes | verified | [INEI](https://www.mesadeconcertacion.org.pe/sites/default/files/archivos/2017/documentos/09/censo_el_nino_costero_2017.pdf) |
| HIST-2017-15 | Piura region | 59453 | persons | People in damnificada homes in INEI's surveyed areas (highest region) | verified | [INEI](https://www.mesadeconcertacion.org.pe/sites/default/files/archivos/2017/documentos/09/censo_el_nino_costero_2017.pdf) |
| HIST-2017-16 | Piura region | 43732 | persons | People in afectada homes in INEI's surveyed areas | verified | [INEI](https://www.mesadeconcertacion.org.pe/sites/default/files/archivos/2017/documentos/09/censo_el_nino_costero_2017.pdf) |
| HIST-2017-17 | Piura region | 59335 | persons | People reporting economic-loss impact (highest region; Áncash next at 20,383) | verified | [INEI](https://www.mesadeconcertacion.org.pe/sites/default/files/archivos/2017/documentos/09/censo_el_nino_costero_2017.pdf) |
| HIST-2017-18 | Piura region | 91835 | persons | COEN consolidated damnificados | sourced | [El Comercio](https://elcomercio.pe/peru/piura-ano-tragedia-situacion-actual-nino-costero-noticia-507536-noticia/) |
| HIST-2017-19 | Piura region | 310570 | persons | COEN consolidated afectados | sourced | [El Comercio](https://elcomercio.pe/peru/piura-ano-tragedia-situacion-actual-nino-costero-noticia-507536-noticia/) |
| HIST-2017-20 | Piura region | 5724 | homes | COEN consolidated homes collapsed (8,469 uninhabitable, 71,008 affected) | sourced | [El Comercio](https://elcomercio.pe/peru/piura-ano-tragedia-situacion-actual-nino-costero-noticia-507536-noticia/) |
| HIST-2017-21 | Piura region | 15 | bridges | Bridges destroyed as of 21 Apr 2017 (71 affected), per COEN | sourced | [Cámara de Comercio y Producción de Piura](https://www.camcopiura.org.pe/revistas/2017/Revista%20Empresario%2086.pdf) |
| HIST-2017-22 | Piura region | 147 | km | Highway km destroyed as of 21 Apr 2017 (463 km affected), per COEN | sourced | [Cámara de Comercio y Producción de Piura](https://www.camcopiura.org.pe/revistas/2017/Revista%20Empresario%2086.pdf) |
| HIST-2017-23 | Piura region | 7500 | million soles | Chamber of Commerce estimate of regional economic losses (lower bound) | sourced | [Cámara de Comercio y Producción de Piura](https://www.camcopiura.org.pe/revistas/2017/Revista%20Empresario%2086.pdf) |
| HIST-2017-24 | Piura region | 4591 | ha | Crop area lost Dec 2016–Apr 2017 (22,915 ha affected) | sourced | [Cámara de Comercio y Producción de Piura](https://www.camcopiura.org.pe/revistas/2017/Revista%20Empresario%2086.pdf) |
| HIST-2017-25 | Piura region | 41078 | cases | Dengue cases in 2017 through epidemiological week 25 (incidence 219.3 per 10,000) | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/3892774/Semana%20Epidemiol%C3%B3gica%20N%C2%B0%2025-2019.pdf) |
| HIST-2017-26 | Piura region | 17 | deaths | Dengue deaths in the 2017 outbreak per DIRESA outbreak table (same bulletin shows 14 by week 25) | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/3892774/Semana%20Epidemiol%C3%B3gica%20N%C2%B0%2025-2019.pdf) |
| HIST-2017-27 | Piura region | 6270 | confirmed cases | Confirmed dengue cases (of 32,630 reported) | verified | [OPS/PAHO Perú](https://www.paho.org/es/peru/emergencia-por-impacto-fenomeno-nino-costero-peru-2017) |
| HIST-2017-28 | Piura;Castilla;Sullana;Veintiséis de Octubre;Tambogrande;Talara;Catacaos;Bellavista | 87 | % | Share of notified dengue cases concentrated in 8 districts (Talara = Pariñas district) | verified | [OPS/PAHO Perú](https://www.paho.org/es/peru/emergencia-por-impacto-fenomeno-nino-costero-peru-2017) |
| HIST-2017-29 | Catacaos | 10 | of 14 centros poblados | Centros poblados of Catacaos under water, per COER (10 of 14) | sourced | [Mongabay Latam](https://es.mongabay.com/2017/04/emergencia-piura-balance-mes-funesto-norte-del-peru/) |
| HIST-2017-30 | Castilla | 1.20 | m | Floodwater depth inside Castilla's market, three blocks from the river; shortages and price rises at Mercado Modelo | sourced | [Mongabay Latam](https://es.mongabay.com/2017/04/emergencia-piura-balance-mes-funesto-norte-del-peru/) |
| HIST-2017-31 | Piura region | 140 | schools | Schools affected by rains; school year start (13 Mar) postponed | sourced | [Mongabay Latam](https://es.mongabay.com/2017/04/emergencia-piura-balance-mes-funesto-norte-del-peru/) |
| HIST-2017-32 | Piura region | 80 | % | Share of roads damaged, estimate by regional transport director | sourced | [Mongabay Latam](https://es.mongabay.com/2017/04/emergencia-piura-balance-mes-funesto-norte-del-peru/) |
| HIST-2017-33 | Piura;Catacaos;Cura Mori;La Unión;La Arena | 27000 | persons | People affected by the Río Piura overflow; most affected districts named | sourced | [MCLCP Piura](https://mesadeconcertacion.org.pe/storage/documentos/2023-04-14/memoria-evento-a-seis-anos-de-la-inundacion.pdf) |
| HIST-2023-01 | Piura region | 2023-03-16 | date | ENFEN raised the warning status to 'Alerta de El Niño costero' for the 2023 event | verified | [Comunicado Oficial ENFEN N° 03-2023 (16 Mar 2023)](https://repositorio.imarpe.gob.pe/bitstream/20.500.12958/8575/1/Comunicado%20Of_ENFEN%20N%c2%b0%2003-2023.pdf) |
| HIST-2023-02 | Piura region | 2024-04-05 | date | ENFEN ended the 2023-24 coastal El Niño alert (status 'No Activo'); the alert lasted from 16 Mar 2023 to 5 Apr 2024 | verified | [Comunicado Oficial ENFEN N° 06-2024 (5 Apr 2024)](https://www.senamhi.gob.pe/load/file/02204SENA-183.pdf) |
| HIST-2023-03 | Piura region | 5-14 Mar 2023 | dates | SENAMHI: the first spell of extreme rain on the north coast (5-14 March 2023) was driven by cyclone Yaku | verified | [SENAMHI](https://cdn.www.gob.pe/uploads/document/file/4404621/MARZO_2023.pdf) |
| HIST-2023-04 | Chulucanas | 256 | % above normal | March 2023 rainfall anomaly at the Chulucanas station | verified | [SENAMHI](https://cdn.www.gob.pe/uploads/document/file/4404621/MARZO_2023.pdf) |
| HIST-2023-05 | Piura region | 94.5 | mm (one day) | Daily rain at the Miraflores station (Piura city) on 24 Mar 2023, above its 2017 daily maximum of 87.2 mm | sourced | [Infomercado (25 Mar 2023)](https://infomercado.pe/fenomeno-del-nino-costero-lluvias-piura-ciclon-yaku-25032023-ja/) |
| HIST-2023-06 | Piura;Castilla | 1664 | m3/s | Río Piura flow at Puente Sánchez Cerro at 6:00 a.m. on 16 Mar 2023 (channel capacity about 2,000 m3/s) | sourced | [UDEP Hoy (16 Mar 2023)](https://www.udep.edu.pe/hoy/?p=133403) |
| HIST-2023-07 | Piura region | 2945 | m3/s | Poechos dam spillway release on 16-17 Apr 2023; the Río Chira overflowed in Sullana and Paita provinces | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-08 | Piura region | 26605 | persons | Damnificados in Piura department from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 12 dead, 48 injured, 2 missing | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-09 | Piura region | 285638 | persons | Afectados in Piura department from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 9,998 people had their livelihoods affected | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-10 | Piura region | 2282 | homes | Homes destroyed in Piura department, January-May 2023 (D.S. 065-2023 table updated to 19 Jul 2023); 7,795 uninhabitable and 104,014 affected | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-11 | Piura region | 61 | bridges | Vehicle bridges destroyed in Piura department, January-May 2023 (106 affected; footbridges 38 destroyed, 28 affected) (D.S. 065-2023 table updated to 19 Jul 2023) | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-12 | Piura region | 60 | days | D.S. 065-2023-PCM (25 May 2023) extended the state of emergency for a large-scale disaster in districts of Lambayeque, Piura and Tumbes | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-13 | Castilla | 1692 | persons | Damnificados in Castilla from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 10,400 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-14 | Veintiséis de Octubre | 3457 | persons | Damnificados in Veintiséis de Octubre from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 13,010 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-15 | Piura | 804 | persons | Damnificados in Piura from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 7,190 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-16 | Catacaos | 590 | persons | Damnificados in Catacaos from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 32,090 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-17 | Cura Mori | 252 | persons | Damnificados in Cura Mori from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 7,893 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-18 | El Tallán | 402 | persons | Damnificados in El Tallán from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 3,811 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-19 | La Arena | 45 | persons | Damnificados in La Arena from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 15,856 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-20 | La Unión | 667 | persons | Damnificados in La Unión from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 10,713 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-21 | Tambogrande | 2965 | persons | Damnificados in Tambogrande from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 43,027 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-22 | Chulucanas | 426 | persons | Damnificados in Chulucanas from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 14,709 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-23 | Sullana | 1528 | persons | Damnificados in Sullana from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 6,213 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-24 | Bellavista | 320 | persons | Damnificados in Bellavista from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 2,620 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-25 | Talara | 759 | persons | Damnificados in Talara (Pariñas district) from the January-May 2023 rains (D.S. 065-2023 table updated to 19 Jul 2023); 3,053 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-26 | Paita | 1311 | persons | Damnificados in Paita district from the 2023 rains (table 'DEE NO VIGENTE' updated to 9 Jun 2023); 1,407 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-27 | Paita | 2023-03-29 | date | INDECI field report (GIRED Piura, after the 29 Mar 2023 visit): homes damaged and several areas of Paita district still flooded | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-28 | Sechura | 163 | persons | Damnificados in Sechura district from the 2023 rains (table 'DEE NO VIGENTE' updated to 9 Jun 2023); 8,563 afectados | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-29 | Sechura | 121 | days (at least) | The overflowing La Niña lagoon destroyed the Bayóvar-Chiclayo road (PE-04, La Mina sector) on 20 Mar 2023; traffic was still interrupted on 19 Jul 2023 (at least 121 days, counted from the two dates) | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-30 | Paita province (La Huaca) | 12 | days | The Paita-Sullana road was cut 4 km from La Huaca (entry of 30 Mar 2023) and reported reopened on 11 Apr 2023 after the Cuesta Pucuzula landslide was cleared (12 days, counted from the two dates) | verified | [INDECI COEN](https://portal.indeci.gob.pe/wp-content/uploads/2023/07/INFORME-DE-EMERGENCIA-N.%C2%BA-2186-27JUL2023-LLUVIAS-INTENSAS-EN-EL-DEPARTAMENTO-DE-PIURA-164-DEE.pdf) |
| HIST-2023-31 | Piura region | 7 | days | The regional education office moved the start of the public school year from 13 to 20 March 2023 because of the rains | sourced | [Andina (10 Mar 2023)](https://andina.pe/agencia/noticia-lluvias-intensas-piura-tambien-postergan-clases-escolares-hasta-20-marzo-932216.aspx) |
| HIST-2023-32 | Piura region | 12-18 | million soles | Cámara de Comercio de Piura estimate of losses from closed premises (period not stated); 20-30% of premises could not operate normally out of about S/ 60 million of commerce a day | sourced | [Agraria.pe (16 Mar 2023)](https://agraria.pe/noticias/piura-costo-para-transportar-alimentos-sube-debido-a-las-llu-31171) |
| HIST-2023-33 | Piura region | 13 | % | Rise in the cost of transporting basic goods in Piura because of the rains and floods (16 Mar 2023) | sourced | [Agraria.pe (16 Mar 2023)](https://agraria.pe/noticias/piura-costo-para-transportar-alimentos-sube-debido-a-las-llu-31171) |
| HIST-2023-34 | Sullana | 2023-03-24 | date | A canal overflow on 24 Mar 2023 flooded the Sullana city market and swept away stalls; traders suspended service (INDECI: the canal Vía overflow damaged homes and commercial premises in Sullana district) | sourced | [Andina (24 Mar 2023)](https://andina.pe/agencia/noticia-emergencia-piura-lluvia-intensa-arrasa-con-mercadillo-sullana-934067.aspx) |
| HIST-2023-35 | Piura region | 10 | patients moved | The Open Plaza shopping centre in Piura flooded in some sectors and the ICU roof of the Cayetano Heredia hospital collapsed; 10 ICU patients were moved | sourced | [RPP (10 Mar 2023)](https://rpp.pe/peru/piura/piura-lluvias-causan-serios-danos-en-hospital-cayetano-heredia-y-en-centro-comercial-noticia-1471897) |
| HIST-2023-36 | Piura region | 79643 | cases | Dengue cases in Piura region in calendar year 2023 (SE 49 cut of 13 Dec 2023 gave 79,998) | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/6372642/5590673-sala-diaria-dengue-semana-20-2024-piura-17-05-2024.pdf) |
| HIST-2023-37 | Piura region | 148 | deaths | Dengue deaths in Piura region in calendar year 2023 (SE 49 cut of 13 Dec 2023 gave 153) | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/6372642/5590673-sala-diaria-dengue-semana-20-2024-piura-17-05-2024.pdf) |
| HIST-2023-38 | Castilla | 11192 | cases | Dengue cases in Castilla in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |
| HIST-2023-39 | Piura | 10751 | cases | Dengue cases in Piura in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |
| HIST-2023-40 | Sullana | 7660 | cases | Dengue cases in Sullana in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |
| HIST-2023-41 | Chulucanas | 5380 | cases | Dengue cases in Chulucanas in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |
| HIST-2023-42 | Tambogrande | 4678 | cases | Dengue cases in Tambogrande in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |
| HIST-2023-43 | Talara | 4608 | cases | Dengue cases in Talara (Pariñas district) in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |
| HIST-2023-44 | Veintiséis de Octubre | 4055 | cases | Dengue cases in Veintiséis de Octubre in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |
| HIST-2023-45 | Paita | 3888 | cases | Dengue cases in Paita in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |
| HIST-2023-46 | Catacaos | 3358 | cases | Dengue cases in Catacaos in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |
| HIST-2023-47 | Bellavista | 2095 | cases | Dengue cases in Bellavista in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |
| HIST-2023-48 | La Unión | 1764 | cases | Dengue cases in La Unión in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |
| HIST-2023-49 | Sechura | 981 | cases | Dengue cases in Sechura in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |
| HIST-2023-50 | La Arena | 916 | cases | Dengue cases in La Arena in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |
| HIST-2023-51 | Cura Mori | 755 | cases | Dengue cases in Cura Mori in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |
| HIST-2023-52 | El Tallán | 307 | cases | Dengue cases in El Tallán in 2023, cut-off 13 Dec 2023 | verified | [DIRESA Piura](https://cdn.www.gob.pe/uploads/document/file/5610326/4976130-semana-epidemiologica-n-049-2023.pdf) |

**Figures seen but NOT included (UNVERIFIED or conflicting; check before using):**
- "120,000 damnificados/afectados in Piura" for 1997-98: one El Peruano piece says 1997-98, another places it in 1983.
- 1998 Río Piura peak "casi 3,900 m3/s" (La República 2026, quoting an engineer) vs 4,424 m3/s in CAF and PAHO.
- 1983 Río Piura peak: CAF 2,478 m3/s vs PAHO 2,300 m3/s.
- 1998 Miraflores station 777.3 mm (PAHO citing UDEP): period unclear.
- 2017 Río Piura flow in press: "3,100 m3/s según Senamhi", "excedió 2,500" vs INDECI's 3,468 m3/s.
- 2017 COEN totals for Piura vary by cut-off date: 14,933/211,184 (mid-Mar); 18,996/225,492 (Mar); 41,925/349,471 (21 Apr); 91,835/310,570 (El Comercio 2018); 97,708/427,693 (Peru21, not fetched). The CSV uses the 21 Apr figures for roads/bridges and the El Comercio figures for people.
- 2017 Piura dengue deaths: press/IGP say 33, 53 or 61; DIRESA says 14 by week 25 and 17 for the outbreak (CSV uses 17).
- 2017 losses of S/10,000 million (Agraria.pe), US$400 million to 10 Apr (Camcopiura), and Piura's 31% share of 15,129 SBS insurance claims: not read in a source.
- School restart date of 20 Mar 2017 in Piura: not confirmed for 2017; the confirmed 20 Mar postponement is 2023 (HIST-2023-31).
- Not found: duration of the 2017 Piura airport closure; days the Panamericana Piura–Chiclayo was closed in 2017.
- OCHA Sitrep 06 (Apr 2017) "318,871 affected in Piura": ReliefWeb blocked (403).
- ARCC/PIRCC Piura counts (170 roads, 117 bridges): Congreso PDF 404. MCLCP confirms only "Presupuesto inicial ... 7,541 millones".
- 2023 rain deaths: INDECI's table gives 12 (cut 19 Jul 2023, HIST-2023-08); MINSA COE Salud gives 21 (7 Jun 2023). They count different things; the CSV uses INDECI.
- 2023 dengue: 79,643 cases / 148 deaths (calendar year, DIRESA SE 20-2024; used) vs 79,998 / 153 at the 13 Dec 2023 cut (SE 49): likely later reclassification, not confirmed.
- 2023 rain on 24 Mar: 94.5 mm (Infomercado citing SENAMHI; used) vs 101.8 mm in a truncated SENAMHI social-media post that does not name the station.
- 2023 INDECI road lengths (1,045,739.82 m affected / 364,172.4 m destroyed): left out because the table columns could be rural paths or highways.
- 2023 district damage beyond damnificados and afectados (homes destroyed, uninhabitable) was left out: blank cells make the later columns ambiguous in the extracted table.
- Not confirmed (search summaries only, not used): 82 dengue deaths and 42,415 cases in June 2023; 222 schools damaged; 227 damnificados on 10 Mar 2023; Río Piura 1,204 m3/s; Huarmaca 94.5 mm; S/13,000 million losses (Piura, Lambayeque and Tumbes combined).
- Not found for 2023: an exact closure in days of the Panamericana Norte (Piura–Chiclayo, Sullana–Talara, Piura–Chulucanas); any sourced effect of dengue on work, schools or businesses.

## 4. Districts (`data/districts.csv`)

The flood hazard level is **derived by Pirca from the HIST rows above, not an official CENEPRED rating**.
Rule: **high** = district named as flooded in a HIST row, or a HIST row with ≥5,000 people in damaged homes; **medium** = other district-level impacts only; **UNVERIFIED** = no district-level evidence found.

| District | Province | Level | Flood HIST IDs | Other HIST IDs |
|---|---|---|---|---|
| Piura | Piura | high | HIST-2017-01, HIST-2017-02, HIST-2017-33 | HIST-1998-04, HIST-1998-08, HIST-2017-05, HIST-2017-13, HIST-2017-28, HIST-2023-06, HIST-2023-15, HIST-2023-39 |
| Castilla | Piura | high | HIST-2017-02, HIST-2017-10 | HIST-2017-28, HIST-2017-30, HIST-2023-06, HIST-2023-13, HIST-2023-38 |
| Veintiséis de Octubre | Piura | medium | — | HIST-2017-14, HIST-2017-28, HIST-2023-14, HIST-2023-44 |
| Catacaos | Piura | high | HIST-2017-02, HIST-2017-29, HIST-2017-33, HIST-2017-07 | HIST-2017-28, HIST-2023-16, HIST-2023-46 |
| Cura Mori | Piura | high | HIST-1998-12, HIST-2017-33, HIST-2017-11 | HIST-2023-17, HIST-2023-51 |
| La Arena | Piura | high | HIST-2017-33, HIST-2017-09 | HIST-2023-19, HIST-2023-50 |
| La Unión | Piura | high | HIST-2017-33 | HIST-2023-20, HIST-2023-48 |
| El Tallán | Piura | high | HIST-1998-12 | HIST-2023-18, HIST-2023-52 |
| Tambogrande | Piura | high | HIST-1998-12, HIST-2017-08 | HIST-2017-04, HIST-2017-28, HIST-2023-21, HIST-2023-42 |
| Chulucanas | Morropón | high | HIST-2017-12 | HIST-1998-07, HIST-2017-03, HIST-2023-04, HIST-2023-22, HIST-2023-41 |
| Sullana | Sullana | high | HIST-1998-11, HIST-2023-34 | HIST-2017-06, HIST-2017-28, HIST-2023-23, HIST-2023-40 |
| Bellavista | Sullana | medium | — | HIST-2017-28, HIST-2023-24, HIST-2023-47 |
| Paita | Paita | high | HIST-2023-27 | HIST-2023-26, HIST-2023-45 |
| Talara | Talara | medium | — | HIST-1998-09, HIST-1998-10, HIST-2017-28, HIST-2023-25, HIST-2023-43 |
| Sechura | Sechura | medium | — | HIST-2023-28, HIST-2023-29, HIST-2023-49 |

Changes from adding 2023 (Prompt 26): **Paita UNVERIFIED → high** (INDECI field report: "varias zonas aún continúan inundadas", HIST-2023-27; 1,311 damnificados, HIST-2023-26) and **Sechura UNVERIFIED → medium** (district impacts without a flooding statement: HIST-2023-28 and the PE-04 road cut HIST-2023-29). No other level changed.

UNVERIFIED districts now: none. CENEPRED's scenario study (linked from ENFEN-2026-18: https://sigrid.cenepred.gob.pe/sigridv3/documento/22787) remains the best source to check the derived levels against.

## 5. Action catalog (`data/action_catalog.csv`)

Retail prices are Promart's public catalog (VTEX API) as seen on 2026-10-24; the API JSON is saved in `data/raw/actions/`. "protects" = share of the targeted loss the action avoids (0–1). Every recommendation quote was read in the linked source.

| ID | Action | Cost S/ | Cost status | Cost source | Protects | Protects status | Protects source |
|---|---|---|---|---|---|---|---|
| CAT-01 | Raise shelves / store stock on platforms at least 15-30 cm off the floor | 249.90–589.00 (per metal shelving unit) | sourced | [link](https://www.promart.pe/estanteria-cromada-180-cm-x-5-niveles/p) | 0.48 | sourced (proxy) | [link](https://nhess.copernicus.org/articles/5/117/2005/nhess-5-117-2005.pdf) |
| CAT-02 | Sandbags at the shop entrance | 77.00–231.00 (10 to 30 filled sacks) | sourced prices; illustrative quantity | [link](https://www.promart.pe/sacos-de-polipropileno-x-1-unidad-krl-173671/p) | 0.29 | sourced | [link](https://nhess.copernicus.org/articles/5/117/2005/nhess-5-117-2005.pdf) |
| CAT-03 | Sealed / waterproof containers for goods and documents | 64.90–149.90 (per large hermetic box) | sourced | [link](https://www.promart.pe/caja-megarock--90-negro-con-ganchos-y-ruedas-polinplast/p) | 0.5 | illustrative estimate | — |
| CAT-04 | Flood barrier at the door (compuerta / sealed door base) | 500.00 (per barrier (proxy)) | sourced (loose proxy) | [link](https://elbuho.pe/2023/11/trujillo-arturo-fernandez-anuncia-barreras-de-s-500-para-proteger-a-la-poblacion-de-huaicos/) | 0.29 | sourced | [link](https://nhess.copernicus.org/articles/5/117/2005/nhess-5-117-2005.pdf) |
| CAT-05 | Move high-value stock to an upper floor or safe space | 0.00+ (owner's own labour) | illustrative estimate | — | 0.48 | sourced (proxy) | [link](https://nhess.copernicus.org/articles/5/117/2005/nhess-5-117-2005.pdf) |
| CAT-06 | Emergency cash reserve (fondo de emergencia) | — (one month of profit) | sourced rule; no S/ figure | [link](https://www.apec.org/-/media/APEC/Publications/2013/9/Guidebook-on-SME-Business-Continuity-Planning/TOC/Guidebook-on-SME-Business-Continuity-Planning---Spanish.pdf) | 0.3 | illustrative estimate | — |
| CAT-07 | Back up business records (cloud copy, photos of inventory, sealed paper copies) | 64.99–415.00 (per year (cloud) / one-off (external disk)) | sourced | [link](https://larepublica.pe/tecnologia/actualidad/2023/12/26/google-one-en-oferta-podras-tener-hasta-2-tb-de-espacio-en-la-nube-y-pagarlo-entre-5-personas-495014) | 0.5 | illustrative estimate | — |
| CAT-08 | Stock up on non-perishable basics from suppliers before roads are cut | — (working capital, shop-specific) | no sourced figure (left blank) | — | 0.3 | illustrative estimate | — |
| CAT-09 | Mosquito control for dengue (remove standing water, cover containers, screens, repellent) | 5.90–50.90 (1 window screen up to 2 window screens + 1 door screen + 1 repellent) | sourced prices; illustrative quantity | [link](https://www.promart.pe/malla-mosquitera-para-ventana-180x150cm-orange-166130/p) | 0.78 | sourced | [link](https://journals.plos.org/plosntds/article/file?id=10.1371/journal.pntd.0004551&type=printable) |
| CAT-10 | Business insurance covering rain and flood (multirriesgo / microseguro) | 36.00–1944.00 (per year) | sourced | [link](https://www.mapfre.com.pe/media/TARIFARIO-SEGURO-MULTIRIESGO-EMPRESAS-24-HORAS.pdf) | 0.95 | sourced (derived) | [link](https://www.mapfre.com.pe/media/TARIFARIO-SEGURO-MULTIRIESGO-EMPRESAS-24-HORAS.pdf) |
| CAT-11 | Clean gutters and drains; repair and waterproof the roof | 69.90–219.30 (one gutter up to gutter + waterproofing + one roof sheet) | sourced prices; illustrative quantity | [link](https://www.promart.pe/canaleta-pluvial-para-techos-4-100mm-4m/p) | 0.3 | illustrative estimate | — |
| CAT-12 | Electrical safety: 30 mA residual-current breaker, raise outlets, cut power before water enters | 49.90–162.40 (breaker (+ outlet); electrician labour not included) | sourced | [link](https://www.promart.pe/interruptor-diferencial-steck-2x25a-30ma-169424/p) | 0.36 | sourced (proxy) | [link](https://nhess.copernicus.org/articles/5/117/2005/nhess-5-117-2005.pdf) |
| CAT-13 | Business continuity plan and emergency backpack (mochila de emergencia) | 99.90–159.90 (per emergency backpack; plan itself is free (APEC template)) | sourced | [link](https://www.promart.pe/mochila-de-emergencia-basica/p) | 0.2 | illustrative estimate | — |
| CAT-14 | Alternative sales channel (WhatsApp orders, delivery, Yape payments) | 0.00+ (Yape free up to 5 UIT (S/25,750) of sales a month; Yape Empresa 2.95% of daily sales above that) | sourced | [link](https://gestion.pe/tu-dinero/yape-tres-mitos-y-verdades-sobre-los-cobros-en-esta-aplicacion-noticia/) | 0.3 | illustrative estimate | — |
| CAT-15 | Power-outage and cold-chain plan (don't overload freezers, keep non-perishables, rechargeable lights) | 14.90–29.90 (per rechargeable lantern) | sourced | [link](https://www.promart.pe/linterna-4-led-recargable-werken-151900/p) | 0.2 | illustrative estimate | — |

**Caveats to check**
- All sourced "protects" factors come from non-Peruvian studies (German floods: Kreibich et al. 2005; global dengue meta-analysis: Bowman et al. 2016). Several are proxies (e.g. 'flood adapted use' stands in for raised shelves).
- CAT-09's 0.78 is 1 − odds ratio 0.22 for house screening (95% CI 0.05–0.93): an odds reduction, not a risk reduction.
- CAT-10's 0.95 is derived from Mapfre's 5% deductible (min S/500); insurance transfers loss rather than preventing it, and only up to the sum insured.
- CAT-04's S/500 is a municipal quebrada barrier in Trujillo, not a shop-door product. No Peruvian retail flood door barrier was found.
- CAT-07's Google One price is from Dec 2023; Google reportedly raised Peru prices in 2025 (no S/ figure found).
- Quantities in CAT-02, CAT-09 and CAT-11 (number of sacks, screens, sheets) are illustrative; the unit prices are sourced.
- No sourced recommendation was found for disaster-time theft/looting protection, so it is not in the catalog.

## 6. URLs that failed during research

- congreso.gob.pe ARCC Piura PDF (404); scioteca.caf.com (bot-blocked; CAF volume taken from dipecholac.net mirror)
- BCRP Piura síntesis Mar/Apr 2017 PDFs (bot-blocked); ReliefWeb OCHA sitreps (403); IEP Argumentos PDF (expired TLS certificate)
- indeci.gob.pe/recomendaciones (DNS); fema.gov fact sheets (403); ready.gov business flood pages (404); SELA continuity guide (404); NIBS Mitigation Saves (404)
- Mercado Libre Perú (captcha/403); SUNAT emprender (403); WhatsApp Business (400)
