Review the UE5 C++ class specified by the user.

If a file path is provided, read that file. If both .h and .cpp files exist for the class, review both. If only a class name is provided, search for matching files.

Apply the full review checklist from the UE5 code reviewer agent (domains/ue5-cpp/agents/ue5-code-reviewer.md):

1. Reflection system correctness (UCLASS/UPROPERTY/UFUNCTION specifiers, GENERATED_BODY, .generated.h placement)
2. Memory & lifetime (TObjectPtr usage, GC visibility, delegate cleanup)
3. Naming & style (prefixes, PascalCase, bool naming)
4. Module structure (Build.cs dependencies, API export macro, editor guards)
5. Performance (container copies, string type selection, tick avoidance)
6. Include discipline (pragma once, CoreMinimal first, generated last, forward declarations)

Output a structured review with CRITICAL / WARNING / SUGGESTION / GOOD items. Every item must include the specific line, what's wrong, why it matters in UE5, and how to fix it.

$ARGUMENTS
