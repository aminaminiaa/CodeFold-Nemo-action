در ادامه یک فایل راهنمای مارک‌داون (`README-KDE.md` یا `INSTALL-KDE.md`) برای گیت‌هاب آماده کرده‌ام. این راهنما شامل یک اسکریپت یکپارچه است که کاربر (حتی اگر از پوسته fish استفاده کند) می‌تواند با اجرای یک دستور ساده، تمام مراحل نصب، ساخت منوها و تنظیم دسترسی‌ها را به درستی انجام دهد.

شما می‌توانید متن زیر را مستقیماً در فایل راهنمای گیت‌هاب خود قرار دهید:

---

```markdown
# 🐬 نصب CodeFold برای KDE Plasma (Dolphin)

این راهنما برای کاربرانی است که از محیط کاربری **KDE Plasma** و فایل‌منجر **Dolphin** (مانند توزیع‌های CachyOS، Arch Linux، Kubuntu و ...) استفاده می‌کنند. از آنجایی که Dolphin از Nemo Actions پشتیبانی نمی‌کند، ما در اینجا از **Service Menus** استاندارد KDE استفاده می‌کنیم.

## 🚀 نصب سریع (نصب خودکار)

برای نصب کامل اسکریپت و اضافه شدن گزینه‌ها به کلیک‌راست دلفین، کافیست ترمینال را در پوشه‌ای که فایل `codefold.py` قرار دارد باز کنید و دستور زیر را کپی و در ترمینال اجرا کنید:

```bash
bash -c '
echo "=== Installing CodeFold for Dolphin ==="

# 1. Install dependencies (Arch Linux/CachyOS)
if command -v pacman &> /dev/null; then
    sudo pacman -S --needed --noconfirm libnotify
fi

# 2. Copy the main script and set execute permissions
echo "📋 Installing codefold.py to /usr/local/bin..."
sudo cp codefold.py /usr/local/bin/
sudo chmod 755 /usr/local/bin/codefold.py

# 3. Create KDE Service Menus directory
mkdir -p ~/.local/share/kio/servicemenus/

# 4. Create Combine Action (for directories)
echo "📋 Creating Combine action..."
cat << "EOF" > ~/.local/share/kio/servicemenus/codefold-combine.desktop
[Desktop Entry]
Type=Service
MimeType=inode/directory;
Actions=combine;
X-KDE-ServiceTypes=KonqPopupMenu/Plugin

[Desktop Action combine]
Name=CodeFold - Combine
Icon=folder-symbolic
Exec=bash -c "python3 /usr/local/bin/codefold.py -c \"%f\" \"$(dirname \"%f\")/$(basename \"%f\")_combined.txt\""
EOF

# 5. Create Extract Action (for text files)
echo "📋 Creating Extract action..."
cat << "EOF" > ~/.local/share/kio/servicemenus/codefold-extract.desktop
[Desktop Entry]
Type=Service
MimeType=text/plain;
Actions=extract;
X-KDE-ServiceTypes=KonqPopupMenu/Plugin

[Desktop Action extract]
Name=CodeFold - Extract
Icon=folder-symbolic
Exec=bash -c "python3 /usr/local/bin/codefold.py -e \"%f\" \"$(dirname \"%f\")/$(basename \"%f\" .txt)_extracted\""
EOF

# 6. Fix execute permissions for KDE Plasma security
chmod +x ~/.local/share/kio/servicemenus/codefold-combine.desktop
chmod +x ~/.local/share/kio/servicemenus/codefold-extract.desktop

# 7. Update KDE cache and restart Dolphin
echo "🔄 Restarting Dolphin and updating cache..."
kbuildsycoca6 &> /dev/null
killall dolphin &> /dev/null || true

echo "✅ Installation completed successfully! You can now open Dolphin."
'

```

---

## 📖 نحوه استفاده

پس از اجرای کد بالا، دلفین را باز کنید:

* **ترکیب فایل‌ها (Combine):** روی هر پوشه‌ای که می‌خواهید کلیک راست کنید، به بخش **Actions** بروید و روی `CodeFold - Combine` کلیک کنید. یک فایل متنی شامل کل کدهای پروژه در همان مسیر ساخته می‌شود.
* **استخراج فایل‌ها (Extract):** روی فایل متنیِ تولید شده کلیک راست کنید، به بخش **Actions** بروید و روی `CodeFold - Extract` کلیک کنید. پوشه‌ای حاوی فایل‌های اصلی استخراج خواهد شد.

---

## 🗑️ حذف (Uninstall)

در صورتی که می‌خواهید این ابزار را از دلفین حذف کنید، دستور زیر را در ترمینال اجرا کنید:

```bash
bash -c '
echo "🗑️ Removing CodeFold..."
sudo rm -f /usr/local/bin/codefold.py
rm -f ~/.local/share/kio/servicemenus/codefold-combine.desktop
rm -f ~/.local/share/kio/servicemenus/codefold-extract.desktop
kbuildsycoca6 &> /dev/null
killall dolphin &> /dev/null || true
echo "✅ CodeFold uninstalled successfully!"
'

```

```

### چند نکته که در این راهنما رعایت شده است:
1. **سازگاری با Fish و Zsh:** تمام کدها داخل `bash -c` قرار گرفته‌اند تا کاربران Fish با خطاهای مربوط به Here-Document (`<< EOF`) مواجه نشوند.
2. **مجوزهای امنیتی:** بخش `chmod +x` برای فایل‌های `.desktop` و `chmod 755` برای اسکریپت پایتون تعبیه شده تا کاربرانی که آن را نصب می‌کنند با خطای "You are not authorized to execute this file" مواجه نشوند.
3. **مدیریت پکیج‌ها:** از آنجایی که اشاره کردید پروژه بر پایه Arch است، دستور `pacman` برای چک کردن و نصب `libnotify` گنجانده شده است.

```