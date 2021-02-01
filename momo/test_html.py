from core import pretty_html


html = """
<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
<script></script>
<a href='a'>x</a></body></html>
"""

print(pretty_html(html, verbose=True))


# import string
# chars = string.digits + string.ascii_letters + '=+'
# print(chars, len(chars))


# def base(i: int, n: int = 64) -> str:
#     result = ''
#     p = 1
#     while i => 0:
#         x = i % 
#         p += 1
#         result.append(chars[x])
#     return reversed(result)

# print(base(96), '1w')
# print(base(128 + 32), '2w')

# """
# 64 + 32 => 1x
# 2 * 64 + 37 => 2
# """