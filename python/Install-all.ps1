param (
    [Parameter()]
    [switch]
    $Uninstall
)

function Remove-PathElement {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string] 
        $PartialPath
	)

	# Remove unwanted elements
	$path = $env:path
	$Parts = $path.Split(";") 
	$NotEmptyParts = $Parts | Where-Object { ![System.String]::IsNullOrEmpty($_) } 
	$FilteredParts = $NotEmptyParts | Where-Object { !($_.ToLower().Contains($PartialPath)) }
	$PartsToRemove = $NotEmptyParts | Where-Object { ($_.ToLower().Contains($PartialPath)) }
	write-output "Removing:"
	write-output $PartsToRemove

	$Reconstruction = $FilteredParts -join ";"
	# This stupid thing doesn't change the current path AT ALL.  But it's supposed to make it persist.  We'll see.
	[System.Environment]::SetEnvironmentVariable("PATH", $Reconstruction, "Machine")
	# To make it take immediate effect, we do this.
	$env:Path = $Reconstruction
}

function Install-Chocolatey {
    [CmdletBinding()]
    param (
    )

    $ChocoIsInstalled = (get-command choco -ErrorAction SilentlyContinue) -ne $null

    if (!$ChocoIsInstalled) {
        iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex;
        $env:Path = "$env:Path;C:\ProgramData\chocolatey\bin";
    }
}

function Install-VSCode {
    [CmdletBinding()]
    param( )

    choco upgrade vscode -y
    code --install-extension ms-python.python
}

function Uninstall-VSCode {
    [CmdletBinding()]
    param( )

    choco uninstall vscode -y
}

function Uninstall-Chocolatey {
    [CmdletBinding()]
    param()

    choco uninstall chocolatey -y
}

function Install-Python {
    [CmdletBinding()]
    param (
    )

    choco upgrade python3 -y
    #$env:Path = "$env:Path;$env:SystemDrive\Python27";
    Remove-PathElement "python2"
}

function Uninstall-Python {
    [CmdletBinding()]
    param ( )

    choco uninstall python3 -y
}
function Install-PyGame {

    [CmdletBinding()]
    param ( )

    #choco install pip -y
    #$env:Path = "$env:Path;$env:SystemDrive:\Python27\Scripts";

    $env:Path = "$env:Path;$env:SystemDrive:\Python37\Scripts";
    pip install pygame
}

function Uninstall-PyGame {
    [CmdletBinding()]
    param()

    pip uninstall pygame -y
    #choco uninstall pip -y
}


if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) 
{
    echo "Escalating..."
    if($Uninstall) {
        Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -Command `"$PSCommandPath -Uninstall`"" -Verb RunAs;
    }
    else {
        Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; 
    }
    exit;
}

if($Uninstall -eq $true) {
    Uninstall-VSCode
    Uninstall-PyGame
    Uninstall-Python
    #Uninstall-Chocolatey
}
else {
    Install-Chocolatey
    Install-Python
    Install-PyGame
    Install-Vscode
}
write('Done!')
pause