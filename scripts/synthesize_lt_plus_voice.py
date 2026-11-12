import os
import sys
import json
import wave
import subprocess
import numpy as np

FFMPEG_DIR = r"C:\Users\Hang thu\AppData\Local\CapCut\Apps\9.7.1.4203"
os.environ["PATH"] = FFMPEG_DIR + os.pathsep + os.environ.get("PATH", "")

BACKEND_DIR = r"d:\antigraviti\VoiceStudio\project\backend"
sys.path.insert(0, BACKEND_DIR)

OUT_DIR = r"d:\antigraviti\lt_plus_hang_thu\06_Audio_Voiceover"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Cut clean 6.6s reference voice clip from voicestudio-428a4d53.wav
SRC_VO = r"C:\Users\Hang thu\Downloads\voicestudio-428a4d53.wav"
REF_WAV = os.path.join(OUT_DIR, "ref_chi_h_6s6.wav")
subprocess.run([
    os.path.join(FFMPEG_DIR, "ffmpeg.exe"),
    "-y", "-hide_banner", "-loglevel", "error",
    "-ss", "0.0", "-t", "6.62",
    "-i", SRC_VO,
    "-ar", "24000", "-ac", "1",
    REF_WAV
], check=True)
REF_TEXT = "Sau 40, kinh tháng sớm tháng muộn là vì đâu? Nếp sinh hoạt vẫn vậy, nhưng kỳ kinh bỗng khó đoán."

SEGMENTS = [
    ("vo_01", "Qua tuổi 45, vì sao cảm giác khô lại rõ hơn?"),
    ("vo_02", "Trước đây thấy bình thường, gần đây vùng kín lại khô và kém dễ chịu dù thói quen sinh hoạt không đổi."),
    ("vo_03", "Biến động hormone quanh mãn kinh có thể làm lượng dịch tự nhiên giảm;"),
    ("vo_04", "bởi vậy, chăm sóc độ ẩm trở thành nhu cầu riêng, chứ chỉ chú ý làm sạch là chưa đủ."),
    ("vo_05", "LT Plus hộp hồng Hằng Thu có lợi ích hỗ trợ duy trì độ ẩm và pH tự nhiên, đồng thời làm sạch dịch nhầy, giảm mùi khó chịu."),
    ("vo_06", "Điểm đáng cân nhắc là đáp ứng cả nhu cầu làm sạch lẫn giữ ẩm trong sản phẩm."),
    ("vo_07", "Nếu khô kéo dài hoặc đau khi gần gũi, chị nên khám để chọn chăm sóc phù hợp."),
    ("vo_08", "Nhắn LT Plus để được tư vấn nhu cầu hỗ trợ độ ẩm của chị nhé!"),
]

import torch
from services.model_manager import (
    _lazy_omnivoice,
    get_best_device,
    resolve_omnivoice_checkpoint,
)

OmniVoice = _lazy_omnivoice()
checkpoint = resolve_omnivoice_checkpoint()
device = get_best_device()
print(f"Loading OmniVoice from {checkpoint} on {device}...")
model = OmniVoice.from_pretrained(
    checkpoint, device_map=device, dtype=torch.float16, load_asr=False
)
sr = int(getattr(model, "sampling_rate", 24000))
print(f"Loaded! Sample rate = {sr}")

def save_wav(path, pcm_f32, sample_rate):
    pcm_f32 = np.clip(pcm_f32, -1.0, 1.0)
    # Apply gentle 25ms fade-in and 40ms fade-out to prevent any boundary click
    fi = min(int(0.025 * sample_rate), len(pcm_f32) // 4)
    fo = min(int(0.040 * sample_rate), len(pcm_f32) // 4)
    if fi > 0:
        pcm_f32[:fi] *= np.linspace(0.0, 1.0, fi, dtype=np.float32)
    if fo > 0:
        pcm_f32[-fo:] *= np.linspace(1.0, 0.0, fo, dtype=np.float32)
    pcm16 = (pcm_f32 * 32767.0).astype(np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm16.tobytes())

manifest = []
full_chunks = []
cursor_s = 0.25  # 0.25s lead-in
full_chunks.append(np.zeros(int(0.25 * sr), dtype=np.float32))

torch.manual_seed(42)
for seg_id, text in SEGMENTS:
    print(f"Synthesizing {seg_id}: {text}")
    audios = model.generate(
        text=text,
        ref_audio=REF_WAV,
        ref_text=REF_TEXT,
        language="vi",
        num_step=24,
        guidance_scale=2.0,
        speed=1.0,
    )
    a = audios[0] if isinstance(audios, (list, tuple)) else audios
    arr = a.detach().to("cpu").float().numpy().squeeze().astype(np.float32)
    if arr.ndim > 1:
        arr = arr.mean(axis=int(np.argmin(arr.shape)))
    # Trim trailing/leading near-silence cleanly
    abs_arr = np.abs(arr)
    idx = np.where(abs_arr > 0.008)[0]
    if len(idx) > 10:
        s0 = max(0, int(idx[0]) - int(0.04 * sr))
        s1 = min(len(arr), int(idx[-1]) + int(0.08 * sr))
        arr = arr[s0:s1]
    seg_path = os.path.join(OUT_DIR, f"{seg_id}.wav")
    save_wav(seg_path, arr, sr)
    dur_s = round(len(arr) / sr, 3)
    pause_s = 0.32
    manifest.append({
        "id": seg_id,
        "text": text,
        "path": seg_path,
        "start_s": round(cursor_s, 3),
        "duration_s": dur_s,
        "end_s": round(cursor_s + dur_s, 3),
    })
    full_chunks.append(arr)
    full_chunks.append(np.zeros(int(pause_s * sr), dtype=np.float32))
    cursor_s += dur_s + pause_s

full_arr = np.concatenate(full_chunks)
full_wav = os.path.join(OUT_DIR, "LT_PLUS_FULL_VOICEOVER.wav")
save_wav(full_wav, full_arr, sr)
total_s = round(len(full_arr) / sr, 3)

with open(os.path.join(OUT_DIR, "vo_manifest.json"), "w", encoding="utf-8") as f:
    json.dump({"sample_rate": sr, "total_duration_s": total_s, "segments": manifest, "full_wav": full_wav}, f, ensure_ascii=False, indent=2)

print(f"DONE! Synthesized {len(manifest)} segments, total_duration = {total_s}s -> {full_wav}")
for m in manifest:
    print(f"  {m['id']}: {m['start_s']:.2f}s - {m['end_s']:.2f}s ({m['duration_s']:.2f}s)")
