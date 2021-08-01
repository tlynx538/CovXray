import torchvision.transforms as transforms
import torchvision
from PIL import Image
import torch
import os
from densenet121 import DenseNet121



class InferenceEngine:
    def __init__(self,model_state_path):
        # Load GPU for inference
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Load DenseNet121 model with 3 classes
        self.model = DenseNet121(num_classes=3).to(self.device)
        # Load Trained Model state
        try:
            state = torch.load(model_state_path)
            self.model.load_state_dict(state)
        except:
            print("Error Detected: Model State File Not Found")    
        # Load model to GPU
        self.model = self.model.to(self.device)

    def image_transform(self, image):
        # For converting image to PyTorch Tensors
        transform = transforms.Compose([
            torchvision.transforms.Resize(size = (224, 224)),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        return transform(image)   

    def load_image(self,image_path):
        # Loading Image and Processing to use over PyTorch Model
        try:
            self.image = Image.open(image_path).convert('RGB')
        except:
            print("Error Detected: Image Does Not Exist or Invalid Image")    
        self.image = torch.stack([self.image_transform(self.image)]).to(self.device)

    def predict(self):
        # Set Model to Evaluation
        self.model.eval()
        # Predict from image
        outputs  = self.model(self.image)
        # Clear CUDA cache
        if torch.cuda.is_available(): torch.cuda.empty_cache()
        # Collecting inference results
        outputs = outputs.cpu().detach().numpy()
        return outputs