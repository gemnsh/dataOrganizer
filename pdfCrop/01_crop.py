import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
# 여백을 제거하는 함수
def remove_top_bottom_padding(image):
    # 이미지의 알파 채널을 고려하여 배경 색상(흰색 또는 투명)을 기준으로 여백을 자릅니다.
    image = image.convert("RGBA")  # RGBA 모드로 변환하여 알파 채널을 처리합니다.
    
    # 이미지의 픽셀 데이터를 가져옴
    pixels = image.load()

    # 배경 색상 정의 (투명하거나 흰색일 수 있음)
    background_color = (255, 255, 255, 255)  # (R, G, B, A)로 설정. 흰색으로 설정

    # 상단 여백 찾기 (첫 번째 행에서 여백을 찾음)
    top = 0
    while top < image.height and all(pixels[x, top] == background_color for x in range(image.width)):
        top += 1

    # 하단 여백 찾기 (마지막 행에서 여백을 찾음)
    bottom = image.height - 1
    while bottom > top and all(pixels[x, bottom] == background_color for x in range(image.width)):
        bottom -= 1

    # 이미지를 자름 (상단과 하단 여백을 제외)
    image_cropped = image.crop((0, top-10, image.width, bottom + 11))

    return image_cropped

# 특정 폴더 내의 모든 이미지 파일 처리
def process_images_in_folder(folder_path):
    # 폴더 내의 모든 파일을 탐색
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # PNG, JPEG, JPG 파일만 처리
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            print(f"Processing {filename}...")

            try:
                # 이미지 열기
                image = Image.open(file_path)
                # 여백 제거 함수 호출
                image_cropped = remove_top_bottom_padding(image)
                # 여백이 제거된 이미지를 새로운 파일로 저장
                new_file_path = os.path.join('./cropped/', f"cropped_300_{filename}")
                image_cropped.save(new_file_path)
                print(f"Saved cropped image as {new_file_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# 실행 예시
folder_path = './png/'  # 여기에 폴더 경로를 입력하세요
process_images_in_folder(folder_path)
