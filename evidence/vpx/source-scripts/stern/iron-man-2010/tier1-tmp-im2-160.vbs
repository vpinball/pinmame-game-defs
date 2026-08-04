   Option Explicit
   Randomize

   LoadVPM "01560000", "sam.VBS", 3.10

 '******************* Options *********************
' DMD/Backglass Controller Setting
Const cController = 0		'0=Use value defined in cController.txt, 1=VPinMAME, 2=UVP server, 3=B2S server, 4=B2S with DOF (disable VP mech sounds)
'*************************************************

Dim cNewController
Sub LoadVPM(VPMver, VBSfile, VBSver)
	Dim FileObj, ControllerFile, TextStr

	On Error Resume Next
	If ScriptEngineMajorVersion < 5 Then MsgBox "VB Script Engine 5.0 or higher required"
	ExecuteGlobal GetTextFile(VBSfile)
	If Err Then MsgBox "Unable to open " & VBSfile & ". Ensure that it is in the same folder as this table. " & vbNewLine & Err.Description

	cNewController = 1
	If cController = 0 then
		Set FileObj=CreateObject("Scripting.FileSystemObject")
		If Not FileObj.FolderExists(UserDirectory) then 
			Msgbox "Visual Pinball\User directory does not exist. Defaulting to vPinMame"
		ElseIf Not FileObj.FileExists(UserDirectory & "cController.txt") then
			Set ControllerFile=FileObj.CreateTextFile(UserDirectory & "cController.txt",True)
			ControllerFile.WriteLine 1: ControllerFile.Close
		Else
			Set ControllerFile=FileObj.GetFile(UserDirectory & "cController.txt")
			Set TextStr=ControllerFile.OpenAsTextStream(1,0)
			If (TextStr.AtEndOfStream=True) then
				Set ControllerFile=FileObj.CreateTextFile(UserDirectory & "cController.txt",True)
				ControllerFile.WriteLine 1: ControllerFile.Close
			Else
				cNewController=Textstr.ReadLine: TextStr.Close
			End If
		End If
	Else
		cNewController = cController
	End If

	Select Case cNewController
		Case 1
			Set Controller = CreateObject("VPinMAME.Controller")
			If Err Then MsgBox "Can't Load VPinMAME." & vbNewLine & Err.Description
			If VPMver>"" Then If Controller.Version < VPMver Or Err Then MsgBox "VPinMAME ver " & VPMver & " required."
			If VPinMAMEDriverVer < VBSver Or Err Then MsgBox VBSFile & " ver " & VBSver & " or higher required."
		Case 2
			Set Controller = CreateObject("UltraVP.BackglassServ")
		Case 3,4
			Set Controller = CreateObject("B2S.Server")
	End Select
	On Error Goto 0
End Sub

'*************************************************************
'Toggle DOF sounds on/off based on cController value
'*************************************************************
Dim ToggleMechSounds
Function SoundFX (sound)
    If cNewController= 4 and ToggleMechSounds = 0 Then
        SoundFX = ""
    Else
        SoundFX = sound
    End If
End Function

Sub DOF(dofevent, dofstate)	
	If cNewController>2 Then
		If dofstate = 2 Then
			Controller.B2SSetData dofevent, 1:Controller.B2SSetData dofevent, 0
		Else
			Controller.B2SSetData dofevent, dofstate
		End If
	End If
End Sub
 
'********************
'Standard definitions
'********************

	Const cGameName = "im2_160"

     Const UseSolenoids = 1
     Const UseLamps = 0
     Const UseSync = 0
     Const HandleMech = 1 
     Const SSolenoidOn = "Solenoid"
     Const SSolenoidOff = ""
     Const SCoin = "CoinIn"

 '************
' Table init.
'************

    Dim xx
    Dim Bump1, Bump2, Bump3, Mech3bank,bsTrough,bsRHole,DTBank4,turntable,Mag1,Mag2
	Dim PlungerIM

  Sub Table_Init
	With Controller
		.GameName = cGameName
		If Err Then MsgBox "Can't start Game " & cGameName & vbNewLine & Err.Description:Exit Sub
		.SplashInfoLine = "IronMan (Stern 2010)"
		.HandleKeyboard = 0
		.ShowTitle = 0
		.ShowDMDOnly = 1
		.ShowFrame = 0
		.HandleMechanics = 0
		.Hidden = 0
		On Error Resume Next
		.Run GetPlayerHWnd
		If Err Then MsgBox Err.Description
	End With

    On Error Goto 0

