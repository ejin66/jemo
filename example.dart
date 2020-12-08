/*
  Don't edit.
  Code generated by jemo.py.
*/

import 'dart:convert';
import 'XXX456';
import 'XXX123';

class First extends SuperFirst {
    double aaa;
    bool b;
    SubC ccc;
    List<SubF> fff;
    List<String> j;

    First({
        this.aaa,
        this.b,
        this.ccc,
        this.fff,
        this.j,
    });

    factory First.fromRawJson(String str) => First.fromJson(json.decode(str));

    String toRawJson() => json.encode(toJson());

    factory First.fromJson(Map<String, dynamic> json) => First(
        aaa: json['a'],
        b: json['b'],
        ccc: SubC.fromJson(json['c']),
        fff: List<SubF>.from(json['f'].map((e) => e)),
        j: List<String>.from(json['j'].map((e) => e)),
    );

    Map<String, dynamic> toJson() => {
        "a": aaa,
        "b": b,
        "c": ccc.toJson(),
        "f": List<dynamic>.from(fff.map((e) => e)),
        "j": List<dynamic>.from(j.map((e) => e)),
    };
}

class SubC {
    int d;
    String e;

    SubC({
        this.d,
        this.e,
    });

    factory SubC.fromRawJson(String str) => SubC.fromJson(json.decode(str));

    String toRawJson() => json.encode(toJson());

    factory SubC.fromJson(Map<String, dynamic> json) => SubC(
        d: json['d'],
        e: json['e'],
    );

    Map<String, dynamic> toJson() => {
        "d": d,
        "e": e,
    };
}

class SubF {
    int g;
    int h;

    SubF({
        this.g,
        this.h,
    });

    factory SubF.fromRawJson(String str) => SubF.fromJson(json.decode(str));

    String toRawJson() => json.encode(toJson());

    factory SubF.fromJson(Map<String, dynamic> json) => SubF(
        g: json['g'],
        h: json['h'],
    );

    Map<String, dynamic> toJson() => {
        "g": g,
        "h": h,
    };
}

class Second extends SuperSecond {
    String username;
    String password;
    SubC ccc;

    Second({
        this.username,
        this.password,
        this.ccc,
    });

    factory Second.fromRawJson(String str) => Second.fromJson(json.decode(str));

    String toRawJson() => json.encode(toJson());

    factory Second.fromJson(Map<String, dynamic> json) => Second(
        username: json['user_name'],
        password: json['password'],
        ccc: SubC.fromJson(json['duplicateModel']),
    );

    Map<String, dynamic> toJson() => {
        "user_name": username,
        "password": password,
        "duplicateModel": ccc.toJson(),
    };
}
