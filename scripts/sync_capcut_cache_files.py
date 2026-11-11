import os, shutil

PROJ_DIR = r"C:\Users\Hang thu\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\TVC WinHair CS2 - ban Reels_v2 (1)-sao chép"
TL_DIR = os.path.join(PROJ_DIR, "Timelines", "C8D29776-5FFB-4dd3-8698-E26DA5C9C410")
PATCH_DIR = os.path.join(TL_DIR, "attachment", "patch")
DRAFT_INFO = os.path.join(TL_DIR, "draft_info.json")
MAIN_JSON = os.path.join(PROJ_DIR, "draft_content.json")

BAK_DIR = r"C:\Users\Hang thu\.gemini\antigravity\brain\736203b4-cb9e-4e44-b2cb-b3a23baa248a\scratch\backup_tvc_copy"
os.makedirs(BAK_DIR, exist_ok=True)

# Move .bak_before_ai files out of project folder into BAK_DIR to keep CapCut folder clean
for f in [MAIN_JSON + ".bak_before_ai", os.path.join(TL_DIR, "draft_content.json.bak_before_ai")]:
    if os.path.exists(f):
        shutil.copy2(f, os.path.join(BAK_DIR, os.path.basename(f)))
        os.remove(f)

if os.path.exists(PATCH_DIR):
    bak_patch = os.path.join(BAK_DIR, "patch")
    if not os.path.exists(bak_patch):
        shutil.copytree(PATCH_DIR, bak_patch)
    shutil.rmtree(PATCH_DIR)
    print("Backed up and removed stale attachment/patch cache so CapCut loads draft_content.json directly.")

if os.path.exists(DRAFT_INFO):
    shutil.copy2(DRAFT_INFO, os.path.join(BAK_DIR, "draft_info.json.bak"))
    shutil.copy2(MAIN_JSON, DRAFT_INFO)
    print("Synced Timelines/.../draft_info.json with upgraded draft_content.json.")