'Trough
    Set bsTrough = New cvpmBallStack
    bsTrough.InitSw 0, 21, 20, 19, 18, 0, 0, 0
    bsTrough.InitKick BallRelease, 90, 8
    bsTrough.InitExitSnd "ballrelease", "Solenoid"
    bsTrough.Balls = 4

	Set mag1= New cvpmMagnet
 	With mag1
		.InitMagnet Magnet1, 22  
		.GrabCenter = False 
 		.solenoid=3
		.CreateEvents "mag1"
	End With

	Set mag2= New cvpmMagnet
 	With mag2
		.InitMagnet Magnet2, 22  
		.GrabCenter = False 
 		.solenoid=4
		.CreateEvents "mag2"
	End With
    

'Nudging
    	vpmNudge.TiltSwitch=-7
    	vpmNudge.Sensitivity=1
    	vpmNudge.TiltObj=Array(Bumper1b,Bumper2b,Bumper3b,LeftSlingshot,RightSlingshot)

'DropTargets

      '**Main Timer init
	PinMAMETimer.Interval = PinMAMEInterval
	PinMAMETimer.Enabled = 1
 
  'StandUp Init
	ResetAll

  End Sub

 Sub Table_Paused:Controller.Pause = 1:End Sub
 Sub Table_unPaused:Controller.Pause = 0:End Sub


 
'*****Keys
 Sub Table_KeyDown(ByVal keycode)

 	If Keycode = LeftFlipperKey then 
	End If
 	If Keycode = RightFlipperKey then 
	End If
    If keycode = PlungerKey Then Plunger.Pullback
'  	If keycode = LeftTiltKey Then LeftNudge 80, 1, 20
'    If keycode = RightTiltKey Then RightNudge 280, 1, 20
'    If keycode = CenterTiltKey Then CenterNudge 0, 1, 25
    If vpmKeyDown(keycode) Then Exit Sub 
    
End Sub

Sub Table_KeyUp(ByVal keycode)
	If vpmKeyUp(keycode) Then Exit Sub
 	If Keycode = LeftFlipperKey then 
		SolLFlipper false
	End If
 	If Keycode = RightFlipperKey then 
		SolRFlipper False
	End If
	If Keycode = StartGameKey Then Controller.Switch(16) = 0
    If keycode = PlungerKey Then
		Plunger.Fire
        PlaySound "Plunger"
	End If
End Sub


   'Solenoids
SolCallback(1) = "solTrough"
SolCallback(2) = "solAutofire"
'SolCallback(3) = "MongerMagnet"
'SolCallback(4) = whiplash magnet
SolCallback(5) = "WMKick"
SolCallback(6) = "orbitpost"
SolCallback(12) = "ClanePost"
SolCallback(15) = "SolLFlipper"
SolCallback(16) = "SolRFlipper"
SolCallback(19) = "Solmonger"
SolCallBack(20) = "SetLamp 120,"
SolCallback(21) = "SetLamp 121,"
SolCallback(22) = "SetLamp 122,"
'SolCallback(23) = "SetLamp 123,"
'SolCallback(25) = "SetLamp 125,"
SolCallback(26) = "SetLamp 126,"
SolCallback(27) = "SetLamp 127,"
SolCallback(29) = "SetLamp 129,"
'SolCallback(30) = 
SolCallback(31) = "SetLamp 131,"
SolCallback(32) = "SetLamp 132,"


Sub solTrough(Enabled)
	If Enabled Then
		bsTrough.ExitSol_On
		vpmTimer.PulseSw 22
	End If
 End Sub

Sub solAutofire(Enabled)
	If Enabled Then
		PlungerIM.AutoFire
	End If
 End Sub

Sub ClanePost(Enabled)
	If Enabled Then
		ClaneUpPost.Isdropped=false
	Else
		ClaneUpPost.Isdropped=true
	End If
 End Sub

Sub orbitpost(Enabled)
	If Enabled Then
		UpPost.Isdropped=false
	Else
		UpPost.Isdropped=true
	End If
 End Sub

Sub ClanePost(Enabled)
	If Enabled Then
		ClaneUpPost.Isdropped=false
	Else
		ClaneUpPost.Isdropped=true
	End If
 End Sub

Sub WMKick(enabled)
    If enabled Then
     PlaySound "ballhit"
       sw10.Kick 180, 30
       controller.switch(10) = false
    End If 
End Sub
 
'***********************************************
   'Flipper Subs

   
  
Sub SolLFlipper(Enabled)
     If Enabled Then
		 PlaySound SoundFX("FlipperUpLeft")
		 LeftFlipper.RotateToEnd
     Else
		 PlaySound SoundFX("FlipperDown")
		 LeftFlipper.RotateToStart
     End If
 End Sub

Sub SolRFlipper(Enabled)
     If Enabled Then
		 PlaySound SoundFX("FlipperUpRight")
		 RightFlipper.RotateToEnd
     Else
		 PlaySound SoundFX("FlipperDown")
		 RightFlipper.RotateToStart
     End If
 End Sub   

 'Drains and Kickers
