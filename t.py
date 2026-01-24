import time
import os

from kivymd.utils.cubic_bezier import CubicBezier


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


class LinearIndeterminateDisjointAnimator:
    """Ported from material-components-android"""

    # Interpolators (ASSUME CubicBezier is already defined)
    INTERPOLATORS = [
        CubicBezier(0.2, 0.0, 0.8, 1.0).t,  # line1_head
        CubicBezier(0.4, 0.0, 1.0, 1.0).t,  # line1_tail
        CubicBezier(0.0, 0.0, 0.65, 1.0).t,  # line2_head
        CubicBezier(0.1, 0.0, 0.45, 1.0).t,  # line2_tail
    ]

    # Durations & delays from LinearIndeterminateDisjointAnimatorDelegate.java
    DURATION_TO_MOVE_SEGMENT_ENDS = [533, 567, 850, 750]
    DELAY_TO_MOVE_SEGMENT_ENDS = [1267, 1000, 333, 0]

    TOTAL_DURATION_IN_MS = 1800
    LOOP_DELAY = 0

    def get_fraction_in_range(self, playtime, start, duration):
        if duration == 0:
            return 0.0
        return max(0.0, min((playtime - start) / duration, 1.0))

    def compute_bar(self, playtime, head_idx, tail_idx):
        f_head = self.get_fraction_in_range(
            playtime,
            self.DELAY_TO_MOVE_SEGMENT_ENDS[head_idx],
            self.DURATION_TO_MOVE_SEGMENT_ENDS[head_idx],
        )
        f_tail = self.get_fraction_in_range(
            playtime,
            self.DELAY_TO_MOVE_SEGMENT_ENDS[tail_idx],
            self.DURATION_TO_MOVE_SEGMENT_ENDS[tail_idx],
        )

        start = self.INTERPOLATORS[head_idx](f_head)
        end = self.INTERPOLATORS[tail_idx](f_tail)
        return start, end

    def bars(self, time_sec):
        time_ms = (time_sec * 1000) % (
            self.TOTAL_DURATION_IN_MS + self.LOOP_DELAY
        )

        # Android order:
        # Bar 1 → line1 (head=0, tail=1)
        # Bar 2 → line2 (head=2, tail=3)
        bar1 = self.compute_bar(time_ms, 0, 1)
        bar2 = self.compute_bar(time_ms, 2, 3)

        return bar1, bar2


def main():
    animator = LinearIndeterminateDisjointAnimator()

    width = 50
    start_time = time.time()

    try:
        while True:
            now = time.time() - start_time
            bar1, bar2 = animator.bars(now / 5)

            track = ["-"] * (width - 1)

            # Draw bar 1
            s1 = int(bar1[0] * width)
            e1 = int(bar1[1] * width)
            for i in range(s1, e1):
                if 0 <= i < width:
                    track[i] = "="

            # Draw bar 2 (overwrites if overlapping)
            s2 = int(bar2[0] * width)
            e2 = int(bar2[1] * width)
            for i in range(s2, e2):
                if 0 <= i < width:
                    track[i] = "="

            clear_screen()
            print("[" + "".join(track) + "]")

            time.sleep(0.016)  # ~60 FPS

    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
