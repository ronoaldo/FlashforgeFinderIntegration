# Helper script to test reading and writting gx file header.
import gx, sys

orig, changed = b'', b''
orig_name = sys.argv[1] if len(sys.argv)>1 else "testdata/cube.gx"

# Open input file for parsing 
with open(orig_name, 'rb') as fd:
    orig = fd.read()
    fd.close()
    g = gx.GX()
    g.decode(orig)

    d = vars(g)
    for k in d.keys():
        if k[0] == "_":
            continue
        if k == "bmp" or k == "gcode":
            print(k,":",len(d[k]))
        else:
            print(k,":",d[k])

# Write the 
with open('/tmp/test.gx', 'wb') as fd:
    changed = g.encode()
    fd.write(changed)
    fd.close()

# TODO(ronoaldo): investigate a one byte diff before BMP.
if orig != changed:
    print("Failed to render output. input and output differ!")
    print("orig =>   ", orig[:14513])
    print("changed =>", changed[:14513])
