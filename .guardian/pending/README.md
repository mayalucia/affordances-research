# Pending actions for mu2tau (interactive shell needed)

## 1. Refresh `gh` OAuth scope to include `workflow`

The Phase A scaffolding push was rejected because the current OAuth
token lacks the `workflow` scope required to create or update files
under `.github/workflows/`. From an interactive shell:

```bash
gh auth refresh -h github.com -s workflow
```

This opens a browser for OAuth consent. After completion, the token
will have `workflow` scope and Claude Code can push workflow files.

## 2. Move the deploy workflow into place

After the scope refresh:

```bash
cd commissions/affordances-research
mkdir -p .github/workflows
mv .guardian/pending/deploy-workflow.yml .github/workflows/deploy.yml
git add .github/workflows/deploy.yml
git commit -m "ci: add Hugo deploy workflow for GitHub Pages"
git push
```

## 3. Enable GitHub Pages with Actions source

The workflow targets GitHub Pages with the Actions deployment
mechanism. Pages must be enabled with `source: github-actions`:

```bash
gh api -X POST /repos/mayalucia/affordances-research/pages \
  -f 'source[branch]=main' \
  -f 'source[path]=/' \
  -f 'build_type=workflow' 2>&1 | head
```

Or in the web UI:
- Go to https://github.com/mayalucia/affordances-research/settings/pages
- Under "Build and deployment", set Source to "GitHub Actions"

The first push to `main` after enabling will trigger the workflow.

## 4. Verify the deploy

After step 3, the first workflow run kicks off automatically. Check:

```bash
gh run list --repo mayalucia/affordances-research --limit 5
```

Once the run completes, the site is live at:
https://mayalucia.github.io/affordances-research/

## Why this is a pending-actions file

`commissions/affordances-research/.guardian/pending/` holds actions
that require interactive credentials (browser-based OAuth, password
entry) which Claude Code cannot complete inside an automated session.
mu2tau picks these up from the interactive shell.

After all steps complete, this directory can be deleted; the
deploy-workflow.yml content lives in .github/workflows/deploy.yml
on `main`.
