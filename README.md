# 🎬 EDITVIDEO — Hệ Sinh Thái Dựng Video Chuyên Nghiệp (CapCut Pro DNA + HyperFrames + Remotion)

Kho lưu trữ trung tâm (**Master Repository**) chứa toàn bộ **Hồ sơ Phong cách Dựng phim Cá nhân (Editing DNA)**, **Bộ 23 Skills AI Dựng Video**, **Công cụ Tự động hóa CapCut (`capcut_pro_engine.py`)**, cùng các **Script & Dự án mẫu (`draft_content.json`)**.

---

## 📂 Cấu Trúc Kho Lưu Trữ (Repository Structure)

```text
EDITVIDEO/
├── GEMINI.md                          # Hồ sơ & Quy tắc cốt lõi CapCut Pro Editor DNA + HyperFrames + Remotion
├── README.md                          # Tài liệu hướng dẫn sử dụng kho lưu trữ
├── .agents/
│   └── skills/                        # Bộ 23 Skills chuyên sâu cho AI Agent
│       ├── capcut-pro-editor/         # Skill & CLI tự động phân tích, nâng cấp dự án CapCut (draft_content.json)
│       ├── hyperframes/               # Bộ 9 Skills làm video bằng HTML/CSS/GSAP/WebGL Shaders (HeyGen)
│       ├── hyperframes-cli/
│       ├── hyperframes-registry/
│       ├── media-use/
│       ├── reverse-any-video/
│       ├── style-sampling/
│       ├── figma/
│       ├── slideshow/
│       ├── remotion-to-hyperframes/
│       ├── remotion-best-practices/   # Bộ 13 Skills làm video bằng React + TypeScript (Remotion)
│       ├── remotion-create/
│       ├── remotion-markup/
│       ├── remotion-captions/
│       ├── remotion-maps/
│       ├── remotion-multimedia/
│       ├── remotion-interactivity/
│       ├── remotion-render/
│       ├── remotion-studio/
│       ├── remotion-saas/
│       ├── remotion-docs/
│       ├── remotion-upgrade/
│       └── remotion-license/
├── scripts/                           # Các script tự động hóa xử lý dự án CapCut thực tế
│   ├── upgrade_tvc_copy.py            # Script nâng cấp toàn diện TVC WinHair (Text 2 tầng, SFX, chống Jump-cut, Micro-Zoom)
│   ├── verify_tvc_copy.py             # Script kiểm định tính toàn vẹn của draft_content.json
│   └── sync_capcut_cache_files.py     # Script đồng bộ Timelines & dọn cache mini_draft.json của CapCut 9.x
└── projects/                          # Bản lưu trữ cấu trúc Timeline JSON của các dự án tiêu biểu
    └── TVC_WinHair_CS2_Reels_v2_Pro/
        ├── draft_content.json         # File cấu trúc timeline 20 tracks hoàn chỉnh
        └── draft_meta_info.json       # Metadata dự án
```

---

## 🚀 Cách Khôi Phục & Sử Dụng Trên Máy Mới

### 1. Clone dự án về máy
```bash
git clone https://github.com/huusei1234-droid/EDITVIDEO.git
cd EDITVIDEO
```

### 2. Sử dụng Công cụ CapCut Pro Engine
- **Kiểm tra sức khỏe & nhịp cắt dự án CapCut (`audit`)**:
  ```bash
  python .agents/skills/capcut-pro-editor/scripts/capcut_pro_engine.py audit "<Tên_Dự_Án_CapCut>"
  ```
- **Tự động nâng cấp dự án theo chuẩn Pro DNA (`upgrade`)**:
  ```bash
  python .agents/skills/capcut-pro-editor/scripts/capcut_pro_engine.py upgrade "<Tên_Dự_Án_CapCut>"
  ```

### 3. Nâng cấp & Đồng bộ dự án TVC WinHair
```bash
python scripts/upgrade_tvc_copy.py
python scripts/sync_capcut_cache_files.py
python scripts/verify_tvc_copy.py
```
