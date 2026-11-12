import os
import json
import copy
import uuid
import shutil
import time

DRAFTS_ROOT = r"C:\Users\Hang thu\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft"
TEMPLATE_PROJ = os.path.join(DRAFTS_ROOT, "ĐIỀU KINH 1-sao chép")
TARGET_NAME = "LT PLUS HẰNG THU - Video Mẫu"
TARGET_PROJ = os.path.join(DRAFTS_ROOT, TARGET_NAME)

DONOR_V2_JSON = os.path.join(DRAFTS_ROOT, "TVC WinHair CS2 - ban Reels_v2", "draft_content.json")
DONOR_REELS_JSON = os.path.join(DRAFTS_ROOT, "TVC WinHair CS2 - ban Reels_v2 (1)-sao chép", "draft_content.json")

SCENE_DIR = r"d:\antigraviti\lt_plus_hang_thu\05_Scene_Keyframes"
PROD_DIR = r"d:\antigraviti\lt_plus_hang_thu\02_AssetBoard_Products"
VO_DIR = r"d:\antigraviti\lt_plus_hang_thu\06_Audio_Voiceover"


def new_id():
    return str(uuid.uuid4()).upper()


def s2us(sec):
    frames = round(sec * 30.0)
    return int(round(frames * 1000000.0 / 30.0))


