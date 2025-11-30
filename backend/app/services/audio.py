import os
from faster_whisper import WhisperModel

class AudioService:
    def __init__(self):
        # UPGRADE: Using "base" model as agreed for better accuracy
        print("Loading Whisper Model...")
        self.model = WhisperModel("base", device="cpu", compute_type="int8")
        print("Whisper Model Loaded!")

    def transcribe(self, file_path: str, context_text: str = "") -> str:
        """
        Transcribes audio.
        :param context_text: A string (like the Interview Question) to guide the AI.
        """
        try:
            # We use the Question + a generic header as the "prompt" to bias the model
            initial_prompt = f"Technical interview answer regarding: {context_text}"
            
            segments, info = self.model.transcribe(
                file_path, 
                beam_size=5,
                initial_prompt=initial_prompt 
            )
            
            full_text = " ".join([segment.text for segment in segments])
            return full_text.strip()
        except Exception as e:
            print(f"Transcription Error: {e}")
            return ""