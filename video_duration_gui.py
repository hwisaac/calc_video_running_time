import os
import sys
import cv2
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFileDialog,
    QHeaderView,
    QMessageBox,
    QProgressBar,
    QLabel,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class VideoProcessor(QThread):
    """비디오 처리를 위한 스레드 클래스"""
    progress_updated = pyqtSignal(int)
    video_processed = pyqtSignal(str, float)
    processing_finished = pyqtSignal()

    def __init__(self, video_paths):
        super().__init__()
        self.video_paths = video_paths

    def run(self):
        """비디오 처리 실행"""
        for i, video_path in enumerate(self.video_paths):
            # 진행률 업데이트
            progress = int((i / len(self.video_paths)) * 100)
            self.progress_updated.emit(progress)

            # 비디오 길이 계산
            duration = self.get_video_duration(video_path)

            # 파일명만 추출
            file_name = os.path.basename(video_path)

            # 결과 전송
            self.video_processed.emit(file_name, duration)

        # 완료 신호 전송
        self.progress_updated.emit(100)
        self.processing_finished.emit()

    def get_video_duration(self, video_path):
        """비디오 파일의 러닝타임을 분 단위로 반환"""
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
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


class VideoDurationGUI(QMainWindow):
    """동영상 러닝타임 계산 GUI"""

    def __init__(self):
        super().__init__()

        self.video_data = []  # 비디오 데이터 저장 리스트

        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        # 윈도우 설정
        self.setWindowTitle('동영상 러닝타임 계산기')
        self.setGeometry(100, 100, 600, 400)

        # 메인 위젯과 레이아웃
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # 버튼 레이아웃
        button_layout = QHBoxLayout()

        # 파일 추가 버튼
        self.add_button = QPushButton('파일 추가')
        self.add_button.clicked.connect(self.add_videos)
        button_layout.addWidget(self.add_button)

        # 엑셀 저장 버튼
        self.save_button = QPushButton('xlsx 저장')
        self.save_button.clicked.connect(self.save_to_excel)
        button_layout.addWidget(self.save_button)

        # 테이블 위젯 (동영상 목록과 러닝타임 표시)
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['파일명', '러닝타임(분)'])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        # 상태 표시 레이블
        self.status_label = QLabel('준비됨')

        # 진행 표시줄
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        # 레이아웃에 위젯 추가
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.status_label)

        # 메인 위젯 설정
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def add_videos(self):
        """동영상 파일 추가"""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("동영상 파일 (*.mp4 *.avi *.mov *.mkv *.wmv *.flv)")

        if file_dialog.exec_():
            # 선택한 파일 경로
            file_paths = file_dialog.selectedFiles()

            if not file_paths:
                return

            # 진행 표시줄 표시
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.status_label.setText('비디오 처리 중...')
            self.add_button.setEnabled(False)
            self.save_button.setEnabled(False)

            # 비디오 처리 스레드 시작
            self.video_processor = VideoProcessor(file_paths)
            self.video_processor.progress_updated.connect(self.update_progress)
            self.video_processor.video_processed.connect(self.add_video_to_table)
            self.video_processor.processing_finished.connect(self.processing_finished)
            self.video_processor.start()

    def update_progress(self, value):
        """진행률 업데이트"""
        self.progress_bar.setValue(value)

    def add_video_to_table(self, file_name, duration):
        """테이블에 비디오 정보 추가"""
        # 비디오 데이터 저장
        self.video_data.append({
            "제목": file_name,
            "러닝타임(분)": duration
        })

        # 테이블에 행 추가
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # 테이블에 데이터 추가
        self.table.setItem(row_position, 0, QTableWidgetItem(file_name))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(duration)))

    def processing_finished(self):
        """비디오 처리 완료"""
        self.progress_bar.setVisible(False)
        self.status_label.setText(f'준비됨 (총 {len(self.video_data)}개 비디오)')
        self.add_button.setEnabled(True)
        self.save_button.setEnabled(True)

    def save_to_excel(self):
        """비디오 정보를 엑셀 파일로 저장"""
        if not self.video_data:
            QMessageBox.warning(self, '알림', '저장할 비디오 정보가 없습니다.')
            return

        # 저장 경로 선택
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Excel 파일 저장', '', 'Excel 파일 (*.xlsx)')

        if not file_path:
            return

        # 파일 확장자 확인 및 추가
        if not file_path.endswith('.xlsx'):
            file_path += '.xlsx'

        try:
            # 데이터프레임 생성 및 저장
            df = pd.DataFrame(self.video_data)
            df.to_excel(file_path, index=False)

            QMessageBox.information(self, '완료', f'파일이 성공적으로 저장되었습니다:\n{file_path}')
        except Exception as e:
            QMessageBox.critical(self, '오류', f'파일 저장 중 오류 발생:\n{str(e)}')


def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    window = VideoDurationGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
