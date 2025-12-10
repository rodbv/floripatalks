"""
Unit tests for core.utils module.
"""

import pytest

from core.utils import format_comment_count, format_number_pt_br, format_vote_count


class TestFormatNumberPtBr:
    """Tests for format_number_pt_br function."""

    def test_format_single_digit(self):
        assert format_number_pt_br(5) == "5"

    def test_format_two_digits(self):
        assert format_number_pt_br(42) == "42"

    def test_format_three_digits(self):
        assert format_number_pt_br(567) == "567"

    def test_format_four_digits(self):
        assert format_number_pt_br(1234) == "1.234"

    def test_format_five_digits(self):
        assert format_number_pt_br(12345) == "12.345"

    def test_format_six_digits(self):
        assert format_number_pt_br(123456) == "123.456"

    def test_format_seven_digits(self):
        assert format_number_pt_br(1234567) == "1.234.567"

    def test_format_zero(self):
        assert format_number_pt_br(0) == "0"

    def test_format_large_number(self):
        assert format_number_pt_br(1234567890) == "1.234.567.890"


class TestFormatVoteCount:
    """Tests for format_vote_count function."""

    def test_format_zero_votes(self):
        assert format_vote_count(0) == "0 votos"

    def test_format_one_vote(self):
        assert format_vote_count(1) == "1 voto"

    def test_format_two_votes(self):
        assert format_vote_count(2) == "2 votos"

    def test_format_many_votes(self):
        assert format_vote_count(1234) == "1.234 votos"

    def test_format_large_vote_count(self):
        assert format_vote_count(1234567) == "1.234.567 votos"


class TestFormatCommentCount:
    """Tests for format_comment_count function."""

    def test_format_zero_comments(self):
        assert format_comment_count(0) == "0 comentários"

    def test_format_one_comment(self):
        assert format_comment_count(1) == "1 comentário"

    def test_format_two_comments(self):
        assert format_comment_count(2) == "2 comentários"

    def test_format_many_comments(self):
        assert format_comment_count(567) == "567 comentários"

    def test_format_large_comment_count(self):
        assert format_comment_count(1234567) == "1.234.567 comentários"

