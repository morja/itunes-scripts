#!/bin/bash
artist=$1
album=$2
#echo "${artist} ${album}"
encodeArtist="$(perl -MURI::Escape -e 'print uri_escape($ARGV[0]);' "$artist")"
encodeAlbum="$(perl -MURI::Escape -e 'print uri_escape($ARGV[0]);' "$album")"
url="http://musicbrainz.org/ws/2/release/?query=artist:%22${encodeArtist}%22%20AND%20release:%22${encodeAlbum}%22%20AND%20status:Official&fmt=json"
#echo $url
curl -s "$url" | jq -r '.releases[] | .date' | sort | head -n 1  | sed 's/-.*//'