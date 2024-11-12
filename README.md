##### 셀리니움 구글 크롬드라이버
```shell
https://developer.chrome.com/docs/chromedriver/downloads?hl=ko
```

##### requirements 만들기 
```shell
pip freeze > requirements.txt
```

##### 설치 
```shell
# 설치 하기 
pip install -r requirements.txt

# 설치 가능한 패키지만 설치, 오류 패키지 skip
cat requirements.txt | xargs -n 1 pip install
```


##### 히스토그램 설치 
```shell
python -m pip install -U pip
python -m pip install -U matplotlib

```

