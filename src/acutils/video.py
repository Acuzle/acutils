# Functions prefixed with "tmnt" are treatments and must have those parameters:
#  - src: absolute path to the file that will be processed (str)
#  - dstdir: absolute path to the directory that should contain new files (str)
# Also, nothing should be returned.

import os

try:
    import cv2
except ImportError:
    print("|WRN| You must install 'opencv-python' (cv2) to use video module. "
          "Leaving.")
    exit()



def browse_frames_for_binary_classification(src, bound, extra_down, extra_up, 
                                            start=0, end=None):
    '''
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
    '''
    srst = int(bound-extra_down) # skipped range start time
    srse = int(bound+extra_up) # skipped range end time

    cap = cv2.VideoCapture(src)
    duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # as frame amount
    duration = end if end is not None and duration < end else duration

    count = 0 # use it to name frames
    success, frame = cap.read() # load first frame

    while success: # read it frame per frame
        passed = count > srst # True if not before the skipped range

        if passed: # skip frames between srst and srse
            if srse >= duration: break # exit now if no more data
            if count < srse: # go to the end of the skipped range
                count += 1
                success, frame = cap.read() # load next frame
                continue

        elif count <= start: # save nothing before start
            count += 1
            success, frame = cap.read() # load next frame
            continue

        yield passed, count, frame
        
        count += 1
        success, frame = cap.read()



def tmnt_extract_frames_for_binary_classification(src, dstdir, bound, 
        extra_down, extra_up, start=0, end=None, fext="png", before_name="before", 
        after_name="after"):
    '''
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
    '''
    _, vext = os.path.splitext(src)
    vname = os.path.basename(src)[:-len(vext)]

    for passed, count, frame in browse_frames_for_binary_classification(
                              src, bound, extra_down, extra_up, start, end):
        cv2.imwrite(os.path.join(dstdir, after_name if passed else before_name,
             f"{vname}_{count}.{fext}"), frame)



def tmnt_extract_sequences_for_binary_classification(src, dstdir, bound, 
        extra_down, extra_up, seqlen=6, start=0, end=None, sext='mp4', 
        codec='mp4v', fps=12, before_name="before", after_name="after"):
    '''
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
    '''

    _, vext = os.path.splitext(src)
    vname = os.path.basename(src)[:-len(vext)]

    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = None # for VideoWriter
    seq = []
    scount = 0 # sequence counter
    old_passed = False

    for passed, _, frame in browse_frames_for_binary_classification(src, bound, 
      extra_down, extra_up, start, end):
        if old_passed != passed:
            seq = [] # a sequence should be entirely before or after the skip
        
        seq.append(frame) # add the frame to the sequence

        if len(seq) == seqlen: # write a sequence file if enough frames
            out = cv2.VideoWriter(
                os.path.join(dstdir, after_name if passed else before_name, 
                                                  f'{vname}_{scount}.{sext}'), 
                fourcc, 
                fps, 
                frame.shape[:2][::-1]
            )
            for img in seq: 
                out.write(img)
            out.release()
            seq = []
            scount += 1
        
        old_passed = passed