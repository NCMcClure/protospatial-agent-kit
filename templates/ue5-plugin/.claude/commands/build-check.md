Verify that the UE5 project builds successfully.

Look for build scripts in the project root:
1. Check for `build.ps1`, `build.bat`, `Build.ps1`, or `Build.bat` (Windows)
2. Check for `build.sh` or `Build.sh` (Mac/Linux)
3. If no build script exists, look for the .uplugin file to identify the plugin name, then suggest the appropriate RunUAT command

Run the detected build command and analyze the output:

- If the build succeeds: report success and any warnings worth noting
- If the build fails: parse the error output and report:
  - The file and line number of each error
  - A brief explanation of what's wrong
  - A suggested fix

If there are compilation errors that can be fixed (missing includes, typos, incorrect macro usage), offer to fix them.

$ARGUMENTS
