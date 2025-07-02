# Release Final Command

Execute a fully automated final release with LLM-guided release best practices.

This command implements a process to create a final release with automated monitoring and next development cycle setup.

## Usage

```
/release-final <version>
```

Where `<version>` is the target release version (e.g., `1.6.0`, `2.0.0`).

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

## Safety Features

- **Validation at each step**: Process halts if any step fails
- **Real-time status reporting**: Clear progress updates throughout
- **Error handling**: Immediate stop for manual intervention if needed
- **Git hygiene**: Maintains clean commit history and proper branching
- **Development continuity**: Automatically sets up next development cycle

## Command Sequence

Execute these commands, replacing `$ARGUMENTS` with the target version:

```bash
# Parse version to determine release branch and version bump strategy
TARGET_VERSION="$ARGUMENTS"
RELEASE_BRANCH="release-$(echo $TARGET_VERSION | cut -d. -f1-2)"

# 1. Determine if release branch exists and checkout/create appropriately
if git show-ref --verify --quiet refs/remotes/origin/$RELEASE_BRANCH; then
    echo "Existing release branch found"
    git checkout $RELEASE_BRANCH
    git pull origin $RELEASE_BRANCH
else
    echo "Creating new release branch"
    git checkout master
    git pull origin master
    git checkout -b $RELEASE_BRANCH
fi

# 2. Set version to target release
# For new branches: bump major/minor as needed
# For existing branches with RC: convert RC to final with `hatch version release`
# For patch releases: use `hatch version patch`
if [[ "$TARGET_VERSION" =~ ^[0-9]+\.0\.0$ ]]; then
    # Major release
    hatch version major
elif [[ "$TARGET_VERSION" =~ ^[0-9]+\.[0-9]+\.0$ ]]; then
    # Minor release - check if current version is RC
    CURRENT_VERSION=$(hatch version)
    if [[ "$CURRENT_VERSION" =~ rc ]]; then
        hatch version release
    else
        hatch version minor
    fi
else
    # Patch release
    hatch version patch
fi
git add . && git commit -m "Bump version to $(hatch version)."

# 3. Run Towncrier to Build Final Changelog
hatch --env develop run towncrier build --keep --version $(hatch version)
git add . && git commit -m "Update changelog for v$(hatch version) release."

# 4. Push branch with upstream tracking if new, monitor QA
if git show-ref --verify --quiet refs/remotes/origin/$RELEASE_BRANCH; then
    git push origin $RELEASE_BRANCH
else
    git push -u origin $RELEASE_BRANCH
fi
gh run list --workflow=qa --limit=1
gh run watch <qa-run-id> --interval 30 --compact

# 5. Tag the Final Release (After QA Passes)
git tag -m "Release v$(hatch version): <brief-description>." v$(hatch version)
git push --tags

# 6. Monitor Release Workflow
gh run list --workflow=release --limit=1
gh run watch <release-run-id> --interval 30 --compact

# 7. Clean Up News Fragments (After Release Completes)
git rm .auxiliary/data/towncrier/*.rst
git commit -m "Clean up news fragments."
git push origin $RELEASE_BRANCH

# 8. Cherry-pick Back to Master
git checkout master
git pull origin master
git cherry-pick <changelog-commit-hash>
git cherry-pick <cleanup-commit-hash>
git push origin master

# 9. Set Up Next Development Cycle on Master (for new major/minor releases)
if [[ "$TARGET_VERSION" =~ ^[0-9]+\.[0-9]+\.0$ ]]; then
    hatch version minor,alpha
    git add . && git commit -m "Bump version to $(hatch version) for next development cycle."
    
    # 10. Tag Start of Development for Next Release
    git tag -m "Start development for v$(hatch version | sed 's/a[0-9]*$//')." i$(hatch version | sed 's/a[0-9]*$//')
    git push origin master --tags
fi
```

## Notes

- For new release branches: Creates branch from master and sets up upstream tracking
- For existing release branches: Updates from existing RC or patches as appropriate  
- Version bump strategy determined by target version pattern:
  - `X.0.0` → Major release
  - `X.Y.0` → Minor release (or RC→final conversion)
  - `X.Y.Z` → Patch release
- Next development cycle setup only occurs for major/minor releases
- All monitoring and validation ensures quality before deployment