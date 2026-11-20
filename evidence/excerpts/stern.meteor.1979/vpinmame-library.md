Source: the VPinMAME script libraries the retained table and both corpus scripts load (`LoadVPM "01000100", "Stern.VBS", 1.2`), retained as `stern.vbs` (SHA-256 b835ce5b0c11c6d268f58c92e534c1677e64cb47e103b33179b82c6c337be0e5, 6,646 bytes) and `core.vbs` (SHA-256 a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69, 104,981 bytes), both CRLF. Copied from the files as retained; line numbers are the files' own.

# Meteor (Stern 1979) - VPinMAME libraries: the game-on output and the tilt objects

## stern.vbs

Line 1: `'Last Updated in VBS v3.61`

Lines 19-21:

```
'-------------------------
' Flipper Solenoid
Const GameOnSolenoid = 19
```

## core.vbs

Line 3: `Const VPinMAMEDriverVer = 3.61`

Line 2036: `Set vpmNudge = New cvpmNudge`

Line 2059: `dim vpmFlips : set vpmFlips = New cvpmFlips2 : vpmFlips.Name = "vpmFlips"`

cvpmFlips2, lines 2066-2067 and 2086-2088 (`TiltObjects` is public and its constructor sets it to 1):

```
Class cvpmFlips2 'test fastflips switches to rom control after 100ms or so delay
	Public Name, Delay, TiltObjects, Sol, DebugOn
	Private Sub Class_Initialize()
		dim idx :for idx = 0 to 3 :FlipperSub(idx) = "NullFunction" : Set FlipperSubRef(idx) = Nothing: OnOff=True: ButtonState(idx)=0:SolState(idx)=0: Next
		Delay=0: FlippersEnabled=0: DebugOn=0 : LagCompensation=0 : Sol=0 : TiltObjects=1
```

cvpmNudge, lines 1156-1172 (the tilt objects are `vpmNudge.TiltObj`; `mSlingBump` holds them and `mForce` their thresholds):

```
	Public Sub SolGameOn(aEnabled)
		If IsEmpty(mForce) Then Exit Sub 'prevent errors if vpmNudge.TiltObj isn't set
		Dim obj, ii
		If aEnabled Then
			ii = 0
			For Each obj In mSlingBump
				If TypeName(obj) = "Bumper" Then obj.Threshold = mForce(ii)
				If vpmVPVer >= 9000 And TypeName(obj) = "Wall" Then obj.SlingshotThreshold = mForce(ii)
				ii = ii + 1
			Next
		Else
			For Each obj In mSlingBump
				If TypeName(obj) = "Bumper" Then obj.Threshold = 100
				If vpmVPVer >= 9000 And TypeName(obj) = "Wall" Then obj.SlingshotThreshold = 100
			Next
		End If
	End Sub
```

vpmFlips setup, lines 2121-2134:

```
		If UseSolenoids >= 2 Then
			On Error Resume Next
				If UseSolenoids > 2 Then
					Solenoid = UseSolenoids
				Else
					err.clear
					if IsEmpty(GameOnSolenoid) or Err then msgbox "VPMflips error: " & err.description
					if err = 500 then 'Error 500 - Variable not defined
						msgbox "UseSolenoids = 2 error!" & vbnewline & vbnewline & "GameOnSolenoid is not defined!" & vbnewline & _
						"System may be incompatible (Check the compatibility list) or your system scripts may be out of date"
					End If
					Solenoid = GameOnSolenoid
				End If
			On Error Goto 0
```

vpmFlips.TiltSol, lines 2216-2225:

```
	Public Sub TiltSol(ByVal aEnabled) 'Handle solenoid / Delay (if delayinit)
		aEnabled = cBool(aEnabled)
		If delay > 0 and not aEnabled then 'handle delay
			vpmtimer.addtimer Delay, Name & ".FireDelay" & "'"
			LagCompensation = 1
		else
			If Delay > 0 then LagCompensation = 0
			EnableFlippers(aEnabled)
		end If
	End Sub
```

vpmFlips.EnableFlippers, lines 2229-2246 (with `TiltObjects` set, every flipper enable or disable also calls `vpmNudge.SolGameOn` with the same state):

```
	Public Sub EnableFlippers(ByVal aEnabled) 'private
		aEnabled = abs(aEnabled) 'Might fix TMNT issue with vpmnudge.solgameon?
		dim idx, cb
		If aEnabled Then
			For idx = 0 to 3
				Set cb = FlipperSubRef(idx)
				If Not cb is Nothing Then cb ButtonState(idx)
			Next
		End If
		FlippersEnabled = aEnabled
		If TiltObjects then vpmnudge.solgameon aEnabled
		If Not aEnabled then
			For idx = 0 To 3
				Set cb = FlipperSubRef(idx)
				If Not cb is Nothing Then cb 0
			Next
		End If
	End Sub
```

Solenoid dispatch, line 2479:

```
			If UseSolenoids > 1 Then If nsol = vpmFlips.Solenoid Then vpmFlips.TiltSol bstate
```

## What the corpus script sets (lines 24, 27, 133, 302-304 of `Meteor (Stern 1979).vbs`)

```
Const cGameName="meteorb",UseSolenoids=2,UseLamps=0,UseGI=0,SSolenoidOn="Solenoid",SSolenoidOff="SolOff"
LoadVPM "01000100", "Stern.VBS", 1.2
SolCallback(16) =  "vpmNudge.SolGameOn"
  vpmNudge.TiltSwitch = 7
  vpmNudge.Sensitivity = 3
  vpmNudge.TiltObj = Array(Bumper1,LeftSlingshot,RightSlingshot)
```

The standalone corpus script has the same lines with tabs in place of spaces. None of the three scripts (both corpus scripts and the retained table's) mentions `TiltObjects`, so it keeps the constructor's 1.
