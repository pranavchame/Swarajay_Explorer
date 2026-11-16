# Optional GitHub Actions workflows

These templates are preserved outside `.github/workflows` because the publishing OAuth authorization does not include GitHub's `workflow` scope.

Cloudflare Pages uses `python scripts/build_site.py` for build validation and does not require these workflows. When authorized, copy `validate.yml.example` to `.github/workflows/validate.yml` to enable GitHub build checks. The Pages template is a manual alternative host; do not enable duplicate hosting when Cloudflare is the canonical production site.
