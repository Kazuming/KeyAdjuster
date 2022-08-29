import ffmpeg
# 入力
stream = ffmpeg.input("sinjidai.mp4")
# 出力
out = ffmpeg.output(stream, "s.wav")
# 実行
ffmpeg.run(out)