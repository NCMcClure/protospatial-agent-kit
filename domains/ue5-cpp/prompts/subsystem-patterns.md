# UE5 Subsystem Architecture Reference

## The Five Subsystem Types

### UEngineSubsystem
- **Lifetime**: Created when GEngine initializes, destroyed when engine shuts down
- **Access**: `GEngine->GetEngineSubsystem<UMySubsystem>()`
- **Use when**: You need a singleton service that persists across all worlds, PIE sessions, and editor states. Global caching, cross-world coordination, engine-level service registration.

### UEditorSubsystem
- **Lifetime**: Created when the editor starts, destroyed when the editor exits
- **Access**: `GEditor->GetEditorSubsystem<UMySubsystem>()`
- **Use when**: You need editor-only services — tool state management, editor UI coordination, custom editor mode support, asset pipeline hooks. Not available in packaged builds.

### UGameInstanceSubsystem
- **Lifetime**: Created with the UGameInstance, destroyed when the game instance is torn down
- **Access**: `UGameInstance::GetSubsystem<UMySubsystem>(GameInstance)` or from any actor via `GetGameInstance()->GetSubsystem<>()`
- **Use when**: You need state that persists across level transitions but is scoped to a single play session. Player progression, session-level caching, cross-level services.

### UWorldSubsystem
- **Lifetime**: Created when a UWorld is created, destroyed when the world is torn down
- **Access**: `UWorld::GetSubsystem<UMySubsystem>(World)` or from any actor via `GetWorld()->GetSubsystem<>()`
- **Use when**: You need per-level state. Spatial queries, world-specific managers, level-scoped caches. Note: a new instance is created for each world (PIE, editor preview, game world).

### ULocalPlayerSubsystem
- **Lifetime**: Created with each ULocalPlayer, destroyed when the local player is removed
- **Access**: `ULocalPlayer::GetSubsystem<UMySubsystem>(LocalPlayer)`
- **Use when**: You need per-player state in local multiplayer or split-screen. Per-player UI state, input configuration, player-specific settings.

## Decision Framework

```
Does it need to survive level transitions?
├── NO → Is it per-player?
│   ├── YES → ULocalPlayerSubsystem
│   └── NO → UWorldSubsystem
└── YES → Is it editor-only?
    ├── YES → UEditorSubsystem
    └── NO → Does it need to survive game instance changes?
        ├── YES → UEngineSubsystem
        └── NO → UGameInstanceSubsystem
```

## Implementation Pattern

```cpp
// Header
#pragma once
#include "CoreMinimal.h"
#include "Subsystems/EditorSubsystem.h" // or appropriate base
#include "MyEditorSubsystem.generated.h"

UCLASS()
class MYPLUGIN_API UMyEditorSubsystem : public UEditorSubsystem
{
    GENERATED_BODY()

public:
    // Called when the subsystem is initialized
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;

    // Called when the subsystem is deinitialized
    virtual void Deinitialize() override;

    // Optional: control whether this subsystem should be created
    virtual bool ShouldCreateSubsystem(UObject* Outer) const override { return true; }

    // Public API
    UFUNCTION(BlueprintCallable, Category = "MyPlugin")
    void DoWork();

private:
    // Internal state — use UPROPERTY for any UObject references
    UPROPERTY()
    TObjectPtr<UMyDataAsset> CachedData;

    // Non-UObject state doesn't need UPROPERTY
    TMap<FName, FMyStruct> RuntimeCache;
};
```

```cpp
// Source
#include "MyEditorSubsystem.h"

void UMyEditorSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);

    // If you depend on another subsystem being initialized first:
    // Collection.InitializeDependency<UOtherSubsystem>();

    // Initialization work here
}

void UMyEditorSubsystem::Deinitialize()
{
    // Cleanup: unbind delegates, release resources
    RuntimeCache.Empty();

    Super::Deinitialize();
}
```

## Common Patterns

### Settings Subsystem Combo
Pair `UDeveloperSettings` (for persistent config) with a subsystem (for runtime behavior):

```cpp
// Settings — appears in Project Settings
UCLASS(Config = Game, DefaultConfig, meta = (DisplayName = "My Plugin"))
class UMyPluginSettings : public UDeveloperSettings
{
    GENERATED_BODY()
public:
    UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "General")
    bool bEnableFeature = true;

    UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "General")
    float UpdateInterval = 1.0f;

    virtual FName GetContainerName() const override { return TEXT("Project"); }
    virtual FName GetCategoryName() const override { return TEXT("Plugins"); }
    virtual FName GetSectionName() const override { return TEXT("My Plugin"); }
};

// Subsystem — reads settings, provides runtime behavior
UCLASS()
class UMyPluginSubsystem : public UEditorSubsystem
{
    GENERATED_BODY()
public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override
    {
        const UMyPluginSettings* Settings = GetDefault<UMyPluginSettings>();
        if (Settings->bEnableFeature)
        {
            // Start feature
        }
    }
};
```

### Subsystem with Delegates
Expose events that other systems can subscribe to:

```cpp
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnStateChanged, EMyState, NewState);

UCLASS()
class UMyWorldSubsystem : public UWorldSubsystem
{
    GENERATED_BODY()
public:
    UPROPERTY(BlueprintAssignable, Category = "Events")
    FOnStateChanged OnStateChanged;

    void SetState(EMyState NewState)
    {
        CurrentState = NewState;
        OnStateChanged.Broadcast(NewState);
    }

private:
    EMyState CurrentState = EMyState::Idle;
};
```

## Common Pitfalls

1. **Assuming initialization order.** Subsystems of the same type have no guaranteed init order. Use `Collection.InitializeDependency<T>()` if you need ordering.

2. **Storing strong references across subsystem boundaries.** Subsystem A holding a `UPROPERTY()` pointer to Subsystem B's data can cause issues if B deinitializes first. Use weak pointers or re-query.

3. **Using subsystems in constructors.** Subsystems may not exist yet during CDO construction. Access them in BeginPlay, Initialize, or later.

4. **Forgetting `MYPLUGIN_API` export macro.** Without it, other modules can't access your subsystem's public API.

5. **Heavy work in Initialize.** Subsystem initialization blocks the main thread. Defer expensive operations to a timer or async task.
