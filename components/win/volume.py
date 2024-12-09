from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
import comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def set_volume(volume_percent: int) -> bool:
    try:
        comtypes.CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        if volume_percent == 0:
            volume.SetMute(1, None)
        else:
            volume.SetMute(0, None)
            # Volume range is from -65.25 to 0.0 dB
            min_volume = volume.GetVolumeRange()[0]
            max_volume = volume.GetVolumeRange()[1]

            # Convert volume percent to dB
            volume_db = min_volume + (max_volume - min_volume) * (volume_percent / 100.0)
            volume.SetMasterVolumeLevel(volume_db, None)
        return True
    except Exception as e:
        print(f"Error setting volume: {e}")
        return False

if __name__ == "__main__":
    volume_percent = 30
    if set_volume(volume_percent):
        print(f"Volume set to {volume_percent}%")
    else:
        print("Failed to set volume")