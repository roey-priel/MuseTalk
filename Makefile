install:
	@pip install -r requirements.txt
	@pip install --no-cache-dir -U openmim 
	@mim install mmengine
	@mim install "mmcv==2.1.0" 
	@mim install "mmdet>=3.1.0" 
	@mim install "mmpose>=1.1.0" 

ffmpeg-install:
	@wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
	@tar -xvf ffmpeg-git-amd64-static.tar.xz
	@rm ffmpeg-git-amd64-static.tar.xz
	@export FFMPEG_PATH=./ffmpeg-git-20240629-amd64-static/

docker-build:
	@docker build -t rpazpri1/musetalk:latest .

docker-run:
	@docker run --gpus all -p 8080:8080 -v /home/ubuntu/github/MuseTalk/models:/workspace/models rpazpri1/musetalk:latest python3 app.py
