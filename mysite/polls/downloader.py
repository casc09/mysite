# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
import youtube_dl
import json

# take the request
def search(request):
    request.encoding = 'utf-8'
    downloadUrl = request.GET.get('downloadUrl')

    #get video urls
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

    with ydl:
        result = ydl.extract_info(
            downloadUrl,
            # 'https://www.youtube.com/watch?v=-StEklVt4Tk',
            # 'https://www.bilibili.com/video/av15624251/',
            download=False  # We just want to extract the info
        )

    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just a video
        video = result

    #deal with the data returned by youtube-dl
    # print(video)
    audiosAndVideos = video['formats']
    audios = []
    videosSmall = []
    videosMedium = []
    videosHd720 = []
    for mat in audiosAndVideos:
        if mat.has_key('format_note'):
            if mat['format_note'] == 'DASH audio':
                audios.append(mat)
            if mat['format_note'] == 'small':
                videosSmall.append(mat)
            if mat['format_note'] == 'medium':
                videosMedium.append(mat)
            if mat['format_note'] == 'hd720':
                videosHd720.append(mat)
        else:
            return
    # response object
    resp = {}

    if len(audiosAndVideos) > 0 :
        resp['success']='yes'
        resp['thumbnail']=video['thumbnail']
        resp['title']=video['title']
        resp['description']=video['description']
        resp['duration']=video['duration']
    else:
        resp['success'] = 'no'
        
    resp['audios']=audios
    resp['videosSmall']=videosSmall
    resp['videosMedium']=videosMedium
    resp['videoHd720']=videosHd720

    response=HttpResponse(json.dumps(resp), content_type="application/json")
     # allow CORS
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    
    return response
    # video_info = videosHd720[0]
    # video_url = video_info['url']
    # video_formate = video_info['ext']
    # print(video_formate)
