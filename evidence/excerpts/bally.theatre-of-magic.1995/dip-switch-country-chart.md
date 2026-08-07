# Theatre of Magic — DIP switch country chart

Transcribed from `Theatre_of_Magic_OPS.pdf`, PDF page 2, printed front-matter page 2, the DIP switch
country chart and EPROM jumper note. The retained PDF carries a Paper Capture OCR text layer, but per
project policy every table was verified against a 300 dpi render of the page regardless of the text
layer's presence — the OCR text is a search index only.

## EPROM jumper (U6)

`W1` = In, `W2` = Out for 1 MEG / 2 MEG / 4 MEG EPROM.

## Country DIP chart

| Country | SW1 | SW2 | SW3 | SW4 | SW5 | SW6 | SW7 | SW8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| America | Off | Off | On | On | On | On | On | On |
| European | Off | Off | On | On | On | Off | On | On |
| French | Off | Off | On | On | On | On | Off | Off |
| German | Off | Off | On | On | On | On | On | Off |
| Spain | Off | Off | On | On | Off | On | On | On |

No specific country configuration is asserted by this definition; the chart is retained for
reference only, matching the Monster Bash precedent for the CPU option/country DIP bank.
