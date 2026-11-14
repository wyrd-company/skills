# Templates

Starting files for the mechanical requirements — the ones where a template
produces a correct file rather than filler.

| Template                 | Destination                                |
| ------------------------ | ------------------------------------------ |
| `gitattributes`          | `.gitattributes`                           |
| `editorconfig`           | `.editorconfig`                            |
| `renovate.json`          | `.github/renovate.json`                    |
| `lefthook.yml`           | `.config/lefthook.yml`                     |
| `taskfile.yml`           | `taskfile.yml`                             |
| `ci.yml`                 | `.github/workflows/ci.yml`                 |
| `repo-settings.yml`      | `.github/repo-settings.yml`                |
| `reconcile-settings.yml` | `.github/workflows/reconcile-settings.yml` |

There is deliberately **no template for `README.md`, `AGENTS.md`, or
`CONTRIBUTING.md`.** Those require judgment, and a template produces filler that
survives review because it looks finished.

## Pinning actions

Every `uses:` in `ci.yml` carries a **null SHA** — forty zeros — and a trailing
comment naming the tag to resolve:

```yaml
- uses: actions/checkout@0000000000000000000000000000000000000000 # v4
```

A null SHA is not a valid ref, so an unresolved template fails loudly instead of
silently running something unintended. Resolve every one when setting up or
fixing a workflow:

Resolve the reference's object type as well as its SHA. A lightweight tag
points directly to a commit; an annotated tag points to a tag object that must
be peeled. Follow nested tag objects until the target is a commit, and reject
other object types:

```bash
resolve_action_commit() {
  local action_repo="$1" action_tag="$2"
  local action_object action_type action_sha
  action_object=$(gh api "repos/$action_repo/git/ref/tags/$action_tag" \
    --jq '.object | [.type, .sha] | @tsv') || return
  read -r action_type action_sha <<< "$action_object"
  while [[ "$action_type" == tag ]]; do
    action_object=$(gh api "repos/$action_repo/git/tags/$action_sha" \
      --jq '.object | [.type, .sha] | @tsv') || return
    read -r action_type action_sha <<< "$action_object"
  done
  if [[ "$action_type" != commit ]]; then
    printf 'Expected a commit, received %s\n' "$action_type" >&2
    return 1
  fi
  printf '%s\n' "$action_sha"
}

resolve_action_commit '<owner>/<repo>' '<tag>'
```

Use the returned full commit SHA in `uses:` and keep the resolved tag in the
version comment. Do not use the annotated tag object's SHA as the action pin.

An action pinned to a tag is an action whose code can change under you. Renovate
updates pinned SHAs and keeps the comment current.
