import numpy as np
import math

class ImageFilterProcessor:
    def _convolve_channel(self, channel, kernel):
        src_h, src_w = channel.shape
        k_h, k_w = kernel.shape
        pad_h, pad_w = k_h // 2, k_w // 2
        padded = np.pad(channel, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
        
        output = np.zeros_like(channel)
        for i in range(src_h):
            for j in range(src_w):
                roi = padded[i : i + k_h, j : j + k_w]
                val = np.sum(roi * kernel)
                output[i, j] = val
        return output

    def apply_convolution(self, image, kernel):
        if len(image.shape) == 2:
            res = self._convolve_channel(image, kernel)
        else: 
            channels = []
            for c in range(3):
                channels.append(self._convolve_channel(image[:, :, c], kernel))
            res = np.dstack(channels)
        return np.clip(res, 0, 255).astype(np.uint8)

    def apply_box_blur(self, image, kernel_size=3):
        if kernel_size < 1: return image
        kernel = np.ones((kernel_size, kernel_size), dtype=np.float32)
        kernel /= (kernel_size * kernel_size)
        return self.apply_convolution(image, kernel)
    
    def _get_gaussian_kernel(self, size, sigma):
        k = size // 2
        x, y = np.mgrid[-k:k+1, -k:k+1]
        normal = 1 / (2.0 * np.pi * sigma**2)
        g =  np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
        return g

    def apply_gaussian_blur(self, image, kernel_size=3, sigma=1.0):
        kernel = self._get_gaussian_kernel(kernel_size, sigma)
        kernel /= np.sum(kernel)
        return self.apply_convolution(image, kernel)

    def apply_median_filter(self, image, kernel_size=3):
        h, w = image.shape[:2]
        pad = kernel_size // 2

        if len(image.shape) == 3:
            padded = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
        else:
            padded = np.pad(image, ((pad, pad), (pad, pad)), mode='edge')
            
        output = np.zeros_like(image)
        for i in range(h):
            for j in range(w):
                roi = padded[i:i+kernel_size, j:j+kernel_size]
                if len(image.shape) == 3:
                    for c in range(3):
                        output[i, j, c] = np.median(roi[:, :, c])
                else:
                    output[i, j] = np.median(roi)
                    
        return output.astype(np.uint8)
    
    def apply_sobel(self, image):
        if len(image.shape) == 3:
            gray = np.dot(image[...,:3], [0.299, 0.587, 0.114])
        else:
            gray = image

        Gx_kernel = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ], dtype=np.float32)

        Gy_kernel = np.array([
            [-1, -2, -1],
            [ 0,  0,  0],
            [ 1,  2,  1]
        ], dtype=np.float32)

        gx = self._convolve_channel(gray, Gx_kernel)
        gy = self._convolve_channel(gray, Gy_kernel)

        magnitude = np.sqrt(gx**2 + gy**2)
        
        magnitude = (magnitude / magnitude.max()) * 255
        
        return magnitude.astype(np.uint8)
    
    def apply_color_sobel(self, image):

        if len(image.shape) == 3:
            gray = np.dot(image[...,:3], [0.299, 0.587, 0.114])
        else:
            gray = image

        Gx_kernel = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ], dtype=np.float32)

        Gy_kernel = np.array([
            [-1, -2, -1],
            [ 0,  0,  0],
            [ 1,  2,  1]
        ], dtype=np.float32)

        gx = self._convolve_channel(gray, Gx_kernel)
        gy = self._convolve_channel(gray, Gy_kernel)

        magnitude = np.sqrt(gx**2 + gy**2)

        max_val = magnitude.max()
        if max_val > 0:
            mask = magnitude / max_val
        else:
            mask = magnitude
        mask_3d = mask[:, :, np.newaxis]
        result = image * mask_3d * 2.0
        magnitude = (result / result.max()) * 255
        return magnitude.astype(np.uint8)