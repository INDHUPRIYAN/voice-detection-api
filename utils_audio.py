import librosa
import numpy as np

def extract_features_from_file(file_path):
    y, sr = librosa.load(file_path, sr=16000)

    # MFCC
    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40), axis=1)

    # Chroma
    chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr), axis=1)

    # Spectral Contrast
    contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr), axis=1)

    # Zero Crossing Rate
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))

    # Tonnetz
    tonnetz = np.mean(librosa.feature.tonnetz(y=y, sr=sr), axis=1)

    features = np.hstack([mfcc, chroma, contrast, zcr, tonnetz])

    return features
