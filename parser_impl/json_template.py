jsonTemplate = """
class {0} {5}{{
{1}

    {0}({{
{2}
    }});

    factory {0}.fromRawJson(String str) => {0}.fromJson(json.decode(str));

    String toRawJson() => json.encode(toJson());

    factory {0}.fromJson(Map<String, dynamic> json) => {0}(
{3}
    );

    Map<String, dynamic> toJson() => {{
{4}
    }};
}}
"""

