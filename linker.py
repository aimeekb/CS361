import googleapiclient.discovery
import googleapiclient.errors

def youtubeLinker():
    print("YouTube Linker running...")

    videoFunction = open('link-service.txt', 'r+')
    input = videoFunction.readline()
    keywords = input[11: len(input) - 1]
    videoFunction.close()

    print("Keywords found...")

    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyBIiBqvVNia6aUYOhWb9wkvrI5H36UzQNw"
    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        q=keywords,
           maxResults=5
        )
    response = request.execute()
    video = response['items'][0]
    videoID = video['id']['videoId']

    ytLink = "https://www.youtube.com/watch?v=" + videoID

    videoFunction = open('link-service.txt', 'r+')
    videoFunction.seek(0)
    videoFunction.truncate()
    videoFunction.write(ytLink + "\n")
    videoFunction.close()

    return
