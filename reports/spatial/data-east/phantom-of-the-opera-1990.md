# Phantom of the Opera spatial blockers

The record remains **partial**. Coordinates use the exact retained table bounds 952×2162; x runs left to right and y rear to apron.

**input_semantics**: J8 is a real CPU PA7 ground-jumper position, documented installed for this game; its physical circuit and factory low level are known. The firmware interpretation of PA7/configuration bit 0 is unresolved, so an inherited Country/W7 identity is not asserted. Resolution: Game-specific CPU/firmware documentation or ROM dataflow from PIA2 port A at $2800, bit 7, establishing the consuming branch and meaning for the supported production firmware. A board photo can corroborate a surviving board installation, but does not establish firmware purpose.

**output_semantics**: SP6 is physically unfitted. Known direct CRA $2401 writes from shadow $0102 initialized to $38 request inactive CA2; the adjacent indexed PIA-test sequence is gated off. Bounded static analysis did not resolve indirect event dispatch or every indexed-store range. Retained runtime traces did not publish 20, which is not unused proof. Resolution: Resolve event-dispatch targets at ROM $45ED (JSR 0,X) and indexed-store base/value ranges that could modify shadow $0102 or PIA1 CRA $2401; establish whether a reachable enabled path can request low CA2. The known direct stores at $4C96/$4CA3 are already accounted for in the pinned ROM-analysis excerpt.

**spatial_placement**: Three trough sensors, separate left-stack sensor 29, organ motor/limits, rear PHANTOM sockets, all individual flasher sockets and complete GI socket survey lack registered physical coordinates. Insert-overlay candidates and 12 observed VPX bulb meshes do not establish a complete factory-socket inventory. Resolution: Registered own-game drawings/photographs or measured socket survey, including underside/apron and rear-panel bulbs; reconcile each candidate and quantity to the physical circuit.

All raw object candidates, rejected helpers, projection classes and extraction hashes are in the adjacent JSON report and pinned places seed. No Flasher sprite, insert overlay or GI render double is silently promoted to a physical socket.
