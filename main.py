import googleapiclient.discovery
import pytube
import os
from required_var import YPD_API_KEY, YPD_PLAYLIST_ID

API_KEY = YPD_API_KEY
PLAYLIST_ID = YPD_PLAYLIST_ID

def get_playlist(playlist_id):
    """Returns 'videos' list of all video IDs in the playlist passed to this function."""

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=100
    )

    response = request.execute()
    videos = []

    while request is not None:
        response = request.execute()
        
        for item in response["items"]:
            videos.append(item["snippet"]["resourceId"]["videoId"])
        
        request = youtube.playlistItems().list_next(request, response)

    return videos

    
def download_videos(video_ids):
    """Iterate over video IDs and downloads the video with that ID from youtube."""
    
    for video_id in video_ids:
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            yt = pytube.YouTube(url)
            stream = yt.streams.filter(progressive=True,
                                       file_extension="mp4").order_by("resolution").desc().first()
            stream.download(output_path=r'C:\YT Playlist')
            print(f"Downloaded: {yt.title}")

        except Exception as e:
            print(f"Failed to download {video_id}: {e}")


video_ids = get_playlist(PLAYLIST_ID)
download_videos(video_ids)