def main():
    if os.path.exists(TARGET_PROJ):
        shutil.rmtree(TARGET_PROJ)
    shutil.copytree(TEMPLATE_PROJ, TARGET_PROJ)

    main_json = os.path.join(TARGET_PROJ, "draft_content.json")
    meta_json = os.path.join(TARGET_PROJ, "draft_meta_info.json")
    bak_file = main_json + ".bak_before_ai"
    if os.path.exists(bak_file):
        os.remove(bak_file)

    with open(main_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(DONOR_V2_JSON, "r", encoding="utf-8") as f:
        donor_v2 = json.load(f)
    with open(DONOR_REELS_JSON, "r", encoding="utf-8") as f:
        donor_reels = json.load(f)

    vid_seg_tpl = copy.deepcopy(data["tracks"][0]["segments"][0])
    aud_seg_tpl = next(copy.deepcopy(t["segments"][0]) for t in data["tracks"] if t["type"] == "audio" and t["segments"])
    vid_mat_tpl = copy.deepcopy(data["materials"]["videos"][0])
    vo_mat_tpl = copy.deepcopy(data["materials"]["audios"][0])

    tier1_text_tpl = copy.deepcopy(donor_v2["materials"]["texts"][0])
    tier2_text_tpl = next(
        copy.deepcopy(tx) for tx in donor_v2["materials"]["texts"] if "Nơi phong độ" in tx.get("content", "")
    )
    text_seg_tpl = next(
        copy.deepcopy(t["segments"][0]) for t in donor_reels["tracks"] if t["type"] == "text" and t["segments"]
    )
    sfx_mat_tpl = next(
        copy.deepcopy(au) for au in donor_reels["materials"]["audios"] if au.get("type") == "sound"
    )

    for k in list(data["materials"].keys()):
        if isinstance(data["materials"][k], list):
            data["materials"][k] = []

    data["canvas_config"] = {"width": 1080, "height": 1920, "ratio": "9:16"}

    SHOT_FILES = [
        ("s01", os.path.join(SCENE_DIR, "SCENE_01_00s-04s_Hook_Qua_Tuoi_45.jpg")),
        ("s02", os.path.join(SCENE_DIR, "SCENE_02_04s-11s_Kho_Va_Kem_De_Chiu.jpg")),
        ("s03", os.path.join(SCENE_DIR, "SCENE_03_11s-17s_Bien_Dong_Hormone.jpg")),
        ("s04", os.path.join(SCENE_DIR, "SCENE_04_17s-23s_Lam_Sach_Va_Giu_Am.jpg")),
        ("s05a", os.path.join(SCENE_DIR, "SCENE_05_23s-32s_Hero_Hop_Hong_LT_Plus.jpg")),
        ("s05b", os.path.join(PROD_DIR, "PROD_02_LT_Plus_Hop_Mo_Khay_Lo_Ref.jpg")),
        ("s06", os.path.join(SCENE_DIR, "SCENE_06_32s-38s_Dap_Ung_Kep_Rang_Ro.jpg")),
        ("s07", os.path.join(SCENE_DIR, "SCENE_07_38s-43s_Loi_Khuyen_Tham_Kham.jpg")),
        ("s08", os.path.join(SCENE_DIR, "SCENE_08_43s-47s_EndCard_CTA_LT_PLUS.jpg")),
    ]

    photo_ids = {}
    for key, fpath in SHOT_FILES:
        pm = copy.deepcopy(vid_mat_tpl)
        pm["id"] = new_id()
        pm["unique_id"] = uuid.uuid4().hex
        pm["type"] = "photo"
        pm["duration"] = 10800000000
        pm["has_audio"] = False
        pm["width"] = 1080
        pm["height"] = 1920
        pm["path"] = fpath.replace("\\", "/")
        pm["material_name"] = os.path.basename(fpath)
        pm["local_material_id"] = str(uuid.uuid4())
        data["materials"]["videos"].append(pm)
        photo_ids[key] = pm["id"]

    TRANSITION_CATALOG = {
        "ket_hop": {
            "type": "transition",
            "name": "Kết hợp",
            "effect_id": "6724845717472416269",
            "resource_id": "6724845717472416269",
            "third_resource_id": "6724845717472416269",
            "source_platform": 1,
            "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/6724845717472416269/7b53f4c008c4c684fccf8c7d4d46cc92",
            "duration": 400000,
            "is_overlap": True,
            "platform": "all",
            "category_id": "123456",
            "category_name": "Chuyển tiếp",
            "request_id": "",
            "is_ai_transition": False,
            "video_path": "",
            "task_id": "",
        }
    }

    TEXT_ANIM_CATALOG = {
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
        "xoay_lap_lanh": {
            "id": "7573604214547516673",
            "type": "in",
            "start": 0,
            "duration": 700000,
            "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7573604214547516673/73345dbbf45dd954f98b5561f8edbff1",
            "platform": "all",
            "resource_id": "7573604214547516673",
            "third_resource_id": "0",
            "source_platform": 1,
            "name": "Xoay lấp lánh",
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
            "duration": 650000,
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
            "duration": 450000,
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

    AUDIO_LIBRARY = {
        "bgm_spa": {
            "name": "Relaxing Spa Music",
            "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/music/9689a2a9b0378b67a2d3e355049f6b74.mp3",
            "duration": 60000000,
            "type": "music",
            "category_name": "heycan_search_music",
        },
        "bgm_fresh_comfort": {
            "name": "欢快 清新 综艺",
            "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/music/358f869c8ad98d0d8cf11c7ed1ab277d.mp3",
            "duration": 101500000,
            "type": "music",
            "category_name": "heycan_search_music",
        },
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
        "woosh_vshort": {
            "name": "Woosh vshort - chữ.mp3",
            "path": "Z:/Máy tính khác/My Computer/Document HT Media/TLH/Edit/Sound Effect/Woosh vshort - chữ.mp3",
            "duration": 533333,
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

    def add_micro_zoom_kf(seg, s_start, s_end):
        dur = seg["target_timerange"]["duration"]
        kf_x = {
            "id": new_id(),
            "material_id": "",
            "property_type": "KFTypeScaleX",
            "keyframe_list": [
                {"id": new_id(), "curveType": "Line", "time_offset": 0, "left_control": {"x": 0.0, "y": 0.0}, "right_control": {"x": 0.0, "y": 0.0}, "values": [s_start], "string_value": "", "graphID": ""},
                {"id": new_id(), "curveType": "Line", "time_offset": dur, "left_control": {"x": 0.0, "y": 0.0}, "right_control": {"x": 0.0, "y": 0.0}, "values": [s_end], "string_value": "", "graphID": ""},
            ],
        }
        kf_y = copy.deepcopy(kf_x)
        kf_y["id"] = new_id()
        kf_y["property_type"] = "KFTypeScaleY"
        kf_y["keyframe_list"][0]["id"] = new_id()
        kf_y["keyframe_list"][1]["id"] = new_id()
        seg["common_keyframes"].extend([kf_x, kf_y])

    def make_photo_seg(shot_key, st_s, en_s, sc_start=1.02, sc_end=1.08, tr_key=None):
        st_us = s2us(st_s)
        du_us = s2us(en_s) - st_us
        sp_id, pi_id, cv_id, sc_id, mc_id, vs_id = new_id(), new_id(), new_id(), new_id(), new_id(), new_id()
        data["materials"]["speeds"].append({"id": sp_id, "type": "speed", "mode": 0, "speed": 1.0, "curve_speed": None})
        data["materials"]["placeholder_infos"].append({"id": pi_id, "type": "placeholder_info", "meta_type": "none", "res_path": "", "res_text": "", "error_path": "", "error_text": ""})
        data["materials"]["canvases"].append({"id": cv_id, "type": "canvas_color", "color": "", "blur": 0.0, "image": "", "album_image": "", "image_id": "", "image_name": "", "source_platform": 0, "team_id": ""})
        data["materials"]["sound_channel_mappings"].append({"id": sc_id, "type": "", "audio_channel_mapping": 0, "is_config_open": False})
        data["materials"]["material_colors"].append({"id": mc_id, "is_color_clip": False, "is_gradient": False, "solid_color": "", "gradient_colors": [], "gradient_percents": [], "gradient_angle": 90.0, "width": 0.0, "height": 0.0})
        data["materials"]["vocal_separations"].append({"id": vs_id, "type": "vocal_separation", "choice": 0, "removed_sounds": [], "time_range": None, "production_path": "", "final_algorithm": "", "enter_from": ""})
        refs = [sp_id, pi_id, cv_id, sc_id, mc_id, vs_id]
        if tr_key:
            tr_obj = copy.deepcopy(TRANSITION_CATALOG[tr_key])
            tr_obj["id"] = new_id()
            data["materials"]["transitions"].append(tr_obj)
            refs.append(tr_obj["id"])
        seg = copy.deepcopy(vid_seg_tpl)
        seg["id"] = new_id()
        seg["material_id"] = photo_ids[shot_key]
        seg["source_timerange"] = {"start": 1000000, "duration": du_us}
        seg["target_timerange"] = {"start": st_us, "duration": du_us}
        seg["speed"] = 1.0
        seg["volume"] = 0.0
        seg["clip"]["scale"] = {"x": float(sc_start), "y": float(sc_start)}
        seg["clip"]["transform"] = {"x": 0.0, "y": 0.0}
        seg["uniform_scale"] = {"on": True, "value": float(sc_start)}
        seg["extra_material_refs"] = refs
        seg["common_keyframes"] = []
        add_micro_zoom_kf(seg, float(sc_start), float(sc_end))
        return seg

    def make_text_seg(text_str, start_s, end_s, tier=1, anim_key="chu_mo_dan", pos_y=0.62, font_size=13.5):
        st_us = s2us(start_s)
        du_us = s2us(end_s) - st_us
        mat = copy.deepcopy(tier1_text_tpl if tier == 1 else tier2_text_tpl)
        mat["id"] = new_id()
        if mat.get("fonts"):
            mat["fonts"][0]["id"] = new_id()
        c_obj = json.loads(mat["content"])
        c_obj["text"] = text_str
        c_obj["styles"][0]["range"] = [0, len(text_str)]
        c_obj["styles"][0]["size"] = float(font_size)
        mat["font_size"] = float(font_size)
        mat["content"] = json.dumps(c_obj, ensure_ascii=False)
        data["materials"]["texts"].append(mat)

        anim_mat_id = new_id()
        anim_item = copy.deepcopy(TEXT_ANIM_CATALOG[anim_key])
        anim_item["duration"] = min(anim_item["duration"], max(200000, du_us // 2))
        data["materials"]["material_animations"].append(
            {"id": anim_mat_id, "type": "sticker_animation", "animations": [anim_item], "multi_language_current": "none"}
        )

        seg = copy.deepcopy(text_seg_tpl)
        seg["id"] = new_id()
        seg["material_id"] = mat["id"]
        seg["target_timerange"] = {"start": st_us, "duration": du_us}
        seg["clip"]["scale"] = {"x": 1.0, "y": 1.0}
        seg["clip"]["transform"] = {"x": 0.0, "y": float(pos_y)}
        seg["extra_material_refs"] = [anim_mat_id]

        fade_out_len = min(366666, du_us // 3)
        seg["common_keyframes"] = [
            {
                "id": new_id(),
                "material_id": "",
                "property_type": "KFTypeAlpha",
                "keyframe_list": [
                    {"id": new_id(), "curveType": "Line", "time_offset": du_us - fade_out_len, "left_control": {"x": 0.0, "y": 0.0}, "right_control": {"x": 0.0, "y": 0.0}, "values": [1.0], "string_value": "", "graphID": ""},
                    {"id": new_id(), "curveType": "Line", "time_offset": du_us, "left_control": {"x": 0.0, "y": 0.0}, "right_control": {"x": 0.0, "y": 0.0}, "values": [0.0], "string_value": "", "graphID": ""},
                ],
            }
        ]
        return seg

    def make_audio_seg(mat_id, target_start_s, dur_s, src_start_s=0.0, vol=1.0, fade_in_us=33333, fade_out_us=66666):
        st_us = s2us(target_start_s)
        du_us = s2us(dur_s)
        src_st_us = s2us(src_start_s)
        sp_id, pi_id, bt_id, sc_id, vs_id, fd_id = new_id(), new_id(), new_id(), new_id(), new_id(), new_id()
        data["materials"]["speeds"].append({"id": sp_id, "type": "speed", "mode": 0, "speed": 1.0, "curve_speed": None})
        data["materials"]["placeholder_infos"].append({"id": pi_id, "type": "placeholder_info", "meta_type": "none", "res_path": "", "res_text": "", "error_path": "", "error_text": ""})
        data["materials"]["beats"].append({"id": bt_id, "type": "beats", "enable_ai_beats": False, "gear": 404, "gear_count": 0, "mode": 404, "user_beats": [], "user_delete_ai_beats": None, "ai_beats": {"melody_url": "", "melody_path": "", "beats_url": "", "beats_path": "", "melody_percents": [0.0], "beat_speed_infos": []}})
        data["materials"]["sound_channel_mappings"].append({"id": sc_id, "type": "", "audio_channel_mapping": 0, "is_config_open": False})
        data["materials"]["vocal_separations"].append({"id": vs_id, "type": "vocal_separation", "choice": 0, "removed_sounds": [], "time_range": None, "production_path": "", "final_algorithm": "", "enter_from": ""})
        data["materials"]["audio_fades"].append({"id": fd_id, "type": "audio_fade", "fade_type": 0, "fade_in_duration": int(fade_in_us), "fade_out_duration": int(fade_out_us)})

        seg = copy.deepcopy(aud_seg_tpl)
        seg["id"] = new_id()
        seg["material_id"] = mat_id
        seg["source_timerange"] = {"start": src_st_us, "duration": du_us}
        seg["target_timerange"] = {"start": st_us, "duration": du_us}
        seg["volume"] = float(vol)
        seg["last_nonzero_volume"] = float(vol)
        seg["extra_material_refs"] = [sp_id, pi_id, bt_id, sc_id, vs_id, fd_id]
        seg["common_keyframes"] = []
        return seg

    def register_local_vo(fname, dur_s):
        mat = copy.deepcopy(vo_mat_tpl)
        mat["id"] = new_id()
        mat["unique_id"] = uuid.uuid4().hex
        mat["name"] = fname
        mat["path"] = os.path.join(VO_DIR, fname).replace("\\", "/")
        mat["duration"] = s2us(dur_s)
        data["materials"]["audios"].append(mat)
        return mat["id"]

    def register_lib_audio(lib_key):
        info = AUDIO_LIBRARY[lib_key]
        mat = copy.deepcopy(sfx_mat_tpl)
        mat["id"] = new_id()
        mat["unique_id"] = uuid.uuid4().hex
        mat["name"] = info["name"]
        mat["path"] = info["path"]
        mat["duration"] = info["duration"]
        mat["type"] = info["type"]
        mat["category_name"] = info["category_name"]
        mat["effect_id"] = ""
        mat["music_id"] = new_id()
        data["materials"]["audios"].append(mat)
        return mat["id"]

    SHOT_PLAN = [
        ("s01", 0.00, 3.65, 1.02, 1.08, None),
        ("s02", 3.65, 9.75, 1.01, 1.10, "ket_hop"),
        ("s03", 9.75, 13.65, 1.02, 1.08, None),
        ("s04", 13.65, 18.90, 1.02, 1.08, "ket_hop"),
        ("s05a", 18.90, 23.25, 1.08, 1.02, "ket_hop"),
        ("s05b", 23.25, 26.70, 1.02, 1.08, None),
        ("s06", 26.70, 31.45, 1.02, 1.09, "ket_hop"),
        ("s07", 31.45, 36.20, 1.01, 1.07, None),
        ("s08", 36.20, 41.20, 1.03, 1.00, "ket_hop"),
    ]
    track0_segs = [make_photo_seg(*s) for s in SHOT_PLAN]

    CALLOUTS = [
        (0.10, 3.50, "QUA TUỔI 45+", "bui_vang", 0.64, 14.0, 0.35, 3.50, "Vì sao cảm giác khô rõ hơn?", 0.52, 9.5),
        (9.85, 13.50, "BIẾN ĐỘNG HORMONE", "chu_mo_dan", -0.34, 13.0, 10.10, 13.50, "Lượng dịch tự nhiên suy giảm", -0.46, 9.5),
        (13.75, 18.75, "CHĂM SÓC ĐỘ ẨM RIÊNG", "chu_mo_dan", -0.18, 13.0, 14.00, 18.75, "Chỉ chú ý làm sạch là chưa đủ", -0.30, 9.5),
        (19.00, 26.55, "LT PLUS HỘP HỒNG HẰNG THU", "xoay_lap_lanh", 0.64, 13.5, 19.25, 26.55, "Duy trì độ ẩm & pH · Làm sạch dịch nhầy", 0.52, 9.0),
        (26.80, 31.30, "TÁC ĐỘNG KÉP 2 TRONG 1", "bui_vang", -0.34, 13.5, 27.05, 31.30, "Đáp ứng cả làm sạch lẫn giữ ẩm", -0.46, 9.5),
        (36.30, 41.10, "NHẮN “LT PLUS”", "xoay_lap_lanh", 0.62, 15.0, 36.55, 41.10, "Tư vấn nhu cầu hỗ trợ độ ẩm của chị nhé!", 0.49, 9.5),
    ]
    tier1_segs = [make_text_seg(c[2], c[0], c[1], tier=1, anim_key=c[3], pos_y=c[4], font_size=c[5]) for c in CALLOUTS]
    tier2_segs = [make_text_seg(c[8], c[6], c[7], tier=2, anim_key="mo", pos_y=c[9], font_size=c[10]) for c in CALLOUTS]

    with open(os.path.join(VO_DIR, "vo_manifest.json"), "r", encoding="utf-8") as f:
        vo_manifest = json.load(f)

    vo_a, vo_b = [], []
    for idx, item in enumerate(vo_manifest["segments"]):
        fname = os.path.basename(item["path"])
        vid = register_local_vo(fname, item["duration_s"])
        seg = make_audio_seg(vid, item["start_s"], item["duration_s"], src_start_s=0.0, vol=1.35, fade_in_us=33333, fade_out_us=66666)
        (vo_a if idx % 2 == 0 else vo_b).append(seg)

    bgm_spa_id = register_lib_audio("bgm_spa")
    bgm_fresh_id = register_lib_audio("bgm_fresh_comfort")
    bgm_segs = [
        make_audio_seg(bgm_spa_id, 0.00, 18.90, src_start_s=0.00, vol=0.26, fade_in_us=300000, fade_out_us=500000),
        make_audio_seg(bgm_fresh_id, 18.90, 21.10, src_start_s=2.00, vol=0.30, fade_in_us=300000, fade_out_us=66666),
        make_audio_seg(bgm_fresh_id, 40.00, 1.20, src_start_s=23.10, vol=0.48, fade_in_us=66666, fade_out_us=700000),
    ]

    sfx_ids = {k: register_lib_audio(k) for k in ("woosh_vshort", "pop_lower", "magic_reveal", "deep_woosh", "noitifi_chu")}
    SFX_EVENTS = [
        ("woosh_vshort", 0.08, 0.50, 0.00, 0.42, 33333, 66666),
        ("pop_lower", 6.65, 0.16, 0.00, 0.44, 10000, 33333),
        ("magic_reveal", 18.90, 2.00, 0.00, 0.52, 33333, 166666),
        ("deep_woosh", 26.70, 1.80, 0.00, 0.38, 33333, 200000),
        ("magic_reveal", 36.22, 2.00, 0.00, 0.52, 33333, 200000),
        ("noitifi_chu", 36.60, 0.48, 0.00, 0.42, 33333, 66666),
    ]
    sfx_segs = [make_audio_seg(sfx_ids[k], t_st, dur_s, src_start_s=s_st, vol=vol, fade_in_us=fi, fade_out_us=fo) for k, t_st, dur_s, s_st, vol, fi, fo in SFX_EVENTS]

    def make_track(t_type, segs):
        return {"id": new_id(), "type": t_type, "name": "", "attribute": 0, "flag": 0, "is_default_name": True, "segments": segs}

    data["tracks"] = [
        make_track("video", track0_segs),
        make_track("text", tier1_segs),
        make_track("text", tier2_segs),
        make_track("audio", vo_a),
        make_track("audio", vo_b),
        make_track("audio", bgm_segs),
        make_track("audio", sfx_segs),
    ]

    for t_idx, trk in enumerate(data["tracks"]):
        for seg in trk["segments"]:
            seg["track_render_index"] = t_idx

    total_dur_us = s2us(41.20)
    data["duration"] = total_dur_us
    data["id"] = new_id()

    with open(main_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    tl_root = os.path.join(TARGET_PROJ, "Timelines")
    if os.path.exists(tl_root):
        for sub in os.listdir(tl_root):
            tl_dir = os.path.join(tl_root, sub)
            patch_dir = os.path.join(tl_dir, "attachment", "patch")
            if os.path.exists(patch_dir):
                shutil.rmtree(patch_dir)
            tl_json = os.path.join(tl_dir, "draft_content.json")
            if os.path.exists(tl_json):
                with open(tl_json, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False)

    now_us = int(time.time() * 1000000)
    if os.path.exists(meta_json):
        with open(meta_json, "r", encoding="utf-8") as f:
            meta = json.load(f)
        meta["draft_id"] = data["id"]
        meta["draft_name"] = TARGET_NAME
        meta["draft_fold_path"] = TARGET_PROJ.replace("\\", "/")
        meta["draft_root_path"] = DRAFTS_ROOT.replace("\\", "/")
        meta["draft_cover"] = os.path.join(SCENE_DIR, "SCENE_08_43s-47s_EndCard_CTA_LT_PLUS.jpg").replace("\\", "/")
        meta["tm_duration"] = total_dur_us
        meta["tm_draft_modified"] = now_us
        with open(meta_json, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False)

    # Also register in root_meta_info.json if present so CapCut home screen displays it immediately
    root_meta_path = os.path.join(DRAFTS_ROOT, "root_meta_info.json")
    if os.path.exists(root_meta_path):
        with open(root_meta_path, "r", encoding="utf-8") as f:
            rmeta = json.load(f)
        stores = rmeta.get("all_draft_store", [])
        stores = [s for s in stores if s.get("draft_name") != TARGET_NAME]
        if stores:
            entry = copy.deepcopy(stores[0])
            entry["draft_id"] = data["id"]
            entry["draft_name"] = TARGET_NAME
            entry["draft_fold_path"] = TARGET_PROJ.replace("\\", "/")
            entry["draft_json_file"] = main_json.replace("\\", "/")
            entry["draft_cover"] = os.path.join(SCENE_DIR, "SCENE_08_43s-47s_EndCard_CTA_LT_PLUS.jpg").replace("\\", "/")
            entry["tm_duration"] = total_dur_us
            entry["tm_draft_create"] = now_us
            entry["tm_draft_modified"] = now_us
            stores.insert(0, entry)
            rmeta["all_draft_store"] = stores
            with open(root_meta_path, "w", encoding="utf-8") as f:
                json.dump(rmeta, f, ensure_ascii=False)

    print(f"SUCCESS: Created CapCut project '{TARGET_NAME}' ({total_dur_us/1e6:.2f}s)!")


if __name__ == "__main__":
    main()
