@echo off
chcp 65001 >nul
echo ========================================================
echo   ĐỒNG BỘ TOÀN BỘ DỰ ÁN LÊN GITHUB (huusei1234-droid)
echo ========================================================
echo.
echo [1/3] Đang xóa phiên đăng nhập GitHub cũ (hieulan9d) trong Windows Credential Manager...
cmdkey /delete:git:https://github.com >nul 2>&1
cmdkey /delete:LegacyGeneric:target=git:https://github.com >nul 2>&1

echo [2/3] Đang đẩy toàn bộ 678 files lên https://github.com/huusei1234-droid/EDITVIDEO ...
echo       (Cửa sổ đăng nhập GitHub sẽ hiện lên, bạn hãy chọn "Sign in with your browser" với tài khoản huusei1234-droid)
cd /d "d:\antigraviti"
git push -u origin main

echo.
echo [3/3] Hoàn tất!
pause
