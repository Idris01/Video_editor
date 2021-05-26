import sys
from moviepy.editor import VideoFileClip, concatenate_videoclips
from pathlib import Path
from datetime import datetime

from conf import OUTPUT_DIR


def new_location():
	"""
	Return a distinct full name of a .mp4 file to be saved in the OUTPUT_DIR
	"""
	time=datetime.now()
	new_file_name="movieditor_%d_%d%d%d.mp4" % (time.year,time.day,time.minute,time.second)
	return str(Path.joinpath(OUTPUT_DIR,new_file_name))


def mergeVideos(*clip, rotate=None):
	clips=[VideoFileClip(i) for i in clip]
	assert type(clips)==type([0])
	output=concatenate_videoclips(clips)
	output=output.resize(newsize=(clips[0].size[1],clips[0].size[0]))

	if rotate:
		output=output.rotate(int(rotate))

	output.write_videofile(new_location())
	output.close()





def rotate(clip,angle):
	vid=VideoFileClip(clip).rotate(int(angle))
	if (angle//90)%2 > 0:
		vid=vid.resize(newsize=(vid.size[1],vid.size[0]))
	vid.write_videofile(new_location())
	vid.close()


def cut(clip,start,end):
	"""
	Cut off part of a given video clip

	start - the start time of the cut off part in form "HH:MM:SS"
	end  - the end time of the cut off part

	"""
	vid=VideoFileClip(clip)
	vid=vid.resize(newsize=(vid.size[1],vid.size[0]))
	clip_time=int(vid.duration)
	clip_end="%-2d:%-2d:%-2d" % (clip_time/3600,clip_time/60,clip_time%60)

	part1=vid.subclip("00:00:00",start)
	part2=vid.subclip(end,clip_end)

	output=concatenate_videoclips([part1,part2])

	save_location=new_location()
	output.write_videofile(save_location)
	output.close()
	vid.close()


def invert_size(clip):
	vid=VideoFileClip(clip)
	#size=vid.size
	vid=vid.resize(newsize=(vid.size[1],vid.size[0]))
	vid.write_videofile(new_location())
	vid.close()



def hardCoded():
	v=VideoFileClip(sys.argv[1])
	duration=str(v.duration).split(".")
	time=duration[0]
	sec=duration[1]
	#print("%d hours %d minutes %d sec" % (int(time)/3600,int(time)/60, int(time)%60))

	video_time="%d:%d:%d" % (int(time)/3600,int(time)/60, int(time)%60)

	part1Start="00:00:00"
	part1End="00:01:27"

	part2Start="00:1:37"
	part2End=video_time

	print("writing video file ...")
	part1=v.subclip(part1Start,part1End)
	part2=v.subclip(part2Start,part2End)

	part1.write_videofile('part1.mp4')
	part2.write_videofile('part2.mp4')

	final_output=concatenate_videoclips([part1,part2])
	final_output.write_videofile("mergedVideo.mp4")

	print("Video successfully processed")

	part1.close()
	part2.close()
	v.close()
