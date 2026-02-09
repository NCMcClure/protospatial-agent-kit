Verify that the UE5 project builds successfully.

Look for build scripts in the project root:

1. **PowerShell (Windows):** Check for `build.ps1` or `Build.ps1`
   - Run with `-UEVersion <version>` for a specific UE version
   - Run with `-WhatIf` to preview detected installations without building
   - Logs output to `BuildLogs/Build_<version>_<timestamp>.log`

2. **Shell (Mac/Linux):** Check for `build.sh` or `Build.sh`
   - Run with `-v <version>` for a specific UE version
   - Run with `--whatif` to preview detected installations without building
   - Logs output to `BuildLogs/Build_<version>_<timestamp>.log`

3. **RunUAT fallback:** If no build script exists, look for the `.uplugin` file to identify the plugin name, then construct the appropriate RunUAT command:
   - Windows: `RunUAT.bat BuildPlugin -Plugin="<path>" -TargetPlatforms=Win64`
   - Mac: `RunUAT.sh BuildPlugin -Plugin="<path>" -TargetPlatforms=Mac`

Run the detected build command and analyze the output:

- **Success:** Report success and any warnings worth noting
- **Failure:** Parse the error output and report:
  - The file and line number of each error
  - A brief explanation of what's wrong
  - A suggested fix

If there are compilation errors that can be fixed (missing includes, typos, incorrect macro usage), offer to fix them.

$ARGUMENTS
