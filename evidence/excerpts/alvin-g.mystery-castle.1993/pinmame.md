# Pinned PinMAME Alvin G transport and title evidence

Revision 97aa922bf8e4b6970126192ec1ac1fb0305a4f62; exact line ranges below. These are emulator facts, not physical fitment evidence.

## alvggames.c:8-44

```c
#define DMD       alvg_dispDMD
#define DMD2      alvg_dispDMD2
#define DMD3      alvg_dispDMD3

#define FLIP78    FLIP_SWNO(7,8)

/* Dot-Matrix display (128 x 32) */
static core_tLCDLayout alvg_dispDMD[] = {
  {0,0,32,128,CORE_DMD,NULL,NULL}, {0}
};

/* Alpha Numeric Display (2 X 20 Alpha-Numeric) */
static core_tLCDLayout alvg_alpha[] = {
  {0,0, 0,20,CORE_SEG16},
  {3,0,20,20,CORE_SEG16},
  {0}
};

/* Alpha Numeric Display (1 X 20 Alpha-Numeric) */
static core_tLCDLayout alvg_alpha1[] = {
  {0,0, 0,20,CORE_SEG16},
  {0}
};

#define INITGAME(name, disptype, flippers, balls, sb, db, lamps) \
	ALVG_INPUT_PORTS_START(name, balls) ALVG_INPUT_PORTS_END \
	static core_tGameData name##GameData = {GEN_ALVG,disptype,{flippers,4,4,0,sb,db,lamps}}; \
	static void init_##name(void) { \
		core_gameData = &name##GameData; \
	}

#define INITGAME2(name, disptype, flippers, balls, sb, db, lamps) \
	ALVG_INPUT_PORTS_START(name, balls) ALVG_INPUT_PORTS_END \
	static core_tGameData name##GameData = {GEN_ALVG_DMD2,disptype,{flippers,4,4,0,sb,db,lamps}}; \
	static void init_##name(void) { \
		core_gameData = &name##GameData; \
	}
```

## alvggames.c:185-211

```c
/ Mystery Castle (AG08)
/-------------------------------------------------------------------*/
INITGAME2(mystcast, DMD, FLIP78, 3/*?*/, SNDBRD_ALVGS2, SNDBRD_ALVGDMD, 2)
ALVGROMSTART(mystcast,	"mcastle.cpu", CRC(936e6799) SHA1(aa29fb5f12f34c695d1556232744f65cd576a2b1))
ALVGS_SOUNDROM(			"mcastle.102", CRC(752822d0) SHA1(36461ef03cac5aefa0c03dfdc63c3d294a3b9c09),
						"mcastle.sr0", CRC(0855cc73) SHA1(c46e08432bcff24594c33171f20669ba63828931),
						"mcastle.sr1", CRC(3b5d76e0) SHA1(b2e1bca3c596eba89feda868fa56c71a6b22414c),
						"mcastle.sr2", CRC(c3ffd277) SHA1(d16d1b22089b89bbf0db7d2b66c9745a56034322),
						"mcastle.sr3", CRC(740858bb) SHA1(d2e9a0a178977dcc873368b042cea7052578df66))
ALVGDMD_ROM2R(			"mcastle.du4", CRC(686e253a) SHA1(28aff34c120c61e231e2111dc396df515bcbbb89),
						"mcastle.du5", CRC(9095c367) SHA1(9d3e9416f662ee2aad891eef059278c530448fcc))
ALVG_ROMEND
CORE_GAMEDEFNV(mystcast,"Mystery Castle (R02)",1993,"Alvin G",mALVGS2DMD2,0)

// R03 has game ID EPC081
INITGAME2(mystcasa, DMD, FLIP78, 3/*?*/, SNDBRD_ALVGS2, SNDBRD_ALVGDMD, 2)
ALVGROMSTART(mystcasa,	"cpu_103.bin", CRC(70ab8ece) SHA1(2bf8cd042450968b7500552419a9af5df2589c13))
ALVGS_SOUNDROM(			"mcastle.103", CRC(bd4849ac) SHA1(f477ea369539a65c0960be1f1c3b4c5503dd6b75),
						"mcastle.sr0", CRC(0855cc73) SHA1(c46e08432bcff24594c33171f20669ba63828931),
						"mcastle.sr1", CRC(3b5d76e0) SHA1(b2e1bca3c596eba89feda868fa56c71a6b22414c),
						"mcastle.sr2", CRC(c3ffd277) SHA1(d16d1b22089b89bbf0db7d2b66c9745a56034322),
						"mcastle.sr3", CRC(740858bb) SHA1(d2e9a0a178977dcc873368b042cea7052578df66))
ALVGDMD_ROM(			"u4.bin", CRC(a6969efc) SHA1(82da976cb3d30d6fb1576e4c67febd7235f73f51),
						"u5.bin", CRC(e5126980) SHA1(2c6d412c87bf27098dae4351958d84e8f9348423),
						"u6.bin", CRC(eb241633) SHA1(8e5db75b32ed2ea74088615bbe1403d4c8feafbd))
ALVG_ROMEND
CORE_CLONEDEFNV(mystcasa,mystcast,"Mystery Castle (R03)",199?,"Alvin G",mALVGS2DMD2,0)
```

