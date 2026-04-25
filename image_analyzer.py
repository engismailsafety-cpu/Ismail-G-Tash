from PIL import Image
import numpy as np
import io

class ImageAnalyzer:
    def __init__(self):
        pass
    
    def analyze_images(self, image_files):
        results = []
        
        for img_file in image_files:
            try:
                img = Image.open(img_file)
                
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                img_array = np.array(img.resize((100, 100)))
                
                green_mask = (img_array[:, :, 1] > img_array[:, :, 0]) & \
                            (img_array[:, :, 1] > img_array[:, :, 2]) & \
                            (img_array[:, :, 1] > 100)
                green_percentage = (green_mask.sum() / green_mask.size) * 100
                
                dark_pixels = (img_array[:, :, :3].sum(axis=2) < 200).sum()
                pollution_index = dark_pixels / green_mask.size
                
                results.append({
                    'filename': img_file.name,
                    'image': img,
                    'classification': 'Green Area' if green_percentage > 20 else 'Industrial/Urban',
                    'confidence': min(0.95, green_percentage / 100 + 0.3),
                    'detected_objects': ['trees', 'vegetation', 'buildings'] if green_percentage > 20 else ['roads', 'structures'],
                    'green_area_percentage': green_percentage,
                    'pollution_index': pollution_index * 10
                })
            except Exception as e:
                results.append({
                    'filename': img_file.name,
                    'error': str(e),
                    'classification': 'Analysis Failed'
                })
        
        return results
