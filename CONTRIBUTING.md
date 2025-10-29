# Git Workflow and Branching Strategy

## Overview
This document outlines the Git workflow and branching strategy for the Roots Revealed project.

## Branch Structure

### Main Branches

#### `main`
- **Purpose**: Production-ready code
- **Protection**: Protected branch, requires pull request reviews
- **Deployment**: Auto-deploys to production (when CI/CD is set up)
- **Merge Policy**: Only merge from `develop` after thorough testing

#### `develop`
- **Purpose**: Integration branch for features
- **Protection**: Protected branch, requires pull request reviews
- **Testing**: All features must pass tests before merging
- **Merge Policy**: Merge from feature branches via pull requests

### Supporting Branches

#### Feature Branches
- **Naming**: `feature/<feature-name>` or `<username>/<feature-name>`
- **Purpose**: Develop new features
- **Base**: Created from `develop`
- **Merge to**: `develop`
- **Lifecycle**: Delete after merge

**Example**:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/user-authentication
# Make changes
git commit -m "Add JWT authentication"
git push origin feature/user-authentication
# Create pull request to develop
```

#### Bugfix Branches
- **Naming**: `bugfix/<issue-number>-<brief-description>`
- **Purpose**: Fix bugs in develop branch
- **Base**: Created from `develop`
- **Merge to**: `develop`

**Example**:
```bash
git checkout develop
git checkout -b bugfix/123-fix-chart-calculation
# Fix the bug
git commit -m "Fix chart calculation for southern hemisphere"
git push origin bugfix/123-fix-chart-calculation
```

#### Hotfix Branches
- **Naming**: `hotfix/<version>-<issue>`
- **Purpose**: Emergency fixes for production
- **Base**: Created from `main`
- **Merge to**: Both `main` and `develop`
- **Tagging**: Create version tag after merge

**Example**:
```bash
git checkout main
git checkout -b hotfix/1.0.1-critical-bug
# Fix critical bug
git commit -m "Fix critical security issue"
git push origin hotfix/1.0.1-critical-bug
# Merge to main and develop
git tag -a v1.0.1 -m "Hotfix: Critical security patch"
```

#### Release Branches
- **Naming**: `release/<version>`
- **Purpose**: Prepare new production release
- **Base**: Created from `develop`
- **Merge to**: Both `main` and `develop`
- **Activities**: Version bumping, documentation, minor bug fixes only

**Example**:
```bash
git checkout develop
git checkout -b release/1.1.0
# Update version numbers, changelog
git commit -m "Prepare release 1.1.0"
# Merge to main with tag
```

## Commit Message Conventions

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, semicolons, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependency updates
- **perf**: Performance improvements

### Examples
```bash
# Feature commit
git commit -m "feat(chart): Add support for divisional charts"

# Bug fix
git commit -m "fix(api): Correct aspect calculation for retrograde planets"

# Documentation
git commit -m "docs(readme): Update setup instructions for macOS"

# With body and footer
git commit -m "feat(bmad): Integrate BMAD personality analysis

- Add BMAD engine integration
- Create API endpoints for personality analysis
- Update frontend to display BMAD results

Closes #42"
```

## Pull Request Process

### 1. Before Creating PR
- [ ] Update your branch from develop: `git pull origin develop`
- [ ] Run all tests: `npm test` (frontend) and `pytest` (backend)
- [ ] Run linters: `npm run lint` and `flake8`
- [ ] Update documentation if needed
- [ ] Write/update tests for your changes

### 2. Creating the PR
- Use descriptive title: `[Feature] Add user authentication`
- Fill out PR template completely
- Link related issues: `Closes #123`
- Add labels: `enhancement`, `bug`, `documentation`, etc.
- Assign reviewers
- Set milestone if applicable

### 3. PR Review Checklist
- [ ] Code follows project style guidelines
- [ ] Tests pass in CI/CD pipeline
- [ ] Code coverage meets minimum threshold (80%)
- [ ] Documentation is updated
- [ ] No merge conflicts
- [ ] At least one approval from team member

