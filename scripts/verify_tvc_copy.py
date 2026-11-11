import os
import json

PROJ_DIR = r"C:\Users\Hang thu\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\TVC WinHair CS2 - ban Reels_v2 (1)-sao chép"
MAIN_JSON = os.path.join(PROJ_DIR, "draft_content.json")

with open(MAIN_JSON, "r", encoding="utf-8") as f:
    d = json.load(f)

all_mats = {}
for k, v in d["materials"].items():
    if isinstance(v, list):
        for item in v:
            if isinstance(item, dict) and "id" in item:
                all_mats[item["id"]] = (k, item)

missing_mat_ids = []
missing_extra_refs = []
overlaps = []
missing_files = []

for t_idx, trk in enumerate(d["tracks"]):
    segs = trk.get("segments", [])
    for s_idx, s in enumerate(segs):
        mid = s.get("material_id")
        if mid not in all_mats:
            missing_mat_ids.append((t_idx, s_idx, mid))
        else:
            mk, mitem = all_mats[mid]
            p = mitem.get("path", "")
            if p and not p.startswith("##_draftpath_placeholder_"):
                if not os.path.exists(p.replace("/", "\\")):
                    missing_files.append((t_idx, s_idx, mk, p))
        for r in s.get("extra_material_refs", []):
            if r not in all_mats:
                missing_extra_refs.append((t_idx, s_idx, r))
        if s_idx > 0:
            prev = segs[s_idx - 1]
            prev_end = prev["target_timerange"]["start"] + prev["target_timerange"]["duration"]
            cur_st = s["target_timerange"]["start"]
            # Note: video transitions overlap in source or have transition duration, check non-video or > 1 frame overlap
            if cur_st < prev_end - 34000:
                overlaps.append((t_idx, trk["type"], s_idx, prev_end / 1e6, cur_st / 1e6))

print("Total tracks:", len(d["tracks"]))
print("Missing material_ids:", len(missing_mat_ids), missing_mat_ids[:5])
print("Missing extra_material_refs:", len(missing_extra_refs), missing_extra_refs[:5])
print("Missing disk files:", len(missing_files), missing_files[:5])
print("Track overlaps (>1 frame):", len(overlaps), overlaps[:5])
