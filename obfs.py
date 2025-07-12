# obfuscator.py
import marshal, zlib, base64

with open("s10.py", "r", encoding="utf-8") as f:
    source = f.read()

compiled = compile(source, "<string>", "exec")
marshalled = marshal.dumps(compiled)
compressed = zlib.compress(marshalled)
encoded = base64.b64encode(compressed)

with open("obfuscated.py", "w", encoding="utf-8") as f:
    f.write("import marshal, zlib, base64\n")
    f.write("exec(marshal.loads(zlib.decompress(base64.b64decode(" + repr(encoded) + "))))")
