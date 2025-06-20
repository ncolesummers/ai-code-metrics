"""Analyze git commits for AI assistant contribution patterns."""

import re
from typing import Any

import git


class CommitPatternMatcher:
    """Match commit patterns for different AI assistants."""
    
    # Signature patterns for different AI tools
    PATTERNS = {
        "claude_code": [
            r'🤖 Generated with \[Claude Code\]',
            r'Co-Authored-By: Claude <noreply@anthropic.com>'
        ],
        "github_copilot": [
            r'Co-authored-by: Copilot <copilot@github.com>'
        ],
        "cursor": [
            r'Generated by Cursor',
            r'Co-authored-by: Cursor <cursor@cursor.com>'
        ],
        "general_ai": [
            r'AI-generated',
            r'AI-assisted',
            r'Generated by AI',
            r'AI-authored'
        ]
    }
    
    @classmethod
    def identify_ai_assistant(cls, commit_message: str) -> str | None:
        """Identify which AI assistant was used based on commit message."""
        for assistant, patterns in cls.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, commit_message, re.IGNORECASE):
                    return assistant
        return None
    
    @classmethod
    def extract_ai_data(cls, commit_message: str) -> dict[str, Any]:
        """Extract AI-related data from commit message."""
        assistant = cls.identify_ai_assistant(commit_message)
        
        result = {
            "ai_assisted": assistant is not None,
            "ai_assistant": assistant,
            "has_explanation": bool(re.search(r'explanation|reasoning|thinking', commit_message, re.IGNORECASE)),
        }
        
        # Extract additional data for specific assistants
        if assistant == "claude_code":
            # Try to extract model version if present
            model_match = re.search(r'using Claude (\S+)', commit_message, re.IGNORECASE)
            if model_match:
                result["model"] = model_match.group(1)
        
        return result


class CommitAnalyzer:
    """Analyze git repository for AI assistant patterns."""
    
    def __init__(self, repo_path: str):
        """Initialize with repository path."""
        self.repo = git.Repo(repo_path)
    
    def analyze_commits(self, 
                        limit: int | None = None, 
                        since: str | None = None,
                        until: str | None = None) -> list[dict[str, Any]]:
        """Analyze repository commits for AI patterns."""
        commits_data = []
        
        # Build the commit iteration parameters
        kwargs = {}
        if since:
            kwargs['since'] = since
        if until:
            kwargs['until'] = until
        if limit:
            commits = list(self.repo.iter_commits(**kwargs))[:limit]
        else:
            commits = list(self.repo.iter_commits(**kwargs))
        
        for commit in commits:
            commit_data = self._analyze_commit(commit)
            commits_data.append(commit_data)
            
        return commits_data
    
    def _analyze_commit(self, commit) -> dict[str, Any]:
        """Analyze a single commit for AI patterns."""
        # Extract basic commit data
        commit_data = {
            'commit_hash': commit.hexsha,
            'author': commit.author.name,
            'author_email': commit.author.email,
            'timestamp': commit.committed_datetime.isoformat(),
            'message': commit.message,
        }
        
        # Extract stats
        if hasattr(commit, 'stats') and hasattr(commit.stats, 'total'):
            stats = commit.stats.total
            commit_data.update({
                'files_changed': stats.get('files', 0),
                'lines_added': stats.get('insertions', 0),
                'lines_deleted': stats.get('deletions', 0),
            })
        
        # Analyze AI patterns in commit message
        ai_data = CommitPatternMatcher.extract_ai_data(commit.message)
        commit_data.update(ai_data)
        
        return commit_data
    
    def get_ai_usage_stats(self) -> dict[str, Any]:
        """Get statistics on AI usage in the repository."""
        commits = list(self.repo.iter_commits())
        total_commits = len(commits)
        
        ai_commits = 0
        assistant_counts = {}
        
        for commit in commits:
            assistant = CommitPatternMatcher.identify_ai_assistant(commit.message)
            if assistant:
                ai_commits += 1
                assistant_counts[assistant] = assistant_counts.get(assistant, 0) + 1
        
        return {
            'total_commits': total_commits,
            'ai_assisted_commits': ai_commits,
            'ai_percentage': round((ai_commits / total_commits * 100) if total_commits else 0, 2),
            'assistant_breakdown': assistant_counts,
        }