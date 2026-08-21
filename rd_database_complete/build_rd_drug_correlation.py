"""Build the RD drug visual / reagent / 2025 testing correlation layer."""

from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
import re
import sqlite3
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote


BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "rd_complete.db"
HTML_PATH = BASE / "rd_drug_correlation.html"
ASSET_ROOT = BASE / "assets"

REAL_ASSETS = [
    ("real_mdma_kit", "mdma", "assets/real/mdma_kit.png", "https://reduciendodano.cl/wp-content/uploads/2024/05/MDMA_.png", "https://reduciendodano.cl/tienda/kit-de-testeo-para-mdma/", "Kit/producto visual RD asociado a MDMA", "MDMA / éxtasis"),
    ("real_cocaine_kit", "cocaine", "assets/real/cocaine_kit.png", "https://reduciendodano.cl/wp-content/uploads/2024/05/Coca.png", "https://reduciendodano.cl/tienda/kit-de-testeo-para-cocaina/", "Kit/producto visual RD asociado a cocaína", "Cocaína"),
    ("real_tusi_kit", "tusi", "assets/real/tusi_kit.png", "https://reduciendodano.cl/wp-content/uploads/2024/05/Tusi.png", "https://reduciendodano.cl/tienda/kit-de-testeo-para-tusi/", "Kit/producto visual RD asociado a Tusi", "Tusi"),
    ("real_ketamine_kit", "ketamine", "assets/real/ketamine_kit.png", "https://reduciendodano.cl/wp-content/uploads/2024/05/Ketamina.png", "https://reduciendodano.cl/tienda/kit-de-testeo-para-ketamina/", "Kit/producto visual RD asociado a ketamina", "Ketamina"),
    ("real_lsd_kit", "lsd", "assets/real/lsd_kit.png", "https://reduciendodano.cl/wp-content/uploads/2024/05/LSD.png", "https://reduciendodano.cl/tienda/kit-de-testeo-para-lsd/", "Kit/producto visual RD asociado a LSD", "LSD"),
    ("real_cannabis_kit", "cannabis", "assets/real/cannabis_kit.png", "https://reduciendodano.cl/wp-content/uploads/2024/05/Cannabis.png", "https://reduciendodano.cl/tienda/kit-de-testeo-para-thc-cbd/", "Kit/producto visual RD asociado a cannabis", "Cannabis"),
    ("real_amphetamine_kit", "amphetamine", "assets/real/amphetamine_kit.png", "https://reduciendodano.cl/wp-content/uploads/2021/08/A1-copy56.png", "https://reduciendodano.cl/tienda/kit-anfetaminas/", "Kit/producto visual RD asociado a anfetaminas", "Anfetamina"),
    ("real_opioids_kit", "opioids", "assets/real/opioids_kit.png", "https://reduciendodano.cl/wp-content/uploads/2024/05/Opioides.png", "https://reduciendodano.cl/tienda/kit-de-testeo-para-opioides/", "Kit/producto visual RD asociado a opioides", "Opioides"),
    ("real_ghb_test", "ghb_gbl", "assets/real/ghb_test.jpg", "https://reduciendodano.cl/wp-content/uploads/2026/07/Portada-test-de-deteccion-GHB-alcohol.jpg", "https://reduciendodano.cl/tienda/test-de-deteccion-de-ghb-en-bebidas/", "Material visual RD para test de GHB", "GHB / GBL"),
]

PUBLIC_PHOTO_ASSETS = [
    ("public_photo_psychoactive_drugs", ["cocaine", "mdma", "lsd", "psilocybin", "cannabis"], "public_libraries/real_photos/wikimedia_commons/commons_psychoactive_drugs.jpg", "https://commons.wikimedia.org/wiki/File:Psychoactive_Drugs.jpg", "CC BY-SA 2.5", "Thoric / Wikimedia Commons", "Montaje fotográfico de varias sustancias", "Referencia contextual; no identifica individualmente las sustancias del montaje."),
    ("public_photo_cocaine_hcl", ["cocaine"], "public_libraries/real_photos/wikimedia_commons/commons_cocaine_hcl.jpg", "https://commons.wikimedia.org/wiki/File:CocaineHCl.jpg", "CC BY-SA 2.5", "Thoric / Wikimedia Commons", "Fotografía de cocaína comprimida", "Referencia visual; no prueba la identidad de una muestra."),
    ("public_photo_mdma_tablets", ["mdma"], "public_libraries/real_photos/wikimedia_commons/commons_mdma_tablets.jpg", "https://commons.wikimedia.org/wiki/File:MDMA_tablets.jpg", "CC BY 2.0", "Dominic Milton Trott / Wikimedia Commons", "Fotografía de comprimidos identificados como MDMA en la ficha de origen", "La denominación de origen no garantiza la composición de una muestra; usar como referencia visual."),
    ("public_photo_ketamine", ["ketamine"], "public_libraries/real_photos/wikimedia_commons/commons_ketamine_drug.jpg", "https://commons.wikimedia.org/wiki/File:Ketamine_(Drug).jpg", "CC BY-SA 4.0", "DMTrott / Wikimedia Commons", "Fotografía de ketamina", "Referencia visual; no prueba la identidad de una muestra."),
    ("public_photo_amphetamine", ["amphetamine"], "public_libraries/real_photos/wikimedia_commons/commons_amphetamine_drug.jpg", "https://commons.wikimedia.org/wiki/File:Amphetamine_(Drug).jpg", "CC BY-SA 4.0", "DMTrott / Wikimedia Commons", "Fotografía de anfetamina en polvo", "Referencia visual; no prueba la identidad de una muestra."),
    ("public_photo_ghb", ["ghb_gbl"], "public_libraries/real_photos/wikimedia_commons/commons_ghb.jpg", "https://commons.wikimedia.org/wiki/File:GHB_(Gamma-Hydroxybutyric_Acid).jpg", "CC BY-SA 4.0", "DMTrott / Wikimedia Commons", "Fotografía de GHB", "Referencia visual; no prueba la identidad de una muestra."),
    ("public_photo_dmt", ["dmt"], "public_libraries/real_photos/wikimedia_commons/commons_dmt.jpg", "https://commons.wikimedia.org/wiki/File:DMT.jpg", "CC BY-SA 4.0", "DMTrott / Wikimedia Commons", "Fotografía de DMT", "Referencia visual; no prueba la identidad de una muestra."),
    ("public_photo_heroin", ["heroin", "opioids"], "public_libraries/real_photos/wikimedia_commons/commons_heroin_drug.jpg", "https://commons.wikimedia.org/wiki/File:Heroin_(Drug).jpg", "CC BY-SA 4.0", "DMTrott / Wikimedia Commons", "Fotografía de heroína", "Referencia visual; no prueba la identidad de una muestra."),
    ("public_photo_lsd_blotter", ["lsd"], "public_libraries/real_photos/wikimedia_commons/commons_lsd_blotter.jpg", "https://commons.wikimedia.org/wiki/File:LSD_blotter.jpg", "Public domain", "Erik Fenderson / Wikimedia Commons", "Fotografía de blotter LSD", "Referencia visual; no prueba la identidad de una muestra."),
    ("public_photo_cannabis_bud", ["cannabis"], "public_libraries/real_photos/wikimedia_commons/commons_cannabis_bud_01.jpg", "https://commons.wikimedia.org/wiki/File:Cannabis_sativa_bud_(01).jpg", "CC BY-SA 4.0", "Moheen Reeyad / Wikimedia Commons", "Fotografía de flor de cannabis", "No prueba composición de THC/CBD."),
    ("public_photo_psilocybe", ["psilocybin"], "public_libraries/real_photos/wikimedia_commons/commons_psilocybe_cubensis.jpg", "https://commons.wikimedia.org/wiki/File:Psilocybe_cubensis,_2008.jpg", "Public domain", "Zergboy / Wikimedia Commons", "Fotografía de Psilocybe cubensis", "No prueba presencia de psilocibina."),
    ("public_photo_phil_controlled_substances", ["mdma", "cocaine", "fentanyl", "opioids"], "public_libraries/real_photos/cdc_phil/phil_14839_controlled_substances.jpg", "https://wwwn.cdc.gov/phil/Details.aspx?pid=14839", "Public domain", "CDC / Debora Cartagena", "Bodegón educativo con tabletas, polvo, navaja y jeringas", "Referencia educativa; no identifica sustancias individuales."),
    ("public_photo_phil_cannabis", ["cannabis"], "public_libraries/real_photos/cdc_phil/phil_16341_cannabis_context.jpg", "https://wwwn.cdc.gov/phil/Details.aspx?pid=16341", "Public domain", "CDC / PHIL", "Imagen de contexto de cannabis", "No prueba la composición de una muestra."),
]

REAGENT_PHOTOS = [
    ("reagent_photo_marquis", "marquis", "assets/real/reagent_marquis.jpeg", "https://reduciendodano.cl/wp-content/uploads/2021/05/IMG_4401-1-scaled.jpeg", "https://reduciendodano.cl/tienda/marquis/"),
    ("reagent_photo_ehrlich", "ehrlich", "assets/real/reagent_ehrlich.jpeg", "https://reduciendodano.cl/wp-content/uploads/2021/05/IMG_4422-scaled.jpeg", "https://reduciendodano.cl/tienda/ehrlich/"),
    ("reagent_photo_liebermann", "liebermann", "assets/real/reagent_liebermann.jpeg", "https://reduciendodano.cl/wp-content/uploads/2021/05/IMG_4381-scaled.jpeg", "https://reduciendodano.cl/tienda/liebermann/"),
    ("reagent_photo_morris", "morris", "assets/real/reagent_morris.jpeg", "https://reduciendodano.cl/wp-content/uploads/2024/05/IMG_4296-scaled.jpeg", "https://reduciendodano.cl/tienda/morris/"),
    ("reagent_photo_froehde", "froehde", "assets/real/reagent_froehde.jpeg", "https://reduciendodano.cl/wp-content/uploads/2021/05/IMG_4416-scaled.jpeg", "https://reduciendodano.cl/tienda/froehde/"),
    ("reagent_photo_simons", "simons", "assets/real/reagent_simons.jpeg", "https://reduciendodano.cl/wp-content/uploads/2021/08/IMG_4373-scaled.jpeg", "https://reduciendodano.cl/tienda/simons/"),
    ("reagent_photo_zimmermann", "zimmermann", "assets/real/reagent_zimmermann.jpeg", "https://reduciendodano.cl/wp-content/uploads/2024/05/IMG_4406-scaled.jpeg", "https://reduciendodano.cl/tienda/zimmermann/"),
    ("reagent_photo_mandelin", "mandelin", "assets/real/reagent_mandelin.jpeg", "https://reduciendodano.cl/wp-content/uploads/2022/09/IMG_4366-scaled.jpeg", "https://reduciendodano.cl/tienda/test-de-mandelin/"),
    ("reagent_photo_robadope", "robadope", "assets/real/reagent_robadope.jpeg", "https://reduciendodano.cl/wp-content/uploads/2021/08/IMG_4391-scaled.jpeg", "https://reduciendodano.cl/tienda/robadope/"),
    ("reagent_photo_hofmann", "hofmann", "assets/real/reagent_hofmann.jpeg", "https://reduciendodano.cl/wp-content/uploads/2021/05/IMG_4367-scaled.jpeg", "https://reduciendodano.cl/tienda/hofmann/"),
]

