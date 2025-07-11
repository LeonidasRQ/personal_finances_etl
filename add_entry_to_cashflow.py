from openpyxl import load_workbook
from openpyxl.utils import range_boundaries
from copy import copy

# ----------------------
# CONFIG
# ----------------------
excel_file = "copia_finanzas.xlsx"
sheet_name = "cashflow"
table_name = "flujo_dinero"

# ----------------------
# DATOS NUEVA FILA
# ----------------------
tipo_flujo = 'Egreso'   # o 'Egreso'
categoria = 'Necesidades'
subcategoria = 'Mascotas'
descripcion = 'Python Job'
monto = 1500
fecha = '10/07/2025'

# ----------------------
# Ajustar monto según tipo
# ----------------------
if tipo_flujo == 'Ingreso':
    egreso = ''
    ingreso = monto
elif tipo_flujo == 'Egreso':
    egreso = monto
    ingreso = ''
else:
    raise ValueError("⚠ Tipo de Flujo debe ser 'Ingreso' o 'Egreso'.")

# ----------------------
# NUEVA FILA A INSERTAR
# ----------------------
new_row_data = [
    fecha,
    tipo_flujo,
    categoria,
    subcategoria,
    descripcion,
    egreso,
    ingreso
]

# ----------------------
# CARGAR ARCHIVO Y HOJA
# ----------------------
wb = load_workbook(excel_file)
ws = wb[sheet_name]

# ----------------------
# ENCONTRAR LA TABLA
# ----------------------
table = ws.tables[table_name]

# Obtener límites del rango actual
min_col, min_row, max_col, max_row = range_boundaries(table.ref)

# ----------------------
# INSERTAR NUEVA FILA
# ----------------------
next_row = max_row + 1

for idx, value in enumerate(new_row_data, start=min_col):
    ws.cell(row=next_row, column=idx, value=value)

# ----------------------
# COPIAR ESTILO DE LA FILA ANTERIOR
# ----------------------
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

# ----------------------
# COPIAR FÓRMULA DE BALANCE
# (última columna)
# ----------------------
balance_col = max_col
source_balance_cell = ws.cell(row=max_row, column=balance_col)
target_balance_cell = ws.cell(row=next_row, column=balance_col)

if source_balance_cell.data_type == 'f':  # si tiene fórmula
    target_balance_cell.value = source_balance_cell.value.replace(str(max_row), str(next_row))
else:
    # si es valor directo o sin fórmula, simplemente copia el valor
    target_balance_cell.value = source_balance_cell.value

# Copiar el estilo igual por si acaso
target_balance_cell.font = copy(source_balance_cell.font)
target_balance_cell.border = copy(source_balance_cell.border)
target_balance_cell.fill = copy(source_balance_cell.fill)
target_balance_cell.number_format = copy(source_balance_cell.number_format)
target_balance_cell.protection = copy(source_balance_cell.protection)
target_balance_cell.alignment = copy(source_balance_cell.alignment)

# ----------------------
# COPIAR VALIDACIONES DE DATOS
# ----------------------
for dv in ws.data_validations.dataValidation:
    new_sqref = []
    for sq in dv.sqref:
        minc, minr, maxc, maxr = range_boundaries(str(sq))
        # Si la fila anterior estaba en el rango, extendemos para incluir la nueva
        if min_row <= max_row <= maxr:
            new_sqref.append(f"{ws.cell(row=minr, column=minc).coordinate}:{ws.cell(row=maxr+1, column=maxc).coordinate}")
        else:
            new_sqref.append(str(sq))
    dv.sqref = ' '.join(new_sqref)

# ----------------------
# ACTUALIZAR EL RANGO DE LA TABLA
# ----------------------
table.ref = f"{ws.cell(row=min_row, column=min_col).coordinate}:{ws.cell(row=next_row, column=max_col).coordinate}"

# ----------------------
# GUARDAR ARCHIVO
# ----------------------
wb.save(excel_file)

print("✅ Fila agregada exitosamente y tabla actualizada.")
