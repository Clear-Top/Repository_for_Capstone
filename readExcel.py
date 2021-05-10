from openpyxl import load_workbook
from openpyxl import Workbook


def read_excel(i,j):

    # data_only=Ture로 해줘야 수식이 아닌 값으로 받아온다.
    load_wb = load_workbook("static\excel/test1.xlsx", data_only=True)
    # 시트 이름으로 불러오기
    load_ws = load_wb['Sheet']

    cell_obj = load_ws.cell(row=i, column=j)
    print(cell_obj.value)
    if cell_obj.value != None:
        return cell_obj.value
    else:
        return 0


