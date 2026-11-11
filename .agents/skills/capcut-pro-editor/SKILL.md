---
name: capcut-pro-editor
description: >-
  Bộ kỹ năng chuyên sâu mô phỏng và nâng cấp phong cách dựng phim CapCut cá nhân
  của Editor (TVC, Reels, Vlog, Storytelling/AI Drama). Sử dụng khi phân tích,
  chỉnh sửa, nâng cấp hoặc tạo mới dự án CapCut (draft_content.json).
---

# CapCut Pro Editor Skill (Signature Style + Pro Upgrades)

Skill này cung cấp toàn bộ thông số kỹ thuật JSON (`draft_content.json`), ID hiệu ứng/mask/font/SFX trên máy của Editor và bộ công cụ tự động hóa để dựng hoặc nâng cấp dự án CapCut theo đúng chuẩn cá nhân đã nâng tầm.

---

## 1. Cấu Trúc & Quy Chuẩn Dựng Theo Thể Loại

| Thể loại | Tỷ lệ khung | Median Dur (Main Track) | Median Dur (B-Roll) | Speed Đặc Trưng | Phong cách Âm thanh & Chữ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TVC Luxury / Không gian (WinHair...)** | `1920x1080` hoặc `1080x1920` | `1.8s – 2.0s` | `1.1s – 1.67s` (đa tầng Track 1–6) | Slow-mo `0.8x`, `0.7x`, `0.6x` cho cảnh beauty/flycam | Voiceover cắt bậc thang (`vol: 1.12`) + BGM (`vol: 0.26–0.38`) + Text 2 tầng (Vàng Gold `#FFD400` + Trắng) |
| **Reels / Short Trend** | `1080x1920` (`9:16`) | `1.0s – 1.27s` | `0.4s – 1.0s` | Slow-mo `0.6x – 0.8x` xen kẽ `1.2x – 2.3x` | Mute B-roll (`0.0`), bật ASMR thực tế (`vol: 1.98–9.39`), SFX dày (`Magic reveal`, `Deep woosh`, `Pop`, `打字-102214`) |
| **Vlog / Training / Sự kiện (F20...)** | `1080x1920` (`9:16`) | `2.5s` | `2.4s – 6.0s` | `1.0x` tự nhiên | Hook 3s đầu dùng Text 3 cụm (`Montserrat-Bold` / `Oswald-Bold`) + `Camera shutter` + `Máy chữ` + BGM `0.42` |
| **Dược phẩm / Doanh nghiệp (An Vượng...)** | `1920x1080` (`16:9`) | `1.83s` | Logo góc cố định (`scale: 0.11`) | `1.0x` (điểm nhấn `0.9x` / `1.8x`) | Voiceover `vol: 1.0–1.46`, BGM `0.28`, Subtitles IN HOA cỡ `5` tại `Y = -0.85` (~`1.97s`/cụm) |
| **AI Drama / Storytelling (`túi cá`, `1103`)** | `1080x1920` (`9:16`) | `2.6s – 3.57s` | `1.0s – 1.4s` | `1.0x` giữ thoại | Nhạc kịch tính/bi cảm Lê Tuấn Khang (`vol: 0.47–0.62`) + SFX `Tiếng Nổ impact căng căng`, `Deep woosh` |

---

## 2. Danh Mục Resource ID & Đường Dẫn Cache Trên Máy

Khi thêm Transition, Animation, Mask, Font hoặc SFX vào `draft_content.json`, sử dụng chính xác các ID và đường dẫn sau:

### A. Fonts
- **Font mặc định (TVC / Subtitles)**:
  - `id`: `"7542214368361057553"`
  - `path`: `"C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7542214368361057553/d376267c892ee3a53654ae93a78dcfb7/font.ttf"`
- **Montserrat-Bold (Hook / Luxury Title)**:
  - `id`: `"7517455788122705168"`
  - `path`: `"C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7517455788122705168/91d28cfa5e7db054f4872f1ae2417ac2/Montserrat-Bold.otf"`
- **Oswald-Bold (Vlog / Điểm nhấn mạnh)**:
  - `id`: `"7182504807289065985"`
  - `path`: `"C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7182504807289065985/0a5333de6f4d592cb2d2390d68b31efb/Oswald-Bold.ttf"`

