# Check GPU compatibility
def check_gpu_compatibility():
    """
    Verify GPU setup for Ollama acceleration
    """
    import subprocess
    
    try:
        # Check NVIDIA GPU
        result = subprocess.run(['nvidia-smi'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("NVIDIA GPU detected")
            print(result.stdout)
        
        # Check for CUDA support
        cuda_check = subprocess.run(['nvcc', '--version'], 
                                  capture_output=True, text=True)
        if cuda_check.returncode == 0:
            print("CUDA toolkit installed")
            
    except FileNotFoundError:
        print("No NVIDIA GPU or CUDA toolkit detected")
        print("Ollama will run on CPU")

check_gpu_compatibility()