### 4. After Approval
- Squash and merge for feature branches
- Regular merge for release/hotfix branches
- Delete branch after merge

## Workflow Examples

### Working on a New Feature
```bash
# 1. Start from develop
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/symbolon-integration

# 3. Make changes and commit regularly
git add .
git commit -m "feat(symbolon): Add card selection algorithm"

# 4. Push to remote
git push origin feature/symbolon-integration

# 5. Create pull request on GitHub
# Review → Approve → Merge → Delete branch
```

### Fixing a Bug
```bash
# 1. Create bugfix branch
git checkout develop
git checkout -b bugfix/456-aspect-orb-calculation

# 2. Fix the issue
# Edit files...
git add .
git commit -m "fix(aspects): Correct orb calculation for minor aspects"

# 3. Add test
git add .
git commit -m "test(aspects): Add test for minor aspect orbs"

# 4. Push and create PR
git push origin bugfix/456-aspect-orb-calculation
```

### Syncing Your Branch
```bash
# Keep your feature branch up to date with develop
git checkout feature/your-feature
git fetch origin
git rebase origin/develop
git push --force-with-lease origin feature/your-feature
```

## Code Review Guidelines

### For Authors
- Keep PRs small and focused (< 400 lines changed)
- Write clear descriptions
- Respond to feedback promptly
- Don't take criticism personally

### For Reviewers
- Review within 24 hours
- Be constructive and respectful
- Focus on:
  - Logic and correctness
  - Security implications
  - Performance considerations
  - Code readability
  - Test coverage
- Approve only when satisfied

## Merge Strategies

### Feature Branches → Develop
- **Strategy**: Squash and Merge
- **Reason**: Clean history, easier to revert

### Release/Hotfix → Main
- **Strategy**: Merge Commit
- **Reason**: Preserve release history

### Develop → Main (via Release)
- **Strategy**: Merge Commit
- **Reason**: Maintain version history

## Version Tagging

### Semantic Versioning
- Format: `v<MAJOR>.<MINOR>.<PATCH>`
- Example: `v1.2.3`

### When to Bump
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Tagging Process
```bash
# After merging to main
git checkout main
git pull origin main
git tag -a v1.2.0 -m "Release version 1.2.0: BMAD integration"
git push origin v1.2.0
```

## Emergency Procedures

### Rolling Back a Release
```bash
# Revert to previous version
git checkout main
git revert <commit-hash>
git push origin main

# Or use Git tag
git checkout <previous-tag>
git checkout -b hotfix/rollback
```

### Fixing a Bad Merge
```bash
# If merge went wrong
git reset --hard HEAD~1
git push --force-with-lease origin main
```

## Tools and Automation

### Git Hooks (Future)
- Pre-commit: Run linters
- Pre-push: Run tests
- Commit-msg: Validate commit message format

### CI/CD Pipeline (Future)
- Auto-run tests on PR
- Auto-deploy to staging from develop
- Auto-deploy to production from main

## Best Practices

1. **Commit Often**: Small, atomic commits
2. **Write Good Messages**: Clear and descriptive
3. **Pull Before Push**: Avoid conflicts
4. **Don't Commit Generated Files**: Use .gitignore
5. **Review Your Changes**: Before committing
6. **Keep Branches Short-Lived**: < 1 week
7. **Delete Merged Branches**: Keep repo clean
8. **Use Draft PRs**: For work in progress

## Troubleshooting

### Merge Conflicts
```bash
# Update your branch
git pull origin develop

# Resolve conflicts in files
# Edit conflicting files

# Mark as resolved
git add <resolved-files>
git commit -m "Resolve merge conflicts"
```

### Accidentally Committed to Wrong Branch
```bash
# Move commits to correct branch
git log  # Note the commit hash
git checkout correct-branch
git cherry-pick <commit-hash>

# Remove from wrong branch
git checkout wrong-branch
git reset --hard HEAD~1
```

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

---

**Last Updated**: October 28, 2025  
**Maintained By**: Product Management Team
