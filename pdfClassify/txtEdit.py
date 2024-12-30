def classify_pages(input_file, bw_file, color_file):
    # 파일 읽기
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 분류된 데이터 저장
    bw_pages = []
    color_pages = []

    for line in lines:
        # 페이지와 분류 추출
        if line.startswith("페이지"):
            parts = line.strip().split(": ")
            page_number = parts[0].split(" ")[1]
            classification = parts[1]

            if classification == "흑백이미지":
                bw_pages.append(page_number)
            elif classification == "컬러이미지":
                color_pages.append(page_number)

    # 파일에 각각 저장
    with open(bw_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(bw_pages))

    with open(color_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(color_pages))

# 실행 부분
input_file = "output.txt"       # 기존 파일
bw_file = "흑백이미지.txt"       # 흑백이미지 페이지 저장 파일
color_file = "컬러이미지.txt"    # 컬러이미지 페이지 저장 파일

classify_pages(input_file, bw_file, color_file)
