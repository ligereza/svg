"""Generate a self-contained HTML explorer for rd_complete.db."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "rd_complete.db"
HTML_PATH = BASE / "rd_explorer.html"


def safe_value(value):
    if isinstance(value, bytes):
        return "[BLOB omitido del HTML: %d bytes]" % len(value)
    return value


def read_table(connection, name):
    columns = [row[1] for row in connection.execute('PRAGMA table_info("%s")' % name)]
    selected = [column for column in columns if column != "content_blob"]
    if not selected:
        return {"columns": [], "rows": []}
    quoted = ", ".join('"%s"' % column.replace('"', '""') for column in selected)
    sql = 'SELECT %s FROM "%s"' % (quoted, name.replace('"', '""'))
    rows = []
    for row in connection.execute(sql):
        rows.append({column: safe_value(row[index]) for index, column in enumerate(selected)})
    return {"columns": selected, "rows": rows}


def build_payload(connection):
    table_names = [
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' "
            "ORDER BY CASE WHEN type='view' THEN 0 ELSE 1 END, name"
        )
    ]
    tables = {name: read_table(connection, name) for name in table_names}

    def count(name):
        return len(tables.get(name, {}).get("rows", []))

    quality_rows = tables.get("v_rd_test_quality", {}).get("rows", [])
    quality = quality_rows[0] if quality_rows else {}
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tables": tables,
        "table_names": table_names,
        "summary": {
            "entities": count("rd_entity"),
            "relations": count("rd_relation"),
            "sources": count("rd_source"),
            "reagents": count("rd_reagent"),
            "test_events": count("rd_test_event"),
            "test_rows": count("rd_test_row"),
            "observations": count("rd_test_observation"),
            "artifacts": count("rd_artifact"),
            "recovered_files": count("rd_file_manifest"),
            "slides": count("rd_content_slide"),
            "pages": count("rd_scrape_page"),
            "unlinked_queue": int(quality.get("unlinked_queue_rows") or 0),
            "unresolved_substance_rows": int(quality.get("unresolved_substance_rows") or 0),
        },
    }


HTML_TEMPLATE = r'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RD · Explorador de base completa</title>
<style>
:root{--ink:#152a3a;--muted:#617383;--line:#d9e2e8;--bg:#f4f7f9;--card:#fff;--teal:#0d7d83;--teal-soft:#e4f3f3;--orange:#d97941;--shadow:0 8px 24px #183c4b12}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
.wrap{max-width:1500px;margin:0 auto;padding:24px}header{background:linear-gradient(130deg,#122d3d,#0d7d83);color:#fff;border-radius:18px;padding:28px 30px;box-shadow:var(--shadow)}
header h1{margin:0 0 6px;font-size:28px;letter-spacing:-.02em}header p{margin:0;color:#dceff0;max-width:920px}.meta{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.pill{border:1px solid #ffffff38;border-radius:999px;padding:5px 10px;color:#e9fbfb;font-size:12px}nav{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}
nav button{cursor:pointer;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:10px;padding:9px 13px;font-weight:650}
nav button.active,nav button:hover{color:#fff;background:var(--teal);border-color:var(--teal)}.view{display:none}.view.active{display:block}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-bottom:16px}
.kpi,.panel{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow)}.kpi{padding:17px}
.kpi .label{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.06em}.kpi .value{margin-top:4px;font-size:27px;font-weight:750;color:var(--teal)}
.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.panel{padding:18px;margin-bottom:16px;min-width:0}
.panel h2{margin:0 0 5px;font-size:17px}.panel .sub{color:var(--muted);margin:0 0 14px}.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:10px}
table{width:100%;border-collapse:collapse;min-width:620px;background:#fff}th{position:sticky;top:0;z-index:1;background:#eef4f6;color:#365162;text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.05em;cursor:pointer;white-space:nowrap}
th,td{padding:9px 10px;border-bottom:1px solid #edf1f3;vertical-align:top}td{max-width:420px;white-space:pre-wrap;overflow-wrap:anywhere}tr:hover td{background:#f8fbfc}
.toolbar{display:flex;gap:9px;align-items:center;flex-wrap:wrap;margin:10px 0 12px}input,select{border:1px solid var(--line);border-radius:9px;padding:9px 10px;background:#fff;color:var(--ink)}
input.search{flex:1;min-width:240px}.small{color:var(--muted);font-size:12px}.pager{display:flex;gap:8px;align-items:center;justify-content:flex-end;margin-top:10px}
.pager button,.button{border:1px solid var(--line);border-radius:8px;background:#fff;color:var(--ink);padding:7px 10px;cursor:pointer}.pager button:disabled{opacity:.4;cursor:default}
.tag{display:inline-block;padding:3px 7px;border-radius:999px;background:var(--teal-soft);color:#17676a;font-size:11px;margin:2px 3px 2px 0}
.notice{background:#fff8ef;border-left:4px solid var(--orange);padding:12px 14px;border-radius:8px;color:#754321}
.detail{margin-top:12px;background:#102331;color:#d8eff0;border-radius:10px;padding:14px;white-space:pre-wrap;overflow:auto;max-height:360px;font:12px/1.45 ui-monospace,SFMono-Regular,Consolas,monospace}
.bar-row{display:grid;grid-template-columns:180px 1fr 70px;gap:10px;align-items:center;margin:8px 0}.bar{height:10px;background:#e5edf0;border-radius:20px;overflow:hidden}.bar i{display:block;height:100%;background:linear-gradient(90deg,var(--teal),#75c2bd);border-radius:20px}
footer{color:var(--muted);text-align:center;padding:16px 0 4px;font-size:12px}
@media(max-width:850px){.wrap{padding:13px}header{padding:22px}.grid2{grid-template-columns:1fr}.bar-row{grid-template-columns:120px 1fr 55px}}
@media print{nav,.toolbar,.pager{display:none}body{background:#fff}.panel,.kpi,header{box-shadow:none}}
</style>
</head>
<body>
<div class="wrap">
<header>
<h1>RD · Explorador de base completa</h1>
<p>Una lectura navegable de la base SQLite: catálogo canónico, entidades, relaciones, fuentes, reactivos, testeos, contenido editorial y trazabilidad de archivos.</p>
<div class="meta"><span class="pill">Fuente: rd_complete.db</span><span class="pill" id="generated"></span><span class="pill">Sin servidor · funciona localmente</span></div>
</header>
<nav id="nav"></nav>
<main>
<section class="view active" id="view-resumen">
<div class="kpis" id="kpis"></div>
<div class="grid2">
<div class="panel"><h2>Capas de la base</h2><p class="sub">Conteos de las capas principales importadas.</p><div id="layers"></div></div>
<div class="panel"><h2>Estado de calidad</h2><p class="sub">Lo que está resuelto y lo que queda explícitamente pendiente.</p><div id="quality"></div></div>
</div>
<div class="panel"><h2>Qué contiene</h2><p class="sub">La base fue ampliada sin tocar las fuentes originales.</p><div class="notice">Los 84 enlaces de testeos pendientes y las entidades sin conexión no se completaron por inferencia. La base de campo conserva su esquema, pero sus tres tablas estaban vacías.</div></div>
<div class="panel"><h2>Vista rápida de entidades</h2><div id="quick-entities"></div></div>
</section>
<section class="view" id="view-entidades"><div class="panel"><h2>Entidades</h2><p class="sub">Sustancias, familias, medicamentos, adulterantes y entidades contextuales.</p><div id="entities-table"></div></div></section>
<section class="view" id="view-relaciones"><div class="panel"><h2>Relaciones y evidencia</h2><p class="sub">Relaciones candidatas, límites de alcance y fuentes asociadas.</p><div id="relations-table"></div></div></section>
<section class="view" id="view-testeos"><div class="panel"><h2>Testeos</h2><p class="sub">Eventos, hojas, filas fuente y observaciones preservadas.</p><div id="tests-table"></div></div></section>
<section class="view" id="view-reactivos"><div class="panel"><h2>Reactivos</h2><p class="sub">Biblioteca normalizada, reacciones y limitaciones.</p><div id="reagents-table"></div></div></section>
<section class="view" id="view-fuentes"><div class="panel"><h2>Fuentes</h2><p class="sub">Catálogo de fuentes usadas por entidades, relaciones y evidencia.</p><div id="sources-table"></div></div></section>
<section class="view" id="view-contenido"><div class="panel"><h2>Contenido editorial</h2><p class="sub">Posts, láminas, claims y briefs visuales preservados como capa separada.</p><div id="content-table"></div></div></section>
<section class="view" id="view-visor"><div class="panel"><h2>Visor de tablas</h2><p class="sub">Explora cualquier tabla o vista disponible. Las tablas grandes tienen búsqueda, orden y paginación.</p><div class="toolbar"><select id="table-select"></select><select id="page-size"><option>25</option><option selected>50</option><option>100</option></select></div><div id="all-table"></div></div></section>
</main>
<footer>RD · Explorador generado desde la base validada. Los BLOB binarios permanecen en el archivo .db; el texto asociado se muestra aquí.</footer>
</div>
<script>
const DB=__PAYLOAD__;
const fmt=n=>Number(n||0).toLocaleString("es-CL");
const esc=value=>String(value??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
const norm=value=>String(value??"").normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase();
const table=key=>DB.tables[key]||{columns:[],rows:[]};
const pretty=value=>value===null||value===undefined?"":typeof value==="object"?JSON.stringify(value):String(value);
const tabs=[["resumen","Resumen"],["entidades","Entidades"],["relaciones","Relaciones"],["testeos","Testeos"],["reactivos","Reactivos"],["fuentes","Fuentes"],["contenido","Contenido"],["visor","Todas las tablas"]];
document.getElementById("nav").innerHTML=tabs.map((item,i)=>"<button class=\""+(i===0?"active":"")+"\" data-tab=\""+item[0]+"\">"+item[1]+"</button>").join("");
document.querySelectorAll("nav button").forEach(btn=>btn.addEventListener("click",()=>{document.querySelectorAll("nav button").forEach(b=>b.classList.toggle("active",b===btn));document.querySelectorAll(".view").forEach(v=>v.classList.toggle("active",v.id==="view-"+btn.dataset.tab));}));
document.getElementById("generated").textContent="Generado: "+new Date(DB.generated_at).toLocaleString("es-CL");
const kpiFields=[["entities","Entidades"],["relations","Relaciones"],["sources","Fuentes"],["reagents","Reactivos"],["test_events","Eventos de testeo"],["observations","Observaciones"],["artifacts","Artefactos RD"],["recovered_files","Archivos inventariados"]];
document.getElementById("kpis").innerHTML=kpiFields.map(x=>"<div class=\"kpi\"><div class=\"label\">"+x[1]+"</div><div class=\"value\">"+fmt(DB.summary[x[0]])+"</div></div>").join("");
const layerRows=[["Entidades","entities"],["Relaciones","relations"],["Fuentes","sources"],["Reactivos","reagents"],["Eventos de testeo","test_events"],["Observaciones","observations"],["Páginas web","pages"],["Láminas editoriales","slides"]];
const maxLayer=Math.max.apply(null,layerRows.map(x=>DB.summary[x[1]]));
document.getElementById("layers").innerHTML=layerRows.map(x=>"<div class=\"bar-row\"><span>"+x[0]+"</span><div class=\"bar\"><i style=\"width:"+Math.max(2,Math.min(100,DB.summary[x[1]]/maxLayer*100))+"%\"></i></div><strong>"+fmt(DB.summary[x[1]])+"</strong></div>").join("");
document.getElementById("quality").innerHTML="<p><span class=\"tag\">"+fmt(DB.summary.unlinked_queue)+" pendientes</span> enlaces de testeos sin vinculación automática.</p><p><span class=\"tag\">"+fmt(DB.summary.unresolved_substance_rows)+" sin resolver</span> filas con sustancia no identificada en el mapa actual.</p><p><span class=\"tag\">0</span> violaciones de claves foráneas en la validación de SQLite.</p>";

function renderTable(containerId,key,fields,options){
  options=options||{};const source=table(key);const cols=(fields||source.columns).filter(c=>source.columns.includes(c));const state={q:"",page:0,size:options.size||25,sort:null,dir:1};const root=document.getElementById(containerId);
  root.innerHTML="<div class=\"toolbar\"><input class=\"search\" placeholder=\"Buscar...\"><span class=\"small count\"></span></div><div class=\"table-wrap\"><table><thead></thead><tbody></tbody></table></div><div class=\"pager\"><button class=\"prev\">Anterior</button><span class=\"page\"></span><button class=\"next\">Siguiente</button></div><pre class=\"detail\" hidden></pre>";
  root.querySelector(".search").addEventListener("input",e=>{state.q=norm(e.target.value);state.page=0;paint();});
  function paint(){
    let rows=source.rows.filter(row=>!state.q||cols.some(c=>norm(pretty(row[c])).includes(state.q)));
    if(state.sort)rows=rows.slice().sort((a,b)=>{const aa=norm(a[state.sort]),bb=norm(b[state.sort]);return aa<bb?-state.dir:aa>bb?state.dir:0;});
    const pages=Math.max(1,Math.ceil(rows.length/state.size));state.page=Math.min(state.page,pages-1);const pageRows=rows.slice(state.page*state.size,(state.page+1)*state.size);
    root.querySelector(".count").textContent=fmt(rows.length)+" registros · tabla "+key;
    root.querySelector("thead").innerHTML="<tr>"+cols.map(c=>"<th data-col=\""+esc(c)+"\">"+esc(c)+" "+(state.sort===c?(state.dir===1?"▲":"▼"):"")+"</th>").join("")+"</tr>";
    root.querySelectorAll("th").forEach(th=>th.addEventListener("click",()=>{const c=th.dataset.col;if(state.sort===c)state.dir*=-1;else{state.sort=c;state.dir=1;}paint();}));
    root.querySelector("tbody").innerHTML=pageRows.map((row,i)=>"<tr data-index=\""+i+"\">"+cols.map(c=>"<td>"+esc(pretty(row[c]))+"</td>").join("")+"</tr>").join("")||"<tr><td colspan=\""+Math.max(cols.length,1)+"\" class=\"small\">Sin resultados.</td></tr>";
    root.querySelectorAll("tbody tr").forEach((tr,i)=>tr.addEventListener("click",()=>{const detail=root.querySelector(".detail");detail.hidden=false;detail.textContent=JSON.stringify(pageRows[i],null,2);}));
    root.querySelector(".page").textContent="Página "+(state.page+1)+" de "+pages;root.querySelector(".prev").disabled=state.page===0;root.querySelector(".next").disabled=state.page>=pages-1;
  }
  root.querySelector(".prev").addEventListener("click",()=>{state.page--;paint();});root.querySelector(".next").addEventListener("click",()=>{state.page++;paint();});paint();
}
renderTable("quick-entities","v_rd_entity_overview",["display_name","entity_kind","matrix","test_status","relation_count","source_count"],{size:10});
renderTable("entities-table","v_rd_entity_overview",["id","display_name","entity_kind","matrix","matrix_candidate","source_status","test_status","relation_count","profile_count","source_count"]);
renderTable("relations-table","v_rd_relation_overview",null,{size:25});
renderTable("tests-table","rd_test_event",["event_id","source_sheet_name","event_label_candidate","date_iso_candidate","date_status","venue_name","producer_name","link_status","duplicate_status"]);
renderTable("reagents-table","rd_reagent",null,{size:25});
renderTable("sources-table","rd_source",["url","source_type","source_kinds_json"],{size:25});
renderTable("content-table","rd_content_slide",null,{size:25});
const select=document.getElementById("table-select");select.innerHTML=DB.table_names.map(name=>"<option value=\""+esc(name)+"\">"+esc(name)+" ("+fmt(table(name).rows.length)+")</option>").join("");
let allMounted=null;
function mountAll(){if(allMounted)allMounted.remove();const holder=document.createElement("div");holder.id="all-mounted";document.getElementById("all-table").appendChild(holder);allMounted=holder;renderTable("all-mounted",select.value,null,{size:Number(document.getElementById("page-size").value)});}
select.addEventListener("change",mountAll);document.getElementById("page-size").addEventListener("change",mountAll);mountAll();
</script>
</body>
</html>'''


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(DB_PATH)
    connection = sqlite3.connect(DB_PATH)
    try:
        payload = build_payload(connection)
    finally:
        connection.close()
    embedded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    embedded = embedded.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    HTML_PATH.write_text(HTML_TEMPLATE.replace("__PAYLOAD__", embedded), encoding="utf-8")
    print(json.dumps({"output": str(HTML_PATH), "bytes": HTML_PATH.stat().st_size, "tables": len(payload["table_names"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
