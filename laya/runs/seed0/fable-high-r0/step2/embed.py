"""Run frozen Laya on your own messages: python embed.py out.npz "message 1" "message 2" ...
Writes M [n, 5, 1024]: the scorer input for each department option. Takes ~10 s to load."""
import sys
sys.path.insert(0, '<lab>/laya')
import numpy as np, laya_lab as L
a = L.load_agent()
np.savez(sys.argv[1], M=L.marker_vectors(a, sys.argv[2:]))
print("wrote", sys.argv[1], len(sys.argv) - 2, "messages")
