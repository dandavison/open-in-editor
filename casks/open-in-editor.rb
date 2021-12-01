cask "open-in-editor" do
  version "1.0"
  sha256 "68554df16c05a222f9fd95c8ce0f51a07e0a714db31dc43bf06e5addf591b15d"

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
