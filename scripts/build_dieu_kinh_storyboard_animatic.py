import os
import json
import copy
import uuid
import shutil

PROJ_DIR = r"C:\Users\Hang thu\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\ĐIỀU KINH 1-sao chép"
MAIN_JSON = os.path.join(PROJ_DIR, "draft_content.json")
META_JSON = os.path.join(PROJ_DIR, "draft_meta_info.json")
TIMELINE_DIR = os.path.join(PROJ_DIR, "Timelines", "EDFEB15A-2B91-4b7a-A32A-DF48A6E5FA3E")
TIMELINE_JSON = os.path.join(TIMELINE_DIR, "draft_content.json")
PATCH_DIR = os.path.join(TIMELINE_DIR, "attachment", "patch")

DONOR_V2_JSON = r"C:\Users\Hang thu\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\TVC WinHair CS2 - ban Reels_v2\draft_content.json"
DONOR_REELS_JSON = r"C:\Users\Hang thu\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\TVC WinHair CS2 - ban Reels_v2 (1)-sao chép\draft_content.json"

SB_DIR = r"d:\antigraviti\storyboard_dieukinh_comfort\02_Storyboard_11_Shots"
FULL_VO_PATH = "C:/Users/Hang thu/Downloads/voicestudio-428a4d53.wav"


def new_id():
    return str(uuid.uuid4()).upper()


def s2us(sec):
    frames = round(sec * 30.0)
    return int(round(frames * 1000000.0 / 30.0))


