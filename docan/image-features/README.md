# Image features

| Module | Topic |
|---|---|
| [image-gradients](image-gradients/) | the Sobel masks and the sign that hides |
| [sift-descriptors](sift-descriptors/) | cells, histograms and what the clip really bounds |
| [dense-grid](dense-grid/) | why the grid and not a detector |
| [lloyd-clustering](lloyd-clustering/) | the two conditions and the local optimum |
| [bag-of-features](bag-of-features/) | quantisation and the spatial pyramid |

The block builds the image side of the same representation the corpus block
builds for text: descriptors instead of words, a clustered vocabulary instead
of a frequency list, and a histogram at the end. The two halves of the course
meet here, and the spatial pyramid is the one part with no counterpart on the
text side.

Sobel is verified against an analytic answer: on a plane the response is
exactly eight times the slope at every interior pixel.
