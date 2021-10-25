cask "open-in-editor" do
  version "1.0"
  sha256 "4361436566e9b707af4607f25c1135729447f1a7e00670d8a582ccbb0c992658"

  github_user = "dandavison"
  url "https://github.com/#{github_user}/#{token}/archive/master.zip"
  name "OpenInEditor"
  desc "Open a local file from a URL at a line number in an editor/IDE"
  homepage "#{url}#readme"

  depends_on formula: "duti"

  bundle_id = "org.#{github_user}.#{name.first}"
  installer script: {
    executable: "#{HOMEBREW_PREFIX}/bin/duti",
    args:       %W[-s #{bundle_id} file-line-column],
  }

  uninstall quit: bundle_id
end