Dim BallCount:BallCount = 0
   Sub Drain_Hit():PlaySound "Drain"
	'ClearBallID
	BallCount = BallCount - 1
	bsTrough.AddBall Me
	If BallCount = 0 then GIOff
   End Sub
   Sub BallRelease_UnHit()
	'NewBallID
		BallCount = BallCount + 1
		GIOn
	End Sub



'Switches

'1 monger down
'3 monger up
'4 monger left shoulder
'5 monger legs
Sub sw5_Hit:vpmTimer.PulseSw 5:PlaySound "target":End Sub
'6 monger rt shoulder

Sub sw7_Hit:Controller.Switch(7) = 1:PlaySound "rollover":End Sub
Sub sw7_UnHit:Controller.Switch(7) = 0:End Sub 
Sub sw9_Hit:Controller.Switch(9) = 1:PlaySound "rollover":End Sub
Sub sw9_UnHit:Controller.Switch(9) = 0:End Sub
Sub sw10_Hit():controller.switch(10)=true:End Sub 
Sub sw11_Spin:vpmTimer.PulseSw 11::playsound"fx_spinner":End Sub 
Sub sw12_Hit:Controller.Switch(12) = 1:End Sub
Sub sw12_UnHit:Controller.Switch(12) = 0:End Sub	
Sub sw13_Spin:vpmTimer.PulseSw 13::playsound"fx_spinner":End Sub 
Sub sw14_Spin:vpmTimer.PulseSw 14::playsound"fx_spinner":End Sub 
Sub sw23_Hit:Playsound "rollover":Controller.Switch(23)=1:End Sub 
Sub sw23_UnHit:Playsound "rollover":Controller.Switch(23)=0:End Sub 
Sub sw24_Hit:Controller.Switch(24) = 1:PlaySound "rollover":End Sub
Sub sw24_UnHit:Controller.Switch(24) = 0:End Sub
Sub sw25_Hit:Controller.Switch(25) = 1:PlaySound "rollover":End Sub
Sub sw25_UnHit:Controller.Switch(25) = 0:End Sub
Sub sw28_Hit:Controller.Switch(28) = 1:PlaySound "rollover":End Sub
Sub sw28_UnHit:Controller.Switch(28) = 0:End Sub
Sub sw29_Hit:Controller.Switch(29) = 1:PlaySound "rollover":End Sub
Sub sw29_UnHit:Controller.Switch(29) = 0:End Sub
Sub sw33_Hit:vpmTimer.PulseSw 33:PlaySound "target":End Sub
'Sub sw33_Timer:sw33.IsDropped = 0:sw33a.IsDropped = 1:Me.TimerEnabled = 0:End Sub 
Sub sw34_Hit:vpmTimer.PulseSw 34:PlaySound "target":End Sub
'Sub sw34_Timer:sw34.IsDropped = 0:sw34a.IsDropped = 1:Me.TimerEnabled = 0:End Sub 
Sub sw35_Hit:vpmTimer.PulseSw 35:PlaySound "target":End Sub
'Sub sw35_Timer:sw35.IsDropped = 0:sw35a.IsDropped = 1:Me.TimerEnabled = 0:End Sub 
Sub sw36_Hit:vpmTimer.PulseSw 36:PlaySound "target":End Sub
'Sub sw36_Timer:sw36.IsDropped = 0:sw36a.IsDropped = 1:Me.TimerEnabled = 0:End Sub 
Sub sw37_Hit:Controller.Switch(37) = 1:PlaySound "Gate":RightCount = RightCount + 1:End Sub
Sub sw37_UnHit:Controller.Switch(37) = 0:End Sub 
Sub sw38_Hit:Controller.Switch(38) = 1:PlaySound "rollover":End Sub
Sub sw38_UnHit:Controller.Switch(38) = 0:End Sub 
Sub sw39_Hit:Controller.Switch(39) = 1:PlaySound "rollover":End Sub
Sub sw39_UnHit:Controller.Switch(39) = 0:End Sub 
Sub sw40_Hit:vpmTimer.PulseSw 40:PlaySound "target":End Sub
'Sub sw40_Timer:sw40.IsDropped = 0:sw40a.IsDropped = 1:Me.TimerEnabled = 0:End Sub 
Sub sw41_Hit:vpmTimer.PulseSw 41:PlaySound "target":End Sub
'Sub sw41_Timer:sw41.IsDropped = 0:sw41a.IsDropped = 1:Me.TimerEnabled = 0:End Sub 
Sub sw42_Hit:vpmTimer.PulseSw 42:PlaySound "target":End Sub
'Sub sw42_Timer:sw42.IsDropped = 0:sw42a.IsDropped = 1:Me.TimerEnabled = 0:End Sub 
Sub sw44_Hit:vpmTimer.PulseSw 44:PlaySound "target":End Sub
Sub sw43_Hit:Controller.Switch(43) = 1:End Sub
Sub sw43_UnHit:Controller.Switch(43) = 0:End Sub	
'Sub sw44_Timer:sw44.IsDropped = 0:sw44a.IsDropped = 1:Me.TimerEnabled = 0:End Sub 
Sub sw45_Hit:vpmTimer.PulseSw 45:PlaySound "target":End Sub
'Sub sw45_Timer:sw45.IsDropped = 0:sw45a.IsDropped = 1:Me.TimerEnabled = 0:End Sub 
Sub sw46_Hit:vpmTimer.PulseSw 46:PlaySound "target":End Sub
'Sub sw46_Timer:sw46.IsDropped = 0:sw46a.IsDropped = 1:Me.TimerEnabled = 0:End Sub 
Sub sw47_Hit:vpmTimer.PulseSw 47:PlaySound "target":End Sub
'Sub sw47_Timer:sw47.IsDropped = 0:sw47a.IsDropped = 1:Me.TimerEnabled = 0:End Sub 
Sub sw48_Hit:vpmTimer.PulseSw 48:PlaySound "target":End Sub
'Sub sw48_Timer:sw48.IsDropped = 0:sw48a.IsDropped = 1:Me.TimerEnabled = 0:End Sub 
Sub sw49_Hit:Controller.Switch(49) = 1:PlaySound "Gate":LeftCount = LeftCount + 1:End Sub
Sub sw49_UnHit:Controller.Switch(49) = 0:End Sub 
Sub sw50_Hit:vpmTimer.PulseSw 50:PlaySound "target":End Sub
'Sub sw50_Timer:sw50.IsDropped = 0:sw50a.IsDropped = 1:Me.TimerEnabled = 0:End Sub 




