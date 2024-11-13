import torch

x = torch.rand(5, 3)
print(f"Random Tensor:\n{x}")

# CUDA가 사용 가능한지 확인
if torch.cuda.is_available():
    print("CUDA is available!")
    device = torch.device("cuda")
else:
    print("CUDA is not available. Using CPU.")
    device = torch.device("cpu")

x = x.to(device)
print(f"Tensor on {device}:\n{x}")

