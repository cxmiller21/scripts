from subprocess import call

channel_name = 'GodsConnect'
youtube_link = f'https://www.youtube.com/user/{channel_name}'

archive_cmd = f'youtube-dl -i {youtube_link}'.split(' ')
print(archive_cmd)
call(archive_cmd)
