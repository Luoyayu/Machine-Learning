int calculate(dynamic a, dynamic b) {
  var c = a * b;
  print('${a.runtimeType} ${b.runtimeType} ${c.runtimeType}');
  return int.parse(c.toStringAsFixed(2));
}
