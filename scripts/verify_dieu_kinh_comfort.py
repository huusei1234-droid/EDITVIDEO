import os
import json

PROJ_DIR = r"C:\Users\Hang thu\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\ĐIỀU KINH 1-sao chép"
MAIN_JSON = os.path.join(PROJ_DIR, "draft_content.json")
TIMELINE_JSON = os.path.join(PROJ_DIR, "Timelines", "EDFEB15A-2B91-4b7a-A32A-DF48A6E5FA3E", "draft_content.json")
PATCH_DIR = os.path.join(PROJ_DIR, "Timelines", "EDFEB15A-2B91-4b7a-A32A-DF48A6E5FA3E", "attachment", "patch")


def main():
    with open(MAIN_JSON, "r", encoding="utf-8") as f:
        d = json.load(f)

    errors = []

    # 1. Index all materials by ID and check disk paths
    all_mats = {}
    vid_durs = {}
    aud_durs = {}
    for cat, items in d["materials"].items():
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and "id" in item:
                    all_mats[item["id"]] = (cat, item)
                    p = item.get("path", "")
                    if p and not p.startswith("##"):
                        if not os.path.exists(p):
                            errors.append(f"MISSING PATH in {cat}: {p}")
                    if cat == "videos":
                        vid_durs[item["id"]] = item["duration"]
                    elif cat == "audios":
                        aud_durs[item["id"]] = item["duration"]
                    elif cat == "material_animations":
                        for an in item.get("animations", []):
                            ap = an.get("path", "")
                            if ap and not os.path.exists(ap):
                                errors.append(f"MISSING ANIM PATH: {ap}")
                    elif cat == "texts":
                        fp = item.get("font_path", "")
                        if fp and not os.path.exists(fp):
                            errors.append(f"MISSING FONT PATH: {fp}")

    # 2. Check every track & segment
    for ti, trk in enumerate(d["tracks"]):
        prev_end = 0
        for si, seg in enumerate(trk["segments"]):
            mid = seg["material_id"]
            if mid not in all_mats:
                errors.append(f"Track {ti} Seg {si}: missing material_id {mid}")
            for ref in seg.get("extra_material_refs", []):
                if ref not in all_mats:
                    errors.append(f"Track {ti} Seg {si}: missing extra_material_ref {ref}")

            t_st = seg["target_timerange"]["start"]
            t_du = seg["target_timerange"]["duration"]
            if t_du <= 0:
                errors.append(f"Track {ti} Seg {si}: non-positive duration {t_du}")

            if ti == 0:
                # Track 00 must be strictly contiguous with zero black gaps!
                if abs(t_st - prev_end) > 5:
                    errors.append(f"Track 00 gap/overlap at Seg {si}: start={t_st} vs prev_end={prev_end}")
            else:
                if t_st < prev_end - 5:
                    errors.append(f"Track {ti} overlap at Seg {si}: start={t_st} < prev_end={prev_end}")
            prev_end = t_st + t_du

            # Check source timerange within media duration
            src = seg.get("source_timerange")
            if src:
                s_st = src["start"]
                s_du = src["duration"]
                if mid in vid_durs and s_st + s_du > vid_durs[mid] + 34000:
                    errors.append(f"Track {ti} Seg {si}: video source {s_st}+{s_du} > {vid_durs[mid]}")
                if mid in aud_durs and s_st + s_du > aud_durs[mid] + 34000:
                    errors.append(f"Track {ti} Seg {si}: audio source {s_st}+{s_du} > {aud_durs[mid]}")

    # 3. Check Timeline sync & absence of stale WAL patch
    if os.path.exists(TIMELINE_JSON):
        if os.path.getsize(MAIN_JSON) != os.path.getsize(TIMELINE_JSON):
            errors.append("Size mismatch between root draft_content.json and Timelines draft_content.json")
    if os.path.exists(PATCH_DIR):
        errors.append(f"Stale WAL patch folder still exists: {PATCH_DIR}")

    print(f"=== VERIFY ĐIỀU KINH 1-sao chép ===")
    print(f"Canvas: {d['canvas_config']['width']}x{d['canvas_config']['height']} @ {d['fps']}fps | Duration: {d['duration']/1e6:.2f}s")
    print(f"Total materials indexed: {len(all_mats)} | Tracks: {len(d['tracks'])}")
    for ti, trk in enumerate(d["tracks"]):
        print(f"  Track {ti:02d} ({trk['type']:5s}): {len(trk['segments']):2d} segments")
    if errors:
        print("ERRORS FOUND:")
        for e in errors:
            print("  [X]", e)
        raise SystemExit(1)
    else:
        print("ALL CHECKS PASSED: 0 missing refs, 0 missing disk paths, 0 gaps/overlaps, WAL cache clean!")


if __name__ == "__main__":
    main()