ICON_ASSETS = [
    ("icon_bioicons_mushroom", "assets/icons/bioicons_mushroom.svg", "CC BY 3.0", "Servier / Bioicons", "mushroom icon"),
    ("icon_bioicons_dropper", "assets/icons/bioicons_dropper.svg", "CC0", "OpenClipart / Bioicons", "generic reagent dropper"),
    ("icon_bioicons_testtube_yellow", "assets/icons/bioicons_testtube_yellow.svg", "CC BY 3.0", "Servier / Bioicons", "yellow color reference"),
    ("icon_bioicons_testtube_purple", "assets/icons/bioicons_testtube_purple.svg", "CC BY 3.0", "Servier / Bioicons", "purple color reference"),
    ("icon_bioicons_testtube_pink", "assets/icons/bioicons_testtube_pink.svg", "CC BY 3.0", "Servier / Bioicons", "pink color reference"),
    ("icon_bioicons_testtube_green", "assets/icons/bioicons_testtube_green.svg", "CC BY 3.0", "Servier / Bioicons", "green color reference"),
    ("icon_healthicons_cannabis", "assets/icons/healthicons_cannabis.svg", "MIT", "Resolve to Save Lives / Healthicons", "cannabis symbol"),
    ("icon_healthicons_pill", "assets/icons/healthicons_pill.svg", "MIT", "Resolve to Save Lives / Healthicons", "generic pill symbol"),
    ("icon_healthicons_syringe", "assets/icons/healthicons_syringe.svg", "MIT", "Resolve to Save Lives / Healthicons", "route / equipment symbol"),
    ("icon_healthicons_test_tubes", "assets/icons/healthicons_test_tubes.svg", "MIT", "Resolve to Save Lives / Healthicons", "testing equipment symbol"),
    ("icon_healthicons_diagnostics", "assets/icons/healthicons_diagnostics.svg", "MIT", "Resolve to Save Lives / Healthicons", "diagnostics symbol"),
    ("icon_bioicons_drug_tablet_1", "assets/icons/bioicons_drug_tablet_1.svg", "CC BY 3.0", "Servier / Bioicons", "tablet form reference 1"),
    ("icon_bioicons_drug_tablet_2", "assets/icons/bioicons_drug_tablet_2.svg", "CC BY 3.0", "Servier / Bioicons", "tablet form reference 2"),
    ("icon_bioicons_drug_tablet_3", "assets/icons/bioicons_drug_tablet_3.svg", "CC BY 3.0", "Servier / Bioicons", "tablet form reference 3"),
    ("icon_bioicons_drug_tablet_4", "assets/icons/bioicons_drug_tablet_4.svg", "CC BY 3.0", "Servier / Bioicons", "tablet form reference 4"),
    ("icon_bioicons_drug_tablet_5", "assets/icons/bioicons_drug_tablet_5.svg", "CC BY 3.0", "Servier / Bioicons", "tablet form reference 5"),
    ("icon_bioicons_drug_tablet_6", "assets/icons/bioicons_drug_tablet_6.svg", "CC BY 3.0", "Servier / Bioicons", "tablet form reference 6"),
    ("icon_bioicons_drug_tablet_7", "assets/icons/bioicons_drug_tablet_7.svg", "CC BY 3.0", "Servier / Bioicons", "tablet form reference 7"),
    ("icon_bioicons_drug_capsule_1", "assets/icons/bioicons_drug_capsule_1.svg", "CC BY 3.0", "Servier / Bioicons", "capsule form reference 1"),
    ("icon_bioicons_drug_capsule_2", "assets/icons/bioicons_drug_capsule_2.svg", "CC BY 3.0", "Servier / Bioicons", "capsule form reference 2"),
    ("icon_bioicons_drug_capsule_3", "assets/icons/bioicons_drug_capsule_3.svg", "CC BY 3.0", "Servier / Bioicons", "capsule form reference 3"),
    ("icon_bioicons_drug_capsule_4", "assets/icons/bioicons_drug_capsule_4.svg", "CC BY 3.0", "Servier / Bioicons", "capsule form reference 4"),
    ("icon_bioicons_granule_bottle_open", "assets/icons/bioicons_granule_bottle_open.svg", "CC BY 3.0", "Servier / Bioicons", "powder / granule form reference, open"),
    ("icon_bioicons_granule_bottle_closed", "assets/icons/bioicons_granule_bottle_closed.svg", "CC BY 3.0", "Servier / Bioicons", "powder / granule form reference, closed"),
    ("icon_bioicons_bottle_drug", "assets/icons/bioicons_bottle_drug.svg", "CC BY 3.0", "Servier / Bioicons", "medicine bottle form reference"),
    ("icon_bioicons_paper_chromatography", "assets/icons/bioicons_paper_chromatography.svg", "CC BY 3.0", "Servier / Bioicons", "paper / blotter form and analysis context"),
    ("icon_bioicons_wine", "assets/icons/bioicons_wine.svg", "CC BY 3.0", "Servier / Bioicons", "alcohol context symbol"),
    ("icon_bioicons_water_bottle", "assets/icons/bioicons_water_bottle.svg", "CC BY 3.0", "Servier / Bioicons", "liquid / bottle form reference"),
    ("icon_bioicons_inhaler", "assets/icons/bioicons_inhaler.svg", "CC BY 3.0", "Servier / Bioicons", "inhalation route context"),
    ("icon_bioicons_particles_smoke", "assets/icons/bioicons_particles_smoke.svg", "CC0", "OpenClipart / Bioicons", "aerosol / smoke context, not substance identity"),
    ("icon_bioicons_smiles", "assets/icons/bioicons_smiles.svg", "CC0", "Simon Dürr / Bioicons", "molecular representation context"),
    ("icon_bioicons_chemical_library", "assets/icons/bioicons_chemical_library.svg", "CC0", "Simon Dürr / Bioicons", "chemical family reference"),
]

CHEMICAL_ASSETS = [
    ("chemical_pubchem_2c_b", "two_c_b", "assets/chemical/pubchem_2c_b.png", "2C-B"),
    ("chemical_pubchem_five_meo_dmt", "five_meo_dmt", "assets/chemical/pubchem_five_meo_dmt.png", "5-MeO-DMT"),
    ("chemical_pubchem_alcohol", "alcohol", "assets/chemical/pubchem_alcohol.png", "Etanol"),
    ("chemical_pubchem_amphetamine", "amphetamine", "assets/chemical/pubchem_amphetamine.png", "Anfetamina"),
    ("chemical_pubchem_caffeine", "caffeine", "assets/chemical/pubchem_caffeine.png", "Cafeína"),
    ("chemical_pubchem_cocaine", "cocaine", "assets/chemical/pubchem_cocaine.png", "Cocaína"),
    ("chemical_pubchem_codeine", "codeine", "assets/chemical/pubchem_codeine.png", "Codeína"),
    ("chemical_pubchem_det", "det", "assets/chemical/pubchem_det.png", "DET"),
    ("chemical_pubchem_dmt", "dmt", "assets/chemical/pubchem_dmt.png", "DMT"),
    ("chemical_pubchem_dxm", "dxm", "assets/chemical/pubchem_dxm.png", "Dextrometorfano"),
    ("chemical_pubchem_escopolamina", "escopolamina", "assets/chemical/pubchem_escopolamina.png", "Escopolamina"),
    ("chemical_pubchem_phenacetin", "phenacetin", "assets/chemical/pubchem_phenacetin.png", "Fenacetina"),
    ("chemical_pubchem_fentanyl", "fentanyl", "assets/chemical/pubchem_fentanyl.png", "Fentanilo"),
    ("chemical_pubchem_ghb_gbl", "ghb_gbl", "assets/chemical/pubchem_ghb_gbl.png", "GHB"),
    ("chemical_pubchem_heroin", "heroin", "assets/chemical/pubchem_heroin.png", "Heroína"),
    ("chemical_pubchem_ketamine", "ketamine", "assets/chemical/pubchem_ketamine.png", "Ketamina"),
    ("chemical_pubchem_lsd", "lsd", "assets/chemical/pubchem_lsd.png", "LSD"),
    ("chemical_pubchem_levamisole", "levamisole", "assets/chemical/pubchem_levamisole.png", "Levamisol"),
    ("chemical_pubchem_lidocaine", "lidocaine", "assets/chemical/pubchem_lidocaine.png", "Lidocaína"),
    ("chemical_pubchem_mda", "mda", "assets/chemical/pubchem_mda.png", "MDA"),
    ("chemical_pubchem_mdma", "mdma", "assets/chemical/pubchem_mdma.png", "MDMA"),
    ("chemical_pubchem_mdpv", "mdpv", "assets/chemical/pubchem_mdpv.png", "MDPV"),
    ("chemical_pubchem_mephedrone", "mephedrone", "assets/chemical/pubchem_mephedrone.png", "Mefedrona"),
    ("chemical_pubchem_methamphetamine", "methamphetamine", "assets/chemical/pubchem_methamphetamine.png", "Metanfetamina"),
    ("chemical_pubchem_morphine", "morphine", "assets/chemical/pubchem_morphine.png", "Morfina"),
    ("chemical_pubchem_oxycodone", "oxycodone", "assets/chemical/pubchem_oxycodone.png", "Oxicodona"),
    ("chemical_pubchem_pma", "pma", "assets/chemical/pubchem_pma.png", "PMA"),
    ("chemical_pubchem_pmma", "pmma", "assets/chemical/pubchem_pmma.png", "PMMA"),
    ("chemical_pubchem_ritonavir", "ritonavir_cobicistat", "assets/chemical/pubchem_ritonavir.png", "Ritonavir (componente de la entidad)"),
    ("chemical_pubchem_tropacocaine", "tropacocaine_and_related_impurities", "assets/chemical/pubchem_tropacocaine.png", "Tropacocaína"),
    ("chemical_pubchem_xylazine", "xylazine", "assets/chemical/pubchem_xylazine.png", "Xilazina"),
    ("chemical_pubchem_a_pvp", "a_pvp", "assets/chemical/pubchem_a_pvp.png", "alfa-PVP"),
    ("chemical_pubchem_psilocybin", "psilocybin", "assets/chemical/pubchem_psilocybin.png", "Psilocibina"),
]

