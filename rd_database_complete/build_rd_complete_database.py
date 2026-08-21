from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SOURCE_ROOT = Path(r"C:\Users\issvk\claude_sesiones_recuperadas")
IMPORT_ROOT = Path(r"C:\IA\svg\remote_imports")
DEFAULT_CANONICAL = IMPORT_ROOT / "rd_canonical_from_mak_20260818.db"
DEFAULT_FIELD = IMPORT_ROOT / "rd_datos_from_mak_20260818.db"
DEFAULT_OUTPUT = Path(r"C:\IA\svg\rd_database_complete\rd_complete.db")


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    row = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
    ).fetchone()
    return row is not None


def insert_row(
    connection: sqlite3.Connection,
    table: str,
    values: dict[str, Any],
    replace: bool = True,
) -> None:
    columns = list(values)
    placeholders = ",".join("?" for _ in columns)
    verb = "INSERT OR REPLACE" if replace else "INSERT"
    connection.execute(
        f"{verb} INTO {table} ({','.join(columns)}) VALUES ({placeholders})",
        [values[column] for column in columns],
    )


def create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        PRAGMA foreign_keys = ON;
        PRAGMA journal_mode = WAL;
        PRAGMA synchronous = NORMAL;

        CREATE TABLE IF NOT EXISTS rd_import_run (
            run_id TEXT PRIMARY KEY,
            started_at TEXT NOT NULL,
            completed_at TEXT,
            builder_version TEXT NOT NULL,
            source_root TEXT NOT NULL,
            canonical_database TEXT NOT NULL,
            field_database TEXT,
            status TEXT NOT NULL,
            notes TEXT
        );

        CREATE TABLE IF NOT EXISTS rd_file_manifest (
            relative_path TEXT PRIMARY KEY,
            file_name TEXT NOT NULL,
            extension TEXT NOT NULL,
            bytes INTEGER NOT NULL,
            sha256 TEXT NOT NULL,
            modified_at TEXT,
            category TEXT NOT NULL,
            in_venv INTEGER NOT NULL DEFAULT 0,
            imported_raw INTEGER NOT NULL DEFAULT 0,
            parse_status TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_artifact (
            relative_path TEXT PRIMARY KEY,
            source_role TEXT NOT NULL,
            mime_type TEXT,
            bytes INTEGER NOT NULL,
            sha256 TEXT NOT NULL,
            text_content TEXT,
            content_blob BLOB,
            parse_status TEXT NOT NULL,
            notes TEXT
        );

        CREATE TABLE IF NOT EXISTS rd_catalog_table_count (
            table_name TEXT PRIMARY KEY,
            row_count INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_schema_registry (
            table_name TEXT PRIMARY KEY,
            layer TEXT NOT NULL,
            description TEXT NOT NULL,
            source_path TEXT
        );

        CREATE TABLE IF NOT EXISTS rd_entity (
            id TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            aliases_json TEXT NOT NULL,
            entity_kind TEXT NOT NULL,
            matrix INTEGER,
            matrix_candidate INTEGER,
            source_status TEXT,
            test_status TEXT,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_entity_alias (
            entity_id TEXT NOT NULL,
            alias TEXT NOT NULL,
            ordinal INTEGER NOT NULL,
            PRIMARY KEY (entity_id, alias),
            FOREIGN KEY (entity_id) REFERENCES rd_entity(id)
        );

        CREATE TABLE IF NOT EXISTS rd_entity_profile (
            entity_id TEXT PRIMARY KEY,
            profile_json TEXT NOT NULL,
            FOREIGN KEY (entity_id) REFERENCES rd_entity(id)
        );

        CREATE TABLE IF NOT EXISTS rd_entity_source (
            entity_id TEXT NOT NULL,
            source_url TEXT NOT NULL,
            ordinal INTEGER NOT NULL,
            PRIMARY KEY (entity_id, source_url),
            FOREIGN KEY (entity_id) REFERENCES rd_entity(id)
        );

        CREATE TABLE IF NOT EXISTS rd_source (
            url TEXT PRIMARY KEY,
            source_type TEXT,
            source_kinds_json TEXT NOT NULL,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_source_ref (
            url TEXT NOT NULL,
            ref TEXT NOT NULL,
            ref_kind TEXT NOT NULL,
            PRIMARY KEY (url, ref, ref_kind),
            FOREIGN KEY (url) REFERENCES rd_source(url)
        );

        CREATE TABLE IF NOT EXISTS rd_relation (
            id TEXT PRIMARY KEY,
            source_ref TEXT NOT NULL,
            target_ref TEXT NOT NULL,
            source_kind TEXT,
            target_kind TEXT,
            relation_type TEXT NOT NULL,
            status TEXT NOT NULL,
            confidence TEXT,
            matrix_relevance TEXT,
            notes TEXT,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_relation_evidence (
            relation_id TEXT NOT NULL,
            url TEXT NOT NULL,
            ordinal INTEGER NOT NULL,
            PRIMARY KEY (relation_id, url),
            FOREIGN KEY (relation_id) REFERENCES rd_relation(id),
            FOREIGN KEY (url) REFERENCES rd_source(url)
        );

        CREATE TABLE IF NOT EXISTS rd_relation_integration (
            relation_id TEXT NOT NULL,
            record_json TEXT NOT NULL,
            PRIMARY KEY (relation_id, record_json),
            FOREIGN KEY (relation_id) REFERENCES rd_relation(id)
        );

        CREATE TABLE IF NOT EXISTS rd_reagent (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            reagent_type TEXT,
            components TEXT,
            observation_window TEXT,
            source_url TEXT,
            guide_url TEXT,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_reagent_reaction (
            reagent_id TEXT NOT NULL,
            ordinal INTEGER NOT NULL,
            target TEXT NOT NULL,
            sequence TEXT,
            source_wording TEXT,
            raw_json TEXT NOT NULL,
            PRIMARY KEY (reagent_id, ordinal),
            FOREIGN KEY (reagent_id) REFERENCES rd_reagent(id)
        );

        CREATE TABLE IF NOT EXISTS rd_reagent_limitation (
            reagent_id TEXT NOT NULL,
            limitation TEXT NOT NULL,
            ordinal INTEGER NOT NULL,
            PRIMARY KEY (reagent_id, limitation),
            FOREIGN KEY (reagent_id) REFERENCES rd_reagent(id)
        );

        CREATE TABLE IF NOT EXISTS rd_reagent_complement (
            reagent_id TEXT NOT NULL,
            complement_id TEXT NOT NULL,
            ordinal INTEGER NOT NULL,
            PRIMARY KEY (reagent_id, complement_id),
            FOREIGN KEY (reagent_id) REFERENCES rd_reagent(id)
        );

        CREATE TABLE IF NOT EXISTS rd_reagent_audit_finding (
            finding_id TEXT PRIMARY KEY,
            status TEXT,
            finding TEXT NOT NULL,
            sources_json TEXT NOT NULL,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_reagent_audit_override (
            reagent_id TEXT PRIMARY KEY,
            evidence_status TEXT,
            observation_override TEXT,
            important_correction TEXT,
            sources_json TEXT NOT NULL,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_test_batch (
            batch_id TEXT PRIMARY KEY,
            source_file TEXT,
            source_copy TEXT,
            sha256 TEXT,
            filename_period_label TEXT,
            formula_count INTEGER,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_test_source_sheet (
            source_sheet_index INTEGER PRIMARY KEY,
            source_sheet_name TEXT NOT NULL,
            data_row_count_including_anomalies INTEGER,
            source_sheet_hash TEXT,
            duplicate_group_id TEXT,
            duplicate_group_size INTEGER,
            duplicate_status TEXT,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_test_event (
            event_id TEXT PRIMARY KEY,
            source_sheet_index INTEGER,
            source_sheet_name TEXT,
            event_label_candidate TEXT,
            event_label_status TEXT,
            source_period_label TEXT,
            date_raw_token TEXT,
            date_iso_candidate TEXT,
            date_status TEXT,
            date_parse_style TEXT,
            date_confidence TEXT,
            outside_filename_period_candidate INTEGER,
            is_source_copy_candidate INTEGER,
            duplicate_group_id TEXT,
            duplicate_group_size INTEGER,
            duplicate_status TEXT,
            duplicate_canonical_sheet_candidate TEXT,
            venue_id TEXT,
            venue_name TEXT,
            producer_id TEXT,
            producer_name TEXT,
            link_status TEXT,
            link_evidence_ref TEXT,
            link_confidence TEXT,
            link_review_status TEXT,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_test_row (
            test_id TEXT PRIMARY KEY,
            event_id TEXT,
            source_sheet_name TEXT,
            source_row INTEGER,
            row_status TEXT,
            substance_raw TEXT,
            substance_normalized_candidate TEXT,
            substance_map_status TEXT,
            format_raw TEXT,
            test_1_raw TEXT,
            result_1_raw TEXT,
            test_2_raw TEXT,
            result_2_raw TEXT,
            test_3_raw TEXT,
            result_3_raw TEXT,
            test_4_raw TEXT,
            result_4_raw TEXT,
            extra_1_raw TEXT,
            source_duplicate_group_id TEXT,
            source_duplicate_status TEXT,
            interpretation_policy TEXT,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_test_observation (
            observation_id TEXT PRIMARY KEY,
            test_id TEXT,
            event_id TEXT,
            source_sheet_name TEXT,
            source_row INTEGER,
            observation_ordinal INTEGER,
            substance_raw TEXT,
            substance_normalized_candidate TEXT,
            reagent_raw TEXT,
            reagent_normalized_candidate TEXT,
            reagent_map_status TEXT,
            result_raw TEXT,
            result_normalized_candidate TEXT,
            result_map_status TEXT,
            observation_status TEXT,
            interpretation_policy TEXT,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_test_substance_map (
            raw_label TEXT PRIMARY KEY,
            count INTEGER,
            normalized_id TEXT,
            mapping_status TEXT,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_test_reagent_map (
            raw_label TEXT PRIMARY KEY,
            count INTEGER,
            normalized_id TEXT,
            mapping_status TEXT,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_test_link_queue (
            link_id TEXT PRIMARY KEY,
            event_id TEXT,
            source_sheet_name TEXT,
            target_kind TEXT,
            target_id TEXT,
            target_name TEXT,
            relation_type TEXT,
            evidence_ref TEXT,
            confidence TEXT,
            status TEXT,
            review_status TEXT,
            not_inferred_from_sheet_name INTEGER,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_content_post (
            post_id TEXT PRIMARY KEY,
            schema_version TEXT,
            language TEXT,
            status TEXT,
            source_document TEXT,
            source_sha256 TEXT,
            source_page_count INTEGER,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_content_post_policy (
            post_id TEXT NOT NULL,
            policy_key TEXT NOT NULL,
            policy_value TEXT NOT NULL,
            PRIMARY KEY (post_id, policy_key),
            FOREIGN KEY (post_id) REFERENCES rd_content_post(post_id)
        );

        CREATE TABLE IF NOT EXISTS rd_content_slide (
            slide_id TEXT PRIMARY KEY,
            post_id TEXT NOT NULL,
            sequence INTEGER NOT NULL,
            source_pages_json TEXT NOT NULL,
            role TEXT,
            title TEXT,
            layout_policy TEXT,
            raw_json TEXT NOT NULL,
            FOREIGN KEY (post_id) REFERENCES rd_content_post(post_id)
        );

        CREATE TABLE IF NOT EXISTS rd_content_slide_text (
            slide_id TEXT NOT NULL,
            ordinal INTEGER NOT NULL,
            text TEXT NOT NULL,
            PRIMARY KEY (slide_id, ordinal),
            FOREIGN KEY (slide_id) REFERENCES rd_content_slide(slide_id)
        );

        CREATE TABLE IF NOT EXISTS rd_content_slide_entity (
            slide_id TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            ordinal INTEGER NOT NULL,
            PRIMARY KEY (slide_id, entity_id),
            FOREIGN KEY (slide_id) REFERENCES rd_content_slide(slide_id)
        );

        CREATE TABLE IF NOT EXISTS rd_content_slide_relation (
            slide_id TEXT NOT NULL,
            relation_id TEXT NOT NULL,
            status TEXT,
            relation_type TEXT,
            PRIMARY KEY (slide_id, relation_id),
            FOREIGN KEY (slide_id) REFERENCES rd_content_slide(slide_id)
        );

        CREATE TABLE IF NOT EXISTS rd_content_slide_claim (
            slide_id TEXT NOT NULL,
            claim_id TEXT NOT NULL,
            PRIMARY KEY (slide_id, claim_id),
            FOREIGN KEY (slide_id) REFERENCES rd_content_slide(slide_id)
        );

        CREATE TABLE IF NOT EXISTS rd_content_interaction_card (
            card_id TEXT PRIMARY KEY,
            slide_id TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            relation_id TEXT,
            claim_id TEXT,
            semantic_link_json TEXT,
            raw_json TEXT NOT NULL,
            FOREIGN KEY (slide_id) REFERENCES rd_content_slide(slide_id)
        );

        CREATE TABLE IF NOT EXISTS rd_content_claim (
            claim_id TEXT PRIMARY KEY,
            post_id TEXT NOT NULL,
            source_slide TEXT,
            source_card TEXT,
            source_text_preserved INTEGER,
            claim_status TEXT,
            required_relation_type TEXT,
            public_rule TEXT,
            raw_json TEXT NOT NULL,
            FOREIGN KEY (post_id) REFERENCES rd_content_post(post_id)
        );

        CREATE TABLE IF NOT EXISTS rd_visual_brief (
            brief_id TEXT PRIMARY KEY,
            slide_id TEXT NOT NULL,
            visual_role TEXT,
            primary_form TEXT,
            animation_logic TEXT,
            raw_json TEXT NOT NULL,
            FOREIGN KEY (slide_id) REFERENCES rd_content_slide(slide_id)
        );

        CREATE TABLE IF NOT EXISTS rd_visual_brief_vector (
            brief_id TEXT NOT NULL,
            ordinal INTEGER NOT NULL,
            vector TEXT NOT NULL,
            PRIMARY KEY (brief_id, vector),
            FOREIGN KEY (brief_id) REFERENCES rd_visual_brief(brief_id)
        );

        CREATE TABLE IF NOT EXISTS rd_visual_brief_do_not (
            brief_id TEXT NOT NULL,
            ordinal INTEGER NOT NULL,
            rule TEXT NOT NULL,
            PRIMARY KEY (brief_id, rule),
            FOREIGN KEY (brief_id) REFERENCES rd_visual_brief(brief_id)
        );

        CREATE TABLE IF NOT EXISTS rd_scrape_batch (
            crawl_id TEXT PRIMARY KEY,
            status TEXT,
            total INTEGER,
            completed INTEGER,
            credits_used INTEGER,
            retrieved_at TEXT,
            source_file TEXT,
            raw_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rd_scrape_page (
            crawl_id TEXT NOT NULL,
            page_index INTEGER NOT NULL,
            url TEXT,
            page_status TEXT,
            title TEXT,
            markdown TEXT,
            html TEXT,
            metadata_json TEXT,
            raw_json TEXT NOT NULL,
            PRIMARY KEY (crawl_id, page_index),
            FOREIGN KEY (crawl_id) REFERENCES rd_scrape_batch(crawl_id)
        );

        CREATE INDEX IF NOT EXISTS idx_rd_entity_kind ON rd_entity(entity_kind);
        CREATE INDEX IF NOT EXISTS idx_rd_entity_test_status ON rd_entity(test_status);
        CREATE INDEX IF NOT EXISTS idx_rd_relation_type ON rd_relation(relation_type);
        CREATE INDEX IF NOT EXISTS idx_rd_relation_status ON rd_relation(status);
        CREATE INDEX IF NOT EXISTS idx_rd_relation_source ON rd_relation(source_ref);
        CREATE INDEX IF NOT EXISTS idx_rd_relation_target ON rd_relation(target_ref);
        CREATE INDEX IF NOT EXISTS idx_rd_test_row_substance ON rd_test_row(substance_normalized_candidate);
        CREATE INDEX IF NOT EXISTS idx_rd_test_obs_reagent ON rd_test_observation(reagent_normalized_candidate);
        CREATE INDEX IF NOT EXISTS idx_rd_test_event_period ON rd_test_event(source_period_label);

        CREATE VIEW IF NOT EXISTS v_rd_entity_overview AS
        SELECT e.id, e.display_name, e.entity_kind, e.matrix, e.matrix_candidate,
               e.source_status, e.test_status,
               (SELECT COUNT(*) FROM rd_relation r WHERE r.source_ref=e.id OR r.target_ref=e.id) AS relation_count,
               (SELECT COUNT(*) FROM rd_entity_profile p WHERE p.entity_id=e.id) AS profile_count,
               (SELECT COUNT(*) FROM rd_entity_source s WHERE s.entity_id=e.id) AS source_count
        FROM rd_entity e;

        CREATE VIEW IF NOT EXISTS v_rd_relation_overview AS
        SELECT r.id, r.source_ref, r.target_ref, r.relation_type, r.status,
               r.confidence, r.matrix_relevance,
               (SELECT COUNT(*) FROM rd_relation_evidence e WHERE e.relation_id=r.id) AS evidence_count,
               (SELECT COUNT(*) FROM rd_relation_integration i WHERE i.relation_id=r.id) AS integration_count
        FROM rd_relation r;

        CREATE VIEW IF NOT EXISTS v_rd_test_quality AS
        SELECT
          (SELECT COUNT(*) FROM rd_test_source_sheet) AS source_sheet_count,
          (SELECT COUNT(*) FROM rd_test_event) AS event_count,
          (SELECT COUNT(*) FROM rd_test_row) AS test_row_count,
          (SELECT COUNT(*) FROM rd_test_row WHERE row_status='data') AS data_row_count,
          (SELECT COUNT(*) FROM rd_test_observation) AS observation_count,
          (SELECT COUNT(*) FROM rd_test_row WHERE substance_map_status LIKE '%unresolved%' OR substance_map_status LIKE '%misplaced%') AS unresolved_substance_rows,
          (SELECT COUNT(*) FROM rd_test_link_queue WHERE status='unlinked') AS unlinked_queue_rows;

        CREATE VIEW IF NOT EXISTS v_rd_content_surface AS
        SELECT p.post_id, p.language, p.status, s.sequence, s.slide_id, s.role,
               s.title, COUNT(DISTINCT t.ordinal) AS text_block_count,
               COUNT(DISTINCT e.entity_id) AS entity_count,
               COUNT(DISTINCT r.relation_id) AS relation_count,
               COUNT(DISTINCT c.claim_id) AS claim_count
        FROM rd_content_post p
        JOIN rd_content_slide s ON s.post_id=p.post_id
        LEFT JOIN rd_content_slide_text t ON t.slide_id=s.slide_id
        LEFT JOIN rd_content_slide_entity e ON e.slide_id=s.slide_id
        LEFT JOIN rd_content_slide_relation r ON r.slide_id=s.slide_id
        LEFT JOIN rd_content_slide_claim c ON c.slide_id=s.slide_id
        GROUP BY p.post_id, p.language, p.status, s.sequence, s.slide_id, s.role, s.title;

        CREATE VIEW IF NOT EXISTS v_rd_catalog_summary AS
        SELECT 'canonical_catalog' AS layer, COUNT(*) AS rows FROM productoras
        UNION ALL SELECT 'canonical_venues', COUNT(*) FROM venues
        UNION ALL SELECT 'canonical_events', COUNT(*) FROM productora_eventos
        UNION ALL SELECT 'entities', COUNT(*) FROM rd_entity
        UNION ALL SELECT 'relations', COUNT(*) FROM rd_relation
        UNION ALL SELECT 'sources', COUNT(*) FROM rd_source
        UNION ALL SELECT 'reagents', COUNT(*) FROM rd_reagent
        UNION ALL SELECT 'test_events', COUNT(*) FROM rd_test_event
        UNION ALL SELECT 'test_rows', COUNT(*) FROM rd_test_row
        UNION ALL SELECT 'test_observations', COUNT(*) FROM rd_test_observation
        UNION ALL SELECT 'content_posts', COUNT(*) FROM rd_content_post;
        """
    )


def category_for(path: Path, root: Path) -> str:
    rel = path.relative_to(root).as_posix()
    name = path.name.lower()
    if name.startswith("rd_") or name.startswith("carrusel chemsex") or name.startswith("testeo 2025"):
        return "rd"
    if "fondart" in name or "fondos" in rel.lower() or "bases_pdf" in rel.lower():
        return "fondart"
    if "claude_web_export" in rel or name.endswith("_nombre-cauce.md"):
        return "session_export"
    if "solid_hpi" in rel or name in {"memoria_direccion.md", "protocolofase0.md"}:
        return "research_or_direction"
    return "other"


def ingest_file_manifest(connection: sqlite3.Connection, root: Path) -> None:
    rows = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        in_venv = int(rel.startswith(".venv/"))
        category = "dependency" if in_venv else category_for(path, root)
        try:
            digest = sha256_path(path)
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
            parse_status = "not_requested" if in_venv else "inventoried"
            rows.append(
                (
                    rel,
                    path.name,
                    path.suffix.lower(),
                    path.stat().st_size,
                    digest,
                    modified,
                    category,
                    in_venv,
                    0,
                    parse_status,
                )
            )
        except OSError as exc:
            rows.append((rel, path.name, path.suffix.lower(), 0, "", None, category, in_venv, 0, f"error:{exc}"))
    connection.executemany(
        """
        INSERT OR REPLACE INTO rd_file_manifest
        (relative_path,file_name,extension,bytes,sha256,modified_at,category,in_venv,imported_raw,parse_status)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        rows,
    )


def ingest_raw_artifacts(connection: sqlite3.Connection, root: Path) -> None:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.relative_to(root).as_posix().startswith(".venv/"):
            continue
        rel = path.relative_to(root).as_posix()
        if category_for(path, root) != "rd":
            continue
        try:
            blob = path.read_bytes()
            digest = hashlib.sha256(blob).hexdigest()
            text_content = None
            if path.suffix.lower() in {".json", ".md", ".html", ".py", ".svg", ".txt", ".csv", ".yaml", ".yml"}:
                text_content = blob.decode("utf-8", errors="replace")
            mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            insert_row(
                connection,
                "rd_artifact",
                {
                    "relative_path": rel,
                    "source_role": "rd_source_artifact",
                    "mime_type": mime,
                    "bytes": len(blob),
                    "sha256": digest,
                    "text_content": text_content,
                    "content_blob": sqlite3.Binary(blob),
                    "parse_status": "raw_preserved",
                    "notes": "Original recovery artifact preserved inside the database.",
                },
            )
            connection.execute("UPDATE rd_file_manifest SET imported_raw=1, parse_status='raw_preserved' WHERE relative_path=?", (rel,))
        except OSError as exc:
            connection.execute("UPDATE rd_file_manifest SET parse_status=? WHERE relative_path=?", (f"raw_error:{exc}", rel))


def ingest_catalog_counts(connection: sqlite3.Connection) -> None:
    rows = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'rd_%' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'field_%' ORDER BY name"
    ).fetchall()
    for (name,) in rows:
        count = connection.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
        insert_row(connection, "rd_catalog_table_count", {"table_name": name, "row_count": count})


def ingest_entities(connection: sqlite3.Connection, root: Path) -> None:
    data = load_json(root / "rd_universo_entidades_2026-08-11.json")
    for record in data.get("records", []):
        entity_id = record["id"]
        insert_row(
            connection,
            "rd_entity",
            {
                "id": entity_id,
                "display_name": record.get("display_name", entity_id),
                "aliases_json": json_text(record.get("aliases", [])),
                "entity_kind": record.get("entity_kind", "unknown"),
                "matrix": record.get("matrix"),
                "matrix_candidate": record.get("matrix_candidate"),
                "source_status": record.get("source_status"),
                "test_status": record.get("test_status"),
                "raw_json": json_text(record),
            },
        )
        for ordinal, alias in enumerate(record.get("aliases", [])):
            insert_row(connection, "rd_entity_alias", {"entity_id": entity_id, "alias": alias, "ordinal": ordinal})
        for ordinal, url in enumerate(record.get("source_urls", [])):
            insert_row(connection, "rd_entity_source", {"entity_id": entity_id, "source_url": url, "ordinal": ordinal})

    profiles = load_json(root / "rd_fichas_entidades_2026-08-11.json")
    for profile in profiles.get("profiles", []):
        entity_id = profile.get("entity_id") or profile.get("id") or profile.get("entity_ref")
        if entity_id:
            insert_row(connection, "rd_entity_profile", {"entity_id": entity_id, "profile_json": json_text(profile)})


def ingest_sources_and_relations(connection: sqlite3.Connection, root: Path) -> None:
    sources = load_json(root / "rd_fuentes_catalogo_2026-08-11.json")
    for record in sources.get("records", []):
        url = record.get("url")
        if not url:
            continue
        insert_row(
            connection,
            "rd_source",
            {
                "url": url,
                "source_type": record.get("source_type"),
                "source_kinds_json": json_text(record.get("source_kinds", [])),
                "raw_json": json_text(record),
            },
        )
        for kind in record.get("source_kinds", []):
            for ref in record.get("source_refs", []):
                insert_row(connection, "rd_source_ref", {"url": url, "ref": ref, "ref_kind": kind})

    graph = load_json(root / "rd_grafo_relaciones_2026-08-11.json")
    for relation in graph.get("relations", []):
        relation_id = relation["id"]
        insert_row(
            connection,
            "rd_relation",
            {
                "id": relation_id,
                "source_ref": relation.get("source_ref", ""),
                "target_ref": relation.get("target_ref", ""),
                "source_kind": relation.get("source_kind"),
                "target_kind": relation.get("target_kind"),
                "relation_type": relation.get("relation_type", "unknown"),
                "status": relation.get("status", "unknown"),
                "confidence": relation.get("confidence"),
                "matrix_relevance": relation.get("matrix_relevance"),
                "notes": relation.get("notes"),
                "raw_json": json_text(relation),
            },
        )
        for ordinal, url in enumerate(relation.get("evidence_urls", [])):
            insert_row(connection, "rd_relation_evidence", {"relation_id": relation_id, "url": url, "ordinal": ordinal})

    index = load_json(root / "rd_indice_integracion_relaciones_2026-08-11.json")
    for record in index.get("records", []):
        relation_id = record.get("relation_id") or record.get("id")
        if relation_id:
            insert_row(connection, "rd_relation_integration", {"relation_id": relation_id, "record_json": json_text(record)})


def ingest_reagents(connection: sqlite3.Connection, root: Path) -> None:
    data = load_json(root / "rd_reactivos_normalizados_2026-08-11.json")
    for reagent in data.get("reagents", []):
        reagent_id = reagent["id"]
        insert_row(
            connection,
            "rd_reagent",
            {
                "id": reagent_id,
                "name": reagent.get("name", reagent_id),
                "reagent_type": reagent.get("type"),
                "components": reagent.get("components"),
                "observation_window": reagent.get("observation_window"),
                "source_url": reagent.get("source_url"),
                "guide_url": reagent.get("guide_url"),
                "raw_json": json_text(reagent),
            },
        )
        for ordinal, reaction in enumerate(reagent.get("reactions", [])):
            insert_row(
                connection,
                "rd_reagent_reaction",
                {
                    "reagent_id": reagent_id,
                    "ordinal": ordinal,
                    "target": reaction.get("target", ""),
                    "sequence": reaction.get("sequence"),
                    "source_wording": reaction.get("source_wording"),
                    "raw_json": json_text(reaction),
                },
            )
        for ordinal, limitation in enumerate(reagent.get("limitations", [])):
            insert_row(connection, "rd_reagent_limitation", {"reagent_id": reagent_id, "limitation": limitation, "ordinal": ordinal})
        for ordinal, complement in enumerate(reagent.get("complements", [])):
            insert_row(connection, "rd_reagent_complement", {"reagent_id": reagent_id, "complement_id": complement, "ordinal": ordinal})

    audit = load_json(root / "rd_reactivos_auditoria_internacional_2026-08-11.json")
    for finding in audit.get("global_findings", []):
        insert_row(
            connection,
            "rd_reagent_audit_finding",
            {
                "finding_id": finding["id"],
                "status": finding.get("status"),
                "finding": finding.get("finding", ""),
                "sources_json": json_text(finding.get("sources", [])),
                "raw_json": json_text(finding),
            },
        )
    for override in audit.get("reagent_overrides", []):
        insert_row(
            connection,
            "rd_reagent_audit_override",
            {
                "reagent_id": override["id"],
                "evidence_status": override.get("evidence_status"),
                "observation_override": override.get("observation_override"),
                "important_correction": override.get("important_correction"),
                "sources_json": json_text(override.get("sources", [])),
                "raw_json": json_text(override),
            },
        )


def ingest_testing(connection: sqlite3.Connection, root: Path) -> None:
    data = load_json(root / "rd_testeos_eventos_2025_evidence_2026-08-12.json")
    source = data.get("source", {})
    insert_row(
        connection,
        "rd_test_batch",
        {
            "batch_id": "testeo-2025",
            "source_file": source.get("file_name"),
            "source_copy": source.get("source_copy"),
            "sha256": source.get("sha256"),
            "filename_period_label": source.get("filename_period_label"),
            "formula_count": source.get("formula_count"),
            "raw_json": json_text(data),
        },
    )
    for record in data.get("source_sheets", []):
        insert_row(connection, "rd_test_source_sheet", {**record, "raw_json": json_text(record)})
    event_columns = {
        "event_id", "source_sheet_index", "source_sheet_name", "event_label_candidate", "event_label_status",
        "source_period_label", "date_raw_token", "date_iso_candidate", "date_status", "date_parse_style",
        "date_confidence", "outside_filename_period_candidate", "is_source_copy_candidate", "duplicate_group_id",
        "duplicate_group_size", "duplicate_status", "duplicate_canonical_sheet_candidate", "venue_id", "venue_name",
        "producer_id", "producer_name", "link_status", "link_evidence_ref", "link_confidence", "link_review_status",
    }
    for record in data.get("events", []):
        insert_row(connection, "rd_test_event", {**{k: record.get(k) for k in event_columns}, "raw_json": json_text(record)})
    row_columns = {
        "test_id", "event_id", "source_sheet_name", "source_row", "row_status", "substance_raw",
        "substance_normalized_candidate", "substance_map_status", "format_raw", "test_1_raw", "result_1_raw",
        "test_2_raw", "result_2_raw", "test_3_raw", "result_3_raw", "test_4_raw", "result_4_raw", "extra_1_raw",
        "source_duplicate_group_id", "source_duplicate_status", "interpretation_policy",
    }
    for record in data.get("test_rows", []):
        insert_row(connection, "rd_test_row", {**{k: record.get(k) for k in row_columns}, "raw_json": json_text(record)})
    observation_columns = {
        "observation_id", "test_id", "event_id", "source_sheet_name", "source_row", "observation_ordinal",
        "substance_raw", "substance_normalized_candidate", "reagent_raw", "reagent_normalized_candidate",
        "reagent_map_status", "result_raw", "result_normalized_candidate", "result_map_status", "observation_status",
        "interpretation_policy",
    }
    for record in data.get("observations", []):
        insert_row(connection, "rd_test_observation", {**{k: record.get(k) for k in observation_columns}, "raw_json": json_text(record)})
    for record in data.get("substance_map", []):
        insert_row(connection, "rd_test_substance_map", {**record, "raw_json": json_text(record)})
    for record in data.get("reagent_map", []):
        insert_row(connection, "rd_test_reagent_map", {**record, "raw_json": json_text(record)})
    link_columns = {
        "link_id", "event_id", "source_sheet_name", "target_kind", "target_id", "target_name", "relation_type",
        "evidence_ref", "confidence", "status", "review_status", "not_inferred_from_sheet_name",
    }
    for record in data.get("link_queue", []):
        insert_row(connection, "rd_test_link_queue", {**{k: record.get(k) for k in link_columns}, "raw_json": json_text(record)})


def ingest_content(connection: sqlite3.Connection, root: Path) -> None:
    spec = load_json(root / "rd_post_chemsex_spec_2026-08-11.json")
    post_id = spec["post_id"]
    insert_row(
        connection,
        "rd_content_post",
        {
            "post_id": post_id,
            "schema_version": spec.get("schema_version"),
            "language": spec.get("language"),
            "status": spec.get("status"),
            "source_document": spec.get("source_document"),
            "source_sha256": spec.get("source_sha256"),
            "source_page_count": spec.get("source_page_count"),
            "raw_json": json_text(spec),
        },
    )
    for key, value in spec.get("post_policy", {}).items():
        insert_row(connection, "rd_content_post_policy", {"post_id": post_id, "policy_key": key, "policy_value": str(value)})
    for slide in spec.get("slides", []):
        slide_id = slide["slide_id"]
        insert_row(
            connection,
            "rd_content_slide",
            {
                "slide_id": slide_id,
                "post_id": post_id,
                "sequence": slide.get("sequence"),
                "source_pages_json": json_text(slide.get("source_pages", [])),
                "role": slide.get("role"),
                "title": slide.get("title"),
                "layout_policy": slide.get("layout_policy"),
                "raw_json": json_text(slide),
            },
        )
        for ordinal, text in enumerate(slide.get("text_blocks", [])):
            insert_row(connection, "rd_content_slide_text", {"slide_id": slide_id, "ordinal": ordinal, "text": text})
        for ordinal, entity_id in enumerate(slide.get("entity_refs", [])):
            insert_row(connection, "rd_content_slide_entity", {"slide_id": slide_id, "entity_id": entity_id, "ordinal": ordinal})
        for relation in slide.get("relation_refs", []):
            insert_row(
                connection,
                "rd_content_slide_relation",
                {
                    "slide_id": slide_id,
                    "relation_id": relation.get("relation_ref", ""),
                    "status": relation.get("status"),
                    "relation_type": relation.get("relation_type"),
                },
            )
        for claim_id in slide.get("claim_refs", []):
            insert_row(connection, "rd_content_slide_claim", {"slide_id": slide_id, "claim_id": claim_id})
        for card in slide.get("interaction_cards", []):
            insert_row(
                connection,
                "rd_content_interaction_card",
                {
                    "card_id": card["card_id"],
                    "slide_id": slide_id,
                    "title": card.get("title", ""),
                    "body": card.get("text", ""),
                    "relation_id": card.get("relation_ref"),
                    "claim_id": card.get("claim_ref"),
                    "semantic_link_json": json_text(card.get("semantic_link")) if card.get("semantic_link") else None,
                    "raw_json": json_text(card),
                },
            )
    for claim in spec.get("content_claims", []):
        insert_row(
            connection,
            "rd_content_claim",
            {
                "claim_id": claim["claim_id"],
                "post_id": post_id,
                "source_slide": claim.get("source_slide"),
                "source_card": claim.get("source_card"),
                "source_text_preserved": claim.get("source_text_preserved"),
                "claim_status": claim.get("claim_status"),
                "required_relation_type": claim.get("required_relation_type"),
                "public_rule": claim.get("public_rule"),
                "raw_json": json_text(claim),
            },
        )

    brief = load_json(root / "rd_post_chemsex_visual_brief_2026-08-11.json")
    for item in brief.get("briefs", []):
        brief_id = f"{post_id}:{item['slide_id']}"
        insert_row(
            connection,
            "rd_visual_brief",
            {
                "brief_id": brief_id,
                "slide_id": item["slide_id"],
                "visual_role": item.get("visual_role"),
                "primary_form": item.get("primary_form"),
                "animation_logic": item.get("animation_logic"),
                "raw_json": json_text(item),
            },
        )
        for ordinal, vector in enumerate(item.get("semantic_vector", [])):
            insert_row(connection, "rd_visual_brief_vector", {"brief_id": brief_id, "ordinal": ordinal, "vector": vector})
        for ordinal, rule in enumerate(item.get("do_not", [])):
            insert_row(connection, "rd_visual_brief_do_not", {"brief_id": brief_id, "ordinal": ordinal, "rule": rule})


def ingest_scrapes(connection: sqlite3.Connection, root: Path) -> None:
    for name in ("rd_firecrawl_2026-08-11.json", "rd_firecrawl_matriz_2026-08-11.json"):
        data = load_json(root / name)
        crawl_id = data.get("crawl_id", name)
        insert_row(
            connection,
            "rd_scrape_batch",
            {
                "crawl_id": crawl_id,
                "status": data.get("status"),
                "total": data.get("total"),
                "completed": data.get("completed"),
                "credits_used": data.get("credits_used"),
                "retrieved_at": data.get("retrieved_at"),
                "source_file": name,
                "raw_json": json_text({k: v for k, v in data.items() if k != "data"}),
            },
        )
        for index, page in enumerate(data.get("data", [])):
            metadata = page.get("metadata") if isinstance(page, dict) else None
            insert_row(
                connection,
                "rd_scrape_page",
                {
                    "crawl_id": crawl_id,
                    "page_index": index,
                    "url": page.get("url") if isinstance(page, dict) else None,
                    "page_status": page.get("status") if isinstance(page, dict) else None,
                    "title": page.get("title") if isinstance(page, dict) else None,
                    "markdown": page.get("markdown") if isinstance(page, dict) else None,
                    "html": page.get("html") if isinstance(page, dict) else None,
                    "metadata_json": json_text(metadata) if metadata is not None else None,
                    "raw_json": json_text(page),
                },
            )


def register_tables(connection: sqlite3.Connection) -> None:
    registry = {
        "rd_import_run": ("governance", "One reproducible construction/import run.", None),
        "rd_file_manifest": ("governance", "Hash and inventory of every recovered file, including dependencies.", None),
        "rd_artifact": ("provenance", "Original RD artifacts preserved as bytes and/or UTF-8 text.", None),
        "rd_catalog_table_count": ("catalog", "Row counts of the inherited canonical Mak catalog tables.", str(DEFAULT_CANONICAL)),
        "rd_entity": ("semantic", "The 48-entity RD universe.", "rd_universo_entidades_2026-08-11.json"),
        "rd_entity_profile": ("semantic", "Derived public-facing profile records.", "rd_fichas_entidades_2026-08-11.json"),
        "rd_source": ("evidence", "Classified source URLs.", "rd_fuentes_catalogo_2026-08-11.json"),
        "rd_relation": ("semantic", "Candidate relations with status, confidence and scope.", "rd_grafo_relaciones_2026-08-11.json"),
        "rd_reagent": ("testing", "Normalized reagent library.", "rd_reactivos_normalizados_2026-08-11.json"),
        "rd_reagent_audit_override": ("testing", "International audit corrections and scope limits.", "rd_reactivos_auditoria_internacional_2026-08-11.json"),
        "rd_test_event": ("testing", "Evidence events derived from source sheets.", "rd_testeos_eventos_2025_evidence_2026-08-12.json"),
        "rd_test_row": ("testing", "Preserved source rows, including anomalies.", "rd_testeos_eventos_2025_evidence_2026-08-12.json"),
        "rd_test_observation": ("testing", "Individual reagent/result observations.", "rd_testeos_eventos_2025_evidence_2026-08-12.json"),
        "rd_content_post": ("content", "Source-preserving post specifications.", "rd_post_chemsex_spec_2026-08-11.json"),
        "rd_visual_brief": ("content", "Semantic visual instructions associated with slides.", "rd_post_chemsex_visual_brief_2026-08-11.json"),
        "rd_scrape_page": ("evidence", "Raw page-level Firecrawl evidence.", "rd_firecrawl_2026-08-11.json"),
    }
    for table_name, (layer, description, source_path) in registry.items():
        insert_row(connection, "rd_schema_registry", {"table_name": table_name, "layer": layer, "description": description, "source_path": source_path})


def merge_field_store(connection: sqlite3.Connection, field_path: Path) -> None:
    if not field_path.exists():
        return
    field_uri = field_path.as_posix().replace("'", "''")
    connection.execute(f"ATTACH DATABASE '{field_uri}' AS field_source")
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS field_atenciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            evento TEXT,
            tipo TEXT NOT NULL,
            derivado_a TEXT,
            rango_etario TEXT,
            notas TEXT
        );
        CREATE TABLE IF NOT EXISTS field_encuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            evento TEXT,
            pregunta_id TEXT NOT NULL,
            respuesta TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS field_registros_testeo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            evento TEXT,
            sustancia_declarada TEXT NOT NULL,
            reactivo TEXT NOT NULL,
            resultado_color TEXT,
            familia_detectada TEXT,
            coincide INTEGER,
            adulterante_sospechado TEXT,
            descartada INTEGER DEFAULT 0,
            notas TEXT
        );
        """
    )
    connection.execute("INSERT INTO field_atenciones SELECT * FROM field_source.atenciones")
    connection.execute("INSERT INTO field_encuestas SELECT * FROM field_source.encuestas")
    connection.execute("INSERT INTO field_registros_testeo SELECT * FROM field_source.registros_testeo")
    # SQLite cannot detach an attached database while writes in the outer
    # connection remain in a transaction. Commit the copied field rows first;
    # the caller's surrounding transaction continues with the next imports.
    connection.commit()
    connection.execute("DETACH DATABASE field_source")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the complete RD SQLite database from recovered and Mak sources.")
    parser.add_argument("--source-root", type=Path, default=SOURCE_ROOT)
    parser.add_argument("--canonical", type=Path, default=DEFAULT_CANONICAL)
    parser.add_argument("--field", type=Path, default=DEFAULT_FIELD)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for path in (args.source_root, args.canonical):
        if not path.exists():
            raise FileNotFoundError(path)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists() and not args.force:
        raise FileExistsError(f"Destination exists; use --force only for an intentional rebuild: {args.output}")

    if args.output.exists():
        args.output.unlink()
    shutil.copy2(args.canonical, args.output)
    run_id = datetime.now().strftime("rd-complete-%Y%m%d-%H%M%S")
    connection = sqlite3.connect(args.output)
    connection.row_factory = sqlite3.Row
    try:
        create_schema(connection)
        insert_row(
            connection,
            "rd_import_run",
            {
                "run_id": run_id,
                "started_at": now_utc(),
                "completed_at": None,
                "builder_version": "rd-complete-v1",
                "source_root": str(args.source_root),
                "canonical_database": str(args.canonical),
                "field_database": str(args.field) if args.field.exists() else None,
                "status": "running",
                "notes": "Canonical catalog copied first; expanded layers imported transactionally.",
            },
        )
        with connection:
            ingest_file_manifest(connection, args.source_root)
            ingest_raw_artifacts(connection, args.source_root)
            ingest_catalog_counts(connection)
            ingest_entities(connection, args.source_root)
            ingest_sources_and_relations(connection, args.source_root)
            ingest_reagents(connection, args.source_root)
            ingest_testing(connection, args.source_root)
            ingest_content(connection, args.source_root)
            ingest_scrapes(connection, args.source_root)
            merge_field_store(connection, args.field)
            register_tables(connection)
            connection.execute(
                "UPDATE rd_import_run SET completed_at=?, status='completed' WHERE run_id=?",
                (now_utc(), run_id),
            )
        connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        connection.execute("VACUUM")
        connection.commit()
        result = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if result != "ok":
            raise RuntimeError(f"SQLite integrity check failed: {result}")
        print(json.dumps({
            "output": str(args.output),
            "bytes": args.output.stat().st_size,
            "sha256": sha256_path(args.output),
            "integrity_check": result,
            "run_id": run_id,
        }, ensure_ascii=False, indent=2))
    finally:
        connection.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