## alvg.c:147-202

```c
/*Solenoids - Need to verify correct solenoid # here!*/
static WRITE_HANDLER(solenoid_w)
{
	switch(offset) {
		case 0:
			coreGlobals.pulsedSolState = (coreGlobals.pulsedSolState & 0xFFFFFF00) | data;
			break;
		case 1:
			alvglocals.swAvail2 = (data & 0x40) ? 1 : 0;
			coreGlobals.pulsedSolState = (coreGlobals.pulsedSolState & 0xFFFF00FF) | (data<<8);
			break;
		case 2:
			alvglocals.swAvail1 = data ? 1 : 0;
			coreGlobals.pulsedSolState = (coreGlobals.pulsedSolState & 0xFF00FFFF) | (data<<16);
			break;
		case 3:
			coreGlobals.pulsedSolState = (coreGlobals.pulsedSolState & 0x00FFFFFF) | (data<<24);
			break;
		default:
			LOG(("Solenoid_W Logic Error\n"));
	}
	alvglocals.solenoids |= coreGlobals.pulsedSolState;
	core_write_pwm_output_8b(CORE_MODOUT_SOL0 + offset * 8, data);
}

//See U7-PB Read for more info
READ_HANDLER(CoinDoorSwitches_Read)
{
//According to manual (but doesn't work)
#if 0
	int data = 0;
	data |= (alvglocals.DMDAck   << 7);	 //DMD Ack		(?)
	data |= (alvglocals.swTest   << 5);	 //Test Sw.		(Not Inverted)
	data |= (alvglocals.swEnter  << 4);  //Enter Sw.	(Not Inverted)
	data |= (alvglocals.swAvail1 << 3);  //Avail1		(Not Inverted)
	data |= (alvglocals.swAvail2 << 2);  //Avail2		(Not Inverted)
#else
//Seems to work, note that the ticket switch may only be set when the ticket solenoid is pulled in,
//as this input is also connected to a flasher lamp test!
	int data = 0;
	data |= (alvglocals.DMDAck   << 7);	 //DMD Ack		(?)				(8)
	data |= ((alvglocals.swTicket | alvglocals.swAvail1) << 5);	 //Ticket Sw.	(Not Inverted)	(6)
	data |= (alvglocals.swEnter  << 4);  //Enter Sw.	(Not Inverted)	(5)
	data |= (alvglocals.swAvail2 << 3);  //Avail2		(Not Inverted)	(4)
	data |= (alvglocals.swTest   << 2);	 //Test Sw.		(Not Inverted)	(3)
	data |= (alvglocals.swAvail1 << 1);  //Avail1		(Not Inverted)	(2)
#endif
//printf("%x:data = %x\n",activecpu_get_previouspc(),data);
return data;
}

/* U7 - 6522 */

//PA0-7 (IN) - Switch Return (Switches are inverted!)
static READ_HANDLER( xvia_0_a_r ) { return coreGlobals.swMatrix[alvglocals.swCol]^0xff; }

```

## alvg.c:338-367

