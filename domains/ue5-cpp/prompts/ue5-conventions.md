# UE5 C++ Conventions Reference

Dense reference for UE5 reflection macros, specifiers, and idioms. This is a knowledge base for agents and commands to draw from.

## UPROPERTY Specifiers

### Visibility & Editing
| Specifier | Meaning |
|-----------|---------|
| `EditAnywhere` | Editable on instances and archetypes in property panels |
| `EditInstanceOnly` | Editable on instances only, not archetypes |
| `EditDefaultsOnly` | Editable on archetypes only (class defaults), not instances |
| `VisibleAnywhere` | Visible in panels but not editable |
| `VisibleInstanceOnly` | Visible on instances only |
| `VisibleDefaultsOnly` | Visible on archetypes only |

### Blueprint Access
| Specifier | Meaning |
|-----------|---------|
| `BlueprintReadWrite` | Readable and writable from Blueprint |
| `BlueprintReadOnly` | Readable from Blueprint, not writable |
| `BlueprintGetter=FuncName` | Custom getter function for Blueprint access |
| `BlueprintSetter=FuncName` | Custom setter function for Blueprint access |

### Serialization & Lifetime
| Specifier | Meaning |
|-----------|---------|
| `Transient` | Not serialized, zero-initialized on load |
| `DuplicateTransient` | Not copied during object duplication |
| `Config` | Serialized to/from config (.ini) files |
| `GlobalConfig` | Like Config but uses the CDO's config section |
| `SaveGame` | Included in save game serialization |

### Organization
| Specifier | Meaning |
|-----------|---------|
| `Category="Name"` | Groups the property in details panels (required for Blueprint-exposed) |
| `meta=(AllowPrivateAccess="true")` | Allows Blueprint access to private members |
| `meta=(ClampMin="0", ClampMax="100")` | Numeric range clamping in editor |
| `meta=(DisplayName="Nice Name")` | Override display name in editor |
| `meta=(EditCondition="bOtherBool")` | Only editable when condition is true |
| `meta=(EditConditionHides)` | Hides property when EditCondition is false |
| `meta=(MakeStructureDefaultValue)` | Sets a default for struct properties |

### Common Combinations
```cpp
// Editor-configurable setting exposed to Blueprint
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Settings")

// Read-only status visible everywhere
UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Status")

// Internal state, no editor/BP access, not serialized
UPROPERTY(Transient)

// Private member accessible from Blueprint
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Config", meta = (AllowPrivateAccess = "true"))

// Config-driven setting
UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "Configuration")
```

## UFUNCTION Specifiers

### Blueprint Integration
| Specifier | Meaning |
|-----------|---------|
| `BlueprintCallable` | Can be called from Blueprint graphs |
| `BlueprintPure` | No side effects, no exec pin, used as expression |
| `BlueprintImplementableEvent` | No C++ body; implemented in Blueprint |
| `BlueprintNativeEvent` | C++ default implementation, overridable in Blueprint |
| `BlueprintAuthorityOnly` | Only executes on network authority |

### Editor & Utility
| Specifier | Meaning |
|-----------|---------|
| `CallInEditor` | Callable from details panel button in editor |
| `Exec` | Console command, callable from command line |
| `Category="Name"` | Required for BlueprintCallable/BlueprintPure |

### Common Combinations
```cpp
// Standard Blueprint-callable function
UFUNCTION(BlueprintCallable, Category = "MyCategory")
void DoSomething();

// Pure getter for Blueprint
UFUNCTION(BlueprintPure, Category = "MyCategory")
float GetValue() const;

// Overridable event with C++ default
UFUNCTION(BlueprintNativeEvent, Category = "Events")
void OnSomethingHappened();

// Editor utility button
UFUNCTION(CallInEditor, Category = "Debug")
void DebugDumpState();
```

## UCLASS Specifiers

| Specifier | Meaning |
|-----------|---------|
| `Blueprintable` | Can be subclassed in Blueprint |
| `BlueprintType` | Can be used as a variable type in Blueprint |
| `NotBlueprintable` | Cannot be subclassed in Blueprint |
| `Abstract` | Cannot be instantiated, only subclassed |
| `MinimalAPI` | Only the type is exported, not its methods |
| `Within=OuterClass` | Must be created as a sub-object of the specified outer class |
| `meta=(DisplayName="Name")` | Override class display name |
| `ClassGroup="Group"` | Groups in editor class pickers |
| `HideCategories=(Cat1,Cat2)` | Hides specified property categories in editor |
| `ShowCategories=(Cat1)` | Shows previously hidden categories |

