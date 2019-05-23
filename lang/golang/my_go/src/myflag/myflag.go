package myflag

import (
	"flag"
	"fmt"
)

var v = flag.Float64("v", 0, "version")
var sep = flag.String("s", "", "separator")

// MyflagMain ...
func MyflagMain() {
	flag.Parse()
	fmt.Println(*v, *sep)
	fmt.Println(flag.Args())
}
