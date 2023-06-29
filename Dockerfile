FROM python
WORKDIR /music_bot
COPY . /music_bot
RUN pip install discord youtube_dl
EXPOSE 8000
CMD ["python3", "run.py"]