# Every entity receives an explicit visual plan. A form/context symbol is labelled as
# such; it is never presented as chemical identification. Named compounds use a
# compound-specific PubChem structure image when one is available.
ENTITY_VISUAL_PLAN = {
    "two_c_b": [("chemical_pubchem_2c_b", "chemical_reference", "high", "Estructura 2D específica de 2C-B; no confirma la composición de una muestra." )],
    "four_ho_substances": [("icon_bioicons_chemical_library", "family_reference", "medium", "Referencia visual de familia química 4-HO; no representa una molécula única." )],
    "benzofurans": [("icon_bioicons_drug_capsule_1", "form_reference", "low", "Referencia de forma farmacéutica; no identifica 5-APB ni 6-APB." )],
    "five_meo_dmt": [("chemical_pubchem_five_meo_dmt", "chemical_reference", "high", "Estructura 2D específica de 5-MeO-DMT; no confirma la composición de una muestra." )],
    "alcohol": [("chemical_pubchem_alcohol", "chemical_reference", "high", "Estructura 2D de etanol, usada como referencia del componente; no representa todas las bebidas." ), ("icon_bioicons_wine", "context_symbol", "medium", "Símbolo de contexto alcohólico; no identifica una bebida concreta." )],
    "amphetamine": [("chemical_pubchem_amphetamine", "chemical_reference", "high", "Estructura 2D específica de anfetamina; no confirma la composición de una muestra." )],
    "benzodiazepines": [("icon_bioicons_bottle_drug", "form_reference", "low", "Referencia de medicamento en envase; la entidad es una familia y no una molécula única." )],
    "caffeine": [("chemical_pubchem_caffeine", "chemical_reference", "high", "Estructura 2D específica de cafeína." )],
    "cannabis": [("icon_healthicons_cannabis", "specific_symbol", "high", "Símbolo específico de cannabis; no distingue THC, CBD ni composición de una muestra." )],
    "cathinones": [("icon_bioicons_granule_bottle_open", "form_reference", "low", "Referencia de polvo/gránulos para una familia de catinonas; no identifica una molécula." )],
    "cocaine": [("chemical_pubchem_cocaine", "chemical_reference", "high", "Estructura 2D específica de cocaína; no confirma la composición de una muestra." )],
    "codeine": [("chemical_pubchem_codeine", "chemical_reference", "high", "Estructura 2D específica de codeína." )],
    "dissociative_derivatives": [("icon_bioicons_chemical_library", "family_reference", "medium", "Referencia visual de familia disociativa; no representa una molécula única." )],
    "det": [("chemical_pubchem_det", "chemical_reference", "high", "Estructura 2D específica de DET." )],
    "dmt": [("chemical_pubchem_dmt", "chemical_reference", "high", "Estructura 2D específica de DMT." )],
    "dox_family": [("icon_bioicons_paper_chromatography", "form_reference", "low", "Referencia de papel/blotter y contexto analítico para una familia DOx; no identifica una molécula." )],
    "dxm": [("chemical_pubchem_dxm", "chemical_reference", "high", "Estructura 2D específica de dextrometorfano." )],
    "escopolamina": [("chemical_pubchem_escopolamina", "chemical_reference", "high", "Estructura 2D específica de escopolamina." )],
    "phenacetin": [("chemical_pubchem_phenacetin", "chemical_reference", "high", "Estructura 2D específica de fenacetina." )],
    "fentanyl": [("chemical_pubchem_fentanyl", "chemical_reference", "high", "Estructura 2D específica de fentanilo." )],
    "ghb_gbl": [("chemical_pubchem_ghb_gbl", "chemical_reference", "high", "Estructura 2D de GHB; la entidad también incluye GBL." ), ("icon_bioicons_water_bottle", "form_reference", "medium", "Referencia de forma líquida/envase; no identifica GHB o GBL por sí sola." )],
    "harmala_compounds": [("icon_bioicons_chemical_library", "family_reference", "medium", "Referencia visual de familia de harmalas; no representa una molécula única." )],
    "heroin": [("chemical_pubchem_heroin", "chemical_reference", "high", "Estructura 2D específica de heroína." )],
    "ketamine": [("chemical_pubchem_ketamine", "chemical_reference", "high", "Estructura 2D específica de ketamina; no confirma la composición de una muestra." )],
    "lsd": [("chemical_pubchem_lsd", "chemical_reference", "high", "Estructura 2D específica de LSD; no confirma la composición de una muestra." )],
    "levamisole": [("chemical_pubchem_levamisole", "chemical_reference", "high", "Estructura 2D específica de levamisol." )],
    "lidocaine": [("chemical_pubchem_lidocaine", "chemical_reference", "high", "Estructura 2D específica de lidocaína." )],
    "mda": [("chemical_pubchem_mda", "chemical_reference", "high", "Estructura 2D específica de MDA." )],
    "mdma": [("chemical_pubchem_mdma", "chemical_reference", "high", "Estructura 2D específica de MDMA; no confirma la composición de una muestra." )],
    "mdpv": [("chemical_pubchem_mdpv", "chemical_reference", "high", "Estructura 2D específica de MDPV." )],
    "erectile_dysfunction_medications": [("icon_bioicons_drug_capsule_2", "form_reference", "low", "Referencia de forma farmacéutica para una categoría de medicamentos; no representa sildenafil, tadalafil y vardenafil a la vez." )],
    "mephedrone": [("chemical_pubchem_mephedrone", "chemical_reference", "high", "Estructura 2D específica de mefedrona / 4-MMC." )],
    "methamphetamine": [("chemical_pubchem_methamphetamine", "chemical_reference", "high", "Estructura 2D específica de metanfetamina." )],
    "morphine": [("chemical_pubchem_morphine", "chemical_reference", "high", "Estructura 2D específica de morfina." )],
    "nbome_family": [("icon_bioicons_paper_chromatography", "form_reference", "low", "Referencia de papel/blotter y contexto analítico para una familia NBOMe; no identifica una molécula." )],
    "opioids": [("icon_bioicons_bottle_drug", "form_reference", "low", "Referencia de medicamento/envase para una familia de opioides; no identifica un opioide concreto." )],
    "oxycodone": [("chemical_pubchem_oxycodone", "chemical_reference", "high", "Estructura 2D específica de oxicodona." )],
    "pcp_derivatives": [("icon_bioicons_chemical_library", "family_reference", "medium", "Referencia visual de familia PCP/disociativos; no representa una molécula única." )],
    "pma": [("chemical_pubchem_pma", "chemical_reference", "high", "Estructura 2D específica de PMA." )],
    "pmma": [("chemical_pubchem_pmma", "chemical_reference", "high", "Estructura 2D específica de PMMA." )],
    "alkyl_nitrites": [("icon_bioicons_inhaler", "route_context", "low", "Referencia de vía inhalada; no identifica un nitrito de alquilo concreto." )],
    "prep_pep_doxypep": [("icon_bioicons_bottle_drug", "form_reference", "low", "Referencia de medicamentos en envase para una categoría terapéutica; no representa una molécula única." )],
    "psilocybin": [("chemical_pubchem_psilocybin", "chemical_reference", "high", "Estructura 2D específica de psilocibina; no confirma la composición de una muestra." ), ("icon_bioicons_mushroom", "specific_symbol", "high", "Símbolo específico de hongos; no confirma presencia de psilocibina." )],
    "ritonavir_cobicistat": [("icon_bioicons_bottle_drug", "form_reference", "low", "Referencia de medicamento en envase para una entidad combinada; no representa ambos componentes." )],
    "tropacocaine_and_related_impurities": [("chemical_pubchem_tropacocaine", "chemical_reference", "high", "Estructura 2D de tropacocaína como referencia dentro de la entidad; no representa todas las impurezas relacionadas." )],
    "tusi": [("icon_bioicons_granule_bottle_open", "form_reference", "medium", "Referencia de polvo/gránulos para una mezcla de mercado; no identifica sus componentes." )],
    "xylazine": [("chemical_pubchem_xylazine", "chemical_reference", "high", "Estructura 2D específica de xilazina." )],
    "a_pvp": [("chemical_pubchem_a_pvp", "chemical_reference", "high", "Estructura 2D específica de alfa-PVP." )],
}