Sub ResetAll()
ClaneUpPost.Isdropped=true:UpPost.Isdropped=true
mongerhitpoint.isdropped=1:sw5.isdropped=1
End Sub

'***Slings and rubbers
  ' Slings
 Dim LStep, RStep
 
 Sub LeftSlingShot_Slingshot
    vpmTimer.PulseSw 26
 	PlaySound SoundFX("left_slingshot")
	Me.TimerEnabled = 1
  End Sub
 
 Sub LeftSlingShot_Timer

 End Sub
 
 Sub RightSlingShot_Slingshot
    vpmTimer.PulseSw 27
 	PlaySound SoundFX("right_slingshot")
	Me.TimerEnabled = 1
  End Sub
 
 Sub RightSlingShot_Timer

 End Sub


     ' Impulse Plunger
    Const IMPowerSetting = 50
    Const IMTime = 0.6
    Set plungerIM = New cvpmImpulseP
    With plungerIM
        .InitImpulseP swplunger, IMPowerSetting, IMTime
        .Random 0.3
        .InitExitSnd "plunger2", "plunger"
        .CreateEvents "plungerIM"
    End With

   'Bumpers
      Sub Bumper1b_Hit
      vpmTimer.PulseSw 31
      PlaySound SoundFX("fx_bumper1")
    	End Sub
     
 
      Sub Bumper2b_Hit
      vpmTimer.PulseSw 30
      PlaySound SoundFX("fx_bumper1")
       End Sub
 
      Sub Bumper3b_Hit
      vpmTimer.PulseSw 32
      PlaySound SoundFX("fx_bumper1")
       End Sub
 
Dim LampState(200), FadingLevel(200), FadingState(200)
Dim FlashState(200), FlashLevel(200)
Dim FlashSpeedUp, FlashSpeedDown
Dim x

AllLampsOff()
LampTimer.Interval = 40 'lamp fading speed
LampTimer.Enabled = 1
'
FlashInit()
FlasherTimer.Interval = 10 'flash fading speed
FlasherTimer.Enabled = 1

'' Lamp & Flasher Timers

Sub LampTimer_Timer()
    Dim chgLamp, num, chg, ii
    chgLamp = Controller.ChangedLamps
    If Not IsEmpty(chgLamp) Then
        For ii = 0 To UBound(chgLamp)
            LampState(chgLamp(ii, 0) ) = chgLamp(ii, 1)
            FadingLevel(chgLamp(ii, 0) ) = chgLamp(ii, 1) + 4
			FlashState(chgLamp(ii, 0) ) = chgLamp(ii, 1)
        Next
    End If

    UpdateLamps
End Sub

Sub FlashInit
    Dim i
    For i = 0 to 200
        FlashState(i) = 0
        FlashLevel(i) = 0
    Next

    FlashSpeedUp = 50   ' fast speed when turning on the flasher
    FlashSpeedDown = 10 ' slow speed when turning off the flasher, gives a smooth fading
    AllFlashOff()
End Sub

