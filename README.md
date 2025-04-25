> videos 폴더의 동영상을 읽고, 모든 동영상의 러닝 타임을 추출하여 xlxs 파일로 기록한다

예시
```
제목 | 러닝타임(분)
--- | ---
video1 | 20
video2 | 60
```

## 사용 방법

### 1. CLI 버전 

1. 필수 라이브러리 설치:
```
pip install -r requirements.txt
```

2. videos 폴더에 동영상 파일을 업로드합니다.

3. 스크립트 실행:
```
python calc_video_running_time.py
```

4. 실행 후 `video_durations.xlsx` 파일에서 결과를 확인할 수 있습니다.

### 2. GUI 버전

1. 필수 라이브러리 설치:
```
pip install -r requirements.txt
```

2. GUI 프로그램 실행:
```
python video_duration_gui.py
```

3. 사용 방법:
   - [파일 추가] 버튼을 클릭하여 동영상 파일을 선택합니다 (여러 파일 선택 가능)
   - 선택한 동영상의 러닝타임이 자동으로 계산되어 테이블에 표시됩니다
   - [xlsx 저장] 버튼을 클릭하여 결과를 엑셀 파일로 저장할 수 있습니다

### 3. 실행 파일 생성 방법

1. 필요한 라이브러리 설치:
```
pip install -r requirements.txt
```

2. 실행 파일 빌드 스크립트 실행:
```
python build_executable.py
```

3. 빌드가 완료되면 `dist` 폴더에 실행 파일이 생성됩니다:
   - Windows: `동영상러닝타임계산기.exe`
   - macOS: `동영상러닝타임계산기.app`
   - Linux: `동영상러닝타임계산기`

## 지원하는 비디오 형식
- MP4, AVI, MOV, MKV, WMV, FLV

