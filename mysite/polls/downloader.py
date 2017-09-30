# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import youtube_dl
from django.http import HttpResponse

# 接收请求数据
def search(request):
    request.encoding = 'utf-8'
    downloadUrl=request.GET.get('downloadUrl')
    urls=[downloadUrl]
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
    return HttpResponse(message)