Sub AllFlashOff
    Dim i
    For i = 0 to 200
        FlashState(i) = 0
    Next
End Sub
 
 Sub UpdateLamps
NFadeL 3, l3
NFadeL 4, l4
NFadeL 5, l5
NFadeL 6, l6
NFadeL 7, l7
NFadeL 8, l8
NFadeL 9, l9
NFadeL 10, l10
NFadeL 11, l11
NFadeL 12, l12
NFadeL 13, l13
NFadeL 14, l14
NFadeL 15, l15
NFadeL 16, l16
NFadeL 17, l17
NFadeL 18, l18
NFadeL 19, l19
NFadeL 20, l20
NFadeL 21, l21
NFadeL 22, l22
NFadeL 23, l23
NFadeL 24, l24
NFadeL 25, l25
NFadeL 26, l26
NFadeL 27, l27
NFadeL 28, l28
NFadeL 29, l29
NFadeL 30, l30
NFadeL 31, l31
NFadeL 32, l32
NFadeL 33, l33
NFadeL 34, l34
NFadeL 35, l35
NFadeL 36, l36
NFadeL 37, l37
NFadeL 38, l38
NFadeL 39, l39
NFadeL 40, l40
NFadeL 41, l41
NFadeL 42, l42
NFadeL 43, l43
NFadeL 44, l44
NFadeL 45, l45
NFadeL 46, l46
NFadeL 47, l47
NFadeL 48, l48
NFadeL 49, l49
NFadeL 50, l50
NFadeL 51, l51
NFadeL 52, l52
NFadeL 53, l53
NFadeL 54, l54
NFadeL 55, l55
NFadeL 56, l56
NFadeL 57, l57
NFadeL 58, l58
NFadeL 59, l59

NFadeLm 121, f121a
NFadeL 121, f121b
NFadeLm 126, f126a
NFadeL 126, f126b
NFadeLm 132, f132a
NFadeL 132, f132b
NFadeLm 131, f131a
NFadeLm 131, f131b
NFadeLm 131, f131c
NFadeL 131, f131d

' FlashAR 60, f160, "bf_on", "bf_a", "bf_b", ARRefresh
' FlashAR 61, f161, "bf_on", "bf_a", "bf_b", ARRefresh
' FlashAR 62, f162, "bf_on", "bf_a", "bf_b", ARRefresh
' NFadeL 60, bumper2b
' NFadeL 61, bumper1b
' NFadeL 62, bumper3b
' FadeL 63, l63, l63a 
'
' FadeLm 120, l90, l90a
' FlashAR 120, f120, "wf_on", "wf_a", "wf_b", ARRefresh
' FadeLm 122, l89, l89a
' FlashAR 122, f189, "rf_on", "rf_a", "rf_b", ARRefresh
' FlashAR 121, f121, "yf_on", "yf_a", "yf_b", ARRefresh
' FlashARm 123, f125, "bf_on", "bf_a", "bf_b", ARRefresh
' FlashAR 123, f125a, "bf_on", "bf_a", "bf_b", ARRefresh
' FlashAR 126, f126, "yf_on", "yf_a", "yf_b", ARRefresh
' FlashAR 127, f127, "wf_on", "wf_a", "wf_b", ARRefresh
' FlashAR 129, f129, "wf_on", "wf_a", "wf_b", ARRefresh
' FlashARm 131, f131a, "rf_on", "rf_a", "rf_b", ARRefresh
' FlashAR 131, f131, "rf_on", "rf_a", "rf_b", ARRefresh
' FlashAR 132, f132, "rf_on", "rf_a", "rf_b", ARRefresh
   End Sub

Sub FadePrim(nr, pri, a, b, c, d)
    Select Case FadingLevel(nr)
        Case 2:pri.image = d:FadingLevel(nr) = 0
        Case 3:pri.image = c:FadingLevel(nr) = 1
        Case 4:pri.image = b:FadingLevel(nr) = 2
        Case 5:pri.image = a:FadingLevel(nr) = 3
    End Select
End Sub

''Lights

Sub NFadeL(nr, a)
    Select Case FadingLevel(nr)
        Case 4:a.state = 0:FadingLevel(nr) = 0
        Case 5:a.State = 1:FadingLevel(nr) = 1
    End Select
End Sub

Sub NFadeLm(nr, a)
    Select Case FadingLevel(nr)
        Case 4:a.state = 0
        Case 5:a.State = 1
    End Select
End Sub

' Flasher objects
' Uses own faster timer

Sub Flash(nr, object)
    Select Case FlashState(nr)
        Case 0 'off
            FlashLevel(nr) = FlashLevel(nr) - FlashSpeedDown
            If FlashLevel(nr) < 0 Then
                FlashLevel(nr) = 0
                FlashState(nr) = -1 'completely off
            End if
            Object.opacity = FlashLevel(nr)
        Case 1 ' on
            FlashLevel(nr) = FlashLevel(nr) + FlashSpeedUp
            If FlashLevel(nr) > 1000 Then
                FlashLevel(nr) = 1000
                FlashState(nr) = -2 'completely on
            End if
            Object.opacity = FlashLevel(nr)
    End Select