# The visual catalog intentionally uses real reference photographs plus icons for
# form, family, route, or editorial context.  It does not use chemical structures
# as a substitute for a photograph or a presumptive test.
CHEMICAL_ASSETS = []
_ICON_PLAN = {
    "two_c_b": ("icon_bioicons_drug_tablet_1", "form_reference", "medium", "Referencia de presentación en tableta; no identifica químicamente 2C-B."),
    "four_ho_substances": ("icon_bioicons_drug_capsule_1", "family_reference", "low", "Referencia editorial de presentación; la entidad es una familia."),
    "benzofurans": ("icon_bioicons_drug_capsule_2", "family_reference", "low", "Referencia editorial de presentación; no identifica 5-APB ni 6-APB."),
    "five_meo_dmt": ("icon_bioicons_particles_smoke", "context_symbol", "low", "Referencia editorial de vía/contexto; no identifica una molécula."),
    "alcohol": ("icon_bioicons_wine", "context_symbol", "high", "Símbolo de contexto alcohólico; no identifica una bebida concreta."),
    "amphetamine": ("icon_bioicons_drug_capsule_3", "form_reference", "medium", "Referencia de presentación sólida; no confirma la identidad de una muestra."),
    "benzodiazepines": ("icon_bioicons_bottle_drug", "form_reference", "low", "Referencia de medicamento/envase para una familia."),
    "caffeine": ("icon_bioicons_drug_tablet_2", "form_reference", "low", "Referencia editorial de presentación; no identifica cafeína."),
    "cannabis": ("icon_healthicons_cannabis", "specific_symbol", "high", "Símbolo específico de cannabis; no distingue THC, CBD ni composición."),
    "cathinones": ("icon_bioicons_granule_bottle_open", "form_reference", "medium", "Referencia de polvo/gránulos para una familia de catinonas."),
    "cocaine": ("icon_bioicons_granule_bottle_closed", "form_reference", "medium", "Referencia de polvo/gránulos; no sustituye la fotografía real ni el testeo."),
    "codeine": ("icon_bioicons_drug_tablet_3", "form_reference", "low", "Referencia de medicamento en tableta; no identifica codeína."),
    "dissociative_derivatives": ("icon_bioicons_chemical_library", "family_reference", "low", "Símbolo editorial de familia/disociativos; no es una estructura química."),
    "det": ("icon_bioicons_drug_capsule_4", "form_reference", "low", "Referencia editorial de presentación; no identifica DET."),
    "dmt": ("icon_bioicons_particles_smoke", "context_symbol", "low", "Referencia editorial de contexto/vía; no identifica DMT."),
    "dox_family": ("icon_bioicons_paper_chromatography", "form_reference", "low", "Referencia de papel/blotter y análisis; no identifica una molécula."),
    "dxm": ("icon_bioicons_drug_tablet_4", "form_reference", "low", "Referencia de medicamento en tableta; no identifica DXM."),
    "escopolamina": ("icon_bioicons_drug_tablet_5", "form_reference", "low", "Referencia de presentación farmacéutica; no identifica escopolamina."),
    "phenacetin": ("icon_bioicons_drug_tablet_6", "form_reference", "low", "Referencia de presentación sólida; no identifica fenacetina."),
    "fentanyl": ("icon_healthicons_syringe", "route_context", "low", "Símbolo de equipo/vía; no identifica fentanilo."),
    "ghb_gbl": ("icon_bioicons_water_bottle", "form_reference", "medium", "Referencia de forma líquida/envase; no identifica GHB o GBL."),
    "harmala_compounds": ("icon_bioicons_chemical_library", "family_reference", "low", "Símbolo editorial de familia; no es una estructura química."),
    "heroin": ("icon_bioicons_granule_bottle_open", "form_reference", "medium", "Referencia de polvo/gránulos; no identifica heroína."),
    "ketamine": ("icon_bioicons_bottle_drug", "form_reference", "medium", "Referencia de envase/medicamento; no identifica ketamina."),
    "lsd": ("icon_bioicons_paper_chromatography", "form_reference", "medium", "Referencia de blotter y análisis; no sustituye la fotografía real."),
    "levamisole": ("icon_bioicons_drug_capsule_2", "form_reference", "low", "Referencia de presentación sólida; no identifica levamisol."),
    "lidocaine": ("icon_bioicons_drug_capsule_3", "form_reference", "low", "Referencia farmacéutica; no identifica lidocaína."),
    "mda": ("icon_bioicons_drug_tablet_7", "form_reference", "low", "Referencia de tableta; no identifica MDA."),
    "mdma": ("icon_bioicons_drug_tablet_1", "form_reference", "medium", "Referencia de tableta; no confirma la identidad de un comprimido."),
    "mdpv": ("icon_bioicons_drug_capsule_4", "form_reference", "low", "Referencia de presentación sólida; no identifica MDPV."),
    "erectile_dysfunction_medications": ("icon_bioicons_bottle_drug", "form_reference", "low", "Referencia de medicamentos en envase para una categoría."),
    "mephedrone": ("icon_bioicons_granule_bottle_closed", "form_reference", "medium", "Referencia de polvo/gránulos; no identifica mefedrona."),
    "methamphetamine": ("icon_bioicons_granule_bottle_open", "form_reference", "medium", "Referencia de polvo/cristales; no identifica metanfetamina."),
    "morphine": ("icon_bioicons_bottle_drug", "form_reference", "low", "Referencia de medicamento/envase; no identifica morfina."),
    "nbome_family": ("icon_bioicons_paper_chromatography", "form_reference", "low", "Referencia de papel/blotter y análisis; no identifica una molécula."),
    "opioids": ("icon_healthicons_syringe", "route_context", "low", "Símbolo de equipo/vía; no identifica un opioide concreto."),
    "oxycodone": ("icon_bioicons_drug_tablet_4", "form_reference", "low", "Referencia de medicamento en tableta; no identifica oxicodona."),
    "pcp_derivatives": ("icon_bioicons_chemical_library", "family_reference", "low", "Símbolo editorial de familia/disociativos; no es una estructura química."),
    "pma": ("icon_bioicons_drug_tablet_5", "form_reference", "low", "Referencia de tableta; no identifica PMA."),
    "pmma": ("icon_bioicons_drug_tablet_6", "form_reference", "low", "Referencia de tableta; no identifica PMMA."),
    "alkyl_nitrites": ("icon_bioicons_inhaler", "route_context", "low", "Referencia de vía inhalada; no identifica un nitrito concreto."),
    "prep_pep_doxypep": ("icon_bioicons_bottle_drug", "form_reference", "low", "Referencia de medicamentos en envase; no identifica un producto concreto."),
    "psilocybin": ("icon_bioicons_mushroom", "specific_symbol", "high", "Símbolo específico de hongo; no confirma presencia de psilocibina."),
    "ritonavir_cobicistat": ("icon_bioicons_bottle_drug", "form_reference", "low", "Referencia de medicamentos en envase para una entidad combinada."),
    "tropacocaine_and_related_impurities": ("icon_bioicons_chemical_library", "family_reference", "low", "Símbolo editorial de familia/impurezas; no es una estructura química."),
    "tusi": ("icon_bioicons_granule_bottle_open", "form_reference", "medium", "Referencia de polvo/gránulos para una mezcla; no identifica sus componentes."),
    "xylazine": ("icon_bioicons_drug_tablet_7", "form_reference", "low", "Referencia de presentación sólida; no identifica xilazina."),
    "a_pvp": ("icon_bioicons_drug_capsule_4", "form_reference", "low", "Referencia de presentación sólida; no identifica alfa-PVP."),
}
ENTITY_VISUAL_PLAN = {entity_id: [details] for entity_id, details in _ICON_PLAN.items()}

# Replace the old repeated library symbols in the active drug layer with one
# generated editorial icon per entity. The downloaded public icon libraries stay
# archived, but the dashboard uses this curated one-to-one set.
ICON_ASSETS = []
GENERATED_ICON_ENTITIES = [
    "two_c_b", "four_ho_substances", "benzofurans", "five_meo_dmt", "alcohol", "amphetamine",
    "benzodiazepines", "caffeine", "cannabis", "cathinones", "cocaine", "codeine",
    "dissociative_derivatives", "det", "dmt", "dox_family", "dxm", "escopolamina", "phenacetin",
    "fentanyl", "ghb_gbl", "harmala_compounds", "heroin", "ketamine", "lsd", "levamisole",
    "lidocaine", "mda", "mdma", "mdpv", "erectile_dysfunction_medications", "mephedrone",
    "methamphetamine", "morphine", "nbome_family", "opioids", "oxycodone", "pcp_derivatives",
    "pma", "pmma", "alkyl_nitrites", "prep_pep_doxypep", "psilocybin", "ritonavir_cobicistat",
    "tropacocaine_and_related_impurities", "tusi", "xylazine", "a_pvp",
]
ENTITY_VISUAL_PLAN = {
    entity_id: [("generated_icon_" + entity_id, "generated_editorial_symbol", "high", "Icono editorial único generado para esta entidad; no identifica químicamente una muestra." )]
    for entity_id in GENERATED_ICON_ENTITIES
}

COLOR_INFO = {
    "black": ("Negro", "#111111"),
    "violet": ("Violeta", "#7c3aed"),
    "purple": ("Morado", "#8b5cf6"),
    "orange": ("Naranja", "#f97316"),
    "red": ("Rojo", "#ef4444"),
    "yellow": ("Amarillo", "#eab308"),
    "green": ("Verde", "#22c55e"),
    "blue": ("Azul", "#2563eb"),
    "cyan": ("Celeste", "#06b6d4"),
    "pink": ("Rosado", "#ec4899"),
    "brown": ("Café", "#92400e"),
    "transparent": ("Transparente", "#dbeafe"),
    "no_reaction": ("Sin reacción", "#cbd5e1"),
    "mixed": ("Mezcla de colores", "#64748b"),
    "other": ("Otro / texto no normalizado", "#94a3b8"),
}

SPANISH_COLOR_WORDS = {
    "negro": "black", "naranjo": "orange", "naranja": "orange", "rojo": "red",
    "amarillo": "yellow", "morado": "purple", "violeta": "violet", "azul": "blue",
    "celeste": "cyan", "verde": "green", "rosado": "pink", "rosa": "pink",
    "cafe": "brown", "café": "brown", "transparente": "transparent",
}


def norm(value):
    text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def data_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return "data:%s;base64,%s" % (mime, base64.b64encode(path.read_bytes()).decode("ascii"))


def parse_color(raw):
    text = norm(raw)
    if not text:
        return ("other", "Sin dato", COLOR_INFO["other"][1], "missing")
    no_reaction = any(token in text for token in ("sin reaccion", "no reacciona", "no reaccion", "negativo", "sin"))
    found = []
    for word, family in SPANISH_COLOR_WORDS.items():
        if word in text and family not in found:
            found.append(family)
    if no_reaction and not found:
        return ("no_reaction", COLOR_INFO["no_reaction"][0], COLOR_INFO["no_reaction"][1], "heuristic")
    if len(found) > 1:
        return ("mixed", " / ".join(COLOR_INFO[x][0] for x in found), COLOR_INFO["mixed"][1], "heuristic")
    if len(found) == 1:
        family = found[0]
        return (family, COLOR_INFO[family][0], COLOR_INFO[family][1], "heuristic")
    return ("other", "Otro / texto no normalizado", COLOR_INFO["other"][1], "unparsed")


def sequence_color(sequence):
    text = norm(sequence)
    families = []
    for token, family in [
        ("black", "black"), ("violet", "violet"), ("purple", "purple"),
        ("orange", "orange"), ("red", "red"), ("yellow", "yellow"),
        ("green", "green"), ("blue", "blue"), ("pink", "pink"),
        ("transparent", "transparent"), ("no change", "no_reaction"),
    ]:
        if token in text and family not in families:
            families.append(family)
    if len(families) > 1:
        return ("mixed", " / ".join(COLOR_INFO[x][0] for x in families), ",".join(COLOR_INFO[x][1] for x in families))
    if len(families) == 1:
        family = families[0]
        return (family, COLOR_INFO[family][0], COLOR_INFO[family][1])
    return ("other", sequence or "Sin referencia cromática", COLOR_INFO["other"][1])


