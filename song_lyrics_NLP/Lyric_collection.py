# Using genius lyrics api to gain access to song lyrics
import lyricsgenius


token = 'h-TIDAcISlX300SMx450ZbqTWfITn69gmsoAN5RZlEn_wWsv08OTf1ld8XOlXKT4'
genius = lyricsgenius.Genius(token)


def genius_lyrics_extracter(song_name):
    """
    func that reads into genius api to search for song and extract lyrics into txt file
    :param song_name: name of song wanted to be searched
    :return: txt file of lyrics
    """
    song = genius.search_song(song_name)
    lyrics = song.lyrics
    file = open(f'{song_name}.txt', 'w')
    file.write(lyrics)
    file.close()