End Sub

 Sub AllLampsOff():For x = 1 to 200:LampState(x) = 4:FadingLevel(x) = 4:Next:UpdateLamps:UpdateLamps:Updatelamps:End Sub
 

Sub SetLamp(nr, value)
    If value = 0 AND LampState(nr) = 0 Then Exit Sub
    If value = 1 AND LampState(nr) = 1 Then Exit Sub
    LampState(nr) = abs(value) + 4
FadingLevel(nr ) = abs(value) + 4: FadingState(nr ) = abs(value) + 4
End Sub

Sub SetFlash(nr, stat)
    FlashState(nr) = ABS(stat)
End Sub

Sub FlasherTimer_Timer()
'Flash 3, fire
'
'Flash 80, f80
'Flash 119, f119
'Flash 120, f120 'right ramp flash
'Flash 129, f29 'left loop / spinner flash
'Flash 131, f31 'vengeance flash
 End Sub

'MONGER
'sw1 monger down
'sw3 monger up
'sw4 monger left shoulder
'sw5 monger legs
'sw6 monger rt shoulder


 '************************
 '    monger Animation
 '************************
 
 Dim monger, mongerPos, mongerDir, mongerFlash
 'monger = Array(monger1, monger2, monger3, monger4, monger5, monger6, monger7, monger8, monger9, monger10)
 mongerDir = 0:mongerPos = 0:mongerFlash = 0
 sw5.IsDropped = 1
 switchframe.IsDropped = 1
 'For x = 1 to 9:monger(x).IsDropped = 1:Next
 
 Sub Solmonger(Enabled)
     If Enabled Then
         If mongerDir = 0 Then
             Controller.Switch(3) = 0
             Controller.Switch(1) = 1
             mongerClose.Enabled = 0
             mongerOpen.Enabled = 1
             mongerOpen_Timer
             mongerDir = 1
         Else
             Controller.Switch(1) = 0
             Controller.Switch(3) = 1
             mongerOpen.Enabled = 0
             mongerClose.Enabled = 1
             mongerClose_Timer
             mongerDir = 0
         End If
     End If
 End Sub
 
 Sub mongerOpen_Timer()
     Updatemonger
     mongerPos = mongerPos + 1
 
     If mongerPos> 41 Then
         mongerPos = 41
         mongerOpen.Enabled = 0
     End If
 End Sub
 
 Sub mongerClose_Timer()
     Updatemonger
     mongerPos = mongerPos - 1
 
     If mongerPos <0 Then
         mongerPos = 0
         mongerClose.Enabled = 0
     End If
 End Sub
 
 Sub Updatemonger
     Select Case mongerPos