def asset_row(asset_id, kind, path_text, source_url, source_page_url, license_name, attribution, alt_text, notes, rights_status):
    path = BASE / path_text
    return {
        "asset_id": asset_id,
        "asset_kind": kind,
        "relative_path": path_text,
        "source_url": source_url,
        "source_page_url": source_page_url,
        "license": license_name,
        "attribution": attribution,
        "rights_status": rights_status,
        "sha256": sha256(path) if path.exists() else None,
        "mime_type": mimetypes.guess_type(path.name)[0] if path.exists() else None,
        "alt_text": alt_text,
        "notes": notes,
        "local_exists": path.exists(),
    }


def ensure_schema(connection):
    connection.executescript(
        """
        PRAGMA foreign_keys = ON;
        DROP TABLE IF EXISTS rd_drug_reagent_test_summary;
        DROP TABLE IF EXISTS rd_drug_test_summary;
        DROP TABLE IF EXISTS rd_test_observed_color;
        DROP TABLE IF EXISTS rd_drug_reagent_map;
        DROP TABLE IF EXISTS rd_reagent_visual_link;
        DROP TABLE IF EXISTS rd_visual_entity_link;
        DROP TABLE IF EXISTS rd_visual_asset;
        DROP TABLE IF EXISTS rd_drug_correlation_run;
        CREATE TABLE rd_drug_correlation_run (
            run_id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT
        );
        CREATE TABLE rd_visual_asset (
            asset_id TEXT PRIMARY KEY,
            asset_kind TEXT NOT NULL,
            relative_path TEXT,
            source_url TEXT,
            source_page_url TEXT,
            license TEXT,
            attribution TEXT,
            rights_status TEXT NOT NULL,
            sha256 TEXT,
            mime_type TEXT,
            alt_text TEXT,
            notes TEXT
        );
        CREATE TABLE rd_visual_entity_link (
            entity_id TEXT NOT NULL,
            asset_id TEXT NOT NULL,
            link_role TEXT NOT NULL,
            confidence TEXT NOT NULL,
            note TEXT,
            PRIMARY KEY(entity_id, asset_id, link_role),
            FOREIGN KEY(entity_id) REFERENCES rd_entity(id),
            FOREIGN KEY(asset_id) REFERENCES rd_visual_asset(asset_id)
        );
        CREATE TABLE rd_reagent_visual_link (
            reagent_id TEXT NOT NULL,
            asset_id TEXT NOT NULL,
            link_role TEXT NOT NULL,
            note TEXT,
            PRIMARY KEY(reagent_id, asset_id, link_role),
            FOREIGN KEY(asset_id) REFERENCES rd_visual_asset(asset_id)
        );
        CREATE TABLE rd_drug_reagent_map (
            entity_id TEXT NOT NULL,
            reagent_ref TEXT NOT NULL,
            reagent_id TEXT,
            relation_id TEXT,
            relation_type TEXT,
            relation_status TEXT,
            relation_confidence TEXT,
            expected_target TEXT,
            expected_sequence TEXT,
            expected_color_family TEXT,
            expected_color_label TEXT,
            expected_color_hex TEXT,
            observed_2025_count INTEGER DEFAULT 0,
            mapping_status TEXT NOT NULL,
            notes TEXT,
            PRIMARY KEY(entity_id, reagent_ref, relation_id),
            FOREIGN KEY(entity_id) REFERENCES rd_entity(id)
        );
        CREATE TABLE rd_test_observed_color (
            observation_id TEXT PRIMARY KEY,
            test_id TEXT,
            event_id TEXT,
            entity_id TEXT,
            reagent_ref TEXT,
            reagent_id TEXT,
            source_sheet_name TEXT,
            source_row INTEGER,
            raw_result TEXT,
            normalized_color_family TEXT,
            normalized_color_label TEXT,
            color_hex TEXT,
            color_parse_status TEXT,
            result_interpretation_policy TEXT
        );
        CREATE TABLE rd_drug_test_summary (
            entity_id TEXT PRIMARY KEY,
            data_row_count INTEGER NOT NULL,
            observation_count INTEGER NOT NULL,
            distinct_test_count INTEGER NOT NULL,
            distinct_event_count INTEGER NOT NULL,
            observed_reagents_json TEXT NOT NULL,
            observed_color_families_json TEXT NOT NULL,
            FOREIGN KEY(entity_id) REFERENCES rd_entity(id)
        );
        CREATE TABLE rd_drug_reagent_test_summary (
            entity_id TEXT NOT NULL,
            reagent_ref TEXT NOT NULL,
            reagent_id TEXT,
            observation_count INTEGER NOT NULL,
            distinct_test_count INTEGER NOT NULL,
            distinct_event_count INTEGER NOT NULL,
            result_examples_json TEXT NOT NULL,
            color_counts_json TEXT NOT NULL,
            sheet_examples_json TEXT NOT NULL,
            analysis_note TEXT NOT NULL,
            PRIMARY KEY(entity_id, reagent_ref),
            FOREIGN KEY(entity_id) REFERENCES rd_entity(id)
        );
        """
    )


def build_assets(connection):
    assets = []
    for asset_id, entity_id, path_text, source_url, page_url, alt_text, display in REAL_ASSETS:
        assets.append(asset_row(asset_id, "real_reference_photo", path_text, source_url, page_url, "No indicado en la fuente recuperada", "Reduciendo Daño; permiso/licencia por verificar", alt_text, "Fotografía de un kit o material visual RD; no es una fotografía de la sustancia pura.", "source_license_unverified"))
    for asset_id, reagent_id, path_text, source_url, page_url in REAGENT_PHOTOS:
        assets.append(asset_row(asset_id, "reagent_reference_photo", path_text, source_url, page_url, "No indicado en la fuente recuperada", "Reduciendo Daño; permiso/licencia por verificar", "Fotografía de reactivo " + reagent_id, "Fotografía de producto/material RD; no se asume licencia de reutilización.", "source_license_unverified"))
    for asset_id, path_text, license_name, attribution, note in ICON_ASSETS:
        assets.append(asset_row(asset_id, "icon", path_text, None, "https://bioicons.com/" if "bioicons" in asset_id else "https://healthicons.org/", license_name, attribution, note, "Icono genérico o símbolo de método; no identifica por sí solo una sustancia.", "licensed_open_source"))
    for asset_id, entity_ids, path_text, source_url, license_name, attribution, alt_text, notes in PUBLIC_PHOTO_ASSETS:
        assets.append(asset_row(asset_id, "real_public_photo", path_text, source_url, source_url, license_name, attribution, alt_text, notes, "licensed_open_source"))
    display_names = {row[0]: row[1] for row in connection.execute("SELECT id, display_name FROM rd_entity")}
    for entity_id in GENERATED_ICON_ENTITIES:
        assets.append(asset_row(
            "generated_icon_" + entity_id,
            "generated_icon",
            "assets/generated_icons/" + entity_id + ".png",
            None,
            None,
            "Generated project asset",
            "OpenAI image generation tool",
            "Icono editorial generado para " + display_names.get(entity_id, entity_id),
            "Símbolo visual editorial; no prueba identidad, pureza, dosis ni composición.",
            "generated_internal",
        ))
    for asset_id, entity_id, path_text, compound_name in CHEMICAL_ASSETS:
        encoded_name = quote(compound_name, safe="")
        source_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/%s/PNG?image_size=small" % encoded_name
        assets.append(asset_row(asset_id, "chemical_reference_image", path_text, source_url, "https://pubchem.ncbi.nlm.nih.gov/", "PubChem public-domain data; image reuse terms to verify", "PubChem / NCBI", "Estructura química 2D de referencia para " + compound_name, "Imagen estructural específica de un compuesto; no representa una muestra real ni permite inferir pureza o composición completa.", "source_terms_to_verify"))
    connection.executemany(
        """INSERT INTO rd_visual_asset(asset_id,asset_kind,relative_path,source_url,source_page_url,license,attribution,rights_status,sha256,mime_type,alt_text,notes)
        VALUES(:asset_id,:asset_kind,:relative_path,:source_url,:source_page_url,:license,:attribution,:rights_status,:sha256,:mime_type,:alt_text,:notes)""",
        assets,
    )
    return assets


def link_visuals(connection, assets):
    asset_ids = {row["asset_id"] for row in assets}
    entities = {row[0]: row[1] for row in connection.execute("SELECT id, display_name FROM rd_entity")}
    for asset_id, entity_id, *_ in REAL_ASSETS:
        if asset_id in asset_ids and entity_id in entities:
            connection.execute(
                "INSERT INTO rd_visual_entity_link VALUES(?,?,?,?,?)",
                (entity_id, asset_id, "real_reference", "medium", "Referencia visual del material RD; no equivale a identidad de la muestra."),
            )
    for asset_id, entity_ids, *_ in PUBLIC_PHOTO_ASSETS:
        for entity_id in entity_ids:
            if asset_id in asset_ids and entity_id in entities:
                connection.execute(
                    "INSERT INTO rd_visual_entity_link VALUES(?,?,?,?,?)",
                    (entity_id, asset_id, "real_reference", "medium", "Fotografía pública real; licencia y atribución registradas. Referencia visual, no prueba de identidad."),
                )
    for entity_id, display in entities.items():
        plan = ENTITY_VISUAL_PLAN.get(entity_id)
        if not plan:
            raise ValueError("Missing explicit visual plan for entity: %s" % entity_id)
        for asset_id, role, confidence, note in plan:
            if asset_id not in asset_ids:
                raise FileNotFoundError("Visual asset %s required by entity %s" % (asset_id, entity_id))
            connection.execute(
                "INSERT INTO rd_visual_entity_link VALUES(?,?,?,?,?)",
                (entity_id, asset_id, role, confidence, note),
            )
    # Specific method/reagent symbols are linked to the reagent layer, not to a drug identity.
    if "icon_bioicons_dropper" in asset_ids:
        for row in connection.execute("SELECT id FROM rd_reagent"):
            connection.execute(
                "INSERT INTO rd_reagent_visual_link VALUES(?,?,?,?)",
                (row[0], "icon_bioicons_dropper", "generic_reagent_icon", "Símbolo de gotero; no representa el color de una reacción."),
            )
    for asset_id, reagent_id, *_ in REAGENT_PHOTOS:
        if asset_id in asset_ids and connection.execute("SELECT 1 FROM rd_reagent WHERE id=?", (reagent_id,)).fetchone():
            connection.execute(
                "INSERT INTO rd_reagent_visual_link VALUES(?,?,?,?)",
                (reagent_id, asset_id, "reference_photo", "Fotografía de producto/material RD; derechos por verificar."),
            )


