from __future__ import unicode_literals
import youtube_dl
import os
import sys
import glob
import random

def music_download(url: str, playlist: str = '다운로드', start: int = None, end: int = None) -> None:
    """
    옵션 설명
    --------
    * `url`: 유튜브 영상 링크.
    * `playlist`: 플레이리스트 이름.

    플레이리스트를 다운로드 하려는 경우
    * `start`: `start`번째 부터 다운로드.
    * `end`: `end`번째 까지 다운로드."""

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': playlist + r'/%(title)s [%(id)s].%(ext)s',
        'writethumbnail': True,
        'nooverwrites': True,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            },
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegMetadata'},
        ]
    }

    if playlist != '다운로드':
        confirm = input(f'플레이리스트 파일을 생성하시겠습니까? (y/N): ')
        if confirm in 'Yy':
            music_lst = []
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                playlist_dict = ydl.extract_info(url, False)
                playlist = playlist_dict['title']
                if sys.platform == 'win32':
                    for video in playlist_dict['entries']:
                        title, id = video.get('title'), video.get('id')
                        title = "".join(i for i in title if i not in '\/:*?"<>|')
                        music_lst.append(f'{playlist}/{title} [{id}].mp3')
                else:
                    for video in playlist_dict['entries']:
                        title, id = video.get('title'), video.get('id')
                        music_lst.append(f'{playlist}/{title} [{id}].mp3')

            with open(f'{playlist}.m3u', 'w', encoding='utf8') as m3u:
                m3u.write('\n'.join(music_lst))
            
            start, end = None, None

    if start:
        ydl_opts['playliststart'] = start
    if end:
        ydl_opts['playlistend'] = end
    
    log = f'{playlist}.log'
    ydl_opts['download_archive'] = log
    mp3_lst = glob.glob(f'{playlist}/*.mp3')
    webm_lst = glob.glob(f'{playlist}/*.webm')
    with open(log, 'w', encoding='utf8') as log_file:
        for music in mp3_lst:
            if music not in webm_lst:
                log_file.write(f'youtube {music[-16:-5]}\n')

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def lst_create(playlist: str) -> None:
    """`download` 함수로 플레이리스트 폴더가 이미 생성되었다면 (즉, 옵션 `playlist = True`였다면),
    이 함수가 실행되는 순간 플레이리스트 `playlist`.m3u 파일이 생성됨.
    
    VLC media player로 플레이 하는 걸 추천."""

    lst = []
    for ext in ('*.mp3', '*.flac', '*.aac'):
        lst.extend(glob.glob(f'{playlist}/{ext}'))
    if lst != []:
        with open(f'{playlist}.m3u', 'w', encoding='utf8') as m3u:
            for music in lst:
                m3u.write(music + '\n')

def lst_suffle(playlist: str) -> None:
    """플레이리스트 셔플 기능. 파일 `playlist`.m3u에 있는 음악들을 랜덤으로 셔플."""

    with open(f'{playlist}.m3u', 'r+', encoding='utf8') as m3u:
        lines = m3u.readlines()
        m3u.seek(0)
        random.shuffle(lines)
        m3u.writelines(lines)
        m3u.truncate()

def lst_order(playlist: str, by: str = 'author') -> None:
    """플레이리스트 정렬 기능.""" # TODO author 순대로 정렬

    with open(f'{playlist}.m3u', 'r+', encoding='utf8') as m3u:
        lines = m3u.readlines()
        m3u.seek(0)
        m3u.writelines(sorted(lines))
        m3u.truncate()

if __name__ == '__main__':
    music_download('https://www.youtube.com/playlist?list=PLL1k3JLqzzPQjXlpuevJFMswY0NjRWdxf', '내가 좋아하는 노래')
