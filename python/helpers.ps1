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
	# This stupid fuckin thing doesn't change the current path AT ALL.  But it's supposed to make it persist.  We'll see.
	[System.Environment]::SetEnvironmentVariable("PATH", $Reconstruction, "Machine")
	# To make it take immediate effect, we do this.
	$env:Path = $Reconstruction
}

function New-PathElement {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string] 
        $NewPath
	)

	# Remove unwanted elements
	[string]$Path = $env:Path
	if (!$Path.EndsWith(";")) { $Path = $Path + ";" }
	$Path = $Path + $Newpath
	
	# Set the path
	[System.Environment]::SetEnvironmentVariable("PATH", $Reconstruction, "Machine")
	$env.Path = $Path
}