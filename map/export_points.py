from openpyxl import load_workbook

from geocode import generate_points_js

if __name__ == "__main__":
    wb = load_workbook("cdek_PVZ.xlsx")
    ws = wb.active
    n = generate_points_js(ws)
    print(f"points.js written with {n} points")
