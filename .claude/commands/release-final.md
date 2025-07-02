# Release Final Command

Execute a fully automated final release with proven LLM-guided release best practices.

This command implements a validated process to create a final release with automated monitoring and next development cycle setup. Successfully tested with frigid v4.1 release.

## Usage

```
/release-final <version>
```

Where `<version>` is the target release version (e.g., `1.6.0`, `2.0.0`). Claude Code will substitute the version argument into the instructions below.

## Prerequisites

Before running this command, ensure:
- GitHub CLI (`gh`) is installed and authenticated
- For new releases: All changes are committed to `master` branch
- For existing release branches: Release candidate has been validated and tested

## Process

The command will guide you through:

1. **Branch Setup**: Create new release branch or checkout existing one
2. **Version Bump**: Set version to final release (major/minor/patch as appropriate)
3. **Update Changelog**: Run Towncrier to build final changelog
4. **QA Monitoring**: Push commits and monitor QA workflow with GitHub CLI
5. **Tag Release**: Create signed git tag after QA passes
6. **Release Monitoring**: Monitor release workflow deployment
7. **Cleanup**: Remove news fragments and cherry-pick back to master
8. **Next Development Cycle**: Set up master branch for next development version

## GitHub CLI Monitoring

The process uses optimized GitHub CLI commands for real-time workflow monitoring:

- `gh run watch --compact --interval 30` for efficient token usage
- Two-phase validation: QA workflow → Release workflow
- Automatic halt on any failures for human consultation

## Safety Requirements

**CRITICAL**: You MUST halt the process and consult with the user if ANY of the following occur:

- **Step failures**: If any command fails, git operation errors, or tests fail
- **Workflow failures**: If QA or release workflows show failed jobs
- **Unexpected output**: If commands produce unclear or concerning results
- **Version conflicts**: If version bumps don't match expected patterns
- **Network issues**: If GitHub operations timeout or fail repeatedly

**Your responsibilities**:
- Validate each step succeeds before proceeding to the next
- Monitor workflow status and halt on any failures
- Provide clear progress updates throughout the process
- Maintain clean git hygiene and proper branching
- Use your judgment to assess when manual intervention is needed

## Release Process

Execute the following steps for target version `$ARGUMENTS`:

### 1. Pre-Release Quality Check
Run local quality assurance to catch issues early:
```bash
git status && git pull origin master
hatch --env develop run linters
hatch --env develop run testers  
hatch --env develop run docsgen
```

### 2. Release Branch Setup
Determine release branch name from target version (e.g., `4.1` → `release-4.1`).

**If release branch exists** (for RC→final conversion or patches):
```bash
git checkout release-X.Y
git pull origin release-X.Y
```

**If creating new release branch**:
```bash
git checkout master && git pull origin master
git checkout -b release-X.Y
```

### 3. Version Management
Choose appropriate version bump based on target version:
- **X.Y.0 with existing RC**: Use `hatch version release` (converts RC to final)
- **X.Y.0 new minor**: Use `hatch version minor` or `hatch version release` as appropriate
- **X.0.0 major**: Use `hatch version major`  
- **X.Y.Z patch**: Use `hatch version patch`

```bash
hatch version <strategy>
git add . && git commit -m "Bump version to $(hatch version)."
```

### 4. Changelog Generation
```bash
hatch --env develop run towncrier build --keep --version $(hatch version)
git add . && git commit -m "Update changelog for v$(hatch version) release."
```

### 5. Quality Assurance Phase
Push branch and monitor QA workflow:
```bash
# Use -u flag for new branches, omit for existing
git push [-u] origin release-X.Y

# Monitor QA workflow - get run ID from output
gh run list --workflow=qa --limit=1
gh run watch <qa-run-id> --interval 30 --compact
```
**Halt if any QA jobs fail.**

### 6. Release Deployment
After QA passes, tag and monitor release:
```bash
git tag -m "Release v$(hatch version): <brief-description>." v$(hatch version)
git push --tags

gh run list --workflow=release --limit=1  
gh run watch <release-run-id> --interval 30 --compact
```
**Halt if release workflow fails.**

### 7. Post-Release Cleanup
```bash
git rm .auxiliary/data/towncrier/*.rst
git commit -m "Clean up news fragments."
git push origin release-X.Y
```

### 8. Master Branch Integration
Cherry-pick release commits back to master:
```bash
git checkout master && git pull origin master
git cherry-pick <changelog-commit-hash>
git cherry-pick <cleanup-commit-hash>
git push origin master
```

### 9. Next Development Cycle (Major/Minor Releases Only)
For X.Y.0 releases, set up next development version:
```bash
hatch version minor,alpha
git add . && git commit -m "Bump version to $(hatch version) for next development cycle."
git tag -m "Start development for v$(hatch version | sed 's/a[0-9]*$//')." i$(hatch version | sed 's/a[0-9]*$//')
git push origin master --tags
```

**Skip this step for patch releases (X.Y.Z).**

## Notes

- **Branch Detection**: Use your judgment to determine if release branch exists
- **Version Strategy**: Choose appropriate `hatch version` command based on target version pattern
- **Monitoring**: If `gh watch` times out, simply reissue the same command
- **Validation**: Ensure all test matrix jobs pass before proceeding to next phase
- **Development Cycle**: Only set up next minor version for X.Y.0 releases, not patches
- **Commit References**: Use `git log --oneline` to identify commit hashes for cherry-picking

## Proven Results

Successfully validated with frigid v4.1 release (July 2025):
- ✅ Complete automation from branch creation to PyPI publication
- ✅ Full test matrix across 3 platforms and multiple Python versions
- ✅ Real-time workflow monitoring with GitHub CLI
- ✅ Clean git hygiene and proper development cycle transition
- ✅ Zero manual intervention required