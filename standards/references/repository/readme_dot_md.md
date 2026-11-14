# README.md

A README.md must be added to the root of every repository, and may be added to sub-folders selectively.

README.md files are primarily for human users. [AGENTS.md](agents_dot_md.md) are for agents.

## Root README.md contents

The root README.md serves as the front-door to the repo for users into the repo.

What it contains depends on the nature of the repo. 

### Non-monorepos

In rought order, each section as applicable:

- Badges & product/docs link
- Title/logo (light/dark)
- Tagline. This should be catchy.
- Animated gif (preferred), hero screenshot - where applicable
- Features: list the major features of the repo
- How to get it: How to get/download/install whatever the repo produces
- Quickstart: the best way to understand the value/get the value in the most minimal usage example
- Credits: What inspired/similar projects, major dependencies, upstream if it is a fork, etc
- License: How is the project licensed with a link to the LICENSE file

### Monorepos

- A title
- Components:
    - Name and logo
    - A brief description
    - Link to the component's website (when it exists) and readme
    - Badges
- Credits: What inspired/similar projects, major dependencies, upstream if it is a fork, etc
- License: How is the project licensed with a link to the LICENSE file

Each component's readme should mirror a non-monorepo readme.

## Other README.md

How the user should use/understand this sub-folder. Reserve this for folders with non-obvious content.