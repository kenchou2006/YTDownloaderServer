from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from yt_dlp import YoutubeDL
from concurrent.futures import ThreadPoolExecutor
import os
import shutil
import logging

executor = ThreadPoolExecutor(max_workers=None)

HIDE_NULL = True

def ytdownload(request):
    return render(request, 'ytdownload.html', {'video_url': ''})

class VideoDownloadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        video_url = request.data.get('video_url')

        if video_url:
            try:
                video_info = self.get_video_info(video_url)

                if video_info:
                    return Response({'status': 'success', 'video_info': video_info}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'error', 'error_message': 'Failed to fetch video info.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logging.error(f"Error processing video info: {e}")
                return Response({'status': 'error', 'error_message': 'Internal server error.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'status': 'error', 'error_message': 'No video URL provided.'},
                        status=status.HTTP_400_BAD_REQUEST)

    def get_video_info(self, video_url):
        future = executor.submit(self._fetch_video_info, video_url)
        return future.result()

    def _fetch_video_info(self, video_url):
        try:
            ydl_opts = {
                'quiet': False,
                'extract_flat': True,
                'force_generic_extractor': True,
            }
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                video_info = {
                    'video_title': info_dict.get('title'),
                    'views': info_dict.get('view_count'),
                    'publish_date': info_dict.get('upload_date'),
                    'thumbnail_url': info_dict.get('thumbnail'),
                    'streams_info': [
                        {
                            'type': format.get('ext'),
                            'resolution': format.get('height'),
                            'filesize': format.get('filesize') / (1024 * 1024) if format.get('filesize') else None,
                            'url': format.get('url')
                        }
                        for format in info_dict.get('formats', [])
                    ]
                }

                if HIDE_NULL:
                    video_info['streams_info'] = [stream for stream in video_info['streams_info'] if
                                                  stream['filesize'] is not None]

                categorized_streams = {}
                for stream in video_info['streams_info']:
                    stream_type = stream['type']
                    if stream_type not in categorized_streams:
                        categorized_streams[stream_type] = []
                    categorized_streams[stream_type].append(stream)

                for stream_type, streams in categorized_streams.items():
                    streams.sort(key=lambda x: -x['filesize'] if x['filesize'] else float('inf'))
                    streams.sort(key=lambda x: (
                    -x['filesize'] if x['filesize'] else float('inf'), -x['resolution'] if x['resolution'] else 0))

                video_info['streams_info'] = [stream for streams in categorized_streams.values() for stream in streams]

            return video_info
        except Exception as e:
            logging.error(f"Error fetching video info: {e}")
            return None
