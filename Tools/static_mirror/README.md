# Static GitHub Pages mirror

Builds a static, indexable mirror of the PHP site for `https://pablocirre.github.io/`.

## Local build

```powershell
python Tools/static_mirror/build_pages.py --base-url https://pablocirre.github.io --output ..\PabloCirre.github.io
```

The builder starts a temporary local PHP server, reads `sitemap_index.xml`, renders every public sitemap URL, rewrites PHP/query URLs to clean static paths, copies only public assets, writes `.nojekyll`, and validates the output.

## Publish model

The source of truth remains this PHP repository. The generated output is meant to be pushed to the separate public repository `PabloCirre/PabloCirre.github.io`, which GitHub Pages serves at the root user-site URL.

For GitHub Actions publishing, create a repository secret named `PAGES_DEPLOY_TOKEN` with write access to `PabloCirre/PabloCirre.github.io`.

## First publish

The first publish needs a one-time GitHub setup:

1. Create a public empty repository named `PabloCirre.github.io` under the `PabloCirre` account.
2. Push the generated local mirror:

```powershell
cd ..\PabloCirre.github.io
git push -u origin main
```

3. In this source repository, add the `PAGES_DEPLOY_TOKEN` Actions secret.
4. Commit and push `.github/workflows/publish-static-mirror.yml` and `Tools/static_mirror/` to `main`.

After that, every push to `main` in this source repository rebuilds and publishes the mirror.
