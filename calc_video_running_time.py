import os
import cv2
import pandas as pd
from tqdm import tqdm

def get_video_duration(video_path):
    """비디오 파일의 러닝타임을 분 단위로 반환합니다."""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"오류: {video_path} 파일을 열 수 없습니다.")
            return 0
        
        # 프레임 수와 초당 프레임 레이트 가져오기
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # 러닝타임 계산 (초 단위)
        duration_sec = frame_count / fps if fps > 0 else 0
        
        # 분 단위로 변환
        duration_min = duration_sec / 60
        
        cap.release()
        return round(duration_min, 2)  # 소수점 2자리까지 반올림
    except Exception as e:
        print(f"오류 발생: {e}")
        return 0

def main():
    # 비디오 폴더 경로
    video_dir = "videos"
    
    # 결과를 저장할 데이터 프레임 초기화
    results = []
    
    # 지원하는 비디오 확장자
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
    
    # 폴더 내 모든 파일 검사
    video_files = [f for f in os.listdir(video_dir) 
                  if os.path.isfile(os.path.join(video_dir, f)) and 
                  os.path.splitext(f)[1].lower() in video_extensions]
    
    print(f"총 {len(video_files)}개의 비디오 파일을 처리합니다...")
    
    # 각 비디오 파일의 러닝타임 계산
    for video_file in tqdm(video_files):
        video_path = os.path.join(video_dir, video_file)
        duration = get_video_duration(video_path)
        results.append({
            "제목": video_file,
            "러닝타임(분)": duration
        })
    
    # 데이터프레임 생성
    df = pd.DataFrame(results)
    
    # 엑셀 파일로 저장
    output_file = "video_durations.xlsx"
    df.to_excel(output_file, index=False)
    
    print(f"처리 완료! 결과가 {output_file}에 저장되었습니다.")

if __name__ == "__main__":
    main() 