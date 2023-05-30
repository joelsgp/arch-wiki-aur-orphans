#  arch-wiki-aur-orphans

Script to locate any AUR packages that are broken and also referenced in the arch wiki

1. Clone
   - `git clone https://github.com/joelsgp/arch-wiki-aur-orphans.git`
2. Install dependencies from PKGBUILD
   - `makepkg --install`
3. Run the script
   - `./run.sh`
   - This will give you some output like: `Non-existent: reflector-timer`
4. Find where the listed packages are
   - `./aur-wiki-find 'reflector-timer'`
