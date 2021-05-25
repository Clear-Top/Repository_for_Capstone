from openpyxl import Workbook


def write_excel_prepare():
    print('액셀작성실행')
    write_wb = Workbook()

    # 엑셀작성을 위한 정보 = {'워크시트','활성화키','입력개수'}
    excel = {}
    excel[0] = write_wb
    excel[1] = write_wb.active
    excel[2] = 1
    return excel


def write_excel_init(excel):
    excel[1]['B1'] = '번호판'
    excel[1]['C1'] = '위치'
    excel[1]['D1'] = '날짜/시각'
    excel[1]['E1'] = '사진경로'
    excel[1]['F1'] = '사진이름'
    excel[1]['G1'] = '위도'
    excel[1]['H1'] = '경도'


def write_excel(excel, carnum, gps, date, image_path, image_name, lalo1,lalo2):
    # write_ws = write_wb.active

    # 행 단위로 추가
    excel[1].append([excel[2], carnum, gps, date,
                    image_path, image_name, lalo1,lalo2])

    # 셀 단위로 추가
    excel[0].save('static/excel/download.xlsx')
    excel[2] = excel[2] + 1


# excel = write_excel_prepare()
# write_excel(excel, 1, 2, 3, 'static/upload/', 5, 6)
