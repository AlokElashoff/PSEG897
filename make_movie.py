import os
import moviepy.video.io.ImageSequenceClip
image_folder='image_data'
fps=3

image_files = [image_folder+'/'+img for img in os.listdir(image_folder) if img.endswith(".png")]
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
clip.write_videofile('night_sky.mp4')