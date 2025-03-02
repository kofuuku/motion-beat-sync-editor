import pandas as pd

def create_motion_dataframe():
    """
    Creates an empty Pandas DataFrame with predefined columns for motion tracking.
    """
    columns = [
        "frame_index",          # (int) Unique index for each frame in the video
        "timestamp",            # (float) Time (in seconds) of the frame
        "position_x",           # (float) X-coordinate of detected motion center
        "position_y",           # (float) Y-coordinate of detected motion center
        "velocity_x",           # (float) X-component of velocity (px/sec)
        "velocity_y",           # (float) Y-component of velocity (px/sec)
        "speed",                # (float) Magnitude of velocity (overall motion speed)
        "acceleration_x",       # (float) X-component of acceleration (px/sec²)
        "acceleration_y",       # (float) Y-component of acceleration (px/sec²)
        "acceleration",         # (float) Magnitude of acceleration
        "motion_intensity",     # (float) Score representing movement intensity in the frame
        "dopamine_hit_score",   # (float) A score (0-1) based on high-energy motion patterns
        "is_peak_moment",       # (bool) True if this frame is identified as a high-impact moment
        "aligned_beat",         # (float) The closest beat drop timestamp to this frame
        "beat_alignment_score", # (float) How well this motion peak aligns with the beat
        "optical_flow_x",       # (float) Average X-direction motion from optical flow
        "optical_flow_y",       # (float) Average Y-direction motion from optical flow
        "optical_flow_magnitude" # (float) Strength of motion detected via optical flow
    ]
    
    motion_df = pd.DataFrame(columns=columns)
    return motion_df

# Example usage (for testing)
if __name__ == "__main__":
    df = create_motion_dataframe()
    print(df.head())  # Prints empty DataFrame with defined column names