def build_drug_reagent_map(connection):
    entities = {}
    for row in connection.execute("SELECT id,display_name,aliases_json FROM rd_entity"):
        aliases = json.loads(row[2] or "[]")
        entities[row[0]] = {"display_name": row[1], "tokens": {norm(row[0]), norm(row[1]), *[norm(x) for x in aliases]}}
    reactions = defaultdict(list)
    for row in connection.execute("SELECT reagent_id,target,sequence FROM rd_reagent_reaction ORDER BY ordinal"):
        reactions[row[0]].append(row)
    rows = []
    relation_sql = """SELECT id,source_ref,target_ref,source_kind,target_kind,relation_type,status,confidence,notes
                      FROM rd_relation WHERE (source_kind <> 'entity' AND target_kind='entity')
                      OR (source_kind='entity' AND target_kind <> 'entity')"""
    for relation in connection.execute(relation_sql):
        relation_id, source_ref, target_ref, source_kind, target_kind, rel_type, status, confidence, notes = relation
        if target_kind == "entity" and target_ref in entities:
            entity_id, reagent_ref = target_ref, source_ref
        elif source_kind == "entity" and source_ref in entities:
            entity_id, reagent_ref = source_ref, target_ref
        else:
            continue
        reagent_id = reagent_ref.split(":", 1)[1] if reagent_ref.startswith("reagent:") else None
        expected_target = expected_sequence = expected_family = expected_label = expected_hex = None
        for reaction in reactions.get(reagent_id, []):
            target_norm = norm(reaction[1])
            if target_norm in entities[entity_id]["tokens"] or any(target_norm and target_norm in token for token in entities[entity_id]["tokens"]):
                expected_target, expected_sequence = reaction[1], reaction[2]
                expected_family, expected_label, expected_hex = sequence_color(expected_sequence)
                break
        mapping_status = "registry_relation"
        if reagent_id is None:
            mapping_status = "method_or_strip_relation"
        elif not expected_sequence:
            mapping_status = "registry_relation_without_sequence_match"
        rows.append((entity_id, reagent_ref, reagent_id, relation_id, rel_type, status, confidence, expected_target, expected_sequence, expected_family, expected_label, expected_hex, mapping_status, notes))
    connection.executemany(
        """INSERT INTO rd_drug_reagent_map(entity_id,reagent_ref,reagent_id,relation_id,relation_type,relation_status,relation_confidence,expected_target,expected_sequence,expected_color_family,expected_color_label,expected_color_hex,mapping_status,notes)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        rows,
    )


def build_test_color_layer(connection):
    valid_entities = {row[0] for row in connection.execute("SELECT id FROM rd_entity")}
    valid_reagents = {row[0] for row in connection.execute("SELECT id FROM rd_reagent")}
    observations = []
    for row in connection.execute(
        """SELECT o.observation_id,o.test_id,o.event_id,o.substance_normalized_candidate,
                  o.reagent_normalized_candidate,o.source_sheet_name,o.source_row,o.result_raw,
                  o.interpretation_policy,r.row_status
           FROM rd_test_observation o JOIN rd_test_row r ON r.test_id=o.test_id
           WHERE r.row_status='data'"""
    ):
        observation_id, test_id, event_id, entity_id, reagent_id, sheet, source_row, raw_result, policy, row_status = row
        family, label, color_hex, parse_status = parse_color(raw_result)
        entity_id = entity_id if entity_id in valid_entities else None
        reagent_id = reagent_id if reagent_id in valid_reagents else None
        reagent_ref = "reagent:" + reagent_id if reagent_id else "raw:" + norm(row[4] or "unknown")
        observations.append((observation_id, test_id, event_id, entity_id, reagent_ref, reagent_id, sheet, source_row, raw_result, family, label, color_hex, parse_status, policy))
    connection.executemany(
        """INSERT INTO rd_test_observed_color(observation_id,test_id,event_id,entity_id,reagent_ref,reagent_id,source_sheet_name,source_row,raw_result,normalized_color_family,normalized_color_label,color_hex,color_parse_status,result_interpretation_policy)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        observations,
    )
    return observations


def build_test_summaries(connection):
    rows = connection.execute(
        """SELECT entity_id,reagent_ref,reagent_id,COUNT(*) AS observations,
                  COUNT(DISTINCT test_id),COUNT(DISTINCT event_id),
                  GROUP_CONCAT(DISTINCT raw_result),
                  GROUP_CONCAT(DISTINCT normalized_color_family),
                  GROUP_CONCAT(DISTINCT source_sheet_name)
           FROM rd_test_observed_color WHERE entity_id IS NOT NULL
           GROUP BY entity_id,reagent_ref,reagent_id"""
    ).fetchall()
    for row in rows:
        entity_id, reagent_ref, reagent_id, observations, tests, events, raw_results, colors, sheets = row
        result_examples = [x for x in (raw_results or "").split(",") if x][:12]
        color_counts = Counter(
            r[0] for r in connection.execute(
                "SELECT normalized_color_family FROM rd_test_observed_color WHERE entity_id=? AND reagent_ref=?",
                (entity_id, reagent_ref),
            )
        )
        sheet_examples = [x for x in (sheets or "").split(",") if x][:8]
        note = "Observación textual del registro 2025; no es una confirmación de identidad, pureza, dosis ni composición completa."
        connection.execute(
            """INSERT INTO rd_drug_reagent_test_summary VALUES(?,?,?,?,?,?,?,?,?,?)""",
            (entity_id, reagent_ref, reagent_id, observations, tests, events, json.dumps(result_examples, ensure_ascii=False), json.dumps(dict(color_counts), ensure_ascii=False), json.dumps(sheet_examples, ensure_ascii=False), note),
        )
    connection.execute(
        """INSERT INTO rd_drug_test_summary
        SELECT entity_id,COUNT(DISTINCT test_id),
               COUNT(*),COUNT(DISTINCT test_id),COUNT(DISTINCT event_id),
               json_group_array(DISTINCT reagent_ref),json_group_array(DISTINCT normalized_color_family)
        FROM rd_test_observed_color WHERE entity_id IS NOT NULL GROUP BY entity_id"""
    )
    connection.execute(
        """UPDATE rd_drug_reagent_map
           SET observed_2025_count=COALESCE((SELECT observation_count FROM rd_drug_reagent_test_summary s WHERE s.entity_id=rd_drug_reagent_map.entity_id AND s.reagent_ref=rd_drug_reagent_map.reagent_ref),0)"""
    )


def load_html_payload(connection):
    entities = []
    summary_by_entity = {row[0]: dict(row) for row in connection.execute("SELECT * FROM rd_drug_test_summary").fetchall()}
    entity_rows = connection.execute("SELECT id,display_name,aliases_json,entity_kind,matrix,source_status,test_status FROM rd_entity ORDER BY display_name").fetchall()
    asset_rows = {row[0]: dict(row) for row in connection.execute("SELECT * FROM rd_visual_asset").fetchall()}
    for row in entity_rows:
        entity_id, display_name, aliases_json, entity_kind, matrix, source_status, test_status = row
        visuals = []
        for link in connection.execute(
            """SELECT l.link_role,l.confidence,l.note,a.* FROM rd_visual_entity_link l JOIN rd_visual_asset a ON a.asset_id=l.asset_id WHERE l.entity_id=? ORDER BY l.link_role""",
            (entity_id,),
        ):
            item = dict(link)
            path = BASE / (item.get("relative_path") or "")
            item["data_uri"] = data_uri(path) if path.exists() else None
            visuals.append(item)
        reagent_rows = []
        for m in connection.execute(
            """SELECT m.*,r.name,r.observation_window FROM rd_drug_reagent_map m LEFT JOIN rd_reagent r ON r.id=m.reagent_id WHERE m.entity_id=? ORDER BY m.observed_2025_count DESC,m.reagent_ref""",
            (entity_id,),
        ):
            item = dict(m)
            test = connection.execute(
                "SELECT * FROM rd_drug_reagent_test_summary WHERE entity_id=? AND reagent_ref=?",
                (entity_id, item["reagent_ref"]),
            ).fetchone()
            item["test_summary"] = dict(test) if test else None
            reagent_rows.append(item)
        existing_refs = {item["reagent_ref"] for item in reagent_rows}
        for test in connection.execute(
            """SELECT s.*,r.name,r.observation_window
               FROM rd_drug_reagent_test_summary s
               LEFT JOIN rd_reagent r ON r.id=s.reagent_id
               WHERE s.entity_id=? ORDER BY s.observation_count DESC,s.reagent_ref""",
            (entity_id,),
        ):
            if test["reagent_ref"] in existing_refs:
                continue
            reagent_rows.append({
                "entity_id": entity_id,
                "reagent_ref": test["reagent_ref"],
                "reagent_id": test["reagent_id"],
                "relation_id": None,
                "relation_type": None,
                "relation_status": "no_direct_registry_relation",
                "relation_confidence": "none",
                "expected_target": None,
                "expected_sequence": None,
                "expected_color_family": None,
                "expected_color_label": None,
                "expected_color_hex": None,
                "observed_2025_count": test["observation_count"],
                "mapping_status": "observed_2025_only",
                "notes": "Observado en 2025, pero sin relación directa droga–reactivo en el registro semántico; no se interpreta como identidad.",
                "name": test["name"],
                "observation_window": test["observation_window"],
                "test_summary": dict(test),
            })
        reagent_rows.sort(key=lambda item: (-int(item.get("observed_2025_count") or 0), item.get("reagent_ref") or ""))
        summary = summary_by_entity.get(entity_id, {})
        entities.append({
            "id": entity_id,
            "display_name": display_name,
            "aliases": json.loads(aliases_json or "[]"),
            "entity_kind": entity_kind,
            "matrix": matrix,
            "source_status": source_status,
            "test_status": test_status,
            "summary": summary,
            "visuals": visuals,
            "reagents": reagent_rows,
        })
    reagent_catalog = []
    for row in connection.execute("SELECT id,name,reagent_type,observation_window,source_url,guide_url FROM rd_reagent ORDER BY name"):
        item = dict(zip(["id","name","reagent_type","observation_window","source_url","guide_url"], row))
        photos = []
        for link in connection.execute(
            """SELECT l.*,a.* FROM rd_reagent_visual_link l JOIN rd_visual_asset a ON a.asset_id=l.asset_id WHERE l.reagent_id=?""",
            (item["id"],),
        ):
            photo = dict(link)
            path = BASE / (photo.get("relative_path") or "")
            photo["data_uri"] = data_uri(path) if path.exists() else None
            photos.append(photo)
        item["visuals"] = photos
        reagent_catalog.append(item)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "entities": entities,
        "reagents": reagent_catalog,
        "stats": {
            "entities": len(entities),
            "with_2025": sum(1 for e in entities if e["summary"]),
            "observations_2025": connection.execute("SELECT COUNT(*) FROM rd_test_observed_color").fetchone()[0],
            "mapped_observations_2025": connection.execute("SELECT COUNT(*) FROM rd_test_observed_color WHERE entity_id IS NOT NULL").fetchone()[0],
            "visual_assets": connection.execute("SELECT COUNT(*) FROM rd_visual_asset").fetchone()[0],
            "real_assets": connection.execute("SELECT COUNT(*) FROM rd_visual_asset WHERE asset_kind LIKE 'real_%'").fetchone()[0],
            "icons": connection.execute("SELECT COUNT(*) FROM rd_visual_asset WHERE asset_kind='icon'").fetchone()[0],
            "generated_icons": connection.execute("SELECT COUNT(*) FROM rd_visual_asset WHERE asset_kind='generated_icon'").fetchone()[0],
            "drug_reagent_relations": connection.execute("SELECT COUNT(*) FROM rd_drug_reagent_map").fetchone()[0],
        },
    }


