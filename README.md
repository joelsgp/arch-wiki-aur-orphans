#  arch-wiki-aur-orphans

update: lol I think their bot already does this actually,

https://wiki.archlinux.org/title/Special:WhatLinksHere/Template:Broken_package_link

Here, function `update_package_template`
https://github.com/lahwaacz/wiki-scripts/blob/master/update-package-templates.py

See also:
* https://wiki.archlinux.org/title/Template:Broken_package_link
* https://wiki.archlinux.org/title/Help:Procedures#Fix_broken_package_links
* https://wiki.archlinux.org/title/ArchWiki:Bots#Package_templates
* https://wiki.archlinux.org/title/AUR_Cleanup_Day

Script to locate any AUR packages that are broken and also referenced in the arch wiki

Current output as of 2023-05-30: https://gist.github.com/joelsgp/f2090cf0744cacd964e6f29a06ef6362

## Instructions
1. Clone
   - `git clone https://github.com/joelsgp/arch-wiki-aur-orphans.git`
2. Install dependencies from PKGBUILD
   - `makepkg --install`
3. Run the script
   - `./run.sh`
   - This will give you some output like: `Non-existent: reflector-timer`
4. Find where the listed packages are
   - `./aur-wiki-find 'reflector-timer'`


## Notes
Mediawiki has this feature but I don't think it's enabled for archwiki https://www.mediawiki.org/wiki/Help:Linksearch

nvm it is, see here https://wiki.archlinux.org/title/Special:LinkSearch/