def main():
    bak_main = MAIN_JSON + ".bak_before_ai"
    with open(bak_main if os.path.exists(bak_main) else MAIN_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    if os.path.exists(PATCH_DIR):
        shutil.rmtree(PATCH_DIR)

    with open(DONOR_V2_JSON, "r", encoding="utf-8") as f:
        donor_v2 = json.load(f)
    with open(DONOR_REELS_JSON, "r", encoding="utf-8") as f:
        donor_reels = json.load(f)

    vid_seg_tpl = copy.deepcopy(data["tracks"][0]["segments"][0])
    aud_seg_tpl = copy.deepcopy(data["tracks"][1]["segments"][0])
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

    # Register full 40.04s Voiceover (voicestudio-428a4d53.wav)
    vo_mat = copy.deepcopy(vo_mat_tpl)
    vo_mat["id"] = new_id()
    vo_mat["unique_id"] = uuid.uuid4().hex
    vo_mat["name"] = "voicestudio-428a4d53.wav"
    vo_mat["path"] = FULL_VO_PATH
    vo_mat["duration"] = 40040000
    data["materials"]["audios"].append(vo_mat)

    # Register all 11 Storyboard First-Frame Photos as photo materials
    SHOT_FILES = [
        ("shot01", "SHOT_01_00s-03s_Nhin_Lich_Treo_Tuong.jpg"),
        ("shot02", "SHOT_02_03s-06s6_But_Vang_Khoanh_Lich_Lech.jpg"),
        ("shot03", "SHOT_03_06s6-11s5_Tram_Tu_Ben_Cua_So_Vom.jpg"),
        ("shot04", "SHOT_04_11s5-17s2_3D_Nhip_Sinh_Hoc_Pha_Le.jpg"),
        ("shot05", "SHOT_05_17s2-20s8_Gap_Lich_Diem_Tinh.jpg"),
        ("shot06", "SHOT_06_20s8-24s7_Hoa_Mau_Don_No_San_Pham.jpg"),
        ("shot07", "SHOT_07_24s7-27s3_Uong_Nuoc_Am_Thu_Thai.jpg"),
        ("shot08", "SHOT_08_27s3-30s1_Bien_Hinh_Dam_Cam_Rang_Ro.jpg"),
        ("shot09", "SHOT_09_30s1-35s6_3D_CGI_4_Vi_Thao_Duoc.jpg"),
        ("shot10", "SHOT_10_35s6-37s6_Xoay_Vay_Goc_Cao_Comfort.jpg"),
        ("shot11", "SHOT_11_37s6-40s8_Tiec_Tra_Packshot_CTA.jpg"),
    ]

    photo_ids = {}
    for key, fname in SHOT_FILES:
        pm = copy.deepcopy(vid_mat_tpl)
        pm["id"] = new_id()
        pm["unique_id"] = uuid.uuid4().hex
        pm["type"] = "photo"
        pm["duration"] = 10800000000
        pm["has_audio"] = False
        pm["width"] = 768
        pm["height"] = 1376
        pm["path"] = os.path.join(SB_DIR, fname).replace("\\", "/")
        pm["material_name"] = fname
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
        },
        "choi_loa_2": {
            "type": "transition",
            "name": "Chói lòa 2",
            "effect_id": "6952697917563998722",
            "resource_id": "6952697917563998722",
            "third_resource_id": "6952697917563998722",
            "source_platform": 1,
            "sub_type": 0,
            "adjust_params": [],
            "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/6952697917563998722/aafb556352016d087cddd1939ada20f8",
            "duration": 466666,
            "is_overlap": False,
            "platform": "all",
            "category_id": "123456",
            "category_name": "Chuyển tiếp",
            "request_id": "",
            "is_ai_transition": False,
            "video_path": "",
            "task_id": "",
        },
        "mo_kim_sa": {
            "type": "transition",
            "name": "Mờ kim sa",
            "effect_id": "7682682952043547911",
            "resource_id": "7682682952043547911",
            "third_resource_id": "0",
            "source_platform": 1,
            "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7682682952043547911/b4dfe4a57a9fa3595b08b6e91f4820c4",
            "duration": 600000,
            "is_overlap": True,
            "platform": "all",
            "category_id": "2037713378",
            "category_name": "Whimsical",
            "request_id": "",
            "is_ai_transition": False,
            "video_path": "",
            "task_id": "",
        },
        "mo_thu_phong": {
            "type": "transition",
            "name": "Mờ thu phóng hiện ra",
            "effect_id": "7621850078533143861",
            "resource_id": "7621850078533143861",
            "third_resource_id": "0",
            "source_platform": 1,
            "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7621850078533143861/01e4b5812c36fd59c8e3e776bd411d35",
            "duration": 466666,
            "is_overlap": True,
            "platform": "all",
            "category_id": "123456",
            "category_name": "heycan_search_transition",
            "request_id": "",
            "is_ai_transition": False,
            "video_path": "",
            "task_id": "",
        },
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
            "duration": 500000,
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

    def make_photo_seg(shot_key, st_s, en_s, sc_start=1.02, sc_end=1.09, tr_key=None):
        st_us = s2us(st_s)
        du_us = s2us(en_s) - st_us

        sp_id = new_id()
        data["materials"]["speeds"].append({"id": sp_id, "type": "speed", "mode": 0, "speed": 1.0, "curve_speed": None})
        pi_id = new_id()
        data["materials"]["placeholder_infos"].append(
            {"id": pi_id, "type": "placeholder_info", "meta_type": "none", "res_path": "", "res_text": "", "error_path": "", "error_text": ""}
        )
        cv_id = new_id()
        data["materials"]["canvases"].append(
            {"id": cv_id, "type": "canvas_color", "color": "", "blur": 0.0, "image": "", "album_image": "", "image_id": "", "image_name": "", "source_platform": 0, "team_id": ""}
        )
        sc_id = new_id()
        data["materials"]["sound_channel_mappings"].append({"id": sc_id, "type": "", "audio_channel_mapping": 0, "is_config_open": False})
        mc_id = new_id()
        data["materials"]["material_colors"].append(
            {"id": mc_id, "is_color_clip": False, "is_gradient": False, "solid_color": "", "gradient_colors": [], "gradient_percents": [], "gradient_angle": 90.0, "width": 0.0, "height": 0.0}
        )
        vs_id = new_id()
        data["materials"]["vocal_separations"].append(
            {"id": vs_id, "type": "vocal_separation", "choice": 0, "removed_sounds": [], "time_range": None, "production_path": "", "final_algorithm": "", "enter_from": ""}
        )
        refs = [sp_id, pi_id, cv_id, sc_id, mc_id, vs_id]

        if tr_key is not None:
            tr_obj = copy.deepcopy(TRANSITION_CATALOG[tr_key])
            tr_obj["id"] = new_id()
            data["materials"]["transitions"].append(tr_obj)
            refs.append(tr_obj["id"])

        seg = copy.deepcopy(vid_seg_tpl)
        seg["id"] = new_id()
        seg["material_id"] = photo_ids[shot_key]
        # Give plenty of source_timerange start (1s) so overlap transitions have full handles on still photos!
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

    def make_text_seg(text_str, start_s, end_s, tier=1, anim_key="chu_mo_dan", pos_y=-0.42, font_size=12.0):
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

    # 11 Storyboard Animatic Cuts (00.00s .. 39.60s)
    SHOT_PLAN = [
        ("shot01", 0.00, 3.05, 1.02, 1.09, None),
        ("shot02", 3.05, 6.45, 1.08, 1.02, None),
        ("shot03", 6.45, 11.25, 1.02, 1.09, "ket_hop"),
        ("shot04", 11.25, 16.85, 1.02, 1.10, None),
        ("shot05", 16.85, 20.20, 1.08, 1.02, "choi_loa_2"),
        ("shot06", 20.20, 23.70, 1.10, 1.02, None),
        ("shot07", 23.70, 25.95, 1.02, 1.08, "mo_kim_sa"),
        ("shot08", 25.95, 28.85, 1.02, 1.09, "ket_hop"),
        ("shot09", 28.85, 34.30, 1.02, 1.10, None),
        ("shot10", 34.30, 36.45, 1.09, 1.02, "mo_thu_phong"),
        ("shot11", 36.45, 39.60, 1.02, 1.07, None),
    ]
    track0_segs = [make_photo_seg(*s) for s in SHOT_PLAN]

    # Dual-Tier Headlines
    CALLOUTS = [
        (0.15, 2.95, "SAU TUỔI 40", "bui_vang", 0.62, 14.0, 0.40, 2.95, "Kinh tháng sớm · Tháng muộn vì đâu?", 0.49, 9.5),
        (11.35, 16.70, "GIAI ĐOẠN TIỀN MÃN KINH", "chu_mo_dan", 0.62, 12.5, 11.60, 16.70, "Thay đổi hoạt động buồng trứng", 0.49, 9.5),
        (20.30, 23.55, "ĐIỀU KINH HẰNG THU", "xoay_lap_lanh", 0.62, 14.0, 20.55, 23.55, "Hỗ trợ điều hòa kinh nguyệt tự nhiên", 0.49, 9.5),
        (23.80, 28.70, "BỔ HUYẾT · LƯU THÔNG KHÍ HUYẾT", "chu_mo_dan", 0.62, 12.0, 24.05, 28.70, "Giảm đau bụng khi hành kinh", 0.49, 9.5),
        (28.95, 34.15, "CÔNG THỨC THẢO DƯỢC NỔI TRỘI", "bui_vang", 0.14, 12.5, 29.20, 34.15, "Đương Quy · Hương Phụ · Sài Hồ · Huyền Hồ", 0.01, 9.0),
        (36.55, 39.50, "ĐIỀU KINH HẰNG THU", "xoay_lap_lanh", 0.64, 14.5, 36.80, 39.50, "Nhắn mình ngay để được tư vấn chi tiết!", 0.51, 9.5),
    ]
    tier1_segs = [make_text_seg(c[2], c[0], c[1], tier=1, anim_key=c[3], pos_y=c[4], font_size=c[5]) for c in CALLOUTS]
    tier2_segs = [make_text_seg(c[8], c[6], c[7], tier=2, anim_key="mo", pos_y=c[9], font_size=c[10]) for c in CALLOUTS]

    # Clean Subtitles across all 10 VO phrases (including full CTA!)
    SUBTITLES = [
        (0.12, 2.98, "Sau 40, kinh tháng sớm tháng muộn\nlà vì đâu?"),
        (3.13, 6.37, "Nếp sinh hoạt vẫn vậy,\nnhưng kỳ kinh bỗng khó đoán,"),
        (6.52, 8.80, "có tháng đến sớm, có tháng lại chậm"),
        (8.80, 11.16, "khiến chị em không biết cơ thể\nđang thay đổi thế nào."),
        (11.34, 14.10, "Trong giai đoạn tiền mãn kinh,\nthay đổi hoạt động buồng trứng"),
        (14.10, 16.73, "có thể khiến chu kỳ ngắn hoặc dài hơn."),
        (16.92, 19.96, "Tuy nhiên, không thể chỉ dựa vào tuổi\nđể kết luận nguyên nhân."),
        (20.28, 23.48, "Với nhu cầu hỗ trợ điều hòa kinh nguyệt,\nĐIỀU KINH HẰNG THU"),
        (23.66, 25.67, "giúp bổ huyết, lưu thông khí huyết,"),
        (25.85, 28.54, "hỗ trợ điều hòa kinh\nvà giảm đau bụng khi hành kinh."),
        (28.85, 31.50, "Với công thức nhiều thành phần\nthảo dược nổi trội"),
        (31.50, 34.09, "như Đương Quy, Hương Phụ,\nSài Hồ, Huyền Hồ."),
        (34.32, 36.45, "Nếu bạn đang gặp vấn đề\nvề chu kỳ kinh nguyệt,"),
        (36.45, 38.42, "nhắn mình để được tư vấn nhé!"),
    ]
    subtitle_segs = [make_text_seg(txt, st, en, tier=2, anim_key="mo", pos_y=-0.78, font_size=8.5) for st, en, txt in SUBTITLES]

    # Full 10-phrase Checkerboard Voiceover from voicestudio-428a4d53.wav
    VO_PHRASES = [
        (0.12, 2.86, 0.00),
        (3.13, 3.24, 3.36),
        (6.52, 4.64, 6.96),
        (11.34, 5.39, 11.85),
        (16.92, 3.04, 17.80),
        (20.28, 3.20, 21.40),
        (23.66, 2.01, 24.75),
        (25.85, 2.69, 26.96),
        (28.85, 5.24, 30.38),
        (34.32, 4.10, 35.93),
    ]
    vo_a, vo_b = [], []
    for idx, (t_st, dur_s, s_st) in enumerate(VO_PHRASES):
        seg = make_audio_seg(vo_mat["id"], t_st, dur_s, src_start_s=s_st, vol=1.32, fade_in_us=33333, fade_out_us=66666)
        (vo_a if idx % 2 == 0 else vo_b).append(seg)

    # 2-Stage Comfort BGM + End-Card Swell
    bgm_spa_id = register_lib_audio("bgm_spa")
    bgm_fresh_id = register_lib_audio("bgm_fresh_comfort")
    bgm_segs = [
        make_audio_seg(bgm_spa_id, 0.00, 20.20, src_start_s=0.00, vol=0.24, fade_in_us=300000, fade_out_us=500000),
        make_audio_seg(bgm_fresh_id, 20.20, 18.22, src_start_s=0.00, vol=0.28, fade_in_us=200000, fade_out_us=66666),
        make_audio_seg(bgm_fresh_id, 38.42, 1.18, src_start_s=18.22, vol=0.46, fade_in_us=100000, fade_out_us=900000),
    ]

    # SFX
    sfx_ids = {k: register_lib_audio(k) for k in ("woosh_vshort", "pop_lower", "woosh_chu", "riser_metallic", "magic_reveal", "deep_woosh", "noitifi_chu")}
    SFX_EVENTS = [
        ("woosh_vshort", 0.12, 0.53, 0.00, 0.42, 33333, 66666),
        ("pop_lower", 3.60, 0.16, 0.00, 0.46, 10000, 33333),
        ("woosh_chu", 11.25, 0.66, 0.00, 0.38, 33333, 66666),
        ("riser_metallic", 17.85, 2.30, 2.95, 0.40, 350000, 120000),
        ("magic_reveal", 20.20, 2.03, 0.00, 0.54, 33333, 166666),
        ("woosh_vshort", 25.95, 0.53, 0.00, 0.40, 33333, 66666),
        ("noitifi_chu", 28.90, 0.50, 0.00, 0.38, 33333, 66666),
        ("deep_woosh", 34.25, 2.10, 0.00, 0.42, 33333, 200000),
        ("magic_reveal", 36.45, 2.03, 0.00, 0.50, 33333, 200000),
    ]
    sfx_segs = [make_audio_seg(sfx_ids[k], t_st, dur_s, src_start_s=s_st, vol=vol, fade_in_us=fi, fade_out_us=fo) for k, t_st, dur_s, s_st, vol, fi, fo in SFX_EVENTS]

    def make_track(t_type, segs):
        return {"id": new_id(), "type": t_type, "name": "", "attribute": 0, "flag": 0, "is_default_name": True, "segments": segs}

    data["tracks"] = [
        make_track("video", track0_segs),
        make_track("text", tier1_segs),
        make_track("text", tier2_segs),
        make_track("text", subtitle_segs),
        make_track("audio", vo_a),
        make_track("audio", vo_b),
        make_track("audio", bgm_segs),
        make_track("audio", sfx_segs),
    ]

    for t_idx, trk in enumerate(data["tracks"]):
        for seg in trk["segments"]:
            seg["track_render_index"] = t_idx

    total_dur_us = s2us(39.60)
    data["duration"] = total_dur_us

    with open(MAIN_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    if os.path.exists(TIMELINE_DIR):
        with open(TIMELINE_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    if os.path.exists(META_JSON):
        with open(META_JSON, "r", encoding="utf-8") as f:
            meta = json.load(f)
        meta["tm_duration"] = total_dur_us
        with open(META_JSON, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False)

    print(f"Built 11-Shot Storyboard Animatic in ĐIỀU KINH 1-sao chép ({total_dur_us/1e6:.2f}s, {len(data['tracks'])} tracks)!")


if __name__ == "__main__":
    main()
