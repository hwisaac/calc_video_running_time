import os
import platform
import subprocess

def build_executable():
    """GUI 프로그램을 실행 파일로 빌드합니다."""
    print("동영상 러닝타임 계산기 GUI를 실행 파일로 빌드합니다...")

    # 운영체제 확인
    system = platform.system()
    icon_param = ""

    # 운영체제별 아이콘 파라미터 설정
    if system == "Windows":
        icon_file = "video_icon.ico"
        if os.path.exists(icon_file):
            icon_param = f"--icon={icon_file}"
    elif system == "Darwin":  # macOS
        icon_file = "video_icon.icns"
        if os.path.exists(icon_file):
            icon_param = f"--icon={icon_file}"

    # PyInstaller 명령어
    command = [
        "pyinstaller",
        "--name=동영상러닝타임계산기",
        "--onefile",
        "--windowed",
        "--clean",
        "--add-data=README.md:.",
    ]

    # 아이콘 파라미터 추가
    if icon_param:
        command.append(icon_param)

    # 메인 스크립트 추가
    command.append("video_duration_gui.py")

    # 명령어 실행
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("빌드 성공!")
        print(f"실행 파일은 dist 폴더에 생성되었습니다.")

        # 실행 파일 경로
        if system == "Windows":
            exe_path = os.path.join("dist", "동영상러닝타임계산기.exe")
        elif system == "Darwin":  # macOS
            exe_path = os.path.join("dist", "동영상러닝타임계산기.app")
        else:  # Linux
            exe_path = os.path.join("dist", "동영상러닝타임계산기")

        print(f"실행 파일 경로: {os.path.abspath(exe_path)}")

    except subprocess.CalledProcessError as e:
        print(f"빌드 중 오류 발생: {e}")
        print(f"오류 메시지: {e.stderr}")

if __name__ == "__main__":
    build_executable()
