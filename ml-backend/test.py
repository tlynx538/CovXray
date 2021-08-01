# Ignore PyTorch UserWarnings 
import warnings
warnings.filterwarnings("ignore", category=UserWarning) 


# Load InferenceEngine class
from inference import InferenceEngine
inf = InferenceEngine('model-densenet121.pth')
inf.load_image('COVID-19 Radiography Database/test/covid/COVID-19 (1).png')
print(inf.predict())
