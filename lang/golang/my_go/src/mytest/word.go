package mytest

import (
	"strings"
)

func IsPalindrome(s string) bool {
	var unicodeS = []rune(strings.TrimSpace(s))

	for i := range unicodeS {
		if unicodeS[i] != unicodeS[len(unicodeS)-1-i] {
			return false
		}
	}
	return true
}