```c
*/
WRITE_HANDLER(u13_porta_w) { solenoid_w(3,data); }

void UpdateSwCol(void) {
	int i, tmp, data;
	i = data = 0;
	tmp = alvglocals.swColumn;
	while(tmp)
	{
		i++;
		if(tmp&1) data+=i;
		tmp = tmp>>1;
	}
	alvglocals.swCol = data;
	//printf("COL = %x SwColumn = %d\n",alvglocals.swColumn,data);
	//printf("SwColumn = %d\n",data);
}

WRITE_HANDLER(u13_portb_w) {
	alvglocals.swColumn = (alvglocals.swColumn&0xff00) | (data^0xff);
	UpdateSwCol();
	//printf("SWITCH_STROBE(1-8): data = %x\n",data);
}
WRITE_HANDLER(u13_portc_w) {
	alvglocals.swColumn = (alvglocals.swColumn&0x00ff) | ((data^0xff)<<8);
	UpdateSwCol();
	//printf("SWITCH_STROBE(9-12): data = %x\n",data);
}


```

## alvg.c:374-439

```c

void UpdateLampCol(void) {
	int i, tmp, lmpCol;
	i = lmpCol = 0;
	tmp = alvglocals.lampColumn;
	while(tmp)
	{
		i++;
		if(tmp&1) lmpCol+=i;
		tmp = tmp>>1;
	}
	if (lmpCol != 0)
		coreGlobals.tmpLampMatrix[lmpCol-1] = (coreGlobals.tmpLampMatrix[lmpCol-1]&0xff) | alvglocals.lampRow;
	//printf("COL = %x LampColumn = %d\n",alvglocals.lampColumn,data);
	//printf("LampColumn = %d\n",data);
}

void UpdatePWMLamp(void) {
	for (int lampStrobe = 0, pos = CORE_MODOUT_LAMP0, col = 1; lampStrobe < 12; lampStrobe++, pos += 8, col <<= 1)
		core_write_pwm_output_8b(pos, (alvglocals.lampColumn & col) ? alvglocals.lampRow : 0);
}

/* - Lamp Handling -
   -----------------
   It seems Pistol Poker handles lamps differently from the other games.
   First, the lamp columns are not standard ordering, like the others.
   Second, it writes the lamp column data first, then the lamp data itself.
   The other games write the lamp data first, then the lamp column data. - */
WRITE_HANDLER(u14_porta_w) {
	if (core_gameData->hw.gameSpecific1 == 1)
		alvglocals.lampColumn = (alvglocals.lampColumn&0x0f01) | ((data & 0x7f)<<1);
	else {
		alvglocals.lampColumn = (alvglocals.lampColumn&0x0f80) | (data & 0x7f);
		UpdateLampCol();
	}
	//printf("LAMP STROBE(1-7):  data = %x\n",data&0x7f);
	UpdatePWMLamp();
}
WRITE_HANDLER(u14_portb_w) {
	if (core_gameData->hw.gameSpecific1 == 1)
		alvglocals.lampColumn = (alvglocals.lampColumn&0x00fe) | ((data & 0x0f)<<8) | ((data & 0x10)>>4);
	else {
		alvglocals.lampColumn = (alvglocals.lampColumn&0x007f) | ((data & 0x1f)<<7);
		UpdateLampCol();
	}
	//printf("LAMP STROBE(8-12): data = %x\n",data);
	UpdatePWMLamp();
}
WRITE_HANDLER(u14_portc_w) {
	alvglocals.lampRow = data;
	if (core_gameData->hw.gameSpecific1 == 1)
		UpdateLampCol();
	//printf("LAMP RETURN: data = %x\n",data);
	UpdatePWMLamp();
}

/*
U7 - 6522

PA0-7(In)  = Switch Column 1-8 Return
PB7  (In)  = DMD ACK
PB6  (Out) = NAND Gate -> WD (WatchDog)
PB5  (In)  = Test Switch - Cabinet Switch
PB4  (In)  = Enter Switch - Cabinet Switch
PB3  (In)  = AVAI1 - Cabinet Switch
PB2  (In)  = AVAI2 - Cabinet Switch
```

## alvg.c:557-587

