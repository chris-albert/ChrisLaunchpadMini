import logging

class TrackClipListener:

    def __init__(self, bar_listener):
        self._bar_listener = bar_listener
        self._bar_listener.add_bar_listener(self._on_bar)

        self._active_clip_ptr = None
        self._clip_ptr_dict = {}
        self._active_ptr_dict = {}
        self._clip_ptr_func_dict = {}

    def _add_clip(self, clip):
        self._clip_ptr_dict[str(clip._live_ptr)] = clip
        start = int(clip.start_time)
        end = int(clip.end_time)

        for i in range(start, end):
            self._active_ptr_dict[str(i)] = clip._live_ptr            

    def on_clip_change(self, clip, change_func):
        self._add_clip(clip)
        self._clip_ptr_func_dict[str(clip._live_ptr)] = change_func
            
    def _on_bar(self, bar, time):
        clip_ptr = self._active_ptr_dict.get(str(time), None)

        if self._active_clip_ptr != clip_ptr:

            if clip_ptr is not None:
                # logging.info("Clip [{}] is now active".format(clip_ptr))
                self._clip_ptr_func_dict[str(clip_ptr)](self._clip_ptr_dict[str(clip_ptr)], bar, True)

            if self._active_clip_ptr is not None:
                # logging.info("Clip [{}] is now not active".format(self._active_clip_ptr))
                self._clip_ptr_func_dict[str(self._active_clip_ptr)](self._clip_ptr_dict[str(self._active_clip_ptr)], bar, False)

            self._active_clip_ptr = clip_ptr

        # logging.info("_on_bar({}, {})".format(bar, time)) 
               
