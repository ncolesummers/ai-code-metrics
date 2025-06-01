"""Tests for commit analyzer functionality."""

import unittest
from ai_code_metrics.analyzers.commit_analyzer import CommitPatternMatcher


class TestCommitPatternMatcher(unittest.TestCase):
    """Test suite for the CommitPatternMatcher class."""
    
    def test_claude_code_detection(self):
        """Test that Claude Code signatures are correctly detected."""
        # Test Claude Code signature
        message = """Add new feature
        
        This commit adds a new feature that does X.
        
        🤖 Generated with [Claude Code](https://claude.ai/code)
        
        Co-Authored-By: Claude <noreply@anthropic.com>"""
        
        assistant = CommitPatternMatcher.identify_ai_assistant(message)
        self.assertEqual(assistant, "claude_code")
        
        ai_data = CommitPatternMatcher.extract_ai_data(message)
        self.assertTrue(ai_data["ai_assisted"])
        self.assertEqual(ai_data["ai_assistant"], "claude_code")
    
    def test_github_copilot_detection(self):
        """Test that GitHub Copilot signatures are correctly detected."""
        message = """Fix bug in authentication
        
        Co-authored-by: Copilot <copilot@github.com>"""
        
        assistant = CommitPatternMatcher.identify_ai_assistant(message)
        self.assertEqual(assistant, "github_copilot")
        
        ai_data = CommitPatternMatcher.extract_ai_data(message)
        self.assertTrue(ai_data["ai_assisted"])
        self.assertEqual(ai_data["ai_assistant"], "github_copilot")
    
    def test_generic_ai_detection(self):
        """Test that generic AI signatures are correctly detected."""
        message = """Update documentation
        
        This is AI-generated documentation for the API"""
        
        assistant = CommitPatternMatcher.identify_ai_assistant(message)
        self.assertEqual(assistant, "general_ai")
        
        ai_data = CommitPatternMatcher.extract_ai_data(message)
        self.assertTrue(ai_data["ai_assisted"])
        self.assertEqual(ai_data["ai_assistant"], "general_ai")
    
    def test_non_ai_commit(self):
        """Test that non-AI commits are correctly identified."""
        message = """Fix typo in README
        
        Just a small fix."""
        
        assistant = CommitPatternMatcher.identify_ai_assistant(message)
        self.assertIsNone(assistant)
        
        ai_data = CommitPatternMatcher.extract_ai_data(message)
        self.assertFalse(ai_data["ai_assisted"])
        self.assertIsNone(ai_data["ai_assistant"])


if __name__ == '__main__':
    unittest.main()