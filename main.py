import googleapiclient.discovery
import pytube
import os
import csv
from required_var import YPD_API_KEY, YPD_PLAYLIST_ID


API_KEY = YPD_API_KEY
PLAYLIST_ID = YPD_PLAYLIST_ID

def get_playlist(playlist_id):
    """Returns 'videos' list of all video IDs in the playlist passed to this function."""

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    # Gets list of videos and their properties in the playlist
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=100
    )

    response = request.execute()
    videos = []

    while request is not None:
        response = request.execute()
        
        # Extracts video ID and appends it the the list to use in the download request
        for item in response["items"]:
            videos.append(item["snippet"]["resourceId"]["videoId"])
        
        request = youtube.playlistItems().list_next(request, response)

    return videos

    
def download_videos(video_ids):
    """Iterate over video IDs and downloads the video with that ID from youtube."""

    ids = []

    log_path = './logs'
    log_file = './logs/log.csv'

    # Creates log path and file if none exist
    if not os.path.exists(log_path):
        os.mkdir(log_path)
        with open(log_file, 'w', newline='') as file:
            pass
    with open(log_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            ids.append(row)

    videos_to_append = []

    for video_id in video_ids:
        try:

            # Checks if video ID is in the log file and downloads the video if it is not
            if [video_id] in ids:
                print('Video already downloaded')

            else:
                url = f"https://www.youtube.com/watch?v={video_id}"
                yt = pytube.YouTube(url)
                stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
                stream.download(output_path=r'C:\YT Playlist')
                print(f"Downloaded: {yt.title}")
                videos_to_append.append([video_id])

        except Exception as e:
            print(f"Failed to download {video_id}: {e}")

    # Logs the videos downloaded
    with open(log_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(videos_to_append)

video_ids = get_playlist(PLAYLIST_ID)

# Downloads all videos from a public YouTube Playlist
if __name__ == "__main__":
    download_videos(video_ids)


