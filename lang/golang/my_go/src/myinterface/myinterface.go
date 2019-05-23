package myinterface

import (
	"fmt"
)

// one interface focus in ONE thing

// interface definition
type Printer interface {
	Print()
}

type Changer interface {
	Change(interface{}) bool
}

type Adder interface {
	Add(interface{}) error
}

// sometime one interface does MORE than ONE thing
type ALL interface {
	Print()
	Change(interface{}) bool
	Add(interface{}) error
	//JokeFunc()
}

// ********************************************************* //

// Type 1
type Type1 struct{ data int }

// Type 1 interface Print() function implement
func (t1 Type1) Print() { fmt.Println("me1:", t1) }

// Type 1 interface Change() function implement
func (t1 *Type1) Change(newData interface{}) (ok bool) {
	data, ok := newData.(int) // interface assert
	if ok == true {
		t1.data = data
	}
	return
}

// Type 1 interface Add() function implement
func (t1 *Type1) Add(oper1 interface{}) (err error) {
	your1, ok := oper1.(*Type1)
	if ok == true {
		t1.data += your1.data
	} else {
		err = fmt.Errorf("cannot add between them data\n", )
	}
	return
}

// ********************************************************* //

// Type 2
type Type2 struct{ data string }

//Type 2 interface Print() function implement
func (t2 Type2) Print() { fmt.Println("your1:", t2) }

func (t2 *Type2) Change(newData interface{}) (ok bool) {
	data, ok := newData.(string)
	if ok == true {
		t2.data = data
	}
	return
}

//Type 2 interface Add() function implement
func (t2 *Type2) Add(oper1 interface{}) (err error) {
	your1, ok := oper1.(*Type2)
	if ok == true {
		t2.data += your1.data
	} else {
		err = fmt.Errorf("cannot add between them data\n", )
	}
	return
}

// ********************************************************* //

// 多态函数 1
func PrintStruct(er Printer) { er.Print() }
func PrintAllStruct(ers ...Printer) {
	for _, v := range ers {
		v.Print()
	}
}
func ChangeData(er Changer, newData interface{}) (ok bool) {
	ok = er.Change(newData)
	return
}
func AddToFirst(x1 Adder, x2 Adder) (err error) {
	//fmt.Println(x1, x2)
	err = x1.Add(x2)
	return
}

// 多态函数 2
func PrintStruct_(er ALL) { er.Print() }
func ChangeData_(er ALL, newData interface{}) (ok bool) {
	ok = er.Change(newData)
	return
}
func AddToFirst_(er1 ALL, er2 ALL) (err error) {
	fmt.Println(er1, er2)
	err = er1.Add(er2)
	return
}

// ********************************************************* //

func MyinterfaceMain() {
	var err error
	me1 := Type1{123}
	me2 := Type1{234}
	your1 := Type2{"Hello World!"}
	your2 := Type2{"啊!"}

	fmt.Println("初始对象值:")
	PrintStruct(me1)
	PrintStruct(your1)

	PrintAllStruct(me2, your2)
	fmt.Println()

	// ** CHANGE DATA BETWEEN TYPE1 **
	ok := ChangeData(&me1, 321)
	fmt.Printf("Change data in \"me1\": %t\n", ok)
	fmt.Println("me1 new data: ", me1)

	// ** CHANGE DATA BETWEEN TYPE2 **
	ok = ChangeData(&your1, "你好")
	fmt.Printf("Change data in \"your1\": %t\n", ok)
	fmt.Println("your1 new data: ", your1)

	// ** CHANGE DATA BETWEEN TYPE2 WITH TYPE1**
	ok = ChangeData(&your1, 123)
	fmt.Printf("Change data in \"your1\": %t\n", ok)
	fmt.Println("your1 new data: ", your1)

	// ** ADD BETWEEN TYPE1 **
	err = AddToFirst(&me1, &me2)
	//err = (&me1).Add(&me2) // your1 may want to try this

	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Printf("%d\n", me1.data)
	}

	// ** ADD BETWEEN TYPE2 **
	err = AddToFirst_(&your1, &your2) // NOTICE we UES AddToFirst_ belongs to interface ALL
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(your1.data)
	}
}
