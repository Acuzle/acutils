# video

# browse_frames_for_binary_classification


Browse each frame of a video, from "start" to "end".
Skip from bound-extra_down to bound+extra_up.

PARAMETERS
------
(str) src:
absolute path to the video

(int) bound:
frame number that switch the status from "before" to "after"

(int) extra_down:
how many frames to skip before the bound

(int) extra_up:
how many frames to skip after the bound

(int) start=0:
frame number to start browsing frames

(int) end=None:
frame number to end browsing frames (if None, go for the full duration)

RETURNS
------
(generator of bool) passed:
True from entering inside the skipped range to the end

(generator of int) count:
frame numbers

(generator of numpy.array of uint8) frame:
BGR frames of the video


# tmnt_extract_frames_for_binary_classification


Extract frames of a video, from "start" to "end".
Skip from bound-extra_down to bound+extra_up.
Split them into 2 states "before" or "after" the skipped range.

PARAMETERS
------
(str) src:
absolute path to the video

(str) dstdir:
absolute path to the directory that should contain the frames

(int) bound:
frame number that switch the status from "before" to "after"

(int) extra_down:
how many frames to skip before the bound

(int) extra_up:
how many frames to skip after the bound

(int) start=0:
frame number to start browsing frames

(int) end=None:
frame number to end browsing frames (if None, go for the full duration)

(str) fext="png":
frame extension

(str) before_name="before":
name of the subdir inside dstdir to save frames before skip

(str) after_name="after":
name of the subdir inside dstdir to save frames after skip

RETURNS
-------
None


# tmnt_extract_sequences_for_binary_classification


Extract sequences of a video, from "start" to "end".
Skip from bound-extra_down to bound+extra_up.
Split them into 2 states "before" or "after" the skipped range.

PARAMETERS
----------
(str) src:
absolute path to the video

(str) dstdir:
Absolute path to the directory that should contain the frames.

(int) bound:
Frame number that switch the status from "before" to "after".

(int) extra_down:
How many frames to skip before the bound.

(int) extra_up:
How many frames to skip after the bound.

(int) seqlen=6:
Amount of frames per sequence.

(int) start=0:
Frame number to start browsing frames.

(int) end=None:
Frame number to end browsing frames (if None, go for the full duration).

(str) sext="mp4":
Sequence extension.

(str) codec="mp4v":
Sequence codec, used for: fourcc = cv2.VideoWriter_fourcc(*codec).

(int) fps=12:
saved Sequence frames per second.

(str) before_name="before":
Name of the subdir inside dstdir to save frames before skip.

(str) after_name="after":
Name of the subdir inside dstdir to save frames after skip.