```c

  core_updateSw(core_getSol(27));	//Flipper Enable Relay
}

static SWITCH_UPDATE(alvg) {
  via_irq(1);			//Why is this necessary? - Seems to help switch scanning..
  xvia_0_cb2_w(0,1);	//Force an NMI call - fixes lamps in Pistol Poker & sending data to DMD

  if (inports) {
    coreGlobals.swMatrix[0] = (inports[ALVG_COMINPORT] & 0x0700)>>8;								 	    //Column 0 Switches
    coreGlobals.swMatrix[1] = (coreGlobals.swMatrix[1] & 0xe0) | (inports[ALVG_COMINPORT] & 0x1f);		    //Column 1 Switches
    coreGlobals.swMatrix[2] = (coreGlobals.swMatrix[2] & 0x3c) | ((inports[ALVG_COMINPORT] & 0x1860)>>5);	//Column 2 Switches
  }
  alvglocals.swTest = (core_getSw(ALVG_SWTEST)>0?1:0);
  alvglocals.swEnter = (core_getSw(ALVG_SWENTER)>0?1:0);
  alvglocals.swTicket = (core_getSw(ALVG_SWTICKET)?1:0);
}

//Send a sound command to the sound board
WRITE_HANDLER(alvg_sndCmd_w) {
	sndbrd_0_data_w(0, data);
	sndbrd_0_ctrl_w(0, 0);
}

static int alvg_sw2m(int no) {
	return no + 7;
}

static int alvg_m2sw(int col, int row) {
	return col*8 + row - 7;
}
```

## alvg.c:617-631

```c
  //watchdog_reset_w(0,0);

  // Initialize PWM outputs
  coreGlobals.nLamps = 64 + core_gameData->hw.lampCol * 8;
  core_set_pwm_output_type(CORE_MODOUT_LAMP0, 96, CORE_MODOUT_BULB_44_20V_DC_GTS3); // Actually #555 with a 3 Ohms resistor switched by 2 IRF530 but close enough
  coreGlobals.nSolenoids = CORE_FIRSTCUSTSOL - 1 + core_gameData->hw.custSol;
  core_set_pwm_output_type(CORE_MODOUT_SOL0, coreGlobals.nSolenoids, CORE_MODOUT_SOL_2_STATE);
  // Flashers are switched without resistor, by an IRF530 but close enough to GTS3 wiring
  // All tables have the same wiring with 8 flashers on solenoid outputs 17..24
  core_set_pwm_output_type(CORE_MODOUT_SOL0 + 17 - 1, 8, CORE_MODOUT_BULB_906_20V_DC_GTS3);

  /* Init the sound board */
  sndbrd_0_init(core_gameData->hw.soundBoard, ALVGS_CPUNO,   memory_region(ALVGS_ROMREGION)  ,NULL,NULL);
}
static MACHINE_INIT(alvg) {
```

## core.c:1777-1838

