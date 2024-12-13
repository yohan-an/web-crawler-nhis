import os
from google.cloud import vision
from pdf2image import convert_from_path
import io


class Ocr(object):
    def __init__(self):
        pass

    def detect_text(self, path):
        """Detects text in the file."""
        # Google Cloud Vision 클라이언트 초기화
        client = vision.ImageAnnotatorClient()

        # 이미지 파일 읽기
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        # Vision API에 전달할 이미지 객체 생성
        image = vision.Image(content=content)

        # 텍스트 감지 요청
        response = client.text_detection(image=image)
        texts = response.text_annotations


        # 감지된 텍스트 출력
        if texts:
            # 첫 번째 어노테이션은 전체 텍스트를 포함
            print('전체 텍스트:')
            print(texts[0].description)

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
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

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
        image_paths = ocr.pdf_to_images(pdf_path_file)
        if image_paths:
            ocr.detect_text(image_paths[0])
    except Exception as e:
        print("오류 발생:", str(e))
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()