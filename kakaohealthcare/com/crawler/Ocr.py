import os
from idlelib.browser import file_open

from google.cloud import vision
from pdf2image import convert_from_path
import io


class Ocr(object):
    def __init__(self):
        pass

    def ocr_pdf_images(self, paths):
        for path in paths:
            self.detect_text(path)


    def detect_text(self, image_path):
        """
            이미지 텍스트 변환
        """
        # Google Cloud Vision 클라이언트 초기화
        client = vision.ImageAnnotatorClient()
        # 이미지 파일 읽기
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        # Vision API에 전달할 이미지 객체 생성
        image = vision.Image(content=content)

        # 텍스트 감지 요청
        response = client.text_detection(image=image)
        texts = response.text_annotations


        # 감지된 텍스트 출력
        if texts:
            # 첫 번째 어노테이션은 전체 텍스트를 포함
            print(f"--- OCR 결과 ({image_path}) ---")
            print(texts[0].description)
            print("\n")

            ground_truth = self.file_read_to_text(file_path = "/Users/yohan.an/git/crawling/web-data-crawler/web-crawler-nhis/text/original_sample.txt")
            accuracy = self.calculate_accuracy(ground_truth, texts[0].description)

            # 개별 텍스트 블록 출력
            # print('\n개별 텍스트 블록:')
            # for text in texts[1:]:
            #     print(f'텍스트: {text.description}')
            #     # 텍스트의 경계 상자 좌표 출력
            #     vertices = (['({},{})'.format(vertex.x, vertex.y)
            #                  for vertex in text.bounding_poly.vertices])
            #     print('경계 상자:', ','.join(vertices))

        # 오류 처리
        if response.error.message:
            raise Exception('{}\nFor more info on error messages, check: ''https://cloud.google.com/apis/design/errors'.format(response.error.message))

    def pdf_to_images(self, pdf_path, output_folder='pdf_images'):
        """PDF 파일을 이미지로 변환"""
        # 출력 폴더 생성
        os.makedirs(output_folder, exist_ok=True)

        # PDF를 이미지로 변환
        images = convert_from_path(pdf_path)

        image_paths = []
        for i, image in enumerate(images):
            # 각 페이지를 이미지 파일로 저장
            image_path = os.path.join(output_folder, f'page_{i + 1}.jpg')
            image.save(image_path, 'JPEG')
            image_paths.append(image_path)

        return image_paths


    def calculate_accuracy(self, ground_truth, ocr_result):
        from difflib import SequenceMatcher

        matcher = SequenceMatcher(None, ground_truth, ocr_result)
        accuracy = matcher.ratio() * 100

        print(f"OCR 정확도: {accuracy:.2f}%")



    def file_read_to_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        return content


def main():
    # PDF 파일 경로 설정
    pdf_path_file = '/Users/yohan.an/git/crawling/web-data-crawler/web-crawler-nhis/pdf/3-20241211134336726.pdf'

    # 디버깅: 파일 존재 여부 확인
    print("PDF 파일 존재 여부:", os.path.exists(pdf_path_file))
    print("PDF 파일 경로:", os.path.abspath(pdf_path_file))

    # 구글 클라우드 인증 설정
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/yohan.an/Downloads/gcp-key/dev-dfd-393200-2e2f5ae038e5.json'

    ocr = Ocr()

    # 디버깅: 예외 처리
    try:
        # OCR 함수 호출
        image_paths = ocr.pdf_to_images(pdf_path_file, "/Users/yohan.an/git/crawling/web-data-crawler/web-crawler-nhis/images")
        if image_paths:
            #ocr.detect_text(image_paths[0])
            ocr.ocr_pdf_images(image_paths)
    except Exception as e:
        print("오류 발생:", str(e))
        import traceback
        traceback.print_exc()






if __name__ == '__main__':
    main()