Case 0:Primitive32.Z=300:Primitive31.Z=300::Primitive2.Z=90:mongerAnim.Enabled = 0:sw3.IsDropped = 0:switchframe.IsDropped = 0:sw5.IsDropped = 0' monger1.IsDropped = 0:monger2.IsDropped = 1:
Case 1:Primitive32.Z=292.5:Primitive31.Z=292.5:Primitive2.Z=82.5
Case 2:Primitive32.Z=285:Primitive31.Z=285:Primitive2.Z=75
Case 3:Primitive32.Z=277.5:Primitive31.Z=277.5:Primitive2.Z=67.5
Case 4:Primitive32.Z=270:Primitive31.Z=270:Primitive2.Z=60
Case 5:Primitive32.Z=262.5:Primitive31.Z=262.5:Primitive2.Z=52.5
Case 6:Primitive32.Z=255:Primitive31.Z=255:Primitive2.Z=45
Case 7:Primitive32.Z=247.5:Primitive31.Z=247.5:Primitive2.Z=37.5
Case 8:Primitive32.Z=240:Primitive31.Z=240:Primitive2.Z=30
Case 9:Primitive32.Z=232.5:Primitive31.Z=232.5:Primitive2.Z=22.5
Case 10:Primitive32.Z=225:Primitive31.Z=225:Primitive2.Z=15
Case 11:Primitive32.Z=217.5:Primitive31.Z=217.5:Primitive2.Z=7.5
Case 12:Primitive32.Z=210:Primitive31.Z=210:Primitive2.Z=0
Case 13:Primitive32.Z=202.5:Primitive31.Z=202.5:Primitive2.Z=-7.5
Case 14:Primitive32.Z=195:Primitive31.Z=195:Primitive2.Z=-15
Case 15:Primitive32.Z=187.5:Primitive31.Z=187.5:Primitive2.Z=-22.5
Case 16:Primitive32.Z=180:Primitive31.Z=180:Primitive2.Z=-30
Case 17:Primitive32.Z=172.5:Primitive31.Z=172.5:Primitive2.Z=-37.5
Case 18:Primitive32.Z=165:Primitive31.Z=165:Primitive2.Z=-45
Case 19:Primitive32.Z=157.5:Primitive31.Z=157.5:Primitive2.Z=-52.5
Case 20:Primitive32.Z=150:Primitive31.Z=150:Primitive2.Z=-60
Case 21:Primitive32.Z=142.5:Primitive31.Z=142.5:Primitive2.Z=-67.5
Case 22:Primitive32.Z=135:Primitive31.Z=135:Primitive2.Z=-75
Case 23:Primitive32.Z=127.5:Primitive31.Z=127.5:Primitive2.Z=-82.5
Case 24:Primitive32.Z=120:Primitive31.Z=120:Primitive2.Z=-90
Case 25:Primitive32.Z=112.5:Primitive31.Z=112.5:Primitive2.Z=-97.5
Case 26:Primitive32.Z=105:Primitive31.Z=105:Primitive2.Z=-105
Case 27:Primitive32.Z=97.5:Primitive31.Z=97.5:Primitive2.Z=-112.5
Case 28:Primitive32.Z=90:Primitive31.Z=90:Primitive2.Z=-120
Case 29:Primitive32.Z=82.5:Primitive31.Z=82.5:Primitive2.Z=-127.5
Case 30:Primitive32.Z=75:Primitive31.Z=75:Primitive2.Z=-135
Case 31:Primitive32.Z=67.5:Primitive31.Z=67.5:Primitive2.Z=-142.5
Case 32:Primitive32.Z=60:Primitive31.Z=60:Primitive2.Z=-150
Case 33:Primitive32.Z=52.5:Primitive31.Z=52.5:Primitive2.Z=-157.5
Case 34:Primitive32.Z=45:Primitive31.Z=45:Primitive2.Z=-165
Case 35:Primitive32.Z=37.5:Primitive31.Z=37.5:Primitive2.Z=-172.5
Case 36:Primitive32.Z=30:Primitive31.Z=30:Primitive2.Z=-180
Case 37:Primitive32.Z=22.5:Primitive31.Z=22.5:Primitive2.Z=-187.5
Case 38:Primitive32.Z=15:Primitive31.Z=15:Primitive2.Z=-195
Case 39:Primitive32.Z=7.5:Primitive31.Z=7.5:Primitive2.Z=-202.5
Case 40:Primitive32.Z=0:Primitive31.Z=0:Primitive2.Z=-210:mongerAnim.Enabled = 0:sw3.IsDropped = 1:switchframe.IsDropped = 1:sw5.IsDropped = 1
     End Select
 End Sub

Sub Trigger1_hit
	PlaySound "DROP_LEFT"
 End Sub

 Sub Trigger2_hit
	PlaySound "DROP_RIGHT"
 End Sub 

Sub Table_exit()
	Controller.Pause = False
	Controller.Stop
End Sub

Sub UpdateFlipperLogo_Timer
    LFLogo.RotY = LeftFlipper.CurrentAngle
    RFlogo.RotY = RightFlipper.CurrentAngle
	'LFLogoUP.RotY = LeftFlipper1.CurrentAngle
End Sub

Sub GIOn
	dim bulb
	for each bulb in Collection1
	bulb.state = 1
	next
End Sub

Sub GIOff
	dim bulb
	for each bulb in Collection1
	bulb.state = 0
	next
End Sub

 'Sub RightSlingShot_Timer:Me.TimerEnabled = 0:End Sub
 
' *********************************************************************
'                      Supporting Ball & Sound Functions
' *********************************************************************

Sub Pins_Hit (idx)
	PlaySound "pinhit_low", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 0, 0
End Sub

Sub Targets_Hit (idx)
	PlaySound "target", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 0, 0
End Sub

Sub TargetBankWalls_Hit (idx)
	PlaySound "target", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 0, 0
End Sub

Sub Metals_Thin_Hit (idx)
	PlaySound "metalhit_thin", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0
End Sub

Sub Metals_Medium_Hit (idx)
	PlaySound "metalhit_medium", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0
End Sub

Sub Metals2_Hit (idx)
	PlaySound "metalhit2", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0
End Sub

Sub Gates_Hit (idx)
	PlaySound "gate4", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0
End Sub

Sub Spinner_Spin
	PlaySound "fx_spinner",0,.25,0,0.25
End Sub

Sub Rubbers_Hit(idx)
 	dim finalspeed
  	finalspeed=SQR(activeball.velx * activeball.velx + activeball.vely * activeball.vely)
 	If finalspeed > 20 then 
		PlaySound "fx_rubber2", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0
	End if
	If finalspeed >= 6 AND finalspeed <= 20 then
 		RandomSoundRubber()
 	End If