```cpp
// Standard Blueprint-exposable UObject
UCLASS(BlueprintType, Blueprintable)

// Editor-only subsystem
UCLASS()
class UMyEditorSubsystem : public UEditorSubsystem

// Abstract base class
UCLASS(Abstract, BlueprintType)

// Developer settings (appears in Project Settings)
UCLASS(Config = Game, DefaultConfig, meta = (DisplayName = "My Plugin Settings"))
class UMySettings : public UDeveloperSettings
```

## USTRUCT Specifiers

| Specifier | Meaning |
|-----------|---------|
| `BlueprintType` | Usable as Blueprint variable type |
| `Atomic` | Always serialized as a single unit |
| `NoExport` | Not exported to generated header (manual reflection) |

```cpp
// Standard Blueprint-visible struct
USTRUCT(BlueprintType)
struct FMyData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Data")
    FString Name;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Data")
    int32 Count = 0;
};
```

## UENUM Specifiers

```cpp
// Standard Blueprint-visible enum
UENUM(BlueprintType)
enum class EMyState : uint8
{
    Idle        UMETA(DisplayName = "Idle"),
    Active      UMETA(DisplayName = "Active"),
    Complete    UMETA(DisplayName = "Complete")
};
```

## Container Types

| Container | Use When | Notes |
|-----------|----------|-------|
| `TArray<T>` | Ordered collection, frequent iteration | Most common. Contiguous memory, cache-friendly. |
| `TMap<K,V>` | Key-value lookup | Hash-based. Not ordered. Use TSortedMap if order matters. |
| `TSet<T>` | Unique membership testing | Hash-based. Fast Contains(). |
| `TOptional<T>` | Value may or may not exist | UE5 equivalent of std::optional. |
| `TVariant<Types...>` | Type-safe union | Prefer over raw unions. |

Avoid `std::vector`, `std::map`, `std::unordered_map` — UE5 containers integrate with GC, serialization, and Blueprint.

## Smart Pointer Decision Tree

```
Is it a UObject?
├── YES: Is it a UPROPERTY member?
│   ├── YES → TObjectPtr<T> (UE5.1+)
│   └── NO (local/param) → raw T*
└── NO: Do multiple owners share it?
    ├── YES → TSharedPtr<T> (+ TWeakPtr<T> for observers)
    └── NO → TUniquePtr<T> (exclusive ownership)
```

## Log Category Setup

```cpp
// In .h (public header)
DECLARE_LOG_CATEGORY_EXTERN(LogMyPlugin, Log, All);

// In .cpp
DEFINE_LOG_CATEGORY(LogMyPlugin);

// Usage
UE_LOG(LogMyPlugin, Display, TEXT("Initialized %s"), *Name);
UE_LOG(LogMyPlugin, Warning, TEXT("Missing config for %s"), *Key);
UE_LOG(LogMyPlugin, Error, TEXT("Failed to create %s: %s"), *TypeName, *ErrorMsg);
```

## Module Build.cs Patterns

### Dependency Types
```csharp
// Types other modules need from your public headers
PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject" });

// Types only your .cpp files need
PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore", "UMG" });
```

**Rule**: If a type from module X appears in your public headers, it's a PublicDependency. If it only appears in your .cpp files, it's PrivateDependency.

### Common Module Groups
```csharp
// Minimal runtime plugin
Public: "Core", "CoreUObject", "Engine"

// Editor plugin with UI
Public: "Core", "CoreUObject", "Engine"
Private: "UnrealEd", "Slate", "SlateCore", "EditorStyle",
         "ToolMenus", "InputCore", "Projects"

// Plugin with UMG widgets
Private: "UMG", "Slate", "SlateCore"

// Plugin with HTTP/networking
Private: "HTTP", "Json", "JsonUtilities"

// Plugin with asset registry access
Private: "AssetRegistry", "ContentBrowserData"
```
