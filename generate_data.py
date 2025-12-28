import os
import numpy as np

# Configuration
base_folder = "dummy_data"
groups = {
    "CFA": {"n": 8, "mean_ratio": 1.5, "noise": 0.2},  # CFA has higher ratio
    "Carrageenan": {"n": 8, "mean_ratio": 1.1, "noise": 0.2} # Carrageenan is closer to 1.0
}

def create_files(group_name, n, target_ratio, noise_level):
    # Create directories
    left_dir = os.path.join(base_folder, group_name, "Left_Injected")
    right_dir = os.path.join(base_folder, group_name, "Right_Control")
    os.makedirs(left_dir, exist_ok=True)
    os.makedirs(right_dir, exist_ok=True)

    print(f"--- Generating {group_name} Data ---")
    
    for i in range(1, n + 1):
        # 1. Generate a random baseline for the control paw (Right)
        # Random intensity between 50 and 200 (arbitrary units)
        base_intensity = np.random.uniform(50, 200)
        
        # Create 3-5 measurements for the Right paw (Control)
        # These are just slight variations of the base intensity
        right_measurements = np.random.normal(base_intensity, 5, size=np.random.randint(3, 6))
        
        # 2. Calculate the Left paw (Injected) based on the target ratio
        # Apply the ratio and add some biological noise
        actual_ratio = np.random.normal(target_ratio, noise_level)
        left_base = base_intensity * actual_ratio
        
        # Create 3-5 measurements for the Left paw
        left_measurements = np.random.normal(left_base, 5, size=np.random.randint(3, 6))

        # 3. Save to files
        # Right File
        fname_r = os.path.join(right_dir, f"mouse_{i}_R.txt")
        np.savetxt(fname_r, right_measurements, fmt='%.2f')
        
        # Left File
        fname_l = os.path.join(left_dir, f"mouse_{i}_L.txt")
        np.savetxt(fname_l, left_measurements, fmt='%.2f')
        
        print(f"Mouse {i}: R_mean={right_measurements.mean():.1f}, L_mean={left_measurements.mean():.1f} (Ratio: {actual_ratio:.2f})")

if __name__ == "__main__":
    # Clean up old run if exists
    if os.path.exists(base_folder):
        import shutil
        shutil.rmtree(base_folder)

    for name, params in groups.items():
        create_files(name, params["n"], params["mean_ratio"], params["noise"])
        
    print(f"\n✅ Done! Data generated in folder: '{base_folder}'")
