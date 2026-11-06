$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
cmake -S $root -B "$root/build"
cmake --build "$root/build" --config Release
