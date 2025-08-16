# RujiBoot Development Notes

## Branches

- `ani-dev`: main development branch (default working branch).
- `main`: stable releases only. Merges from `ani-dev` when tested.

## Workflow

1. Work on `ani-dev` branch.
2. Test new features locally (CLI or GUI).
3. Once stable, switch to `main` and merge:

```bash
git checkout main
git merge ani-dev
git tag -a vX.Y.Z -m "Stable release"
git push origin main --tags
```

4. Build release artifacts from `main` (e.g., `.deb`, `.AppImage`).

## Building `.deb` Package

Run from project root:

```bash
bash build_deb.sh
```

Resulting `.deb` file will be in: `dist/rujiboot_<version>.deb`

## Notes

- All source code is inside the `rujiboot/` directory.
- Translations are in `rujiboot/data/lang/`.
- Installer scripts and .desktop entry are in `installer/`.
