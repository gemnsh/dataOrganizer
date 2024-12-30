import tkinter as tk
from tkinter import messagebox
import fitz  # PyMuPDF
import pygame
from PIL import Image, ImageTk

class PDFClassifierApp:
    def __init__(self, root, pdf_path, output_file):
        self.root = root
        self.root.title("PDF 페이지 분류기")

        # PDF 파일 열기
        self.doc = fitz.open(pdf_path)
        self.page_count = self.doc.page_count
        self.output_file = output_file

        self.current_page = 0
        self.classifications = {}

        # Pygame 초기화
        pygame.init()
        
        # Tkinter 캔버스 생성 (이미지를 표시할 공간)
        self.canvas = tk.Canvas(self.root, width=850, height=1050)
        self.canvas.pack(side=tk.LEFT)

        # 버튼 프레임 생성
        self.button_frame = tk.Frame(self.root)
        self.button_frame.place(x=750, y=10)

        # 분류 버튼 생성
        self.buttons = {
            '이미지아님': tk.Button(self.button_frame, text='이미지아님', command=lambda: self.classify('이미지아님')),
            '흑백이미지': tk.Button(self.button_frame, text='흑백이미지', command=lambda: self.classify('흑백이미지')),
            '컬러이미지': tk.Button(self.button_frame, text='컬러이미지', command=lambda: self.classify('컬러이미지')),

        }

        # 버튼을 화면에 배치
        for button in self.buttons.values():
            button.pack(side=tk.TOP, padx=10)

        # 첫 페이지 표시
        self.show_page(self.current_page)

    def show_page(self, page_num):
        """페이지를 이미지로 표시"""
        page = self.doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))  # 2배 확대하여 해상도 향상
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        img = img.resize((750, 1050), Image.ANTIALIAS)  # 이미지 크기 조정

        # Tkinter에서 사용할 수 있는 이미지 포맷으로 변환
        img_tk = ImageTk.PhotoImage(img)

        # 이미지를 캔버스에 표시
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk  # 이미지 객체를 유지하여 가비지 컬렉션 방지

    def classify(self, classification):
        """클릭된 버튼에 대해 분류를 기록"""
        self.classifications[self.current_page + 1] = classification
        print(f"페이지 {self.current_page + 1} 분류: {classification}")
        if self.current_page < self.page_count - 1:
            self.current_page += 1
            self.show_page(self.current_page)
        else:
            messagebox.showinfo("완료", "모든 페이지 분류가 완료되었습니다.")
            self.save_classifications()


    def save_classifications(self):
        """분류 결과를 파일에 저장"""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for page_num, classification in self.classifications.items():
                f.write(f"페이지 {page_num-15}: {classification}\n")
        print(f"결과가 '{self.output_file}'에 저장되었습니다.")

# 실행 부분
if __name__ == "__main__":
    # Tkinter 루트 윈도우 생성
    root = tk.Tk()

    # PDF 파일 경로와 출력 파일 경로 지정
    pdf_path = "example.pdf"
    output_file = "output.txt"

    # PDF 분류기 앱 실행
    app = PDFClassifierApp(root, pdf_path, output_file)

    # Tkinter 이벤트 루프 시작
    root.mainloop()
