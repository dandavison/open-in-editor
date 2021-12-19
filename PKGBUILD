# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.
# Maintainer: Daniel Kukula <daniel.kuku@gmail.com>
pkgname=open-in-editor-git
pkgver=r105.9329799
pkgrel=1
epoch=
pkgdesc="Open a local file from a URL at a line number in an editor/IDE."
arch=('any')
url="https://github.com/dandavison/open-in-editor"
license=()
groups=()
depends=('python')
makedepends=('git')
checkdepends=()
optdepends=()
provides=('open-in-editor')
conflicts=('open-in-editor')
replaces=('open-in-editor')
backup=()
options=()
install=
changelog=
source=("${pkgname}::git+https://github.com/dkuku/open-in-editor.git")
noextract=()
md5sums=('SKIP')
validpgpkeys=()

pkgver() {
  cd "${pkgname}"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

build() {
  cd "${pkgname}"
}

package() {
  cd "${pkgname}"
  install -Dm755 "open-in-editor" "$pkgdir/usr/bin/open-in-editor"
  install -Dm644 "linux/open-in-editor.desktop" "$pkgdir/usr/share/applications/open-in-editor.desktop"
}