### B. Masks (`materials.common_mask`)
1. **Tách (Line Mask - Chia đôi chéo sang trọng)**:
   - `resource_type`: `"line"`, `resource_id`: `"7374020197990011409"`
   - `path`: `"C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/1068046536/4c6a0ef5de6a844342d40330e00c59eb"`
   - `config` chuẩn: `{"width": 0.28, "height": 0.0, "centerX": -0.849, "centerY": 0.137, "rotation": 101.5, "feather": 0.51, "expansion": 0.0, "roundCorner": 0.0, "invert": false, "aspectRatio": 1.0}`
2. **Cuộn phim (Mirror Mask - Lồng cảnh nghệ thuật)**:
   - `resource_type`: `"mirror"`, `resource_id`: `"7374021024985125377"`
   - `path`: `"C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7374021024985125377/d434671c844fde7d8846e8e8019f8b1d"`
   - `config` chuẩn: `{"width": 0.28, "height": 0.759, "centerX": 0.062, "centerY": -0.11, "rotation": -79.0, "feather": 0.27, "expansion": 0.0, "roundCorner": 0.0, "invert": false, "aspectRatio": 1.0}`
3. **Hình chữ nhật (Rectangle Mask - Khung PIP / Collage)**:
   - `resource_type`: `"rectangle"`, `resource_id`: `"7374021450748924432"`
   - `path`: `"C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/1068046537/02b8999168d121538a98ea59127483ef"`
   - `config` chuẩn: `{"width": 0.5, "height": 0.468, "centerX": 0.0, "centerY": 0.0, "rotation": 0.0, "feather": 0.14, "expansion": 0.0, "roundCorner": 0.0, "invert": false, "aspectRatio": 1.0}`

### C. Animations (`materials.material_animations`)
- **Video / PIP In-Out**:
  - `in:Trượt sang trái`: `id="6798332871267324423"`, `duration=466666`, `path="C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/6798332871267324423/667952e8cf6918f62e16b8e6dfc2fef2"`
  - `in:Trượt sang phải`: `id="6798333076469453320"`, `duration=500000`, `path="C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/6798333076469453320/abb44c05890e39fdfeb58abc8524c1a6"`
  - `out:Mờ dần`: `id="6798320902548230669"`, `duration=500000`, `path="C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/6798320902548230669/c6f05ce62355b537be762550040bfc08"`
- **Text Animations**:
  - `in:Máy chữ`: `id="7210980292243231233"`, `duration=800000`, `path="C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7210980292243231233/6828d67634e66ace1e76c4eb7cc2f8e6"`
  - `in:Bụi vàng`: `id="7331632775948145153"`, `duration=700000`, `path="C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7331632775948145153/25d1da238cd78c05757f2d6036dec895"`
  - `in:Chữ mờ dần hiện vào`: `id="7648937403646004500"`, `duration=700000`, `path="C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7648937403646004500/495e55b3bcd1f6420b6e4b1b44ed1fc8"`
  - `in:Mờ`: `id="6923135604519604737"`, `duration=866666`, `path="C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/6923135604519604737/a5f4d3998c0648ec65c03251506bd0a0"`

### D. Transitions (`materials.transitions`)
- `Kéo vào ii`: `effect_id="7291211157254181377"`, `duration=466666`, `is_overlap=true`, `path="C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7291211157254181377/94815943a86e741a5fec1737fbb46d60"`
- `Kết hợp`: `effect_id="6724845717472416269"`, `duration=466666`, `is_overlap=true`, `path="C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/6724845717472416269/7b53f4c008c4c684fccf8c7d4d46cc92"`
- `Mờ thu phóng hiện ra`: `effect_id="7621850078533143861"`, `duration=466666`, `is_overlap=true`, `path="C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7621850078533143861/01e4b5812c36fd59c8e3e776bd411d35"`
- `Chói lòa 1`: `effect_id="6726707814028284423"`, `duration=333333`, `is_overlap=true`, `path="C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/6726707814028284423/a3fd6266c293496fd9480884a93fb90e"`

