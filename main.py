from services import yt_search, yt_audio_download

def main():
    search = input("What is it that you seek? ")
    instance = yt_search(search)

    yt_audio_download(instance[0]['link'])
    
if __name__ == '__main__':
    main()
 