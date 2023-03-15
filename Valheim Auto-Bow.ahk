#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#SingleInstance Force
CoordMode, Mouse, Screen

counter := 0
AutoBowRunning := 0

emote(action) {
	send {enter}
	sleep 50
	send /%action%
	sleep 50
	send {enter}
}
showStaminaBar(){
	MouseClick, Left,,,,,D
	sleep 100
	MouseClick, Right
	MouseClick, Left,,,,,U
}
equipItem(hammer,item){
	send %hammer%
	sleep 50
	send %item%	
	sleep 800
}

F1 Up:: emote("sit")
F2 Up:: emote("dance")
F3 Up:: emote("headbang")
F4 Up:: emote("kneel")

F10:: buildShelteredWorkbench()
F11::  MouseMove, -500, 0, 10, R ; Move left by 500 pixels

#MaxThreadsPerHotkey 3
XButton1::
	#MaxThreadsPerHotkey 1

	if KeepWinZRunning  ; This means an underlying thread is already running the loop below.
	{
		KeepWinZRunning := false  ; Signal that thread's loop to stop.
		return  ; End this thread so that the one underneath will resume and see the change made by the line above.
	}
	KeepWinZRunning := true
	equipItem(4,5) ;select item 4 then select item 5
	showStaminaBar()	
	Loop
	{
		if haveStamina() {
			MouseClick, Left,,,,,D
			sleep 2000
			MouseClick, Left,,,,,U
			sleep 150
		}
		
		if outOfArrows()
			break
			
		if not KeepWinZRunning  ; The user signaled the loop to stop by pressing Win-Z again.
			break  ; Break out of this loop.

	}
	KeepWinZRunning := false 
Return

outOfArrows()
{
	PixelGetColor, pxOutOfArrows1, 777, 394, RGB
	PixelGetColor, pxOutOfArrows2, 1012, 384, RGB
	PixelGetColor, pxOutOfArrows3, 1123, 392, RGB
	PixelGetColor, pxOutOfArrows4, 1146, 395, RGB
	
	if (substr(pxOutOfArrows1,-1) = "00" and substr(pxOutOfArrows2,-1) = "00" and substr(pxOutOfArrows3,-1) = "00" and substr(pxOutOfArrows4,-1) = "00")
		return True
	else
		return False

}
haveStamina()
{
	;StartTime := A_TickCount
	staminaAvailable := False
	pxArray := object()
	RowSamplePoints := 5
	rows = 4
	arrayCountX := 1
	x := 930
	y := 926
	xstep := 0

		
	Loop,%RowSamplePoints% ;loop across stamina (max of 20 columns)
	{
		ystep := 0
		arrayCountY := 1
		Loop, %rows% ; loop down stamina (max of 16 rows)
		{
			xx := x+xstep
			yy := y+ystep
			PixelGetColor, pxStamina, xx, yy, RGB

			pxArray[arrayCountX,arrayCountY] := pxStamina
			;msgbox, %xx%,%yy% | %xstep%, %ystep% = %pxStamina% | saved to %arrayCountX%,%arrayCountY% 
			ystep += 4
			arrayCountY += 1

		}
		xstep += 3
		arrayCountX += 1
	}
	
	;ElapsedTime := A_TickCount - StartTime

	;MsgBox % ElapsedTime

	
	if (pxArray[1,1] != pxArray[5,1]) {
		staminaAvailable := False
		sleep 500
		counter += 1
		if (counter = 5)
		{
			counter := 0
			showStaminaBar()
		}

	}
	else
	{
			
		sucessfulRows := 0	
		Loop, %rows%
		{
			if (pxArray[1,%A_Index%] = pxArray[2,%A_Index%] and pxArray[1,%A_Index%] = pxArray[3,%A_Index%] and pxArray[1,%A_Index%] = pxArray[4,%A_Index%] and pxArray[1,%A_Index%] = pxArray[5,%A_Index%])
				sucessfulRows += 1
		}
		
		if (sucessfulRows = rows)
			staminaAvailable := True
			
	}
		
	return staminaAvailable
}

buildShelteredWorkbench()
{


	send 2
	sleep 100
	MouseClick, Right
	sleep 100
	MouseClick, Left, 865,293
	sleep 100
	MouseClick, Left, 750,350
	
	MouseGetPos, xpos, ypos 
	MouseMove, 0, 500,2,R
	

}

^z:: exitapp