```c
/----------------------*/
void core_updateSw(int flipEn) {
  /*-- handle flippers--*/
  const int flip = core_gameData->hw.flippers;
  const int flipSwCol = (core_gameData->gen & (GEN_GTS3 | GEN_SPA | GEN_ALVG | GEN_ALVG_DMD2 | GEN_WICO)) ? 15 : CORE_FLIPPERSWCOL;
  int inports[CORE_MAXPORTS];
  UINT8 swFlip;
  int ii;

  if (g_fHandleKeyboard) {
    const int n = CORE_COREINPORT+(coreData->coreDips+31)/16;
    for (ii = 0; ii < n; ii++)
      inports[ii] = readinputport(ii);

    /*-- buttons --*/
    swFlip = 0;
    if (inports[CORE_FLIPINPORT] & CORE_LLFLIPKEY) swFlip |= CORE_SWLLFLIPBUTBIT;
    if (inports[CORE_FLIPINPORT] & CORE_LRFLIPKEY) swFlip |= CORE_SWLRFLIPBUTBIT;
    if (locals.flipMask & CORE_SWULFLIPBUTBIT) {    /* have UL switch */
      if (flip & FLIP_BUT(FLIP_UL))
        { if (inports[CORE_FLIPINPORT] & CORE_ULFLIPKEY) swFlip |= CORE_SWULFLIPBUTBIT; }
      else
        { if (inports[CORE_FLIPINPORT] & CORE_LLFLIPKEY) swFlip |= CORE_SWULFLIPBUTBIT; }
    }
    if (locals.flipMask & CORE_SWURFLIPBUTBIT) {    /* have UR switch */
      if (flip & FLIP_BUT(FLIP_UR))
        { if (inports[CORE_FLIPINPORT] & CORE_URFLIPKEY) swFlip |= CORE_SWURFLIPBUTBIT; }
      else
        { if (inports[CORE_FLIPINPORT] & CORE_LRFLIPKEY) swFlip |= CORE_SWURFLIPBUTBIT; }
    }
  }
  else
    swFlip = (coreGlobals.swMatrix[flipSwCol] ^ coreGlobals.invSw[flipSwCol]) & (CORE_SWULFLIPBUTBIT|CORE_SWURFLIPBUTBIT|CORE_SWLLFLIPBUTBIT|CORE_SWLRFLIPBUTBIT);

#ifdef PROC_SUPPORT
  /*-- Only handle flipper switches if we're not in a real game, otherwise they --*/
  /*-- will get physically activated anyway */
  if (!coreGlobals.p_rocEn) {
#endif

    /*-- set switches in matrix for non-fliptronic games --*/
    if (FLIP_SWL(flip)) core_setSw(FLIP_SWL(flip), swFlip & CORE_SWLLFLIPBUTBIT);
    if (FLIP_SWR(flip)) core_setSw(FLIP_SWR(flip), swFlip & CORE_SWLRFLIPBUTBIT);
#ifdef PROC_SUPPORT
  }
#endif

  /*-- fake solenoids if not CPU controlled --*/
  if ((flip & FLIP_SOL(FLIP_L)) == 0) {
    coreGlobals.solenoids2 &= 0xffffff00;
    if (flipEn) {
      if (swFlip & CORE_SWLLFLIPBUTBIT) coreGlobals.solenoids2 |= CORE_LLFLIPSOLBITS;
      if (swFlip & CORE_SWLRFLIPBUTBIT) coreGlobals.solenoids2 |= CORE_LRFLIPSOLBITS;
    }
  }

  /*-- EOS switches --*/
  if (locals.flipMask & CORE_SWULFLIPEOSBIT) {
    if (core_getSol(sULFlip)) locals.flipTimer[0] += 1;
    else                      locals.flipTimer[0] = 0;
    if (locals.flipTimer[0] >= CORE_FLIPSTROKETIME) swFlip |= CORE_SWULFLIPEOSBIT;
  }
```

## alvg.h:19-39

```c
    COREPORT_BITDEF(  0x0004, IPT_COIN3,          KEYCODE_5) \
    COREPORT_BITDEF(  0x0008, IPT_COIN4,          KEYCODE_6) \
    COREPORT_BIT(     0x0010, "Slam Tilt",        KEYCODE_HOME) \
    /* Switch Column 2 */ \
    COREPORT_BITDEF(  0x0020, IPT_START1,         IP_KEY_DEFAULT) \
    COREPORT_BIT(     0x0040, "Ball Tilt",        KEYCODE_INSERT) \
    COREPORT_BIT(     0x0800, "Volume +",         KEYCODE_9) \
    COREPORT_BIT(     0x1000, "Volume -",         KEYCODE_0) \
    /* These are put in switch column 0 since they are not read in the regular switch matrix */ \
    COREPORT_BIT(     0x0100, "Test",             KEYCODE_7) \
    COREPORT_BIT(     0x0200, "Enter",            KEYCODE_8) \
    COREPORT_BITTOG(  0x0400, "Ticket",           KEYCODE_END)

/*-- Standard input ports --*/
#define ALVG_INPUT_PORTS_START(name,balls) \
  INPUT_PORTS_START(name) \
    CORE_PORTS \
    SIM_PORTS(balls) \
    ALVG_COMPORTS

#define ALVG_INPUT_PORTS_END INPUT_PORTS_END
```

## alvg.h:57-62

```c
/*-- Main CPU regions and ROM --*/

/*-- 64K CPU ROM --*/
#define ALVGROMSTART(name, n1, chk1) \
   ROM_START(name) \
   NORMALREGION(0x10000, ALVG_MEMREG_CPU) \
```
