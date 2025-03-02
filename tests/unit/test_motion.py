import pytest
import numpy as np
from core.analysis.velocity import calculate_velocity, calculate_acceleration

def test_calculate_velocity():
    # Test with simple sequential points
    points = [(0, 0), (1, 0), (2, 0)]  # Moving right at constant speed
    timestamps = [0, 1, 2]  # 1 second intervals
    
    velocities = calculate_velocity(points, timestamps)
    
    # Should get [(1, 0), (1, 0)] - constant velocity of 1 unit/sec right
    assert len(velocities) == len(points) - 1
    assert np.allclose(velocities[0], (1, 0))
    assert np.allclose(velocities[1], (1, 0))

def test_calculate_acceleration():
    # Similar pattern for acceleration tests
    velocities = [(1, 0), (2, 0)]  # Increasing speed
    timestamps = [0, 1, 2]
    
    accelerations = calculate_acceleration(velocities, timestamps)
    
    # Should detect acceleration of 1 unit/sec²
    assert len(accelerations) == len(velocities) - 1
    assert np.allclose(accelerations[0], (1, 0))



#Edge Cases to check:
#No movement → velocity should be (0,0).
#Jump in timestamps → should correctly compute velocity.
#Cases where speed remains constant → acceleration should be (0,0).


#Ensure moving objects are detected correctly against the background.
#edge case: 
#No movement → should return zero motion.
#Sudden appearance of an object → should detect new motion.

#Validate contour detection (only actual objects should be outlined)
#Ensure objects are detected and outlined correctly.

#Ensure noise filtering works (small jittering movements should be removed)

#Ensure motion peaks are detected at the right timestamps
#Possible Edge Cases:
#silence → should detect no beats.
#Ensure motion timestamps align with the closest beats.


#Fast beats → should detect multiple beats correctly.
#Check if beat detection aligns with motion intensity
#Validate that synchronization produces expected outputs

#MOtion Visualization: Ensure detected motion is displayed on the video.

#full pipeline tests: Ensure the entire system runs without errors.