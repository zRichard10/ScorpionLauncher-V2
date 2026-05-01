' Scorpion Launcher - Universal Silent Starter
' Finds pythonw.exe automatically on any PC and launches without CMD
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

Dim baseDir
baseDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = baseDir

Dim mainPy
mainPy = baseDir & "\main.py"

If Not fso.FileExists(mainPy) Then
    MsgBox "No se encontro main.py en:" & vbCrLf & mainPy, vbCritical, "Scorpion Launcher"
    WScript.Quit
End If

' --- Find pythonw.exe dynamically ---
Dim pythonw
pythonw = FindPythonW()

If pythonw = "" Then
    MsgBox "No se encontro Python instalado." & vbCrLf & vbCrLf & _
           "1. Descarga Python desde python.org" & vbCrLf & _
           "2. Marca 'Add Python to PATH' al instalar" & vbCrLf & _
           "3. Ejecuta setup.bat para instalar dependencias", _
           vbCritical, "Scorpion Launcher"
    WScript.Quit
End If

' Launch without console window
WshShell.Run """" & pythonw & """ """ & mainPy & """", 0, False


Function FindPythonW()
    FindPythonW = ""
    Dim localApp
    localApp = WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%")

    ' Method 1: Check py launcher (most reliable on modern Windows)
    Dim pyPath
    On Error Resume Next
    Set objExec = WshShell.Exec("cmd /c py -3 -c ""import sys,os;print(os.path.join(os.path.dirname(sys.executable),'pythonw.exe'))""")
    If Err.Number = 0 Then
        pyPath = Trim(objExec.StdOut.ReadAll())
        If pyPath <> "" And fso.FileExists(pyPath) Then
            FindPythonW = pyPath
            Exit Function
        End If
    End If
    On Error GoTo 0

    ' Method 2: Scan common install locations
    Dim versions, v
    versions = Array("313", "312", "311", "310", "39", "38")
    For Each v In versions
        pyPath = localApp & "\Programs\Python\Python" & v & "\pythonw.exe"
        If fso.FileExists(pyPath) Then
            FindPythonW = pyPath
            Exit Function
        End If
        ' Also check Program Files
        pyPath = "C:\Python" & v & "\pythonw.exe"
        If fso.FileExists(pyPath) Then
            FindPythonW = pyPath
            Exit Function
        End If
    Next

    ' Method 3: Try PATH-based where
    On Error Resume Next
    Set objExec = WshShell.Exec("cmd /c where pythonw.exe")
    If Err.Number = 0 Then
        pyPath = Trim(Split(objExec.StdOut.ReadAll(), vbCrLf)(0))
        If pyPath <> "" And fso.FileExists(pyPath) Then
            FindPythonW = pyPath
            Exit Function
        End If
    End If
    On Error GoTo 0
End Function