HTML_TEMPLATE = r'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RD · Drogas, imágenes, reactivos y testeos 2025</title>
<style>
:root{--bg:#08090d;--panel:#11131a;--panel2:#171a23;--line:#2b2e3b;--text:#f0f1f5;--muted:#a8adbc;--acid:#dcff36;--cyan:#58e8f2;--orange:#ffad5c;--red:#ff5f6d;--violet:#b98cff}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 90% 0,#12313a55,transparent 34rem),var(--bg);color:var(--text);font:14px/1.5 Inter,system-ui,sans-serif}
.shell{max-width:1700px;margin:auto;padding:28px 32px 60px}.eyebrow{color:var(--acid);letter-spacing:.25em;text-transform:uppercase;font-size:11px;font-weight:800}
h1{font-size:clamp(36px,5vw,68px);line-height:.95;letter-spacing:-.06em;margin:12px 0}h1 span{color:var(--muted);font-weight:350}.intro{max-width:1000px;color:var(--muted);font-size:16px;line-height:1.55}
.contract{max-width:1150px;padding:16px 18px;margin:20px 0;border:1px solid #dcff3655;border-left:4px solid var(--acid);border-radius:12px;background:#dcff360d}.contract strong{color:var(--acid)}.contract p{margin:6px 0;line-height:1.5}
.stats{display:grid;grid-template-columns:repeat(7,1fr);gap:9px;margin:20px 0}.stat,.panel{background:#11131aee;border:1px solid var(--line);border-radius:14px}.stat{padding:14px}.stat b{display:block;font-size:28px;color:var(--cyan)}.stat small{color:var(--muted)}
.controls{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:9px;margin:18px 0}.control label{display:block;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.12em;margin-bottom:5px}.control input,.control select{width:100%;background:var(--panel);color:var(--text);border:1px solid var(--line);border-radius:8px;padding:10px}
.layout{display:grid;grid-template-columns:minmax(310px,.7fr) minmax(650px,1.55fr);gap:14px;align-items:start}.panel{overflow:hidden}.panel-head{display:flex;justify-content:space-between;gap:10px;padding:16px 18px;border-bottom:1px solid var(--line)}.panel-head h2{font-size:17px;margin:0}.panel-head small{color:var(--muted)}
.cards{display:grid;gap:7px;padding:10px;max-height:860px;overflow:auto}.drug-card{text-align:left;color:var(--text);background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:10px;display:grid;grid-template-columns:45px 1fr auto;gap:9px;align-items:center;cursor:pointer}.drug-card:hover,.drug-card.selected{border-color:var(--cyan)}.thumb{width:45px;height:45px;object-fit:contain;background:#fff;border-radius:8px;padding:4px}.drug-card strong{font-size:14px}.drug-card small{display:block;color:var(--muted);line-height:1.35;margin-top:3px}.badge{color:var(--acid);font-size:10px;text-transform:uppercase;white-space:nowrap}
.detail{min-height:760px}.detail-body{padding:20px}.kicker{color:var(--acid);font-size:10px;text-transform:uppercase;letter-spacing:.15em;font-weight:800}.detail h2{font-size:34px;letter-spacing:-.05em;margin:7px 0}.aliases{color:var(--muted)}.chips{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}.chip{border:1px solid var(--line);border-radius:99px;padding:5px 8px;color:var(--cyan);font-size:11px}
.visuals{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin:16px 0}.visual{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:7px;min-height:132px}.visual img{width:100%;height:100px;object-fit:contain;background:#fff;border-radius:7px}.visual p{font-size:10px;color:var(--muted);margin:5px 2px 0}.visual small{display:block;color:#777c8b;font-size:9px;line-height:1.35;margin:4px 2px}.visual-empty{height:100px;border-radius:7px;background:#0d1118;border:1px dashed var(--line);display:grid;place-items:center;color:var(--muted);font-size:11px;text-align:center;padding:8px}.photo-note{border-left:3px solid var(--orange);background:#ffad5c12;color:#e6d8ca;padding:10px 12px;font-size:12px;line-height:1.5}
.kpis{display:flex;flex-wrap:wrap;gap:7px;margin:14px 0}.mini{border:1px solid var(--line);border-radius:8px;padding:7px 9px;color:var(--muted);font-size:11px}.mini b{color:var(--cyan);font-size:16px;margin-right:4px}
.matrix{overflow:auto;border:1px solid var(--line);border-radius:10px}.matrix table{width:100%;border-collapse:collapse;min-width:900px}.matrix th{background:#171a23;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.07em;text-align:left;white-space:nowrap}.matrix th,.matrix td{padding:9px;border-bottom:1px solid #2b2e3b88;vertical-align:top}.matrix td{font-size:12px}.matrix tr:hover td{background:#1b202b}.sequence{font-family:ui-monospace,monospace;font-size:11px;color:#f4f6fa}.swatch{display:inline-flex;align-items:center;gap:5px;margin:2px 4px 2px 0}.swatch i{display:inline-block;width:12px;height:12px;border-radius:50%;border:1px solid #fff5}.status{color:var(--acid);font-size:10px;text-transform:uppercase}.muted{color:var(--muted)}.note{border-left:3px solid var(--cyan);background:#58e8f20d;padding:10px 12px;color:#dce8ea;font-size:12px;line-height:1.5;margin-top:12px}
.all-reagents{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}.reagent-card{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:11px}.reagent-card h3{font-size:14px;margin:0 0 4px}.reagent-card p{margin:0;color:var(--muted);font-size:11px;line-height:1.4}
.footer{color:#777c8b;font-size:11px;line-height:1.5;margin-top:22px}@media(max-width:1200px){.stats{grid-template-columns:repeat(3,1fr)}.layout{grid-template-columns:1fr}.detail{min-height:0}}@media(max-width:650px){.shell{padding:18px 12px 45px}.stats{grid-template-columns:repeat(2,1fr)}.controls{grid-template-columns:1fr}.visuals{grid-template-columns:repeat(2,1fr)}.all-reagents{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="shell">
<div class="eyebrow">RD · capa de correlación</div>
<h1>Drogas <span>→ imagen → reactivo → color → testeo 2025</span></h1>
<p class="intro">Explorador de sustancias con imágenes de referencia, iconos editoriales, colorimetría documentada y observaciones del análisis 2025. Las conexiones están separadas por nivel de evidencia.</p>
<div class="contract"><strong>Regla de lectura:</strong><p>Un color de reactivo es una señal presumptiva, no una identificación completa. Las observaciones 2025 se muestran tal como fueron registradas y se normalizan solo como familias cromáticas; no se infieren pureza, dosis, seguridad ni composición completa.</p></div>
<div class="stats" id="stats"></div>
<div class="controls">
<div class="control"><label>Buscar droga</label><input id="search" placeholder="MDMA, ketamina, cocaína..."></div>
<div class="control"><label>Mostrar</label><select id="scope"><option value="all">Todas las entidades</option><option value="tested">Con observaciones 2025</option><option value="photo">Con imagen real local</option></select></div>
<div class="control"><label>Tipo de entidad</label><select id="kind"><option value="all">Todos</option></select></div>
<div class="control"><label>Seleccionada</label><select id="entity-select"></select></div>
</div>
<div class="layout">
<div class="panel"><div class="panel-head"><h2>Entidades</h2><small id="card-count"></small></div><div class="cards" id="cards"></div></div>
<div class="panel detail" id="detail"></div>
</div>
<div class="panel" style="margin-top:14px"><div class="panel-head"><h2>Reactivos disponibles</h2><small>Referencia visual · colorimetría · ventana</small></div><div class="all-reagents" id="all-reagents" style="padding:12px"></div></div>
<div class="footer">Las fotografías de kits/materiales RD se conservan como referencias de origen con derechos por verificar. Las fotografías públicas mantienen su fuente y licencia declarada; los iconos generados son símbolos editoriales internos y no identifican químicamente una muestra. La capa 2025 conecta solo filas marcadas como datos y mantiene sus resultados textuales.</div>
</div>
<script>
const DATA=__PAYLOAD__;
const fmt=n=>Number(n||0).toLocaleString("es-CL");
const esc=v=>String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
const norm=v=>String(v??"").normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase();
const state={id:null};
const familyColor={black:"#111111",violet:"#7c3aed",purple:"#8b5cf6",orange:"#f97316",red:"#ef4444",yellow:"#eab308",green:"#22c55e",blue:"#2563eb",cyan:"#06b6d4",pink:"#ec4899",brown:"#92400e",transparent:"#dbeafe",no_reaction:"#cbd5e1",mixed:"#64748b",other:"#94a3b8"};
function entityById(id){return DATA.entities.find(e=>e.id===id);}
function summary(e){return e.summary||{};}
function visual(e,role){return e.visuals.find(v=>v.link_role===role);}
function visualRoleLabel(v){return ({real_reference:"Fotografía real de referencia",generated_editorial_symbol:"Icono editorial generado",specific_symbol:"Símbolo específico",family_reference:"Referencia de familia",form_reference:"Referencia de forma",context_symbol:"Símbolo de contexto",route_context:"Contexto de vía / uso"}[v.link_role]||"Referencia visual");}
function swatch(family,label){return '<span class="swatch"><i style="background:'+(familyColor[family]||familyColor.other)+'"></i>'+esc(label||family||"sin dato")+'</span>';}
function assetLabel(v){if(v.asset_kind==="real_public_photo")return "Fotografía pública";if(v.asset_kind==="real_reference_photo")return "Fotografía RD/material";if(v.asset_kind==="generated_icon")return "Icono generado";return visualRoleLabel(v);}
function renderStats(){const s=DATA.stats;document.getElementById("stats").innerHTML=[["Entidades",s.entities],["Con datos 2025",s.with_2025],["Observaciones 2025",s.observations_2025],["Observaciones mapeadas",s.mapped_observations_2025],["Activos visuales",s.visual_assets],["Iconos generados",s.generated_icons],["Relaciones droga-reactivo",s.drug_reagent_relations]].map(x=>'<div class="stat"><b>'+fmt(x[1])+'</b><small>'+x[0]+'</small></div>').join("");}
function renderFilters(){const kinds=[...new Set(DATA.entities.map(e=>e.entity_kind))].sort();document.getElementById("kind").innerHTML='<option value="all">Todos</option>'+kinds.map(k=>'<option value="'+esc(k)+'">'+esc(k)+'</option>').join("");document.getElementById("entity-select").innerHTML=DATA.entities.map(e=>'<option value="'+esc(e.id)+'">'+esc(e.display_name)+'</option>').join("");}
function filteredEntities(){const q=norm(document.getElementById("search").value),scope=document.getElementById("scope").value,kind=document.getElementById("kind").value;return DATA.entities.filter(e=>{if(q&&!norm(e.display_name+" "+e.id+" "+e.aliases.join(" ")).includes(q))return false;if(scope==="tested"&&!summary(e).observation_count)return false;if(scope==="photo"&&!e.visuals.some(v=>v.link_role==="real_reference"))return false;if(kind!=="all"&&e.entity_kind!==kind)return false;return true;}).sort((a,b)=>(summary(b).observation_count||0)-(summary(a).observation_count||0)||a.display_name.localeCompare(b.display_name));}
function renderCards(){const rows=filteredEntities();document.getElementById("card-count").textContent=fmt(rows.length)+" entidades";document.getElementById("cards").innerHTML=rows.map(e=>{const v=visual(e,"real_reference")||visual(e,"generated_editorial_symbol")||visual(e,"specific_symbol")||visual(e,"family_reference")||visual(e,"form_reference")||visual(e,"context_symbol")||visual(e,"route_context")||e.visuals[0];const image=v&&v.data_uri?v.data_uri:"";const thumb=image?'<img class="thumb" src="'+image+'" alt="'+esc(v.alt_text||"")+'">':'<span class="thumb visual-empty">Referencia visual</span>';return '<button class="drug-card '+(state.id===e.id?"selected":"")+'" data-id="'+esc(e.id)+'">'+thumb+'<span><strong>'+esc(e.display_name)+'</strong><small>'+esc(e.entity_kind)+' · '+fmt(summary(e).observation_count||0)+' observaciones 2025</small></span><span class="badge">'+(summary(e).observation_count?"testeada":"sin fila 2025")+'</span></button>';}).join("")||'<p class="muted" style="padding:12px">No hay entidades con ese filtro.</p>';document.querySelectorAll(".drug-card").forEach(b=>b.addEventListener("click",()=>{state.id=b.dataset.id;document.getElementById("entity-select").value=state.id;renderCards();renderDetail();}));}
function renderDetail(){const e=entityById(state.id)||DATA.entities[0];state.id=e.id;document.getElementById("entity-select").value=e.id;const s=summary(e);const real=e.visuals.filter(v=>v.link_role==="real_reference"),other=e.visuals.filter(v=>v.link_role!=="real_reference");let visuals=real.concat(other).slice(0,4);let html='<div class="detail-body"><div class="kicker">'+esc(e.entity_kind)+' · '+esc(e.test_status||"estado no indicado")+'</div><h2>'+esc(e.display_name)+'</h2><div class="aliases">Alias: '+esc(e.aliases.length?e.aliases.join(", "):"sin alias registrado")+'</div><div class="chips"><span class="chip">Fuente: '+esc(e.source_status||"no indicado")+'</span><span class="chip">Matriz: '+(e.matrix?"sí":"no / candidato")+'</span></div><div class="visuals">'+visuals.map(v=>'<div class="visual">'+(v.data_uri?'<img src="'+v.data_uri+'" alt="'+esc(v.alt_text)+'">':'<div class="visual-empty">Referencia visual registrada</div>')+'<p><strong>'+assetLabel(v)+'</strong><br>'+esc(v.license||"")+'</p><small>'+esc(v.note||"")+'</small></div>').join("")+'</div><div class="photo-note">Las fotografías públicas, las fotografías de kits/materiales y los iconos son referencias visuales. No identifican por sí solos una muestra. La lectura depende de reactivos, colorimetría y datos 2025; una señal colorimétrica es presumptiva.</div><div class="kpis"><span class="mini"><b>'+fmt(s.observation_count||0)+'</b> observaciones</span><span class="mini"><b>'+fmt(s.distinct_test_count||0)+'</b> tests</span><span class="mini"><b>'+fmt(s.distinct_event_count||0)+'</b> eventos</span><span class="mini"><b>'+fmt(e.reagents.length)+'</b> relaciones/reagentes</span></div><h3>Reactivos y colorimetría conectada</h3>'+renderMatrix(e)+'</div>';document.getElementById("detail").innerHTML=html;}
function renderMatrix(e){if(!e.reagents.length)return '<div class="note">No existe una relación directa droga–reactivo en el registro semántico. Si hubo observaciones 2025, se muestran en el visor general como evidencia observada, no como interpretación.</div>';return '<div class="matrix"><table><thead><tr><th>Reactivo</th><th>Relación RD</th><th>Referencia colorimétrica</th><th>Observado 2025</th><th>Lectura</th></tr></thead><tbody>'+e.reagents.map(m=>{const t=m.test_summary||{}, colors=JSON.parse(t.color_counts_json||"{}"), colorHtml=Object.keys(colors).map(k=>swatch(k,k+" ("+fmt(colors[k])+")")).join("");return '<tr><td><strong>'+esc(m.name||m.reagent_ref)+'</strong><br><span class="muted">'+esc(m.reagent_id||"referencia no normalizada")+'</span></td><td><span class="status">'+esc(m.mapping_status)+'</span><br><span class="muted">'+esc(m.relation_status||"")+' · '+esc(m.relation_confidence||"")+'</span></td><td>'+(m.expected_sequence?'<span class="sequence">'+esc(m.expected_sequence)+'</span><br>'+swatch(m.expected_color_family,m.expected_color_label):'<span class="muted">Sin secuencia cromática directa en la ficha del reactivo</span>')+'</td><td><strong>'+fmt(t.observation_count||0)+'</strong> obs.<br>'+colorHtml+'<br><span class="muted">'+esc((JSON.parse(t.result_examples_json||"[]")).slice(0,6).join(" · "))+'</span></td><td><span class="muted">'+esc(t.analysis_note||"La observación se conserva sin inferir identidad.")+'</span></td></tr>';}).join("")+'</tbody></table></div>';}
function renderReagents(){document.getElementById("all-reagents").innerHTML=DATA.reagents.map(r=>'<div class="reagent-card"><h3>'+esc(r.name)+'</h3><p>'+esc(r.reagent_type||"")+' · ventana: '+esc(r.observation_window||"no indicada")+'</p><p style="margin-top:5px;color:var(--cyan)">'+esc(r.source_url||"")+'</p></div>').join("");}
document.getElementById("search").addEventListener("input",()=>{renderCards();});document.getElementById("scope").addEventListener("change",renderCards);document.getElementById("kind").addEventListener("change",renderCards);document.getElementById("entity-select").addEventListener("change",e=>{state.id=e.target.value;renderCards();renderDetail();});
renderStats();renderFilters();state.id=DATA.entities.slice().sort((a,b)=>(summary(b).observation_count||0)-(summary(a).observation_count||0))[0].id;renderCards();renderDetail();renderReagents();
</script>
</body>
</html>'''


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(DB_PATH)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        ensure_schema(connection)
        run_id = datetime.now(timezone.utc).strftime("rd-drug-correlation-%Y%m%d-%H%M%S")
        connection.execute("INSERT INTO rd_drug_correlation_run VALUES(?,?,?,?)", (run_id, datetime.now(timezone.utc).isoformat(), "running", "Visual + reagent/colorimetry + 2025 observations"))
        assets = build_assets(connection)
        link_visuals(connection, assets)
        build_drug_reagent_map(connection)
        build_test_color_layer(connection)
        build_test_summaries(connection)
        connection.execute("UPDATE rd_drug_correlation_run SET status='completed' WHERE run_id=?", (run_id,))
        connection.commit()
        payload = load_html_payload(connection)
    finally:
        connection.close()
    embedded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    embedded = embedded.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    HTML_PATH.write_text(HTML_TEMPLATE.replace("__PAYLOAD__", embedded), encoding="utf-8")
    check = sqlite3.connect(DB_PATH)
    result = check.execute("PRAGMA integrity_check").fetchone()[0]
    foreign = check.execute("PRAGMA foreign_key_check").fetchall()
    counts = {name: check.execute("SELECT COUNT(*) FROM " + name).fetchone()[0] for name in ["rd_visual_asset","rd_visual_entity_link","rd_drug_reagent_map","rd_test_observed_color","rd_drug_test_summary","rd_drug_reagent_test_summary"]}
    check.close()
    print(json.dumps({"database": str(DB_PATH), "html": str(HTML_PATH), "html_bytes": HTML_PATH.stat().st_size, "integrity_check": result, "foreign_key_violations": len(foreign), "counts": counts, "stats": payload["stats"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
