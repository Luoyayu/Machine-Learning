// A Tour of the Dart Language

import 'package:dart/dart.dart' as my_cal;
import 'dart:math';

printObj(dynamic Number, dynamic Str) {
  print("receive [Number = $Number, Str = $Str]");

  String calANY(dynamic Number, dynamic Str) {
    printAny(dynamic Number, dynamic Str) {
      print('ops is $Number, $Str');
    }

    printAny(Number, Str);
    print('cal answer is ${Number + double.parse(Str)}');
    return "I am using <Dart" + double.parse(Str).toStringAsFixed(0) + '>';
  }

  return calANY(Number, Str);
}

main(List<String> arguments) {
  dynamic Var = '2.2';
  print('2.2 ${Var.runtimeType}');
//  print(printObj(2, Var));
  Var = sqrt(3.0) + 1;
  print('sqrt(3)+1 ${Var.runtimeType}');

//  print(printObj(Var, "2.2"));
  print(Var * Var - 2);

  print('Hello world: '
      'Dart'
      '${my_cal.calculate(Var, Var - 2).toStringAsFixed(0)}!');

  int cnt;
  assert(cnt == null);

  final _1ConstString = "VVVV";
  final String _2ConstString = "AAAA";

  String _3String = "----";
  _3String = "====";

  const double atm = 1.01325 * 1000000;
  var foo = const []; // 可再次赋const值
  final bar = const [1, 2, 3];
  const baz = [2, 3, 4];

  foo = [1, 2, 3];
  assert('$foo' == foo.toString());

  print("atm = $atm,\t"
      "foo = $foo,\t"
      "foo = ${foo.toString()},\t"
      "baz length = ${baz.length}");

  assert("a" + "b" == "a" "b");

  // 解析字符串
  var one = int.parse('1'), onePointOne = double.parse('1.1');
  assert(one == 1);
  assert(onePointOne == 1.1);

  //解析实数
  var piAsString = 3.1415926.toStringAsFixed(2);
  assert(piAsString == '3.14');

  // bitwise op
  assert((3 << 1) == 6);
  assert((3 >> 1) == 1);
  assert((3 | 4) == 7);
  assert('${200}' == '${2e2.toInt()}');
}
