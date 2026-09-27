# Project Provenance

## Current project

My360Export is maintained as a Fusion 360 engineering utility by Iván Rodríguez-Méndez.

The repository contains code developed in 2022 together with adapted code from earlier Fusion 360 add-in work.

## Original work

The repository explicitly references Patrick Rainsberry as the author of the original add-in version.

Some files still contain copyright notices such as:

```text
Copyright (c) 2020 by Patrick Rainsberry.
```

Other files identify:

```text
Created By: Ivan Rodriguez-Mendez
Original version by: Patrick Rainsberry
```

These attributions are preserved intentionally.

## License

The repository LICENSE file contains the Apache License 2.0 notice associated with Patrick Rainsberry's original work.

The README previously referenced MIT, which was inconsistent with the actual repository license.

The repository documentation now follows the LICENSE file and identifies Apache 2.0 as the governing license.

## Helper framework

The repository also references the `apper` Fusion 360 helper framework through `.gitmodules`:

```text
https://github.com/tapnair/apper
```

The current repository state should be reviewed before changing dependency handling because the declared submodule path and the current working tree are not fully aligned.

## Maintenance principle

Future changes should preserve:

- original copyright headers
- author attribution
- Apache 2.0 licensing
- references to upstream projects where code was adapted
