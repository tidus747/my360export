# Contributing

## Development model

My360Export uses GitFlow for maintenance.

```mermaid
gitGraph
    commit id: "master"
    branch develop
    checkout develop
    commit id: "integration"

    branch feature/example
    checkout feature/example
    commit id: "work"

    checkout develop
    merge feature/example

    branch release/x.y.z
    checkout release/x.y.z
    commit id: "release prep"

    checkout master
    merge release/x.y.z tag: "vx.y.z"

    checkout develop
    merge master
```

Use:

- `master` for stable released states.
- `develop` for integrated maintenance.
- `feature/<name>` for isolated changes.
- `fix/<name>` for fixes.
- `release/<version>` for release preparation.

## Fusion 360 validation

Most functionality depends on the Fusion 360 runtime.

Any behavior change should document:

- Fusion 360 version used for validation
- operating system
- command tested
- design/project structure used
- export formats tested

## Attribution

Do not remove existing copyright or attribution headers.

The repository includes adapted work from earlier Fusion 360 add-in projects.

See [docs/provenance.md](docs/provenance.md).

## Distribution artifacts

Do not add new large ZIP files directly under `dist/`.

Future packaged versions should preferably be attached to GitHub Releases.

The existing historical ZIP files are preserved until a dedicated migration is performed.
