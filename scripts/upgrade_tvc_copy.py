import os
import json
import copy
import uuid
import shutil

PROJ_DIR = r"C:\Users\Hang thu\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\TVC WinHair CS2 - ban Reels_v2 (1)-sao chép"
MAIN_JSON = os.path.join(PROJ_DIR, "draft_content.json")
TIMELINE_JSON = os.path.join(PROJ_DIR, "Timelines", "C8D29776-5FFB-4dd3-8698-E26DA5C9C410", "draft_content.json")
OLD_V2_JSON = r"C:\Users\Hang thu\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\TVC WinHair CS2 - ban Reels_v2\draft_content.json"

def new_id():
    return str(uuid.uuid4()).upper()

def s2us(sec):
    # snap to nearest frame at 30fps (33333.333 us)
    frames = round(sec * 30.0)
    return int(round(frames * 1000000.0 / 30.0))

def main():
    # 1. Backup original files if backup doesn't exist yet
    bak_main = MAIN_JSON + ".bak_before_ai"
    if not os.path.exists(bak_main):
        shutil.copy2(MAIN_JSON, bak_main)
        print(f"Backed up {MAIN_JSON} -> {bak_main}")
    if os.path.exists(TIMELINE_JSON):
        bak_tl = TIMELINE_JSON + ".bak_before_ai"
        if not os.path.exists(bak_tl):
            shutil.copy2(TIMELINE_JSON, bak_tl)
            print(f"Backed up {TIMELINE_JSON} -> {bak_tl}")

    # Load from clean backup so script is idempotent
    with open(bak_main, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(OLD_V2_JSON, "r", encoding="utf-8") as f:
        old_v2 = json.load(f)

    # Grab authentic templates from old_v2 and data
    tier1_text_tpl = old_v2["materials"]["texts"][0]
    tier2_text_tpl = None
    for tx in old_v2["materials"]["texts"]:
        if "Nơi phong độ" in tx.get("content", ""):
            tier2_text_tpl = tx
            break

    text_seg_tpl = None
    for t in data["tracks"]:
        if t["type"] == "text" and t["segments"]:
            text_seg_tpl = t["segments"][0]
            break

    audio_seg_tpl = None
    for t in data["tracks"]:
        if t["type"] == "audio" and t["segments"]:
            audio_seg_tpl = t["segments"][0]
            break

    audio_mat_tpl = None
    for au in data["materials"]["audios"]:
        if au.get("type") == "sound":
            audio_mat_tpl = au
            break

    # Map materials for quick lookup
    vid_mats = {m["id"]: m for m in data["materials"]["videos"]}
    aud_mats = {m["id"]: m for m in data["materials"]["audios"]}
    fade_mats = {m["id"]: m for m in data["materials"].get("audio_fades", [])}

    # Helper to add an audio_fade to a segment
    def ensure_audio_fade(seg, fade_in_us=33333, fade_out_us=66666, force_update=False):
        existing_fade_id = None
        for ref in seg.get("extra_material_refs", []):
            if ref in fade_mats:
                existing_fade_id = ref
                break
        if existing_fade_id:
            if force_update:
                fade_mats[existing_fade_id]["fade_in_duration"] = fade_in_us
                fade_mats[existing_fade_id]["fade_out_duration"] = fade_out_us
            return existing_fade_id
        fid = new_id()
        fade_obj = {
            "id": fid,
            "type": "audio_fade",
            "fade_type": 0,
            "fade_in_duration": fade_in_us,
            "fade_out_duration": fade_out_us,
        }
        data["materials"]["audio_fades"].append(fade_obj)
        fade_mats[fid] = fade_obj
        seg["extra_material_refs"].append(fid)
        return fid

    # Helper to add ScaleX & ScaleY keyframes (Ken Burns micro-zoom)
    def add_micro_zoom_kf(seg, s_start, s_end):
        dur = seg["target_timerange"]["duration"]
        kf_x = {
            "id": new_id(),
            "material_id": "",
            "property_type": "KFTypeScaleX",
            "keyframe_list": [
                {
                    "id": new_id(),
                    "curveType": "Line",
                    "time_offset": 0,
                    "left_control": {"x": 0.0, "y": 0.0},
                    "right_control": {"x": 0.0, "y": 0.0},
                    "values": [s_start],
                    "string_value": "",
                    "graphID": "",
                },
                {
                    "id": new_id(),
                    "curveType": "Line",
                    "time_offset": dur,
                    "left_control": {"x": 0.0, "y": 0.0},
                    "right_control": {"x": 0.0, "y": 0.0},
                    "values": [s_end],
                    "string_value": "",
                    "graphID": "",
                },
            ],
        }
        kf_y = copy.deepcopy(kf_x)
        kf_y["id"] = new_id()
        kf_y["property_type"] = "KFTypeScaleY"
        kf_y["keyframe_list"][0]["id"] = new_id()
        kf_y["keyframe_list"][1]["id"] = new_id()
        seg["common_keyframes"].extend([kf_x, kf_y])

    # =========================================================================
    # STEP 1: FIX VISUAL & AUDIO ISSUES ON VIDEO TRACKS (TRACKS 00 - 05)
    # =========================================================================
    track0 = data["tracks"][0]
    track1 = data["tracks"][1]
    track2 = data["tracks"][2]

    # 1A. Fix 8-frame glitch at Track 00 #055 (index 54, 01:44.37..01:44.63, C0324.MP4)
    seg_55 = track0["segments"][54]
    seg_55["clip"]["scale"] = {"x": 1.18, "y": 1.18}
    seg_55["clip"]["transform"] = {"x": 0.18, "y": 0.0}
    # Also extend Track 02 #008 (index 7, C0324.MP4 at 01:43.30..01:44.37) by 266667 us to cover 01:44.63
    if len(track2["segments"]) > 7:
        t2_s8 = track2["segments"][7]
        t2_s8["target_timerange"]["duration"] += 266667
        if t2_s8.get("source_timerange"):
            t2_s8["source_timerange"]["duration"] += 266667

    # 1B. Clean up unwanted raw audio on Track 00 (Partículas douradas, drone, B-roll)
    # Keep intentional ASMR (#076, #077 -> indices 75, 76, C9476.MP4 at vol=1.22)
    # Keep Customer & KOC Interviews (#083..#138 -> indices 82..137)
    for idx, seg in enumerate(track0["segments"]):
        mat = vid_mats.get(seg["material_id"], {})
        fname = os.path.basename(mat.get("path", ""))
        if 82 <= idx <= 137:
            # Interview section: normalize C9601 volume from 1.75 -> 1.42 so it doesn't distort,
            # boost quieter interviews slightly to 1.25, and add micro-fade to prevent clicks!
            if "C9601" in fname:
                seg["volume"] = 1.42
            elif seg["volume"] <= 1.05:
                seg["volume"] = 1.25
            ensure_audio_fade(seg, 33333, 66666)
        elif idx in (75, 76):
            # Intentional ASMR hair wash / massage clips (vol = 1.22)
            ensure_audio_fade(seg, 66666, 66666)
        else:
            # Mute raw camera noise / particle overlay audio on all other Track 00 B-roll shots
            seg["volume"] = 0.0

    # Mute raw camera noise on B-roll overlay tracks (Tracks 01 - 05)
    for t_idx in range(1, 6):
        for seg in data["tracks"][t_idx]["segments"]:
            seg["volume"] = 0.0

    # 1C. Fix Jump-Cut Fatigue in Interview Section (indices 82..137, 02:32.63..04:54.80)
    # Alternate punch-in / punch-out scales and subtle Y position on consecutive cuts of same camera,
    # and add Ken Burns micro-zoom to long static takes (#116 and #117, indices 115 & 116).
    punch_toggle = False
    prev_cam = None
    for idx in range(82, 138):
        seg = track0["segments"][idx]
        mat = vid_mats.get(seg["material_id"], {})
        fname = os.path.basename(mat.get("path", ""))
        dur_s = seg["target_timerange"]["duration"] / 1e6

        if fname != prev_cam:
            punch_toggle = False
            prev_cam = fname
        else:
            punch_toggle = not punch_toggle

        if "C9599" in fname:
            sc = 1.20 if punch_toggle else 1.11
            py = -0.02 if punch_toggle else 0.0
            seg["clip"]["scale"] = {"x": sc, "y": sc}
            seg["clip"]["transform"] = {"x": 0.0, "y": py}
        elif "C9601" in fname:
            sc = 1.31 if punch_toggle else 1.20
            py = -0.03 if punch_toggle else 0.0
            seg["clip"]["scale"] = {"x": sc, "y": sc}
            seg["clip"]["transform"] = {"x": 0.0, "y": py}
        elif "C9608" in fname:
            sc = 1.21 if punch_toggle else 1.10
            py = -0.025 if punch_toggle else 0.0
            seg["clip"]["scale"] = {"x": sc, "y": sc}
            seg["clip"]["transform"] = {"x": 0.0, "y": py}
        elif "C9609" in fname:
            # Customer 4 has 2 very long cuts (#116: 8.53s, #117: 11.77s) -> add smooth Ken Burns micro-zoom!
            if idx == 115:  # 8.53s
                add_micro_zoom_kf(seg, 1.10, 1.18)
            elif idx == 116:  # 11.77s
                add_micro_zoom_kf(seg, 1.18, 1.10)
            else:
                seg["clip"]["scale"] = {"x": 1.14, "y": 1.14}
        elif "C9622" in fname:
            sc = 1.10 if punch_toggle else 1.00
            py = -0.02 if punch_toggle else 0.0
            seg["clip"]["scale"] = {"x": sc, "y": sc}
            seg["clip"]["transform"] = {"x": 0.0, "y": py}

    # 1D. Add 3 B-roll cutaway overlays on Track 01 over the rapid-fire jump-cut clusters in the interviews:
    #   - Cluster 1: 02:53.87 .. 02:58.23 (4.37s) during C9601 rapid cuts -> use Track 00 #008 (C9496.MP4) or #044 (C9568.MP4)
    #   - Cluster 2: 03:15.27 .. 03:19.63 (4.37s) during C9608 0.40s rapid cuts -> use Track 00 #062 (C9549.MP4)
    #   - Cluster 3: 03:37.50 .. 03:42.50 (5.00s) in the middle of C9609's 11.77s static take -> use Track 00 #012 (C9527.MP4)
    broll_template = copy.deepcopy(track1["segments"][-1])  # clone from user's own B-roll segment on Track 01
    broll_donors = [
        (track0["segments"][43], s2us(173.866), s2us(4.367)),   # 02:53.87 .. 02:58.23 (C9568.MP4)
        (track0["segments"][61], s2us(195.266), s2us(4.367)),   # 03:15.27 .. 03:19.63 (C9549.MP4)
        (track0["segments"][11], s2us(217.500), s2us(5.000)),   # 03:37.50 .. 03:42.50 (C9527.MP4)
    ]
    for donor_seg, target_st, target_du in broll_donors:
        new_broll = copy.deepcopy(broll_template)
        new_broll["id"] = new_id()
        new_broll["material_id"] = donor_seg["material_id"]
        src_st = donor_seg["source_timerange"]["start"] if donor_seg.get("source_timerange") else 0
        new_broll["source_timerange"] = {"start": src_st, "duration": target_du}
        new_broll["target_timerange"] = {"start": target_st, "duration": target_du}
        new_broll["volume"] = 0.0
        new_broll["speed"] = 1.0
        new_broll["clip"]["scale"] = {"x": 1.04, "y": 1.04}
        new_broll["clip"]["transform"] = {"x": 0.0, "y": 0.0}
        new_broll["common_keyframes"] = []
        add_micro_zoom_kf(new_broll, 1.00, 1.06)
        track1["segments"].append(new_broll)
    track1["segments"].sort(key=lambda s: s["target_timerange"]["start"])

    # 1E. Add subtle Ken Burns Micro-Zoom (1.00 -> 1.06) to long static shots (> 2.4s) in Part A & Part C on Track 00
    zoom_dir = True
    for idx, seg in enumerate(track0["segments"]):
        if (2 <= idx <= 81) or (138 <= idx <= 148):
            dur_s = seg["target_timerange"]["duration"] / 1e6
            if dur_s >= 2.4 and not seg.get("common_keyframes"):
                cur_sc = seg["clip"]["scale"]["x"]
                if abs(cur_sc - 1.0) < 0.02:
                    if zoom_dir:
                        add_micro_zoom_kf(seg, 1.00, 1.06)
                    else:
                        add_micro_zoom_kf(seg, 1.06, 1.00)
                    zoom_dir = not zoom_dir

    # =========================================================================
    # STEP 2: ADD 2-TIER TVC RUNNING TEXT + STAGGERED ANIMATIONS
    # =========================================================================
    ANIM_CATALOG = {
        "bui_vang": {
            "id": "7331632775948145153",
            "type": "in",
            "start": 0,
            "duration": 700000,
            "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7331632775948145153/25d1da238cd78c05757f2d6036dec895",
            "platform": "all",
            "resource_id": "7331632775948145153",
            "third_resource_id": "7331632775948145153",
            "source_platform": 1,
            "name": "Bụi vàng",
            "category_id": "ruchang",
            "category_name": "Vào",
            "panel": "",
            "material_type": "sticker",
            "anim_adjust_params": None,
            "request_id": "",
        },
        "chu_mo_dan": {
            "id": "7648937403646004500",
            "type": "in",
            "start": 0,
            "duration": 700000,
            "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7648937403646004500/495e55b3bcd1f6420b6e4b1b44ed1fc8",
            "platform": "all",
            "resource_id": "7648937403646004500",
            "third_resource_id": "0",
            "source_platform": 1,
            "name": "Chữ mờ dần hiện vào",
            "category_id": "ruchang",
            "category_name": "text",
            "panel": "",
            "material_type": "sticker",
            "anim_adjust_params": None,
            "request_id": "",
        },
        "mo": {
            "id": "6923135604519604737",
            "type": "in",
            "start": 0,
            "duration": 666666,
            "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/6923135604519604737/a5f4d3998c0648ec65c03251506bd0a0",
            "platform": "all",
            "resource_id": "6923135604519604737",
            "third_resource_id": "6923135604519604737",
            "source_platform": 1,
            "name": "Mờ",
            "category_id": "ruchang",
            "category_name": "text",
            "panel": "",
            "material_type": "sticker",
            "anim_adjust_params": None,
            "request_id": "",
        },
    }

    def make_text_seg(text_str, start_s, end_s, tier=1, anim_key="chu_mo_dan", pos_y=None, font_size=None):
        st_us = s2us(start_s)
        du_us = s2us(end_s - start_s)
        mat = copy.deepcopy(tier1_text_tpl if tier == 1 else tier2_text_tpl)
        mat["id"] = new_id()
        if mat.get("fonts"):
            mat["fonts"][0]["id"] = new_id()

        c_obj = json.loads(mat["content"])
        c_obj["text"] = text_str
        c_obj["styles"][0]["range"] = [0, len(text_str)]
        if font_size is not None:
            c_obj["styles"][0]["size"] = font_size
            mat["font_size"] = float(font_size)
        mat["content"] = json.dumps(c_obj, ensure_ascii=False)
        data["materials"]["texts"].append(mat)

        # Create sticker_animation material
        anim_mat_id = new_id()
        anim_item = copy.deepcopy(ANIM_CATALOG[anim_key])
        anim_mat = {
            "id": anim_mat_id,
            "type": "sticker_animation",
            "animations": [anim_item],
            "multi_language_current": "none",
        }
        data["materials"]["material_animations"].append(anim_mat)

        seg = copy.deepcopy(text_seg_tpl)
        seg["id"] = new_id()
        seg["material_id"] = mat["id"]
        seg["target_timerange"] = {"start": st_us, "duration": du_us}
        seg["clip"]["scale"] = {"x": 1.0, "y": 1.0}
        default_y = -0.42 if tier == 1 else -0.64
        seg["clip"]["transform"] = {"x": 0.0, "y": pos_y if pos_y is not None else default_y}
        seg["extra_material_refs"] = [anim_mat_id]

        # Add smooth Alpha fade-out keyframe over the last 0.40s (400,000 us) so text exits gracefully
        fade_out_len = min(400000, du_us // 3)
        kf_alpha = {
            "id": new_id(),
            "material_id": "",
            "property_type": "KFTypeAlpha",
            "keyframe_list": [
                {
                    "id": new_id(),
                    "curveType": "Line",
                    "time_offset": du_us - fade_out_len,
                    "left_control": {"x": 0.0, "y": 0.0},
                    "right_control": {"x": 0.0, "y": 0.0},
                    "values": [1.0],
                    "string_value": "",
                    "graphID": "",
                },
                {
                    "id": new_id(),
                    "curveType": "Line",
                    "time_offset": du_us,
                    "left_control": {"x": 0.0, "y": 0.0},
                    "right_control": {"x": 0.0, "y": 0.0},
                    "values": [0.0],
                    "string_value": "",
                    "graphID": "",
                },
            ],
        }
        seg["common_keyframes"] = [kf_alpha]
        return seg

    # Define the complete 2-Tier TVC Text Plan across 00:00 .. 05:33
    # Format: (start_s, end_s, tier1_title, anim1, [(sub_start_s, sub_end_s, tier2_sub), ...], custom_y1, custom_y2)
    TVC_SECTIONS = [
        (2.40, 12.40, "WIN HAIR SALON · CƠ SỞ 2", "bui_vang", [
            (2.65, 12.40, "Khu cắt tóc hiện đại · Nơi phong độ được tạo nên")
        ], None, None),
        (12.60, 22.30, "TẦNG 2 · KHÔNG GIAN VIP", "chu_mo_dan", [
            (12.85, 22.30, "Tách biệt khói bụi · Mọi ồn ào ở lại phía sau")
        ], None, None),
        (22.50, 37.30, "SOFA ĐỢI · GHẾ MASSAGE KINGSPORT", "chu_mo_dan", [
            (22.75, 29.90, "Thư giãn êm ái ngay từ lúc chờ"),
            (30.10, 37.30, "Nước cam · Trà chanh · Cà phê phục vụ miễn phí"),
        ], None, None),
        (37.60, 46.50, "5 PHÒNG RIÊNG BIỆT", "bui_vang", [
            (37.85, 46.50, "Không gian khép kín · Riêng tư trọn vẹn")
        ], None, None),
        (46.70, 55.50, "DỊCH VỤ TRỌN GÓI TRONG 1 PHÒNG", "chu_mo_dan", [
            (46.95, 55.50, "Gội đầu · Massage · Ráy tai không cần di chuyển")
        ], None, None),
        (58.30, 70.40, "TƯ VẤN & CẮT TÓC TẠO KIỂU", "chu_mo_dan", [
            (58.55, 70.40, "Lắng nghe kỹ chất tóc và khuôn mặt trước khi cầm kéo")
        ], None, None),
        (70.70, 80.00, "RÁY TAI ÊM ÁI · THƯ GIÃN SÂU", "bui_vang", [
            (70.95, 80.00, "Dụng cụ khử trùng · Nhẹ tay đến mức ngủ quên")
        ], None, None),
        (80.40, 90.40, "GỘI ĐẦU · RỬA MẶT · MASSAGE MẶT", "chu_mo_dan", [
            (80.65, 90.40, "Chăm sóc da mặt chuyên sâu · Căng thẳng cứ thế mà tan")
        ], None, None),
        (90.70, 99.80, "MASSAGE CỔ VAI GÁY · TAY · CHÂN", "chu_mo_dan", [
            (90.95, 99.80, "Ấn huyệt đúng điểm mỏi · Đánh thức năng lượng")
        ], None, None),
        (100.00, 104.30, "MASSAGE BODY ĐÁ NÓNG", "bui_vang", [
            (100.25, 104.30, "Nằm xuống nặng nề · Bước ra nhẹ tênh")
        ], None, None),
        (104.70, 115.90, "LÀM SẠCH MÓNG · ĐẮP MẶT NẠ · LỘT MỤN", "chu_mo_dan", [
            (104.95, 115.90, "Chỉn chu tới từng chi tiết · Da khỏe, mặt sáng")
        ], None, None),
        (116.20, 136.40, "KỸ THUẬT VIÊN CHUYÊN NGHIỆP", "bui_vang", [
            (116.45, 126.30, "Không cắt cho nhanh · Mà làm cho chuẩn"),
            (126.50, 136.40, "Tay nghề vững vàng · Phục vụ tận tâm"),
        ], None, None),
        (136.70, 152.20, "ĐẲNG CẤP PHỤC VỤ WIN HAIR", "bui_vang", [
            (136.95, 152.20, "Điểm hẹn thư giãn trọn vẹn dành riêng cho phái mạnh")
        ], None, None),
        # Part B: Customer & KOC Testimonials (02:32.63 .. 04:54.80)
        (152.80, 159.60, "TRẢI NGHIỆM THỰC TẾ", "bui_vang", [
            (153.05, 159.60, "Khách hàng nói gì sau khi trải nghiệm tại Win Hair?")
        ], None, None),
        (160.40, 188.50, "KHÁCH HÀNG THÂN THIẾT CHIA SẺ", "chu_mo_dan", [
            (160.65, 174.50, "\"Không gian rộng rãi, sạch sẽ · Nhân viên nhiệt tình, chu đáo\""),
            (174.70, 188.50, "\"Dịch vụ rất tốt · Chắc chắn sẽ giới thiệu bạn bè ghé trải nghiệm\""),
        ], None, None),
        (189.00, 205.30, "ĐÁNH GIÁ TỪ KHÁCH HÀNG", "chu_mo_dan", [
            (189.25, 205.30, "\"Combo gội đầu, massage, ráy tai quá êm · Giá cả cực kỳ hợp lý\"")
        ], None, None),
        (205.80, 228.50, "CẢM NHẬN SAU TRẢI NGHIỆM", "chu_mo_dan", [
            (206.05, 217.50, "\"Phòng VIP riêng tư · Kỹ thuật viên tay nghề cao, làm rất kỹ\""),
            (217.70, 228.50, "\"Từ cắt tóc đến massage đều chỉnh chu · Rất đáng tiền\""),
        ], None, None),
        (229.00, 255.00, "GÓC REVIEW THỰC TẾ", "bui_vang", [
            (229.25, 242.00, "Trải nghiệm thực tế dịch vụ cắt tóc & thư giãn tại Win Hair CS2"),
            (242.20, 255.00, "\"Một địa chỉ làm đẹp & thư giãn mà anh em Nha Trang không thể bỏ qua\""),
        ], None, None),
        # Part C: Combo Promotions & Outro (04:54.80 .. 05:33.13)
        # Note: 301.03..308.03 is the 4-corner split-screen + "CẮT - CẠO - RÁY - XẢ 129K", kept 100% clear!
        (294.90, 300.90, "ƯU ĐÃI GIỜ VÀNG 8H – 11H", "bui_vang", [
            (295.15, 300.90, "Thứ 2 đến Thứ 6 · Giảm 20% tất cả dịch vụ")
        ], None, None),
        (308.30, 317.40, "COMBO NGỦ TRƯA · CHỈ 79K", "chu_mo_dan", [
            (308.55, 317.40, "Gội đầu · Massage mặt 30 phút · Nạp lại năng lượng buổi trưa")
        ], None, None),
        (317.60, 324.10, "WIN HAIR SALON · PHONG ĐỘ ĐÀN ÔNG", "bui_vang", [
            (317.85, 324.10, "59 Thích Quảng Đức, Nha Trang · Hotline: 0333.45.45.46")
        ], None, None),
        (324.80, 332.30, "ĐẾN WIN HAIR NGAY ANH EM ƠI!", "bui_vang", [
            (325.05, 332.30, "59 Thích Quảng Đức, Nha Trang · Hotline: 0333.45.45.46")
        ], -0.58, -0.74),
    ]

    tier1_segs = []
    tier2_segs = []
    for st_s, en_s, t1_txt, anim1, subs, cy1, cy2 in TVC_SECTIONS:
        tier1_segs.append(make_text_seg(t1_txt, st_s, en_s, tier=1, anim_key=anim1, pos_y=cy1))
        for sub_st, sub_en, t2_txt in subs:
            tier2_segs.append(make_text_seg(t2_txt, sub_st, sub_en, tier=2, anim_key="mo", pos_y=cy2))

    track_text_tier1 = {
        "id": new_id(),
        "type": "text",
        "name": "",
        "attribute": 0,
        "flag": 0,
        "is_default_name": True,
        "segments": tier1_segs,
    }
    track_text_tier2 = {
        "id": new_id(),
        "type": "text",
        "name": "",
        "attribute": 0,
        "flag": 0,
        "is_default_name": True,
        "segments": tier2_segs,
    }

    # Insert the two new text tracks right after Track 09 (before Track 10 video compound clip & audio tracks)
    data["tracks"].insert(10, track_text_tier1)
    data["tracks"].insert(11, track_text_tier2)

    # =========================================================================
    # STEP 3: ADD SOUND EFFECTS (SFX) TRACK FROM CAPCUT CACHE & TLH\EDIT
    # =========================================================================
    SFX_LIBRARY = {
        "magic_reveal": {
            "name": "Magic reveal",
            "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/music/229f88e6452098f686f43df9309b1acc.mp3",
            "duration": 2033333,
            "type": "sound",
            "category_name": "heycan_search_sound",
        },
        "deep_woosh": {
            "name": "Deep woosh",
            "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/music/270677b49d33e1e347819050db9ee915.mp3",
            "duration": 3233333,
            "type": "sound",
            "category_name": "heycan_search_sound",
        },
        "pop_lower": {
            "name": "Pop (lower) telop sound etc",
            "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/music/d3b74afaf571dd3056bd7e9996a683cc.mp3",
            "duration": 166666,
            "type": "sound",
            "category_name": "heycan_search_sound",
        },
        "riser_metallic": {
            "name": "SFX - Riser Metallic (Transition) - YouTube.mp3",
            "path": "Z:/Máy tính khác/My Computer/Document HT Media/TLH/Edit/Sound Effect/SFX - Riser Metallic (Transition) - YouTube.mp3",
            "duration": 5250000,
            "type": "extract_music",
            "category_name": "local",
        },
        "woosh_vshort": {
            "name": "Woosh vshort - chữ.mp3",
            "path": "Z:/Máy tính khác/My Computer/Document HT Media/TLH/Edit/Sound Effect/Woosh vshort - chữ.mp3",
            "duration": 533333,
            "type": "extract_music",
            "category_name": "local",
        },
        "woosh_chu": {
            "name": "Woosh - chữ.mp3",
            "path": "Z:/Máy tính khác/My Computer/Document HT Media/TLH/Edit/Sound Effect/Woosh - chữ.mp3",
            "duration": 666666,
            "type": "extract_music",
            "category_name": "local",
        },
        "noitifi_chu": {
            "name": "Noitifi - chữ.mp3",
            "path": "Z:/Máy tính khác/My Computer/Document HT Media/TLH/Edit/Sound Effect/Noitifi - chữ.mp3",
            "duration": 500000,
            "type": "extract_music",
            "category_name": "local",
        },
    }

    def make_sfx_seg(sfx_key, start_s, vol=0.45, src_start_s=0.0, dur_s=None, fade_in_us=33333, fade_out_us=66666):
        info = SFX_LIBRARY[sfx_key]
        mat = copy.deepcopy(audio_mat_tpl)
        mat["id"] = new_id()
        mat["name"] = info["name"]
        mat["path"] = info["path"]
        mat["duration"] = info["duration"]
        mat["type"] = info["type"]
        mat["category_name"] = info["category_name"]
        mat["effect_id"] = ""
        mat["music_id"] = new_id()
        data["materials"]["audios"].append(mat)

        st_us = s2us(start_s)
        src_st_us = s2us(src_start_s)
        du_us = s2us(dur_s) if dur_s is not None else (info["duration"] - src_st_us)

        # Create required extra_material_refs for an audio segment
        sp_id = new_id()
        data["materials"]["speeds"].append({"id": sp_id, "type": "speed", "mode": 0, "speed": 1.0, "curve_speed": None})
        pi_id = new_id()
        data["materials"]["placeholder_infos"].append({"id": pi_id, "type": "placeholder_info", "meta_type": "none", "res_path": "", "res_text": "", "error_path": "", "error_text": ""})
        bt_id = new_id()
        data["materials"]["beats"].append({"id": bt_id, "type": "beats", "enable_ai_beats": False, "gear": 404, "gear_count": 0, "mode": 404, "user_beats": [], "user_delete_ai_beats": None, "ai_beats": {"melody_url": "", "melody_path": "", "beats_url": "", "beats_path": "", "melody_percents": [0.0], "beat_speed_infos": []}})
        sc_id = new_id()
        data["materials"]["sound_channel_mappings"].append({"id": sc_id, "type": "", "audio_channel_mapping": 0, "is_config_open": False})
        vs_id = new_id()
        data["materials"]["vocal_separations"].append({"id": vs_id, "type": "vocal_separation", "choice": 0, "removed_sounds": [], "time_range": None, "production_path": "", "final_algorithm": "", "enter_from": ""})
        fd_id = new_id()
        data["materials"]["audio_fades"].append({"id": fd_id, "type": "audio_fade", "fade_type": 0, "fade_in_duration": fade_in_us, "fade_out_duration": fade_out_us})

        seg = copy.deepcopy(audio_seg_tpl)
        seg["id"] = new_id()
        seg["material_id"] = mat["id"]
        seg["source_timerange"] = {"start": src_st_us, "duration": du_us}
        seg["target_timerange"] = {"start": st_us, "duration": du_us}
        seg["volume"] = vol
        seg["last_nonzero_volume"] = vol
        seg["extra_material_refs"] = [sp_id, pi_id, bt_id, sc_id, vs_id, fd_id]
        seg["common_keyframes"] = []
        return seg

    # Carefully curated non-overlapping SFX placements across the 5m33s timeline:
    sfx_events = [
        # Opening Flycam Riser + First Title Woosh
        ("riser_metallic", 0.00, 0.38, 3.00, 2.25, 300000, 150000),
        ("woosh_vshort", 2.40, 0.45, 0.0, None, 33333, 66666),
        # Section transitions & Text reveals in Part A
        ("woosh_chu", 12.57, 0.42, 0.0, None, 33333, 66666),
        ("noitifi_chu", 22.47, 0.38, 0.0, None, 33333, 66666),
        ("woosh_vshort", 30.10, 0.36, 0.0, None, 33333, 66666),
        ("magic_reveal", 37.47, 0.46, 0.0, None, 33333, 150000),
        ("woosh_vshort", 46.70, 0.40, 0.0, None, 33333, 66666),
        ("woosh_chu", 58.30, 0.40, 0.0, None, 33333, 66666),
        ("noitifi_chu", 80.40, 0.38, 0.0, None, 33333, 66666),
        # Staggered Multi-Screen Pop-ins during Massage Showcase (01:31.63, 01:33.23, 01:34.07)
        ("pop_lower", 91.63, 0.52, 0.0, None, 10000, 33333),
        ("pop_lower", 93.23, 0.52, 0.0, None, 10000, 33333),
        ("pop_lower", 94.07, 0.52, 0.0, None, 10000, 33333),
        ("woosh_vshort", 104.70, 0.42, 0.0, None, 33333, 66666),
        ("woosh_chu", 116.20, 0.42, 0.0, None, 33333, 66666),
        ("magic_reveal", 136.70, 0.44, 0.0, None, 33333, 150000),
        # Act 1 -> Act 2 Transition Riser (02:30.00 -> 02:32.63) + Title Woosh
        ("riser_metallic", 150.00, 0.40, 2.50, 2.75, 400000, 150000),
        ("woosh_vshort", 152.80, 0.44, 0.0, None, 33333, 66666),
        # Subtle Text Entry Accents for Customer & KOC Testimonials
        ("noitifi_chu", 160.40, 0.36, 0.0, None, 33333, 66666),
        ("woosh_vshort", 189.00, 0.36, 0.0, None, 33333, 66666),
        ("woosh_vshort", 205.80, 0.36, 0.0, None, 33333, 66666),
        ("woosh_chu", 229.00, 0.38, 0.0, None, 33333, 66666),
        # Act 3: Combo Promotions & 4-Corner Split Grid & Final Logo Reveal
        ("magic_reveal", 294.80, 0.48, 0.0, None, 33333, 150000),
        ("pop_lower", 301.03, 0.50, 0.0, None, 10000, 33333),
        ("pop_lower", 301.40, 0.50, 0.0, None, 10000, 33333),
        ("noitifi_chu", 308.30, 0.42, 0.0, None, 33333, 66666),
        ("woosh_chu", 317.60, 0.42, 0.0, None, 33333, 66666),
        ("riser_metallic", 321.80, 0.42, 2.50, 2.50, 400000, 150000),
        ("magic_reveal", 324.33, 0.55, 0.0, None, 33333, 200000),
    ]

    sfx_segs = [make_sfx_seg(*ev) for ev in sfx_events]
    track_sfx_pro = {
        "id": new_id(),
        "type": "audio",
        "name": "",
        "attribute": 0,
        "flag": 0,
        "is_default_name": True,
        "segments": sfx_segs,
    }
    data["tracks"].append(track_sfx_pro)

    # =========================================================================
    # STEP 4: ADD MICRO-FADES TO VOICEOVER (Clip ghép13) & SMOOTH OUTRO BGM FADE
    # =========================================================================
    for t in data["tracks"]:
        if t["type"] == "audio":
            for seg in t["segments"]:
                mat = aud_mats.get(seg["material_id"], {})
                name = mat.get("name", "")
                if "Clip ghép13" in name:
                    ensure_audio_fade(seg, 33333, 66666)
                elif "Cinematic Epic Music" in name and seg["target_timerange"]["start"] > s2us(300):
                    # Final BGM segment ending at 05:32.90 -> smooth 1.5s fade-out
                    ensure_audio_fade(seg, 100000, 1500000, force_update=True)

    # Update track_render_index on all segments to match their track index
    for t_idx, trk in enumerate(data["tracks"]):
        for seg in trk.get("segments", []):
            seg["track_render_index"] = t_idx

    # Save to both root draft_content.json and Timelines/.../draft_content.json
    with open(MAIN_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"Saved upgraded project to {MAIN_JSON}")

    if os.path.exists(TIMELINE_JSON):
        with open(TIMELINE_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        print(f"Synced upgraded project to {TIMELINE_JSON}")

    print(f"Total tracks: {len(data['tracks'])}")
    print(f"Tier 1 Titles added: {len(tier1_segs)} | Tier 2 Subtitles added: {len(tier2_segs)} | Pro SFX added: {len(sfx_segs)}")

if __name__ == "__main__":
    main()