### E. Kho SFX Chủ Lực Có Sẵn Trên Máy
- `Magic reveal`: `"C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/music/229f88e6452098f686f43df9309b1acc.mp3"`
- `Deep woosh`: `"C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/music/270677b49d33e1e347819050db9ee915.mp3"`
- `打字-102214` (Gõ máy chữ): `"C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/music/de7663a758c391a57ebc8060285800f8.mp3"`
- `Pop (lower) telop sound etc`: `"C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/music/d3b74afaf571dd3056bd7e9996a683cc.mp3"`
- `鼠标单击1` (Click chuột): `"C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/music/25b5bc6c42f453173fbf056859eec22b.mp3"`
- `Camera shutter sound`: `"C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/music/66c35a8a836911a52824fcd5c8cb016a.mp3"`
- `Woosh vshort - chữ.mp3`: `"D:/Edit/Sound Effect/Woosh vshort - chữ.mp3"`
- `Noitifi - chữ.mp3`: `"D:/Edit/Sound Effect/Noitifi - chữ.mp3"`
- `Tiếng Nổ impact căng căng.mp3`: `"D:/Edit/SFX LÊ TUẤN KHANG/le tuan khang/Tiếng Nổ impact căng căng.mp3"`

---

## 3. Quy Trình 5 Bước Nâng Cấp Dự Án CapCut (Pro Upgrade Workflow)

Khi người dùng yêu cầu **"nâng cấp"**, **"chuẩn hóa"** hoặc **"dựng theo phong cách của tôi"**, hãy chạy công cụ `scripts/capcut_pro_engine.py` hoặc áp dụng trực tiếp 5 nâng cấp sau:

1. **Khử Click/Pop cho Voiceover cắt nhỏ (Micro-Fade Smoothing)**:
   - Tự động kiểm tra toàn bộ các segment thoại cắt ngắn (`0.4s – 10s`) và gắn `audio_fade` (`fade_in_duration = 33333` µs [1 frame], `fade_out_duration = 66666` µs [2 frames]) để câu chữ nối nhau êm tuyệt đối.
2. **Tạo Nhịp Thở Khung Hình (Subtle Ken Burns Micro-Zoom)**:
   - Với các clip trên Track 0 dài `> 2.3s` đang đứng tĩnh (`common_keyframes` rỗng và `scale == 1.0`), tự động thêm cặp keyframe `KFTypeScaleX` & `KFTypeScaleY` phóng nhẹ từ `1.00 -> 1.06` (hoặc thu từ `1.06 -> 1.00` xen kẽ) suốt thời lượng clip.
3. **Chuẩn Hóa Bố Cục & Hiệu Ứng Chữ 2 Tầng (Staggered Dual-Tier Typography)**:
   - Đảm bảo Tầng 1 (Vàng Gold `#FFD400`, size `12`, `Y = -0.42`) và Tầng 2 (Trắng `#FFFFFF`, size `9`, `Y = -0.64`) có hiệu ứng vào/ra mượt (`in:Chữ mờ dần hiện vào` + `out:Mờ dần`) và Tầng 2 xuất hiện trễ hơn Tầng 1 `0.25s – 0.4s`.
4. **Cân Bằng Âm Lượng Thông Minh (Pro Gain Staging)**:
   - Đưa Voiceover về ngưỡng chuẩn `1.12 – 1.25`, BGM về `0.26 – 0.35` khi có thoại, và tắt tiếng (`volume = 0.0`) các B-roll thừa ngoại trừ các clip ASMR chủ đích.
5. **Kiểm Tra Nhịp Sóng (Wave Pacing Audit)**:
   - Phát hiện các chuỗi > 3 clip liên tiếp có thời lượng quá giống nhau hoặc quá dài (> 4.5s không có B-roll đè lên) để gợi ý điểm chèn B-roll / PIP / Split-Screen.

---

## 4. Sử Dụng Script Tự Động Hóa (`capcut_pro_engine.py`)

Chạy lệnh sau để phân tích (audit) hoặc tự động nâng cấp (upgrade) bất kỳ dự án CapCut nào:

```powershell
# 1. Phân tích & chấm điểm dự án theo chuẩn cá nhân + gợi ý nâng cấp:
python "d:\antigraviti\.agents\skills\capcut-pro-editor\scripts\capcut_pro_engine.py" audit "<Tên dự án CapCut>"

# 2. Tự động áp dụng gói Pro Upgrade (có tự động tạo bản sao lưu .bak):
python "d:\antigraviti\.agents\skills\capcut-pro-editor\scripts\capcut_pro_engine.py" upgrade "<Tên dự án CapCut>" --micro-fade --micro-zoom --text-fade
```
