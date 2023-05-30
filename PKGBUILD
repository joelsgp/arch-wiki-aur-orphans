# Maintainer: jmcb <joelsgp@protonmail.com>

pkgname=arch-wiki-aur-orphans-git
pkgver=v0.1.0.r2.ga495643
pkgrel=1
pkgdesc="Script to locate any AUR packages that are broken and also referenced in the arch wiki"
arch=('any')
url="https://github.com/joelsgp/arch-wiki-aur-orphans"
license=('GPL3')
depends=('arch-wiki-docs'
         'grep'
         'python'
         'python3-aur')
makedepends=('git')
checkdepends=()
optdepends=()
provides=("${pkgname%-git}")
conflicts=("${pkgname%-git}")
source=("git+https://github.com/joelsgp/${pkgname%-git}.git")
sha256sums=('SKIP')

pkgver() {
  cd "${pkgname%-git}"
  git describe --long --tags --abbrev=7 | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}

package() {
  cd "${pkgname%-git}"

  # copy files
  _opt="${pkgdir}/opt/${pkgname%-git}"
  install -D -t "${_opt}/" 'aur_orphans.py' 'list-wiki.sh' 'run.sh'

  # symlink to PATH
  _bin="${pkgdir}/usr/bin"
  install -d "${_bin}"
  ln -s "/opt/${pkgname%-git}/run.sh" "${_bin}/${pkgname%-git}"
}
