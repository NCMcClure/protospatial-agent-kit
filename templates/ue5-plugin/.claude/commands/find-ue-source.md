Locate the Unreal Engine source installation on this machine and update the project's CLAUDE.md.

Search these common paths:

**Windows:**
- `C:\Program Files\Epic Games\UE_*\Engine\Source\`
- `D:\Program Files\Epic Games\UE_*\Engine\Source\`
- `E:\Program Files\Epic Games\UE_*\Engine\Source\`
- `C:\UnrealEngine\Engine\Source\`
- `D:\UnrealEngine\Engine\Source\`

**Mac:**
- `/Users/Shared/Epic Games/UE_*/Engine/Source/`
- `/opt/UnrealEngine/Engine/Source/`

For each path found:
1. Confirm it exists and contains `Runtime/` and `Editor/` subdirectories
2. Detect the UE version from the path or from `Engine/Build/Build.version`
3. Report what was found

If one or more installations are found:
- Ask the user which one to use (if multiple)
- Update the "UE5 Engine Source" section in this project's CLAUDE.md with the selected path
- Confirm the update was made

If no installations are found:
- Ask the user for the path manually
- Validate the provided path has the expected structure

$ARGUMENTS
