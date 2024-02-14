from pydub import AudioSegment

# Open an mp3 file
song = AudioSegment.from_file("audio/cypher006.wav")

# start and end time
start_min = 26
start_sec = 39
end_min = 26
end_sec = 42

# pydub does things in milliseconds, so convert time
start = ((start_min * 60) + start_sec) * 1000
end = ((end_min * 60) + end_sec) * 1000

# song clip of 10 seconds from starting
first_10_seconds = song[start:end]

# save file
first_10_seconds.export("goodtrybrudda.mp3", format="mp3")
print("New Audio file is created and saved")