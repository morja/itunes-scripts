import tidalapi
import re
import sys, getopt

inputfile = ''

def main(argv):
	global inputfile, username, password
	try:
	  opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
	except getopt.GetoptError:
	  print('script.py -u <username> -p <password> -i <inputfile>')
	  sys.exit(2)
	for opt, arg in opts:
	  if opt == '-h':
	     print('script.py -u <username> -p <password> -i <inputfile>')
	     sys.exit()
	  elif opt in ("-i", "--ifile"):
	     inputfile = arg
	  elif opt in ("-u"):
             username = arg
	  elif opt in ("-p"):
             password = arg
	if inputfile == '':
	  print('script.py -u <username> -p <password> -i <inputfile>')
	  sys.exit(2)
	print('Input file is "', inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])

def progressBar(value, endvalue, bar_length=20):

        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()


session = tidalapi.Session()
session.login(username, password)

#print(str(session.user.id))
favs = tidalapi.Favorites(session, session.user.id)

if False:
	results = session.search('artist', 'Käptn Peng')

	for artist in results.artists:
		print(artist.name + ' - ' + str(artist.id))
		favs.add_artist(artist.id)

if True:
	track_list = set()
	artist_list = set()
	album_list = set()
	with open(inputfile) as f:
		for line in f:
			if re.match('^#.*', line, re.M|re.I):
				continue

			line = re.sub('.*/Music/','',line)

			elems = line.split('/')
			a = elems[0]
			al = elems[1]
			t = elems[2]

			t = re.sub('\\..*','',t)
			t = re.sub('^\\d+','',t)
			t = re.sub('\n','',t)
			
			st = a + ' ' + t

			results = session.search('track', st)

			for track in results.tracks:
				if a == track.artist.name:
					print(st + ' ----> ' + track.artist.name + ' - ' + track.name + ' - ' + str(track.id))

					track_list.add(track.id)
					artist_list.add(track.artist.id)
					album_list.add(track.album.id)
					break

			#if len(album_list) > 4: break

	if True:
		print('adding %s tracks: ' % len(track_list))
		for index, track_id in enumerate(track_list):
			progressBar((index+1), len(track_list))
			favs.add_track(track_id)
		print('')

	if True:
		print('adding %s artists: ' % len(artist_list))
		for index, artist_id in enumerate(artist_list):
			progressBar((index+1), len(artist_list))
			favs.add_artist(artist_id)
		print('')

	if True:
		print('adding %s albums: ' % len(album_list))
		for index, album_id in enumerate(album_list):
			progressBar((index+1), len(album_list))
			favs.add_album(album_id)
		print('')


#tracks = session.get_album_tracks(album_id=16909093)
#for track in tracks:
#    print(track.name)