End Sub

Sub Posts_Hit(idx)
 	dim finalspeed
  	finalspeed=SQR(activeball.velx * activeball.velx + activeball.vely * activeball.vely)
 	If finalspeed > 16 then 
		PlaySound "fx_rubber2", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0
	End if
	If finalspeed >= 6 AND finalspeed <= 16 then
 		RandomSoundRubber()
 	End If
End Sub

Sub RandomSoundRubber()
	Select Case Int(Rnd*3)+1
		Case 1 : PlaySound "rubber_hit_1", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0
		Case 2 : PlaySound "rubber_hit_2", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0
		Case 3 : PlaySound "rubber_hit_3", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0
	End Select
End Sub

Sub LeftFlipper_Collide(parm)
 	RandomSoundFlipper()
End Sub

Sub RightFlipper_Collide(parm)
 	RandomSoundFlipper()
End Sub

Sub RandomSoundFlipper()
	Select Case Int(Rnd*3)+1
		Case 1 : PlaySound "flip_hit_1", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0
		Case 2 : PlaySound "flip_hit_2", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0
		Case 3 : PlaySound "flip_hit_3", 0, Vol(ActiveBall), Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0
	End Select
End Sub


'Sub LRRail_Hit:PlaySound "fx_metalrolling", 0, 150, Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0:End Sub
'
'Sub RLRail_Hit:PlaySound "fx_metalrolling", 0, 150, Pan(ActiveBall), 0, Pitch(ActiveBall), 1, 0:End Sub

Function Vol(ball) ' Calculates the Volume of the sound based on the ball speed
    Vol = Csng(BallVel(ball) ^2 / 1)
End Function

Function Pan(ball) ' Calculates the pan for a ball based on the X position on the table. "table1" is the name of the table
    Dim tmp
    tmp = ball.x * 2 / table.width-1
    If tmp > 0 Then
        Pan = Csng(tmp ^10)
    Else
        Pan = Csng(-((- tmp) ^10) )
    End If
End Function

Function Pitch(ball) ' Calculates the pitch of the sound based on the ball speed
    Pitch = BallVel(ball) * 20
End Function

Function BallVel(ball) 'Calculates the ball speed
    BallVel = INT(SQR((ball.VelX ^2) + (ball.VelY ^2) ) )
End Function

'*****************************************
'      JP's VP10 Rolling Sounds
'*****************************************

Const tnob = 5 ' total number of balls
ReDim rolling(tnob)
InitRolling

Sub InitRolling
    Dim i
    For i = 0 to tnob
        rolling(i) = False
    Next
End Sub

Sub RollingTimer_Timer()
    Dim BOT, b
    BOT = GetBalls

	' stop the sound of deleted balls
    For b = UBound(BOT) + 1 to tnob
        rolling(b) = False
        StopSound("fx_ballrolling" & b)
    Next

	' exit the sub if no balls on the table
    If UBound(BOT) = -1 Then Exit Sub

	' play the rolling sound for each ball
    For b = 0 to UBound(BOT)
        If BallVel(BOT(b) ) > 1 AND BOT(b).z < 30 AND BOT(b).z > 0 Then
            rolling(b) = True
            PlaySound("fx_ballrolling" & b), -1, Vol(BOT(b) ), Pan(BOT(b) ), 0, Pitch(BOT(b) ), 1, 0
        Else
            If rolling(b) = True Then
                StopSound("fx_ballrolling" & b)
                rolling(b) = False
            End If
        End If
    Next
End Sub

'**********************
' Ball Collision Sound
'**********************

Sub OnBallBallCollision(ball1, ball2, velocity)
	PlaySound("fx_collide"), 0, Csng(velocity) ^2 / 2000, Pan(ball1), 0, Pitch(ball1), 0, 0
End Sub

Dim LeftCount:LeftCount = 0
Sub leftdrop_hit
	If LeftCount = 1 then
		playsound "BallDrop"
	End If
	LeftCount = 0
End Sub

Dim RightCount:RightCount = 0
Sub rightdrop_hit
	If RightCount = 1 then
		playsound "BallDrop"
	End If
	RightCount = 0
End Sub

Sub RLS_Timer()
'              RampGate1.RotZ = -(Spinner4.currentangle)
'              RampGate2.RotZ = -(Spinner1.currentangle)
              RampGate1.RotZ = -(leftrampgate.currentangle)
              RampGate3.RotZ = -(rightrampgate.currentangle)
              SpinnerT3.RotZ = -(sw11.currentangle)
              SpinnerT1.RotZ = -(sw13.currentangle)
              SpinnerT2.RotZ = -(sw14.currentangle)
End Sub