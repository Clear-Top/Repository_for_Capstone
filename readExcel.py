from openpyxl import load_workbook
from openpyxl import Workbook
import writeExcel


def read_excel():

    # data_only=Ture로 해줘야 수식이 아닌 값으로 받아온다.
    load_wb = load_workbook("Excel/test2.xlsx", data_only=True)
    # 시트 이름으로 불러오기
    load_ws = load_wb['Sheet']

    for i in range(1, load_ws.max_row+1):
        print("\n")
        print("Row", i, "data:")
        for j in range(1, load_ws.max_column+1):
            cell_obj = load_ws.cell(row=i, column=j)
            print(cell_obj.value, end=" ")
