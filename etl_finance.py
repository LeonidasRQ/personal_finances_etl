import argparse
import datetime
import json
import logging
import os
from openpyxl import load_workbook
from openpyxl.utils import range_boundaries
from copy import copy

# ----------------------
# LOGGING SETUP
# ----------------------
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "etl.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# ----------------------
# CONFIG LOADER
# ----------------------
def load_mapping_config(config_path):
    """Load category mapping from JSON config file."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            mapping = json.load(f)
        logger.info(f"Loaded category mapping from {config_path}")
        return mapping["category_to_subcategory"], mapping["subcategory_to_category"]
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise SystemExit(1)

# ----------------------
# SOURCE DATA LOADER
# ----------------------
def extract_source_data(source_file, source_sheet, category_to_subcategory, subcategory_to_category):
    """Extract and map data from source Excel."""
    try:
        wb = load_workbook(source_file)
        ws = wb[source_sheet]
        logger.info(f"Loaded source file: {source_file}")
    except Exception as e:
        logger.error(f"Failed to load source Excel: {e}")
        raise SystemExit(1)

    entries = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        date, description, value, category_origin = row[0], row[1], row[2], row[5]
        if date is None or value is None:
            continue

        subcategoria = category_to_subcategory.get(category_origin, "Otro")
        if subcategoria == "Otro":
            logger.warning(f"Unknown origin category '{category_origin}', using 'Otro'")

        categoria_base = subcategory_to_category.get(subcategoria, "Ingreso")
        tipo_flujo = "Ingreso" if categoria_base == "Ingreso" else "Egreso"
        monto = abs(value)

        if tipo_flujo == "Ingreso":
            categoria = subcategoria
            subcategoria_final = ""
        else:
            categoria = categoria_base
            subcategoria_final = subcategoria

        entries.append({
            "fecha": date.strftime("%Y-%m-%d") if isinstance(date, datetime.datetime) else date,
            "tipo_flujo": tipo_flujo,
            "categoria": categoria,
            "subcategoria": subcategoria_final,
            "descripcion": description or "",
            "monto": monto
        })

    entries.sort(key=lambda x: x["fecha"])
    logger.info(f"{len(entries)} records loaded and mapped from {source_file}")
    return entries

# ----------------------
# DEST FILE LOADER
# ----------------------
def load_destination(dest_file, dest_sheet, table_name):
    """Load destination workbook, worksheet and table boundaries."""
    try:
        wb = load_workbook(dest_file)
        ws = wb[dest_sheet]
        table = ws.tables[table_name]
        min_col, min_row, max_col, max_row = range_boundaries(table.ref)
        logger.info(f"Loaded destination workbook {dest_file}, table {table_name}")
        return wb, ws, table, min_col, min_row, max_col, max_row
    except Exception as e:
        logger.error(f"Failed to load destination workbook: {e}")
        raise SystemExit(1)

# ----------------------
# EXTEND VALIDATIONS
# ----------------------
def extend_validations(ws, min_row, max_row_before, max_row_after):
    for dv in ws.data_validations.dataValidation:
        new_sqref = []
        for sq in dv.sqref:
            minc, minr, maxc, maxr = range_boundaries(str(sq))
            if min_row <= max_row_before <= maxr:
                new_sqref.append(f"{ws.cell(row=minr, column=minc).coordinate}:{ws.cell(row=max_row_after, column=maxc).coordinate}")
            else:
                new_sqref.append(str(sq))
        dv.sqref = ' '.join(new_sqref)

# ----------------------
# INSERT TRANSFORMED DATA
# ----------------------
def insert_entries(ws, table, entries, min_col, min_row, max_col, max_row):
    for entry in entries:
        tipo_flujo = entry["tipo_flujo"]
        monto = entry["monto"]

        fecha_str = entry["fecha"]
        fecha = datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()

        egreso, ingreso = ('', monto) if tipo_flujo == "Ingreso" else (monto, '')

        new_row_data = [
            fecha,
            tipo_flujo,
            entry["categoria"],
            entry["subcategoria"],
            entry["descripcion"],
            egreso,
            ingreso
        ]

        next_row = max_row + 1

        # Insert values
        for idx, value in enumerate(new_row_data, start=min_col):
            ws.cell(row=next_row, column=idx, value=value)

        # Copy styles
        for idx in range(min_col, max_col + 1):
            source_cell = ws.cell(row=max_row, column=idx)
            target_cell = ws.cell(row=next_row, column=idx)
            if source_cell.has_style:
                target_cell.font = copy(source_cell.font)
                target_cell.border = copy(source_cell.border)
                target_cell.fill = copy(source_cell.fill)
                target_cell.number_format = copy(source_cell.number_format)
                target_cell.protection = copy(source_cell.protection)
                target_cell.alignment = copy(source_cell.alignment)

        # Copy balance formula
        balance_col = max_col
        source_balance_cell = ws.cell(row=max_row, column=balance_col)
        target_balance_cell = ws.cell(row=next_row, column=balance_col)
        if source_balance_cell.data_type == 'f':
            target_balance_cell.value = source_balance_cell.value.replace(str(max_row), str(next_row))
        else:
            target_balance_cell.value = source_balance_cell.value

        target_balance_cell.font = copy(source_balance_cell.font)
        target_balance_cell.border = copy(source_balance_cell.border)
        target_balance_cell.fill = copy(source_balance_cell.fill)
        target_balance_cell.number_format = copy(source_balance_cell.number_format)
        target_balance_cell.protection = copy(source_balance_cell.protection)
        target_balance_cell.alignment = copy(source_balance_cell.alignment)

        max_row = next_row

    extend_validations(ws, min_row, max_row - len(entries), max_row)
    table.ref = f"{ws.cell(row=min_row, column=min_col).coordinate}:{ws.cell(row=max_row, column=max_col).coordinate}"
    return max_row

# ----------------------
# MAIN
# ----------------------
def main():
    parser = argparse.ArgumentParser(description="ETL script to import and map Excel financial transactions.")
    parser.add_argument("--source", default="data/mobills_transactions.xlsx", help="Source Excel file")
    parser.add_argument("--dest", default="data/copia_finanzas.xlsx", help="Destination Excel file")
    parser.add_argument("--config", default="config/category_mapping.json", help="JSON config file with category mappings")
    args = parser.parse_args()

    category_to_subcategory, subcategory_to_category = load_mapping_config(args.config)
    entries = extract_source_data(args.source, "Receitas e Despesas", category_to_subcategory, subcategory_to_category)
    wb, ws, table, min_col, min_row, max_col, max_row = load_destination(args.dest, "cashflow", "flujo_dinero")
    max_row = insert_entries(ws, table, entries, min_col, min_row, max_col, max_row)
    wb.save(args.dest)
    logger.info(f"Inserted {len(entries)} rows into {args.dest}")

# ----------------------
# ENTRY POINT
# ----------------------
if __name__ == "__main__":
    main()
