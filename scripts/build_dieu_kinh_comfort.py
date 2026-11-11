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
BACKUP_PATCH_DIR = r"C:\Users\Hang thu\.gemini\antigravity\brain\736203b4-cb9e-4e44-b2cb-b3a23baa248a\scratch\backup_dieu_kinh_patch"


def new_id():
    return str(uuid.uuid4()).upper()


def s2us(sec):
    """Snap seconds to exact 30fps frame boundary in microseconds."""
    frames = round(sec * 30.0)
    return int(round(frames * 1000000.0 / 30.0))


def main():
    # 1. Create clean idempotent backups
    bak_main = MAIN_JSON + ".bak_before_ai"
    if not os.path.exists(bak_main):
        shutil.copy2(MAIN_JSON, bak_main)
        print(f"Backed up {MAIN_JSON} -> {bak_main}")

    if os.path.exists(TIMELINE_JSON):
        bak_tl = TIMELINE_JSON + ".bak_before_ai"
        if not os.path.exists(bak_tl):
            shutil.copy2(TIMELINE_JSON, bak_tl)
            print(f"Backed up {TIMELINE_JSON} -> {bak_tl}")

    if os.path.exists(META_JSON):
        bak_meta = META_JSON + ".bak_before_ai"
        if not os.path.exists(bak_meta):
            shutil.copy2(META_JSON, bak_meta)

    # Clear CapCut 9.7 WAL patch cache so CapCut loads draft_content.json directly
    if os.path.exists(PATCH_DIR):
        os.makedirs(BACKUP_PATCH_DIR, exist_ok=True)
        for fn in os.listdir(PATCH_DIR):
            src_p = os.path.join(PATCH_DIR, fn)
            dst_p = os.path.join(BACKUP_PATCH_DIR, fn)
            if os.path.isfile(src_p):
                shutil.copy2(src_p, dst_p)
        shutil.rmtree(PATCH_DIR)
        print(f"Backed up & cleared stale WAL patch dir: {PATCH_DIR}")

    # 2. Load base project & authentic donor templates
    with open(bak_main, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(DONOR_V2_JSON, "r", encoding="utf-8") as f:
        donor_v2 = json.load(f)

    with open(DONOR_REELS_JSON, "r", encoding="utf-8") as f:
        donor_reels = json.load(f)

    # Authentic segment & material templates
    vid_seg_tpl = copy.deepcopy(data["tracks"][0]["segments"][0])
    aud_seg_tpl = copy.deepcopy(data["tracks"][1]["segments"][0])
    vid_mat_tpl = copy.deepcopy(data["materials"]["videos"][0])
    vo_mat = copy.deepcopy(data["materials"]["audios"][0])

    tier1_text_tpl = copy.deepcopy(donor_v2["materials"]["texts"][0])
    tier2_text_tpl = None
    for tx in donor_v2["materials"]["texts"]:
        if "Nơi phong độ" in tx.get("content", ""):
            tier2_text_tpl = copy.deepcopy(tx)
            break

    text_seg_tpl = None
    for t in donor_reels["tracks"]:
        if t["type"] == "text" and t["segments"]:
            text_seg_tpl = copy.deepcopy(t["segments"][0])
            break

    sfx_mat_tpl = None
    for au in donor_reels["materials"]["audios"]:
        if au.get("type") == "sound":
            sfx_mat_tpl = copy.deepcopy(au)
            break

    # 3. Reset materials cleanly while preserving all required keys
    existing_vids_by_name = {
        os.path.basename(v["path"]): copy.deepcopy(v)
        for v in data["materials"]["videos"]
    }

    # Add 9th clip (Character_in_dress_smiling_joyfully_7334972b.mp4) which is already in draft_meta_info
    clip9_name = "Character_in_dress_smiling_joyfully_7334972b.mp4"
    if clip9_name not in existing_vids_by_name:
        v9 = copy.deepcopy(vid_mat_tpl)
        v9["id"] = new_id()
        v9["unique_id"] = uuid.uuid4().hex
        v9["duration"] = 6000000
        v9["path"] = f"Z:/Máy tính khác/My Computer/Document HT Media/TLH/download (2)/{clip9_name}"
        v9["material_name"] = clip9_name
        v9["width"] = 720
        v9["height"] = 1280
        v9["local_material_id"] = "007bb3b3-96c3-4d65-ab17-b28076c7e504"
        existing_vids_by_name[clip9_name] = v9

    # Clear per-segment material lists so there are zero orphan objects
    for k in list(data["materials"].keys()):
        if isinstance(data["materials"][k], list):
            data["materials"][k] = []

    data["materials"]["videos"] = list(existing_vids_by_name.values())
    data["materials"]["audios"] = [vo_mat]

    vid_id_by_key = {
        "wall_cal": existing_vids_by_name["Woman_looking_at_wall_calendar_6abef791.mp4"]["id"],
        "gold_pen": existing_vids_by_name["Gold_pen_circling_calendar_dates_92a611d0.mp4"]["id"],
        "angelica": existing_vids_by_name["Angelica_root_slices_dissolving_fd6b8722.mp4"]["id"],
        "peony": existing_vids_by_name["Peony_blooms_revealing_product_1a742a80.mp4"]["id"],
        "warm_water": existing_vids_by_name["Woman_sipping_warm_water_335b71e8.mp4"]["id"],
        "party_smile": existing_vids_by_name["Character_in_dress_smiling_joyfully_7334972b.mp4"]["id"],
        "twirl_top": existing_vids_by_name["Woman_twirls_in_coral_dress_036f2841.mp4"]["id"],
        "twirl_wide": existing_vids_by_name["Woman_twirls_in_coral_dress_e5ef1a29.mp4"]["id"],
        "packshot_end": existing_vids_by_name["Woman_smiling_with_cosmetic_product_d3e333e8.mp4"]["id"],
    }

    # =========================================================================
    # CATALOGS: TRANSITIONS, MASKS, ANIMATIONS, BGM & SFX
    # =========================================================================
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
        "ky_uc_gon_song": {
            "type": "transition",
            "name": "Ký ức gợn sóng",
            "effect_id": "7639655148100357383",
            "resource_id": "7639655148100357383",
            "third_resource_id": "0",
            "source_platform": 1,
            "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/7639655148100357383/8a9f133250992e0cc5ecb2b98cc4d645",
            "duration": 533333,
            "is_overlap": True,
            "platform": "all",
            "category_id": "123456",
            "category_name": "heycan_search_transition",
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

    # =========================================================================
    # HELPER BUILDERS
    # =========================================================================
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

    def make_video_seg(
        vid_key,
        target_start_s,
        target_end_s,
        src_start_s=0.0,
        speed=1.0,
        scale_start=1.0,
        scale_end=None,
        pos_x=0.0,
        pos_y=0.0,
        transition_key=None,
        rect_mask_cfg=None,
        pip_in_out=False,
    ):
        st_us = s2us(target_start_s)
        du_us = s2us(target_end_s) - st_us
        src_st_us = s2us(src_start_s)
        src_du_us = int(round(du_us * speed))

        sp_id = new_id()
        data["materials"]["speeds"].append(
            {"id": sp_id, "type": "speed", "mode": 0, "speed": float(speed), "curve_speed": None}
        )
        pi_id = new_id()
        data["materials"]["placeholder_infos"].append(
            {
                "id": pi_id,
                "type": "placeholder_info",
                "meta_type": "none",
                "res_path": "",
                "res_text": "",
                "error_path": "",
                "error_text": "",
            }
        )
        cv_id = new_id()
        data["materials"]["canvases"].append(
            {
                "id": cv_id,
                "type": "canvas_color",
                "color": "",
                "blur": 0.0,
                "image": "",
                "album_image": "",
                "image_id": "",
                "image_name": "",
                "source_platform": 0,
                "team_id": "",
            }
        )
        sc_id = new_id()
        data["materials"]["sound_channel_mappings"].append(
            {"id": sc_id, "type": "", "audio_channel_mapping": 0, "is_config_open": False}
        )
        mc_id = new_id()
        data["materials"]["material_colors"].append(
            {
                "id": mc_id,
                "is_color_clip": False,
                "is_gradient": False,
                "solid_color": "",
                "gradient_colors": [],
                "gradient_percents": [],
                "gradient_angle": 90.0,
                "width": 0.0,
                "height": 0.0,
            }
        )
        vs_id = new_id()
        data["materials"]["vocal_separations"].append(
            {
                "id": vs_id,
                "type": "vocal_separation",
                "choice": 0,
                "removed_sounds": [],
                "time_range": None,
                "production_path": "",
                "final_algorithm": "",
                "enter_from": "",
            }
        )

        refs = [sp_id, pi_id, cv_id, sc_id, mc_id, vs_id]

        if transition_key is not None:
            tr_obj = copy.deepcopy(TRANSITION_CATALOG[transition_key])
            tr_obj["id"] = new_id()
            data["materials"]["transitions"].append(tr_obj)
            refs.append(tr_obj["id"])

        if rect_mask_cfg is not None:
            mk_id = new_id()
            mk_obj = {
                "id": mk_id,
                "type": "mask",
                "category": "video",
                "category_name": "",
                "category_id": "",
                "panel": "",
                "is_old_version": False,
                "resource_id": "7374021450748924432",
                "constant_material_id": new_id(),
                "name": "Hình chữ nhật",
                "resource_type": "rectangle",
                "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/1068046537/02b8999168d121538a98ea59127483ef",
                "position_info": "",
                "config": rect_mask_cfg,
                "text_config": {
                    "content": "",
                    "font_name": "",
                    "font_path": "",
                    "font_resource_id": "",
                    "font_size": 15.0,
                    "bold_width": 0.0,
                    "italic_degree": 0,
                    "has_underline": False,
                    "line_gap": 0.0,
                    "char_spacing": 0.0,
                    "align_type": 15,
                    "scale": 1.0,
                },
                "platform": "all",
                "loader_work_space": "",
                "track_segment": "",
                "contour_path": None,
                "source_platform": 0,
            }
            data["materials"]["common_mask"].append(mk_obj)
            refs.append(mk_id)

        if pip_in_out:
            va_id = new_id()
            out_dur = 466666
            va_obj = {
                "id": va_id,
                "type": "sticker_animation",
                "animations": [
                    {
                        "id": "6798332871267324423",
                        "type": "in",
                        "start": 0,
                        "duration": 466666,
                        "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/6798332871267324423/667952e8cf6918f62e16b8e6dfc2fef2",
                        "platform": "all",
                        "resource_id": "6798332871267324423",
                        "third_resource_id": "6798332871267324423",
                        "source_platform": 1,
                        "name": "Trượt sang trái",
                        "category_id": "in",
                        "category_name": "in",
                        "panel": "video",
                        "material_type": "video",
                        "anim_adjust_params": None,
                        "request_id": "",
                    },
                    {
                        "id": "6798320902548230669",
                        "type": "out",
                        "start": max(0, du_us - out_dur),
                        "duration": out_dur,
                        "path": "C:/Users/Hang thu/AppData/Local/CapCut/User Data/Cache/effect/6798320902548230669/c6f05ce62355b537be762550040bfc08",
                        "platform": "all",
                        "resource_id": "6798320902548230669",
                        "third_resource_id": "6798320902548230669",
                        "source_platform": 1,
                        "name": "Mờ dần",
                        "category_id": "2037708283",
                        "category_name": "Trending-2",
                        "panel": "video",
                        "material_type": "video",
                        "anim_adjust_params": None,
                        "request_id": "",
                    },
                ],
                "multi_language_current": "none",
            }
            data["materials"]["material_animations"].append(va_obj)
            refs.append(va_id)

        seg = copy.deepcopy(vid_seg_tpl)
        seg["id"] = new_id()
        seg["material_id"] = vid_id_by_key[vid_key]
        seg["source_timerange"] = {"start": src_st_us, "duration": src_du_us}
        seg["target_timerange"] = {"start": st_us, "duration": du_us}
        seg["speed"] = float(speed)
        seg["volume"] = 0.0
        seg["last_nonzero_volume"] = 1.0
        seg["clip"]["scale"] = {"x": float(scale_start), "y": float(scale_start)}
        seg["clip"]["transform"] = {"x": float(pos_x), "y": float(pos_y)}
        seg["uniform_scale"] = {"on": True, "value": float(scale_start)}
        seg["extra_material_refs"] = refs
        seg["common_keyframes"] = []

        if scale_end is not None and abs(scale_end - scale_start) > 0.001:
            add_micro_zoom_kf(seg, float(scale_start), float(scale_end))

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
            {
                "id": anim_mat_id,
                "type": "sticker_animation",
                "animations": [anim_item],
                "multi_language_current": "none",
            }
        )

        seg = copy.deepcopy(text_seg_tpl)
        seg["id"] = new_id()
        seg["material_id"] = mat["id"]
        seg["target_timerange"] = {"start": st_us, "duration": du_us}
        seg["clip"]["scale"] = {"x": 1.0, "y": 1.0}
        seg["clip"]["transform"] = {"x": 0.0, "y": float(pos_y)}
        seg["extra_material_refs"] = [anim_mat_id]

        fade_out_len = min(366666, du_us // 3)
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

    def make_audio_seg(mat_id, target_start_s, dur_s, src_start_s=0.0, vol=1.0, fade_in_us=33333, fade_out_us=66666):
        st_us = s2us(target_start_s)
        du_us = s2us(dur_s)
        src_st_us = s2us(src_start_s)

        sp_id = new_id()
        data["materials"]["speeds"].append(
            {"id": sp_id, "type": "speed", "mode": 0, "speed": 1.0, "curve_speed": None}
        )
        pi_id = new_id()
        data["materials"]["placeholder_infos"].append(
            {
                "id": pi_id,
                "type": "placeholder_info",
                "meta_type": "none",
                "res_path": "",
                "res_text": "",
                "error_path": "",
                "error_text": "",
            }
        )
        bt_id = new_id()
        data["materials"]["beats"].append(
            {
                "id": bt_id,
                "type": "beats",
                "enable_ai_beats": False,
                "gear": 404,
                "gear_count": 0,
                "mode": 404,
                "user_beats": [],
                "user_delete_ai_beats": None,
                "ai_beats": {
                    "melody_url": "",
                    "melody_path": "",
                    "beats_url": "",
                    "beats_path": "",
                    "melody_percents": [0.0],
                    "beat_speed_infos": [],
                },
            }
        )
        sc_id = new_id()
        data["materials"]["sound_channel_mappings"].append(
            {"id": sc_id, "type": "", "audio_channel_mapping": 0, "is_config_open": False}
        )
        vs_id = new_id()
        data["materials"]["vocal_separations"].append(
            {
                "id": vs_id,
                "type": "vocal_separation",
                "choice": 0,
                "removed_sounds": [],
                "time_range": None,
                "production_path": "",
                "final_algorithm": "",
                "enter_from": "",
            }
        )
        fd_id = new_id()
        data["materials"]["audio_fades"].append(
            {
                "id": fd_id,
                "type": "audio_fade",
                "fade_type": 0,
                "fade_in_duration": int(fade_in_us),
                "fade_out_duration": int(fade_out_us),
            }
        )

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

    # =========================================================================
    # TRACK 00: MAIN COMMERCIAL VIDEO STORYLINE (00.00s .. 36.80s, 15 CUTS)
    # =========================================================================
    main_cuts = [
        # --- ACT 1: PERIMENOPAUSE PROBLEM & INSIGHT (00.00s .. 20.40s) ---
        # Hook #01 & #02: Worried at wall calendar -> Punch-in on expression & hand on abdomen
        ("wall_cal", 0.00, 1.50, 0.00, 1.00, 1.00, 1.05, 0.00, 0.00, None),
        ("wall_cal", 1.50, 3.30, 1.50, 1.00, 1.24, 1.28, 0.06, -0.05, None),
        # #03 & #04: Gold pen circling calendar dates -> Macro close-up
        ("gold_pen", 3.30, 5.40, 0.00, 1.00, 1.00, 1.06, 0.00, 0.00, None),
        ("gold_pen", 5.40, 7.60, 1.80, 1.00, 1.25, 1.30, -0.05, 0.04, None),
        # #05: Empathetic slow-motion close framing ("có tháng đến sớm, có tháng lại chậm...")
        ("wall_cal", 7.60, 11.10, 0.90, 0.80, 1.15, 1.21, 0.08, -0.04, "ket_hop"),
        # #06: Biological/ovarian rhythm metaphor (pure glowing strands in glass tube, no herbs yet)
        ("angelica", 11.10, 14.10, 1.65, 0.75, 1.14, 1.22, 0.00, 0.00, None),
        # #07: Quiet contemplative moment holding warm cup (before smiling)
        ("warm_water", 14.10, 16.75, 0.00, 0.75, 1.00, 1.06, 0.00, 0.00, "ky_uc_gon_song"),
        # #08: Climax of Act 1 paired with Track 01 PIP Collage -> Chói lòa 2 flash into Peony Reveal!
        ("wall_cal", 16.75, 20.40, 0.35, 0.75, 1.08, 1.14, -0.04, 0.10, "choi_loa_2"),

        # --- ACT 2: COMFORT-STYLE MAGICAL PEONY PRODUCT REVEAL (20.40s .. 24.40s) ---
        # #09: Pink peony bud blooms open on Terrazzo revealing ĐIỀU KINH HT box + bottle
        ("peony", 20.40, 24.40, 0.00, 1.00, 1.00, 1.08, 0.00, 0.00, None),

        # --- ACT 3: HERBAL FORMULA + CORAL DRESS TRANSFORMATION + PARTY END-CARD (24.40s .. 36.80s) ---
        # #10: Savoring warm herbal drink -> eyes open with radiant relieved smile -> Glitter dissolve!
        ("warm_water", 24.40, 26.20, 1.85, 1.00, 1.03, 1.09, 0.00, 0.00, "mo_kim_sa"),
        # #11: Comfort Signature High-Angle Bird's-Eye Spin in Coral Tiered Dress with falling petals!
        ("twirl_top", 26.20, 28.55, 1.10, 1.00, 1.02, 1.09, 0.00, 0.00, "ket_hop"),
        # #12: Comfort Signature Macro 3D Formula (Đương Quy slices dissolving into rose-gold strands)
        ("angelica", 28.55, 31.35, 0.25, 1.00, 1.00, 1.08, 0.00, 0.00, None),
        # #13: Eye-level joyful full-body twirl in sunlit teal-fluted room
        ("twirl_wide", 31.35, 32.80, 2.20, 1.00, 1.04, 1.09, 0.00, 0.00, None),
        # #14: Joyful medium close-up at party (CROPPED scale=1.44, y=-0.40 so bottom MacBook is 100% gone!)
        ("party_smile", 32.80, 34.15, 2.20, 1.00, 1.44, 1.48, 0.00, -0.40, "mo_thu_phong"),
        # #15: Comfort Signature Party + Foreground Packshot End-Card (ĐIỀU KINH HT + pink peonies)
        ("packshot_end", 34.15, 36.80, 1.80, 0.80, 1.00, 1.05, 0.00, 0.00, None),
    ]

    track0_segs = [make_video_seg(*c) for c in main_cuts]

    # =========================================================================
    # TRACK 01: SIGNATURE SOFT-FEATHERED COLLAGE PIP OVERLAY (16.95s .. 20.25s)
    # =========================================================================
    pip_mask_cfg = {
        "width": 0.78,
        "height": 0.52,
        "centerX": 0.0,
        "centerY": 0.0,
        "rotation": 0.0,
        "feather": 0.15,
        "expansion": 0.0,
        "roundCorner": 0.06,
        "invert": False,
        "aspectRatio": 1.0,
    }
    track1_segs = [
        make_video_seg(
            "gold_pen",
            16.95,
            20.25,
            src_start_s=0.40,
            speed=0.80,
            scale_start=0.74,
            scale_end=0.78,
            pos_x=0.14,
            pos_y=-0.28,
            rect_mask_cfg=pip_mask_cfg,
            pip_in_out=True,
        )
    ]

    # =========================================================================
    # TRACK 02 & TRACK 03: STAGGERED 2-TIER GOLD + WHITE COMMERCIAL HEADLINES
    # =========================================================================
    CALLOUT_SECTIONS = [
        # (t1_start, t1_end, t1_title, t1_anim, t1_y, t1_size, t2_start, t2_end, t2_sub, t2_y, t2_size)
        (
            0.15, 3.20, "SAU TUỔI 40", "bui_vang", 0.60, 14.0,
            0.40, 3.20, "Kinh tháng sớm · Tháng muộn vì đâu?", 0.47, 9.5,
        ),
        (
            11.20, 16.60, "GIAI ĐOẠN TIỀN MÃN KINH", "chu_mo_dan", 0.60, 12.5,
            11.45, 16.60, "Thay đổi hoạt động buồng trứng", 0.47, 9.5,
        ),
        (
            20.50, 24.30, "ĐIỀU KINH HẰNG THU", "xoay_lap_lanh", 0.60, 14.0,
            20.75, 24.30, "Hỗ trợ điều hòa kinh nguyệt tự nhiên", 0.47, 9.5,
        ),
        (
            24.65, 28.45, "BỔ HUYẾT · LƯU THÔNG KHÍ HUYẾT", "chu_mo_dan", 0.60, 12.0,
            24.90, 28.45, "Giảm đau bụng khi hành kinh", 0.47, 9.5,
        ),
        # Centered over the 3D CGI herbal tube just like Comfort's "CÔNG THỨC DƯỠNG VẢI CHỐNG NHĂN"
        (
            28.65, 31.30, "CÔNG THỨC THẢO DƯỢC NỔI TRỘI", "bui_vang", 0.08, 12.5,
            28.90, 31.30, "Đương Quy · Hương Phụ · Sài Hồ · Huyền Hồ Sách", -0.05, 9.0,
        ),
        # Upper clear sky/arch zone on Final Party Packshot End-Card
        (
            34.20, 36.70, "ĐIỀU KINH HẰNG THU", "xoay_lap_lanh", 0.62, 14.5,
            34.45, 36.70, "Khí huyết lưu thông · Rạng ngời thanh xuân", 0.49, 9.5,
        ),
    ]

    tier1_segs = []
    tier2_segs = []
    for t1_st, t1_en, t1_txt, t1_anim, t1_y, t1_sz, t2_st, t2_en, t2_txt, t2_y, t2_sz in CALLOUT_SECTIONS:
        tier1_segs.append(make_text_seg(t1_txt, t1_st, t1_en, tier=1, anim_key=t1_anim, pos_y=t1_y, font_size=t1_sz))
        tier2_segs.append(make_text_seg(t2_txt, t2_st, t2_en, tier=2, anim_key="mo", pos_y=t2_y, font_size=t2_sz))

    # =========================================================================
    # TRACK 04: COMFORT-STYLE CLEAN BOTTOM SUBTITLES (SYNCED TO ALL 9 PHRASES)
    # =========================================================================
    COMFORT_SUBTITLES = [
        (0.13, 3.21, "Sau 40, kinh tháng sớm tháng muộn\nlà vì đâu?"),
        (3.37, 5.45, "Nếp sinh hoạt vẫn vậy"),
        (5.45, 7.55, "nhưng kỳ kinh bỗng khó đoán,"),
        (7.68, 9.35, "có tháng đến sớm, có tháng lại chậm"),
        (9.35, 10.99, "khiến chị em không biết cơ thể\nđang thay đổi thế nào."),
        (11.17, 13.90, "Trong giai đoạn tiền mãn kinh,\nthay đổi hoạt động buồng trứng"),
        (13.90, 16.65, "có thể khiến chu kỳ ngắn hoặc dài hơn."),
        (16.82, 20.13, "Tuy nhiên, không thể chỉ dựa vào tuổi\nđể kết luận nguyên nhân."),
        (20.40, 22.65, "Với nhu cầu hỗ trợ điều hòa kinh nguyệt,"),
        (22.65, 24.51, "ĐIỀU KINH HẰNG THU"),
        (24.63, 26.60, "giúp bổ huyết, lưu thông khí huyết,"),
        (26.60, 28.46, "hỗ trợ điều hòa kinh\nvà giảm đau bụng khi hành kinh."),
        (28.66, 31.35, "Với công thức nhiều thành phần\nthảo dược nổi trội"),
        (31.35, 34.06, "như Đương Quy, Hương Phụ,\nSài Hồ, Huyền Hồ..."),
    ]
    subtitle_segs = [
        make_text_seg(txt, st, en, tier=2, anim_key="mo", pos_y=-0.76, font_size=8.5)
        for st, en, txt in COMFORT_SUBTITLES
    ]

    # =========================================================================
    # TRACK 05 & TRACK 06: CHECKERBOARD VOICEOVER (J-CUT/L-CUT + MICRO-FADES)
    # =========================================================================
    # (target_start_s, dur_s, src_start_s, fade_out_us)
    VO_PHRASES = [
        (0.13, 3.08, 0.00, 66666),     # #01: "Sau 40, kinh tháng sớm tháng muộn là vì đâu?"
        (3.37, 4.18, 3.68, 66666),     # #02: "Nếp sinh hoạt vẫn vậy nhưng kỳ kinh bỗng khó đoán,"
        (7.68, 3.31, 8.11, 66666),     # #03: "có tháng đến sớm, có tháng lại chậm..."
        (11.17, 5.48, 11.77, 66666),   # #04: "Trong giai đoạn tiền mãn kinh..."
        (16.82, 3.31, 17.72, 66666),   # #05: "Tuy nhiên, không thể chỉ dựa vào tuổi..."
        (20.40, 4.11, 21.34, 66666),   # #06: "Với nhu cầu hỗ trợ điều hòa kinh nguyệt, Điều Kinh Hằng Thu"
        (24.63, 0.95, 25.70, 66666),   # #07: "giúp bổ huyết,"
        (25.70, 2.76, 26.94, 66666),   # #08: "lưu thông khí huyết, hỗ trợ điều hòa kinh..."
        (28.66, 5.40, 30.13, 266666),  # #09: "Với công thức nhiều thành phần..." (smooth 0.27s exit fade!)
    ]

    vo_track_a_segs = []
    vo_track_b_segs = []
    for idx, (t_st, dur_s, s_st, f_out) in enumerate(VO_PHRASES):
        seg = make_audio_seg(
            vo_mat["id"],
            target_start_s=t_st,
            dur_s=dur_s,
            src_start_s=s_st,
            vol=1.32,
            fade_in_us=33333,
            fade_out_us=f_out,
        )
        if idx % 2 == 0:
            vo_track_a_segs.append(seg)
        else:
            vo_track_b_segs.append(seg)

    # =========================================================================
    # TRACK 07: 2-STAGE COMFORT BGM WITH DYNAMIC END-CARD SWELL
    # =========================================================================
    bgm_spa_id = register_lib_audio("bgm_spa")
    bgm_fresh_id = register_lib_audio("bgm_fresh_comfort")

    bgm_segs = [
        # Stage 1 (00.00 .. 20.40s): Gentle contemplative spa melody under problem section
        make_audio_seg(bgm_spa_id, 0.00, 20.40, src_start_s=0.00, vol=0.24, fade_in_us=300000, fade_out_us=500000),
        # Stage 2A (20.40 .. 34.06s): Bright joyful Comfort commercial music under Peony Reveal & Twirl
        make_audio_seg(bgm_fresh_id, 20.40, 13.66, src_start_s=0.00, vol=0.28, fade_in_us=200000, fade_out_us=66666),
        # Stage 2B (34.06 .. 36.80s): Dynamic Ducking Swell on Brand Packshot End-Card + 1.2s smooth fade-out!
        make_audio_seg(bgm_fresh_id, 34.06, 2.74, src_start_s=13.66, vol=0.48, fade_in_us=150000, fade_out_us=1200000),
    ]

    # =========================================================================
    # TRACK 08: CURATED COMMERCIAL SFX (STRICTLY NON-OVERLAPPING)
    # =========================================================================
    sfx_ids = {
        k: register_lib_audio(k)
        for k in ("woosh_vshort", "pop_lower", "woosh_chu", "riser_metallic", "magic_reveal", "deep_woosh", "noitifi_chu")
    }

    SFX_EVENTS = [
        # (lib_key, target_start_s, dur_s, src_start_s, vol, fade_in_us, fade_out_us)
        ("woosh_vshort", 0.13, 0.53, 0.00, 0.42, 33333, 66666),      # Opening Hook Title
        ("pop_lower", 3.65, 0.16, 0.00, 0.46, 10000, 33333),         # Calendar circle 1
        ("pop_lower", 5.50, 0.16, 0.00, 0.46, 10000, 33333),         # Calendar circle 2
        ("woosh_chu", 11.10, 0.66, 0.00, 0.38, 33333, 66666),        # Biological strands transition
        ("woosh_vshort", 16.95, 0.53, 0.00, 0.40, 33333, 66666),     # PIP Collage slide-in
        ("riser_metallic", 18.05, 2.30, 2.95, 0.40, 350000, 120000), # Tension swell into Peony Reveal
        ("magic_reveal", 20.38, 2.03, 0.00, 0.54, 33333, 166666),    # Magical Pink Peony Product Reveal!
        ("deep_woosh", 26.15, 2.20, 0.00, 0.42, 33333, 200000),      # High-angle Coral Dress Spin!
        ("noitifi_chu", 28.60, 0.50, 0.00, 0.38, 33333, 66666),      # 3D CGI Herbal Formula Callout
        ("magic_reveal", 34.12, 2.03, 0.00, 0.50, 33333, 200000),    # Party Packshot End-Card Sparkle!
    ]

    sfx_segs = [
        make_audio_seg(sfx_ids[k], t_st, dur_s, src_start_s=s_st, vol=vol, fade_in_us=fi, fade_out_us=fo)
        for k, t_st, dur_s, s_st, vol, fi, fo in SFX_EVENTS
    ]

    # =========================================================================
    # ASSEMBLE ALL 9 TRACKS & SAVE TO CAPCUT PROJECT
    # =========================================================================
    def make_track(t_type, segs):
        return {
            "id": new_id(),
            "type": t_type,
            "name": "",
            "attribute": 0,
            "flag": 0,
            "is_default_name": True,
            "segments": segs,
        }

    data["tracks"] = [
        make_track("video", track0_segs),      # Track 00: Main Commercial Storyline (15 cuts)
        make_track("video", track1_segs),      # Track 01: Soft-Feathered Collage PIP
        make_track("text", tier1_segs),        # Track 02: Tier 1 Gold Commercial Callouts
        make_track("text", tier2_segs),        # Track 03: Tier 2 Staggered White Sub-Callouts
        make_track("text", subtitle_segs),     # Track 04: Comfort-Style Clean Subtitles
        make_track("audio", vo_track_a_segs),  # Track 05: Voiceover Checkerboard Track A
        make_track("audio", vo_track_b_segs),  # Track 06: Voiceover Checkerboard Track B
        make_track("audio", bgm_segs),         # Track 07: 2-Stage Comfort BGM + Swell
        make_track("audio", sfx_segs),         # Track 08: Commercial SFX
    ]

    for t_idx, trk in enumerate(data["tracks"]):
        for seg in trk["segments"]:
            seg["track_render_index"] = t_idx

    total_dur_us = s2us(36.80)
    data["duration"] = total_dur_us

    # Write to root draft_content.json and Timelines/<id>/draft_content.json
    with open(MAIN_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"Saved Comfort-style edit -> {MAIN_JSON}")

    if os.path.exists(TIMELINE_DIR):
        with open(TIMELINE_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        print(f"Synced timeline -> {TIMELINE_JSON}")

    if os.path.exists(META_JSON):
        with open(META_JSON, "r", encoding="utf-8") as f:
            meta = json.load(f)
        meta["tm_duration"] = total_dur_us
        with open(META_JSON, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False)
        print(f"Updated tm_duration={total_dur_us} in {META_JSON}")

    print(
        f"Summary: {len(data['tracks'])} tracks | "
        f"{len(track0_segs)} main cuts + {len(track1_segs)} PIP | "
        f"{len(tier1_segs)} Tier-1 + {len(tier2_segs)} Tier-2 + {len(subtitle_segs)} Subtitles | "
        f"{len(VO_PHRASES)} VO phrases | {len(bgm_segs)} BGM stages | {len(sfx_segs)} SFX"
    )


if __name__ == "__main__":
    main()
