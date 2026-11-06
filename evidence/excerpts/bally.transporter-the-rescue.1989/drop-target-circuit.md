# Drop target optical matrix interface

Manual PDF 61, 3-Bank Drop Target Board & Schematic. Method: primary curator visual reading against the native scan. The crop is the circuit region, not the whole manual page.

The board is C-12559. Its three optical emitter/receiver pairs feed LM339 comparator sections whose outputs connect to J1 row 1/pin 4, row 2/pin 5 and row 3/pin 7, with J1 pin 1 as the column. J2 supplies +12V and circuit ground. This drawing establishes optical construction for both banks' switches 19-24 despite the switch matrix's lack of an opto-shading legend. The ROM service tests and the pinned uninverted System 11 read path settle the matrix contact's active level separately; the optical beam's clear/blocked condition is not guessed from the symbol alone.
