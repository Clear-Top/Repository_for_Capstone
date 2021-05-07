from openpyxl import Workbook


def write_excel():
    print('실행')
    write_wb = Workbook()

    # 이름이 있는 시트를 생성
    #write_ws = write_wb.create_sheet('생성시트')

    # Sheet1에다 입력
    write_ws = write_wb.active
    write_ws['B1'] = '번호판'
    write_ws['C1'] = '위치'
    write_ws['D1'] = '날짜/시각'
    write_ws['E1'] = '사진경로'
    write_ws['F1'] = '사진이름'
    write_ws['G1'] = '위도'
    write_ws['H1'] = '경도'

    # 행 단위로 추가
    write_ws.append([1, 2, 3])

    # 셀 단위로 추가
    write_wb.save('Excel/test2.xlsx')


write_excel()
