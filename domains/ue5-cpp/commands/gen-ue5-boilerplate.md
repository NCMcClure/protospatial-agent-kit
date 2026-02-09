Generate boilerplate for a new UE5 C++ class.

Gather the following from the user (ask if not provided):

1. **Class name** with UE5 prefix (U, A, F, E, I)
2. **Base class** — suggest options based on purpose:
   - Service/singleton → UEditorSubsystem, UGameInstanceSubsystem, UWorldSubsystem, UEngineSubsystem, ULocalPlayerSubsystem
   - Persistent settings → UDeveloperSettings
   - Blueprint function library → UBlueprintFunctionLibrary
   - Data asset → UDataAsset
   - Component → UActorComponent, USceneComponent
   - General object → UObject
3. **Module name** it belongs to (for the API export macro)
4. **Blueprint exposure** — Blueprintable? BlueprintType? Or C++ only?
5. **Editor-only** — Should it be guarded with WITH_EDITOR or live in an Editor module?

Generate:

### The .h file
- #pragma once
- CoreMinimal.h + appropriate base class include + .generated.h (last)
- UCLASS with specifiers matching the answers above
- GENERATED_BODY()
- Constructor
- Override stubs appropriate to the base class (e.g., Initialize/Deinitialize for subsystems, GetContainerName/GetCategoryName/GetSectionName for UDeveloperSettings)
- Organized public/protected/private sections
- Correct MODULENAME_API export macro

### The .cpp file
- Header include first
- Constructor implementation
- Override implementations with TODO comments for the user to fill in

### Build.cs additions
- List any new module dependencies needed, classified as Public or Private

Follow the conventions in domains/ue5-cpp/DOMAIN.md. Use TObjectPtr<> for UObject member pointers. Use TEXT() for string literals. Include Category on all exposed UPROPERTY/UFUNCTION.

$ARGUMENTS
