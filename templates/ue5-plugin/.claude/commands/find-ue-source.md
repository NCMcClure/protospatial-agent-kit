Locate the Unreal Engine source installation on this machine and update the project's AGENTS.md.

Search these paths for UE engine source:

**Windows:**
- `C:\Program Files\Epic Games\UE_*\Engine\Source\`
- `D:\Program Files\Epic Games\UE_*\Engine\Source\`
- `E:\Program Files\Epic Games\UE_*\Engine\Source\`
- `F:\Program Files\Epic Games\UE_*\Engine\Source\`
- `C:\UnrealEngine\Engine\Source\`
- `D:\UnrealEngine\Engine\Source\`
- `C:\UE\UE_*\Engine\Source\`
- `D:\UE\UE_*\Engine\Source\`
- `F:\UE\UE_*\Engine\Source\`
- `G:\UE\UE_*\Engine\Source\`

**Mac:**
- `/Users/Shared/Epic Games/UE_*/Engine/Source/`
- `/opt/UnrealEngine/Engine/Source/`

**Additional detection (Windows):**
- Check the Epic Games Launcher config at `%ProgramData%\Epic\UnrealEngineLauncher\LauncherInstalled.dat` for installation paths
- Check registry keys under `HKLM\SOFTWARE\EpicGames\Unreal Engine` for installed versions

For each path found:
1. Confirm it exists and contains `Runtime/` and `Editor/` subdirectories
2. Detect the UE version from the path name or from `Engine/Build/Build.version`
3. Report what was found

If one or more installations are found:
- If multiple, ask the user which one to use
- Update the `UE_SOURCE_PATH:` line in this project's `AGENTS.md` with the selected path
- Confirm the update was made

If no installations are found:
- Ask the user for the path manually
- Validate the provided path has `Runtime/` and `Editor/` subdirectories
- Update `AGENTS.md` with the validated path

$ARGUMENTS
