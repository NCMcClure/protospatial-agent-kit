# UE5 C++ Domain

## Scope

Unreal Engine 5 C++ development focused on **plugins, editor tools, engine-level subsystems, and Slate/UMG from C++**.

### In Scope
- UE5 plugin architecture (.uplugin descriptors, module organization, Build.cs configuration)
- The UObject reflection system (UCLASS, USTRUCT, UENUM, UPROPERTY, UFUNCTION)
- Subsystem architecture (all five subsystem types and their lifecycles)
- Slate and UMG widget development from C++
- Editor extension points (FExtender, detail customizations, tool menus, editor modes)
- MCP tool integration patterns (as demonstrated by NodeToCode's framework)
- Smart pointer and memory management patterns
- Module dependency management and loading phases

### Out of Scope
- Gameplay systems (ACharacter, AGameMode, locomotion, AI behavior trees)
- Blueprint-to-C++ migration workflows
- Blueprint scripting
- Level design and world building
- Animation systems and control rigs

## Key Concepts

### Module System
UE5 organizes code into modules, each with a `.Build.cs` file declaring dependencies and build rules. Plugins contain one or more modules defined in the `.uplugin` descriptor. Module types (Runtime, Editor, Program) determine when and where code loads. Loading phases (PreDefault, Default, PostDefault, PostEngineInit) control initialization order.

### Reflection System
The UObject system provides runtime type information through macros: UCLASS for classes, USTRUCT for value types, UENUM for enumerations, UPROPERTY for member variables, UFUNCTION for member functions. Each macro accepts specifiers that control Blueprint exposure, editor visibility, serialization, and replication. GENERATED_BODY() is required in every reflected type.

### Subsystem Architecture
Five subsystem types provide managed singleton-like lifetime without the pitfalls of static singletons:
- **UEngineSubsystem** — lives for the entire engine session
- **UEditorSubsystem** — lives while the editor is running
- **UGameInstanceSubsystem** — lives per game instance
- **UWorldSubsystem** — lives per UWorld (level)
- **ULocalPlayerSubsystem** — lives per local player

See `prompts/subsystem-patterns.md` for detailed decision framework.

### Smart Pointers
- `TObjectPtr<T>` — for UPROPERTY UObject member pointers (UE5.1+ replacement for raw `T*`)
- `TSharedPtr<T>` / `TWeakPtr<T>` — for non-UObject shared ownership
- `TUniquePtr<T>` — for non-UObject exclusive ownership
- Raw `UObject*` — only in local scope or function parameters, never stored without UPROPERTY

## Conventions

### Naming
- **Type prefixes**: `U` (UObject), `A` (Actor), `F` (struct/non-UObject class), `E` (enum), `I` (interface), `T` (template)
- **PascalCase** for all types, functions, and member variables
- **Boolean prefix**: `b` (e.g., `bIsEnabled`, `bHasCompleted`)
- **Out parameter prefix**: `Out` (e.g., `OutResult`)
- **Project prefix** in class names for plugin code (e.g., `N2C` for NodeToCode, `Proto` for ProtoUI)
- No `using namespace` in headers

### Header Organization
```cpp
#pragma once

#include "CoreMinimal.h"
// Other UE includes
// Project includes (forward declare where possible)
#include "ClassName.generated.h" // Always last

UCLASS(/* specifiers */)
class MODULENAME_API UClassName : public UBaseClass
{
    GENERATED_BODY()

public:
    // Constructors
    // Public UFUNCTION methods
    // Public UPROPERTY members

protected:
    // Protected methods and members

private:
    // Private implementation
};
```

### Include Discipline
- Include what you use, forward-declare what you reference by pointer/reference only
- `#include "CoreMinimal.h"` first in every header
- Generated header (`*.generated.h`) always last
- Prefer forward declarations in headers, full includes in .cpp files

### String Types
- `FName` — identifiers, asset paths, keys (fast comparison, case-insensitive)
- `FString` — string manipulation, formatting, temporary text operations
- `FText` — anything displayed to users (localization-ready)
- Always use `TEXT("literal")` macro for string literals

### Assertions
- `check(expr)` — fatal in all builds, use for invariants that must never be violated
- `checkf(expr, fmt, ...)` — check with formatted message
- `ensure(expr)` — logs error + callstack but continues (use for recoverable unexpected states)
- `ensureMsgf(expr, fmt, ...)` — ensure with formatted message
- `verify(expr)` — like check but expression always evaluated (even in shipping builds)

## Skills

| Skill | Path | Purpose |
|-------|------|---------|
| UE5 Slate UI | `skills/ue-slate-ui/` | Atomic design methodology adapted for Slate's C++ composition model — five-level widget hierarchy, design tokens, style architecture, composition patterns, refactoring playbook |

## Cross-Domain Connections

- **Technical Design**: Editor tooling and Slate/UMG work often starts from design specs. The spec-translator agent can produce implementation-ready technical specs for UI components. The `atomic-design` skill in the technical-design domain provides the foundational methodology that the `ue-slate-ui` skill adapts for Slate.
- **Templates**: The `ue5-plugin` template provides a ready-to-go project scaffold following these conventions.
