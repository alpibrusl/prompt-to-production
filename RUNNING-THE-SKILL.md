# Running the Skill

This book ships with a skill -- a folder an AI agent can read -- that
checks a project against this book's closing checklist -- the real files, the CI configuration, the git history -- before anyone tells you it is ready for real users.

It is the closing chapter, written so an agent runs it on itself. You can
read the chapter and do the checking by hand -- the skill is a convenience,
not a prerequisite -- but it is the difference between remembering to ask
"is this ready to ship?" and having something ask it for you every time.

Installing it is copying a folder. There is nothing to compile, nothing to
sign up for, and no way for it to change anything: the skill reads.

## Get the folder

The skill lives in this book's repository, at `skills/verify-production/`. Download
or clone the repository, and that folder is what you need. It contains a
`SKILL.md` and a `references/` folder next to it, and both have to travel
together -- the checklist the skill actually works from lives in
`references/`, so a copy of `SKILL.md` on its own will load and then have
nothing to check against.

## Claude Code

Copy the folder into your personal skills directory:

```
~/.claude/skills/verify-production/
```

That makes it available in every project. To scope it to one project
instead, copy it to `.claude/skills/verify-production/` inside that project.

Start Claude Code and ask it something the skill is for. It decides for
itself when the skill applies -- you do not invoke it by name.

## opencode

opencode reads `~/.claude/skills/` as well, so if you have already done the
step above there is nothing else to do.

Otherwise, copy the folder to opencode's own directory:

```
~/.config/opencode/skills/verify-production/
```

Or, to keep the skill where it already is rather than copying it, point
opencode at the repository from a project's `opencode.jsonc`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": { "paths": ["/path/to/prompt-to-production/skills"] }
}
```

Check it loaded with `opencode debug skill`, which lists every skill
opencode can see and where each one came from.

Skill support arrived in opencode over several releases, and the fixes that
made a skill's `references/` folder resolve correctly landed in 1.17.10 and
1.17.12. On an older build the skill loads and then cannot read its own
checklist, which is a confusing way to fail. `opencode upgrade` is the fix.

## Anything else

The format is a folder with a `SKILL.md` in it, and a growing number of
agents read it. If yours does, the folder above is the folder to give it.
If it does not, the closing chapter is the same checklist in prose, and
reading it yourself was always the point.
