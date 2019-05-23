package mytest

import "testing"

func TestIsPalindrome(t *testing.T) {
	var tests = []struct {
		// 表格驱动测试任务
		input string
		want  bool
	}{
		{"", true},
		{"abcd", false},
	}

	for _, test := range tests {
		if got := IsPalindrome(test.input); got != test.want {
			t.Errorf(`IsPalindrome("%s")=%t`, test.input, test.want)
		}
	}
}
