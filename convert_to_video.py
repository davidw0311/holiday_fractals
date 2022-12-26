import imageio

# Replace 'gif_file.gif' with the file path of your GIF
gif_reader = imageio.get_reader('Vivian.gif')

# Replace 'output.mp4' with the desired file path of your output video
video_writer = imageio.get_writer('Vivian.mp4', fps=24)

# Convert the GIF frames to video frames
for frame in gif_reader:
    video_writer.append_data(frame)

# Close the writers to save the video
gif_reader.close()
video_writer.close()