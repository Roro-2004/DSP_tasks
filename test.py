import numpy as np

def quantize_signal(signal, num_bits):
    # Define the number of quantization levels
    num_levels = 2 ** num_bits
    min_val, max_val = min(signal), max(signal)
    
    # Create quantization levels as midpoints of each interval
    quantization_levels = np.linspace(min_val, max_val, num_levels + 1)
    quantization_levels = (quantization_levels[:-1] + quantization_levels[1:]) / 2

    # Create binary codes for each level
    binary_codes = [format(i, f'0{num_bits}b') for i in range(num_levels)]

    # Quantize the signal
    quantized_signal = []
    encoded_signal = []

    for value in signal:
        # Find the closest quantization level
        idx = (np.abs(quantization_levels - value)).argmin()
        quantized_value = quantization_levels[idx]
        quantized_signal.append(quantized_value)
        encoded_signal.append(binary_codes[idx])

    return encoded_signal, quantized_signal

# Example usage
signal = [0.387, 0.430, 0.478, 0.531, 0.590, 0.6561, 0.729, 0.81, 0.9, 1, 0.2]
num_bits = 3

encoded_signal, quantized_signal = quantize_signal(signal, num_bits)

# Display results
print("Encoded Value  Quantized Signal")
for code, quantized_value in zip(encoded_signal, quantized_signal):
    print(f"{code}           {quantized_value:.2f}")
