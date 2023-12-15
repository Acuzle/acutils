# video

# browse_frames_for_binary_classification


Browse each frame of a video, from "start" to "end".
Skip from bound-extra_down to bound+extra_up.

PARAMETERS
------
- src (str): absolute path to the video
- bound (int): frame number that switch the status from "before" to "after"
- extra_down (int): how many frames to skip before the bound
- extra_up (int): how many frames to skip after the bound
- start=0 (int): frame number to start browsing frames
- end=None (int): frame number to end browsing frames (if None, go for the
full duration)

RETURNS
------
- passed (generator of bool): True from entering inside the skipped range
to the end
- count (generator of int): frame numbers
- frame (generator of numpy.array of uint8): BGR frames of the video

RAISES
------
None


# tmnt_extract_frames_for_binary_classification


Extract frames of a video, from "start" to "end".
Skip from bound-extra_down to bound+extra_up.
Split them into 2 states "before" or "after" the skipped range.

PARAMETERS
------
- src (str): absolute path to the video
- dstdir (str): absolute path to the directory that should contain the
frames
- bound (int): frame number that switch the status from "before" to "after"
- extra_down (int): how many frames to skip before the bound
- extra_up (int): how many frames to skip after the bound
- start=0 (int): frame number to start browsing frames
- end=None (int): frame number to end browsing frames (if None, go for the
full duration)
- fext="png" (str): frame extension
- before_name="before" (str): name of the subdir inside dstdir to save
frames before skip
- after_name="after" (str): name of the subdir inside dstdir to save frames
after skip

RETURNS
------
None

RAISES
------
None


# tmnt_extract_sequences_for_binary_classification


Extract sequences of a video, from "start" to "end".
Skip from bound-extra_down to bound+extra_up.
Split them into 2 states "before" or "after" the skipped range.

PARAMETERS
----------
- src (str): absolute path to the video
- dstdir (str): Absolute path to the directory that should contain the
frames.
- bound (int): Frame number that switch the status from "before" to "after".
- extra_down (int): How many frames to skip before the bound.
- extra_up (int): How many frames to skip after the bound.
- seqlen=6 (int): Amount of frames per sequence.
- start=0 (int): Frame number to start browsing frames.
- end=None (int): Frame number to end browsing frames (if None, go for the
full duration).
- sext="mp4" (str): Sequence extension.
- codec="mp4v" (str): Sequence codec, used for: fourcc =
cv2.VideoWriter_fourcc(*codec).
- fps=12 (int): saved Sequence frames per second.
- before_name="before" (str): Name of the subdir inside dstdir to save
frames before skip.
- after_name="after" (str): Name of the subdir inside dstdir to save frames
after skip.

RAISES
------
None


